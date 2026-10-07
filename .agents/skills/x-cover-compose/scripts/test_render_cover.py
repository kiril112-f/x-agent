import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

# Pillow is the renderer's existing dependency; no test-only dependencies.
from PIL import Image, ImageChops, ImageFont

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / 'x-content-engine/INDEX.md').is_file())
SCRIPT = ROOT / '.agents/skills/x-cover-compose/scripts/render_cover.py'
sys.dont_write_bytecode = True
module_spec = importlib.util.spec_from_file_location('cover_renderer', SCRIPT)
renderer = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(renderer)
FONT_DIR = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'


class CoverRendererTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / 'tmp/cover-system-qa'
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.sandbox = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(self.sandbox.cleanup)
        self.base = Path(self.sandbox.name)
        self.spec_path = self.base / 'spec.json'
        self.out = self.base / 'output.png'

    def run_spec(self, spec, font_dir=FONT_DIR):
        self.spec_path.write_text(json.dumps(spec), encoding='utf-8')
        return renderer.render(self.spec_path, self.out, font_dir)

    def text(self, **kwargs):
        return dict(type='text', text='gypsy', font='serif', size=80,
                    box=[10, 10, 600, 150], **kwargs)

    def assert_rejected(self, spec, message=None):
        with self.assertRaises((ValueError, TypeError, KeyError, OSError)) as caught:
            self.run_spec(spec)
        if message:
            self.assertIn(message, str(caught.exception))
        self.assertFalse(self.out.exists(), 'Failed render must not create a new output')

    def asset(self, name='red.png', color=(255, 0, 0, 128), size=(40, 20)):
        Image.new('RGBA', size, color).save(self.base / name)
        return name

    def test_master_dimensions_and_thumbnail(self):
        report = self.run_spec({'size': [2000, 800], 'background': '#123456'})
        with Image.open(self.out) as full, Image.open(self.base / 'output-thumb.png') as thumb:
            self.assertEqual(full.size, (2000, 800))
            self.assertEqual(thumb.size, (340, 136))
            self.assertEqual(full.getpixel((100, 100)), (18, 52, 86))
        self.assertTrue(report['automated_geometry_pass'])
        self.assertEqual(report['visual_review'], 'required')

    def test_descenders_fit_without_clipping(self):
        font = ImageFont.truetype(str(FONT_DIR / 'georgia.ttf'), 80)
        bbox = font.getbbox('gypsy')
        height = bbox[3] - bbox[1]
        layer = self.text()
        layer['box'] = [10, 200 - height, 600, height]
        report = self.run_spec({'size': [640, 200], 'background': 'white', 'layers': [layer]})
        with Image.open(self.out) as rendered:
            ink = ImageChops.difference(rendered, Image.new('RGB', rendered.size, 'white')).getbbox()
        self.assertEqual(ink[3], 200)
        self.assertEqual(ink[3] - ink[1], height)
        self.assertEqual(report['layers'][0]['bbox'][3], 200)

    def test_descender_overflow_rejected(self):
        font = ImageFont.truetype(str(FONT_DIR / 'georgia.ttf'), 80)
        box = font.getbbox('gypsy')
        layer = self.text()
        layer['box'][3] = box[3] - box[1] - 1
        self.assert_rejected({'layers': [layer]}, 'Text overflow')

    def test_canvas_overflow_rejected(self):
        layer = self.text()
        layer['box'] = [0, 180, 600, 150]
        self.assert_rejected({'size': [640, 200], 'layers': [layer]}, 'Text outside canvas')

    def test_declared_minimum_allows_controlled_fit(self):
        layer = self.text(min_size=40)
        layer['box'] = [0, 0, 150, 60]
        report = self.run_spec({'layers': [layer]})
        size = report['layers'][0]['size']
        self.assertGreaterEqual(size, 40)
        self.assertLess(size, 80)

    def test_missing_font_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, 'Missing font'):
            self.run_spec({'layers': [self.text()]}, self.base / 'nonexistent-fonts')

    def test_relative_font_and_image_resolve_against_spec(self):
        assets = self.base / 'assets'
        assets.mkdir()
        shutil.copyfile(FONT_DIR / 'georgia.ttf', assets / 'type.ttf')
        self.asset('assets/red.png')
        layer = self.text()
        layer['font'] = 'assets/type.ttf'
        report = self.run_spec({'layers': [layer, {'type': 'image', 'path': 'assets/red.png', 'box': [0, 0, 40, 20]}]})
        self.assertEqual(Path(report['layers'][0]['font']), assets / 'type.ttf')
        self.assertEqual(Path(report['layers'][1]['path']), assets / 'red.png')

    def test_image_alpha_and_layer_order(self):
        self.asset()
        image = {'type': 'image', 'path': 'red.png', 'box': [0, 0, 40, 20]}
        blue = {'type': 'rect', 'box': [0, 0, 40, 20], 'fill': '#0000ff'}
        self.run_spec({'size': [320, 100], 'layers': [blue, image]})
        with Image.open(self.out) as out:
            self.assertEqual(out.getpixel((10, 10)), (128, 0, 127))
        self.run_spec({'size': [320, 100], 'layers': [image, blue]})
        with Image.open(self.out) as out:
            self.assertEqual(out.getpixel((10, 10)), (0, 0, 255))

    def test_opacity_multiplies_source_alpha(self):
        self.asset()
        self.run_spec({'size': [320, 100], 'background': 'black', 'layers': [
            {'type': 'image', 'path': 'red.png', 'box': [0, 0, 40, 20], 'opacity': .5}]})
        with Image.open(self.out) as out:
            self.assertEqual(out.getpixel((10, 10)), (64, 0, 0))

    def test_contain_preserves_ratio_and_does_not_upscale(self):
        self.asset()
        report = self.run_spec({'size': [320, 100], 'layers': [
            {'type': 'image', 'path': 'red.png', 'box': [0, 0, 200, 100]}]})
        self.assertEqual(report['layers'][0]['bbox'], [80, 40, 120, 60])

    def test_trim_entirely_transparent_rejected(self):
        self.asset(color=(1, 2, 3, 0))
        self.assert_rejected({'layers': [{'type': 'image', 'path': 'red.png', 'box': [0, 0, 40, 20], 'trim_alpha': True}]}, 'Entirely transparent')

    def test_repeat_output_and_hash_stable(self):
        spec = {'size': [640, 200], 'layers': [self.text()]}
        first = self.run_spec(spec)
        pixels = self.out.read_bytes()
        second = self.run_spec(spec)
        self.assertEqual(pixels, self.out.read_bytes())
        self.assertEqual(first, second)
        self.assertEqual(first['output_sha256'], hashlib.sha256(pixels).hexdigest())

    def test_empty_multiline_unsupported_size_and_missing_fields_rejected(self):
        cases = [{'size': [1, 10]}, {'layers': [{'type': 'alien'}]},
                 {'layers': [{'type': 'text'}]}]
        for text in ['', '   ', 'one\ntwo']:
            layer = self.text()
            layer['text'] = text
            cases.append({'layers': [layer]})
        for spec in cases:
            with self.subTest(spec=spec):
                self.assert_rejected(spec)

    def test_malformed_json_cli_reports_error(self):
        self.spec_path.write_text('{invalid', encoding='utf-8')
        process = subprocess.run([sys.executable, str(SCRIPT), str(self.spec_path), '--out', str(self.out)], capture_output=True, text=True)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('JSONDecodeError', process.stderr)
        self.assertFalse(self.out.exists())

    def test_out_of_range_opacity_rejected(self):
        self.asset()
        for opacity in [-0.5, 1.5]:
            with self.subTest(opacity=opacity):
                self.assert_rejected({'layers': [{'type': 'image', 'path': 'red.png', 'box': [0, 0, 40, 20], 'opacity': opacity}]})

    def test_invalid_fit_rejected(self):
        self.asset()
        self.assert_rejected({'layers': [{'type': 'image', 'path': 'red.png', 'box': [0, 0, 40, 20], 'fit': 'typo'}]})

    def test_out_of_range_centering_rejected(self):
        self.asset()
        self.assert_rejected({'layers': [{'type': 'image', 'path': 'red.png', 'box': [0, 0, 40, 20], 'fit': 'cover', 'centering': [2, -1]}]})

    def test_lab_glass_smoke(self):
        spec_path = ROOT / 'x-content-engine/assets/covers/cover-lab-2026-10-07/final/05-glass.json'
        report = renderer.render(spec_path, self.out, FONT_DIR)
        self.assertTrue(report['automated_geometry_pass'])
        self.assertEqual(len(report['layers']), 7)
        with Image.open(self.out) as out:
            self.assertEqual(out.size, (2000, 800))


if __name__ == '__main__':
    unittest.main(verbosity=2)
