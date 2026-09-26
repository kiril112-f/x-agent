"""Offline adapter contract tests. Uses only stdlib and synthetic public fixtures.

Run: python -B work/test_research_pilot.py --report-prefix outputs/pilot-adapter-tests
After copying into a skill's tests/ directory, ../scripts/research_pilot.py is used.
Set RESEARCH_PILOT_PATH only when testing a different explicit adapter path.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
DEFAULT_ADAPTER = HERE / 'research_pilot.py'
if not DEFAULT_ADAPTER.exists():
    DEFAULT_ADAPTER = HERE.parent / 'scripts' / 'research_pilot.py'
ADAPTER = Path(os.environ.get('RESEARCH_PILOT_PATH', str(DEFAULT_ADAPTER))).resolve()
spec = importlib.util.spec_from_file_location('research_pilot_under_test', ADAPTER)
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)

PROVIDER = 'https://gemini.google.com/app/abcdef012345'
SPARK_PROVIDER = 'https://gemini.google.com/spark/tasks'
SPARK_TASK_ID = 'goal-c_abcdef0123456789'
SPARK_CHAT_PROVIDER = 'https://gemini.google.com/spark/chat/abcdef0123456789'
PUBLIC_SOURCES = [
    'https://docs.python.org/3/library/unittest.html',
    'https://www.rfc-editor.org/rfc/rfc9110',
    'https://www.w3.org/TR/WCAG22/',
]


def synthetic_case():
    return {
        'version': 1, 'task': 'x-source-brief', 'public_only': True,
        'prompt': 'Compare synthetic public source claims; prepare a draft without external writes.',
        'sources': PUBLIC_SOURCES.copy(), 'timeout_minutes': 15, 'max_words': 300,
    }


def synthetic_result(sources=None, word_count=70):
    sources = PUBLIC_SOURCES if sources is None else sources
    return ('Synthetic evidence for an offline test. ' + 'evidence ' * word_count
            + '\n' + '\n'.join(f'- {url}' for url in sources) + '\n')


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='research-pilot-qa-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.case_path = self.write_json('case.json', synthetic_case())
        self.jobs = self.root / 'jobs'
        # Any unexpected direct network access in the imported adapter fails immediately.
        for target in ('socket.create_connection', 'socket.socket', 'urllib.request.urlopen'):
            patcher = patch(target, side_effect=AssertionError('Offline contract forbids network access'))
            patcher.start()
            self.addCleanup(patcher.stop)

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        return path

    def result(self, body=None, name='result.md'):
        path = self.root / name
        path.write_bytes((synthetic_result() if body is None else body).encode('utf-8'))
        return path

    def prepare(self, mode='existing'):
        state = pilot.prepare(self.case_path, self.jobs, mode)
        return Path(state['job_dir']), state

    def registered(self):
        job, _ = self.prepare('google-deep-research-app')
        return job, pilot.register(job, PROVIDER)

    def imported(self, mode='existing'):
        job, _ = self.registered() if mode == 'google-deep-research-app' else self.prepare()
        return job, pilot.import_result(job, self.result())

    def expire(self, job):
        state = pilot.state(job)
        state['deadline'] = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
        pilot.atomic(job / 'state.json', state)

    def cli(self, *args):
        result = subprocess.run([sys.executable, '-B', str(ADAPTER), *map(str, args)],
                                capture_output=True, text=True, encoding='utf-8', timeout=15)
        self.assertEqual(result.stderr, '', result.stderr)
        return result.returncode, json.loads(result.stdout)

    def accept_review(self):
        return {'verdict': 'accept', 'reason': 'Synthetic claims and cited evidence checked.',
                **{key: True for key in pilot.CHECKS}}

    def test_prepare_defaults_to_existing_and_has_no_external_effects(self):
        job, state = self.prepare()
        self.assertEqual(state['mode'], 'existing')
        self.assertEqual(state['status'], 'prepared')
        self.assertFalse(state['external_writes'])
        self.assertFalse(state['network_used_by_adapter'])
        self.assertEqual(state['provider_launches'], 0)
        self.assertIsNone(state['provider_url'])
        self.assertEqual(pilot.read(job / 'input.json'), synthetic_case())

    def test_prepare_app_and_existing_share_case_id_but_not_mutable_state(self):
        job, state = self.prepare()
        app_job, app = self.prepare('google-deep-research-app')
        self.assertEqual(state['id'], app['id'])
        self.assertNotEqual(job, app_job)
        pilot.register(app_job, PROVIDER)
        self.assertEqual(pilot.state(job)['status'], 'prepared')

    def test_prepare_repeated_is_stable_and_does_not_extend_deadline(self):
        job, first = self.prepare()
        again = pilot.prepare(self.case_path, self.jobs)
        self.assertEqual(first, again)
        self.assertEqual(len(list(self.jobs.glob('*/state.json'))), 1)
        reordered = dict(reversed(list(synthetic_case().items())))
        other = self.write_json('reordered.json', reordered)
        self.assertEqual(pilot.prepare(other, self.jobs)['id'], first['id'])

    def test_changed_input_has_a_different_stable_id(self):
        _, first = self.prepare()
        changed = synthetic_case()
        changed['prompt'] += ' Include a comparison table.'
        self.write_json('case.json', changed)
        self.assertNotEqual(pilot.prepare(self.case_path, self.jobs)['id'], first['id'])

    def test_prepare_unknown_mode_rejected(self):
        with self.assertRaises(ValueError):
            self.prepare('spark-api')

    def test_case_boundary_values_are_accepted(self):
        for prompt_length, max_words, timeout in ((30, 100, 1), (12000, 2000, 60)):
            with self.subTest(prompt_length=prompt_length):
                case = synthetic_case()
                case.update(prompt='a' * prompt_length, max_words=max_words, timeout_minutes=timeout)
                self.assertEqual(pilot.validate_case(case), case)

    def test_case_twelve_public_sources_accepted(self):
        case = synthetic_case()
        case['sources'] = [f'https://example.org/public-{number}' for number in range(12)]
        self.assertEqual(pilot.validate_case(case), case)

    def test_source_public_https_is_accepted(self):
        for source in PUBLIC_SOURCES + ['https://example.org/report?year=2026']:
            with self.subTest(source=source):
                self.assertEqual(pilot.url(source), source)

    def test_register_app_once_and_repeat_same_url_idempotently(self):
        job, state = self.registered()
        again = pilot.register(job, PROVIDER)
        self.assertEqual(state, again)
        self.assertEqual(state['status'], 'awaiting_result')
        self.assertEqual(state['provider_launches'], 1)
        self.assertEqual(state['max_provider_launches'], 1)

    def test_register_different_url_rejected_without_changing_original(self):
        job, first = self.registered()
        with self.assertRaises(ValueError):
            pilot.register(job, 'https://gemini.google.com/app/012345abcdef')
        self.assertEqual(pilot.state(job), first)

    def test_existing_mode_cannot_register_cloud_run(self):
        job, before = self.prepare()
        with self.assertRaises(ValueError):
            pilot.register(job, PROVIDER)
        self.assertEqual(pilot.state(job), before)

    def test_expired_prepared_job_cannot_register_or_refresh_deadline(self):
        job, _ = self.prepare('google-deep-research-app')
        self.expire(job)
        deadline = pilot.state(job)['deadline']
        self.assertEqual(pilot.prepare(self.case_path, self.jobs, 'google-deep-research-app')['deadline'], deadline)
        with self.assertRaises(ValueError):
            pilot.register(job, PROVIDER)
        self.assertEqual(pilot.state(job)['provider_launches'], 0)

    def test_timeout_never_creates_a_duplicate_registration(self):
        job, _ = self.registered()
        self.expire(job)
        for provider in (PROVIDER, 'https://gemini.google.com/app/aaaaaaaaaaaa'):
            with self.subTest(provider=provider), self.assertRaises(ValueError):
                pilot.register(job, provider)
        status = pilot.inspect(job)
        self.assertTrue(status['expired'])
        self.assertEqual(status['provider_launches'], 1)
        self.assertEqual(status['provider_url'], PROVIDER)

    def test_import_valid_evidence_requires_review_before_acceptance(self):
        job, state = self.imported()
        self.assertEqual(state['status'], 'review_required')
        evidence = pilot.read(job / 'result.json')
        self.assertEqual(evidence['body'], synthetic_result())
        self.assertEqual(set(evidence['source_urls']), set(PUBLIC_SOURCES))
        self.assertEqual(evidence['sha256'], hashlib.sha256(self.result().read_bytes()).hexdigest())
        self.assertFalse(evidence['over_word_limit'])

    def test_app_import_requires_registered_actual_conversation(self):
        job, before = self.prepare('google-deep-research-app')
        with self.assertRaises(ValueError):
            pilot.import_result(job, self.result())
        self.assertEqual(pilot.state(job), before)
        self.assertFalse((job / 'result.json').exists())

    def test_import_repeated_same_content_is_idempotent(self):
        job, first = self.imported()
        again = pilot.import_result(job, self.result(name='renamed.md'))
        self.assertEqual(first, again)
        self.assertEqual(pilot.read(job / 'result.json')['source_file'], 'result.md')

    def test_import_repeated_after_review_does_not_reset_acceptance(self):
        job, _ = self.imported()
        accepted = pilot.review(job, self.write_json('review.json', self.accept_review()))
        self.expire(job)
        again = pilot.import_result(job, self.result())
        self.assertEqual(again['status'], accepted['status'])
        self.assertEqual(again['result_sha256'], accepted['result_sha256'])

    def test_import_conflicting_content_cannot_overwrite_evidence(self):
        job, state = self.imported()
        first_evidence = (job / 'result.json').read_bytes()
        with self.assertRaises(ValueError):
            pilot.import_result(job, self.result(synthetic_result() + 'Different finding.'))
        self.assertEqual((job / 'result.json').read_bytes(), first_evidence)
        self.assertEqual(pilot.state(job), state)

    def test_import_over_word_limit_retains_raw_evidence_and_warns(self):
        job, _ = self.prepare()
        body = synthetic_result(word_count=400)
        state = pilot.import_result(job, self.result(body))
        self.assertTrue(state['format_warning'])
        evidence = pilot.read(job / 'result.json')
        self.assertTrue(evidence['over_word_limit'])
        self.assertEqual(evidence['body'], body)

    def test_import_utf8_bom_is_supported(self):
        job, _ = self.prepare()
        path = self.root / 'bom.md'
        path.write_bytes(b'\xef\xbb\xbf' + synthetic_result().encode())
        self.assertEqual(pilot.import_result(job, path)['status'], 'review_required')

    def test_import_invalid_utf8_rejected_and_cli_returns_structured_error(self):
        job, before = self.prepare()
        path = self.root / 'invalid.md'
        path.write_bytes(b'\xff\xfe\xfa')
        code, response = self.cli('import', '--job', job, '--result', path)
        self.assertEqual(code, 1)
        self.assertFalse(response['ok'])
        self.assertEqual(pilot.state(job), before)

    def test_import_excessively_large_result_rejected(self):
        job, before = self.prepare()
        path = self.result('a' * 2_000_001)
        with self.assertRaises(ValueError):
            pilot.import_result(job, path)
        self.assertEqual(pilot.state(job), before)

    def test_import_after_deadline_rejected_without_new_evidence(self):
        job, _ = self.prepare()
        self.expire(job)
        with self.assertRaises(ValueError):
            pilot.import_result(job, self.result())
        self.assertFalse((job / 'result.json').exists())

    def test_review_accept_requires_all_six_explicit_true_checks(self):
        job, _ = self.imported()
        state = pilot.review(job, self.write_json('review.json', self.accept_review()))
        self.assertEqual(state['status'], 'accepted')
        self.assertTrue((job / 'review.json').exists())
        with self.assertRaises(ValueError):
            pilot.cancel(job)
        with self.assertRaises(ValueError):
            pilot.review(job, self.root / 'review.json')

    def test_each_acceptance_check_must_be_explicit_true(self):
        job, before = self.imported()
        for check in pilot.CHECKS:
            for incorrect in (None, False, 1, 'true'):
                with self.subTest(check=check, incorrect=incorrect):
                    verdict = self.accept_review()
                    if incorrect is None:
                        verdict.pop(check)
                    else:
                        verdict[check] = incorrect
                    with self.assertRaises(ValueError):
                        pilot.review(job, self.write_json('review.json', verdict))
                    self.assertEqual(pilot.state(job), before)

    def test_rejection_is_terminal_and_preserves_existing_route(self):
        job, _ = self.imported()
        review = self.write_json('review.json', {'verdict': 'reject', 'reason': 'Unsupported synthetic claim.'})
        state = pilot.review(job, review)
        self.assertEqual(state['status'], 'rejected')
        self.assertFalse(state['external_writes'])
        self.assertEqual(pilot.prepare(self.case_path, self.jobs)['status'], 'rejected')
        with self.assertRaises(ValueError):
            pilot.import_result(job, self.result(synthetic_result() + 'changed'))

    def test_review_requires_an_imported_result(self):
        job, _ = self.prepare()
        with self.assertRaises(ValueError):
            pilot.review(job, self.write_json('review.json', self.accept_review()))

    def test_cancel_unlaunched_job_is_local_idempotent_and_terminal(self):
        job, _ = self.prepare()
        canceled = pilot.cancel(job)
        self.assertEqual(canceled['status'], 'canceled')
        self.assertFalse(canceled['remote_stop_required'])
        self.assertEqual(pilot.cancel(job), canceled)
        with self.assertRaises(ValueError):
            pilot.import_result(job, self.result())

    def test_cancel_registered_job_requires_manual_remote_stop(self):
        job, _ = self.registered()
        canceled = pilot.cancel(job)
        self.assertTrue(canceled['remote_stop_required'])
        status = pilot.inspect(job)
        self.assertFalse(status['remote_cancellation_performed'])
        self.assertEqual(status['provider_url'], PROVIDER)
        self.assertEqual(status['provider_launches'], 1)
        with self.assertRaises(ValueError):
            pilot.register(job, PROVIDER)

    def test_no_bridge_or_automatic_network_resume_is_claimed(self):
        job, _ = self.registered()
        # There is no server/bridge to disable: do not simulate a live integration.
        before = (job / 'state.json').read_bytes()
        status = pilot.inspect(job)
        self.assertFalse(status['network_used_by_adapter'])
        self.assertFalse(status['remote_cancellation_performed'])
        self.assertIn('do not launch a duplicate', status['resume_instruction'])
        self.assertIn('Restore access', status['resume_instruction'])
        self.assertEqual((job / 'state.json').read_bytes(), before)
        self.assertEqual(status['status'], 'awaiting_result')

    def test_process_restart_can_resume_same_job_and_import_without_relaunch(self):
        code, response = self.cli('prepare', '--case', self.case_path, '--out', self.jobs,
                                  '--mode', 'google-deep-research-app')
        self.assertEqual(code, 0)
        job = response['data']['job_dir']
        code, _ = self.cli('register', '--job', job, '--url', PROVIDER)
        self.assertEqual(code, 0)
        code, response = self.cli('status', '--job', job)
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['provider_launches'], 1)
        code, response = self.cli('import', '--job', job, '--result', self.result())
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['status'], 'review_required')
        self.assertEqual(response['data']['provider_launches'], 1)

    def test_os_lock_blocks_concurrent_mutation_and_releases_after_killed_process(self):
        job, _ = self.prepare()
        child_code = (
            'import importlib.util,sys\n'
            's=importlib.util.spec_from_file_location("pilot",sys.argv[1])\n'
            'm=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n'
            'with m.locked(sys.argv[2]):\n'
            ' print("LOCKED",flush=True)\n'
            ' sys.stdin.readline()\n'
        )
        child = subprocess.Popen([sys.executable, '-B', '-c', child_code, str(ADAPTER), str(job)],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, encoding='utf-8')
        try:
            self.assertEqual(child.stdout.readline().strip(), 'LOCKED')
            with self.assertRaises(ValueError):
                pilot.cancel(job)
            self.assertEqual(pilot.state(job)['status'], 'prepared')
            child.kill()
            child.communicate(timeout=10)
            self.assertEqual(pilot.cancel(job)['status'], 'canceled')
        finally:
            if child.poll() is None:
                child.kill()
            child.communicate(timeout=10)

    def test_preexisting_lock_file_does_not_block_a_new_process(self):
        job, _ = self.prepare()
        self.assertTrue((job / '.mutation.lock').exists())
        code, response = self.cli('cancel', '--job', job)
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['status'], 'canceled')

    def test_invalid_case_file_cli_returns_json_error_and_creates_no_job(self):
        self.case_path.write_text('{broken', encoding='utf-8')
        code, response = self.cli('prepare', '--case', self.case_path, '--out', self.jobs)
        self.assertEqual(code, 1)
        self.assertFalse(response['ok'])
        self.assertFalse(self.jobs.exists())

    def test_missing_case_file_cli_returns_json_error(self):
        code, response = self.cli('prepare', '--case', self.root / 'missing.json', '--out', self.jobs)
        self.assertEqual(code, 1)
        self.assertFalse(response['ok'])

    def test_malformed_state_cli_returns_json_error_without_reinitializing(self):
        job, _ = self.prepare()
        (job / 'state.json').write_text('{broken', encoding='utf-8')
        code, response = self.cli('status', '--job', job)
        self.assertEqual(code, 1)
        self.assertFalse(response['ok'])
        self.assertEqual((job / 'state.json').read_text(), '{broken')

    def test_spark_prepare_has_same_case_id_and_independent_mode_state(self):
        existing_job, existing = self.prepare()
        research_job, research = self.prepare('google-deep-research-app')
        spark_job, spark = self.prepare('google-spark-app')
        self.assertEqual({existing['id'], research['id'], spark['id']}, {spark['id']})
        self.assertEqual(len({existing_job, research_job, spark_job}), 3)
        self.assertIsNone(spark['provider_task_id'])
        registered = pilot.register(spark_job, SPARK_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(registered['mode'], 'google-spark-app')
        self.assertEqual(registered['provider_url'], SPARK_PROVIDER)
        self.assertEqual(registered['provider_task_id'], SPARK_TASK_ID)
        self.assertEqual(registered['provider_launches'], 1)
        self.assertEqual(pilot.state(existing_job), existing)
        self.assertEqual(pilot.state(research_job), research)
        self.assertEqual(pilot.prepare(self.case_path, self.jobs, 'google-spark-app'), registered)

    def test_spark_same_url_and_task_id_register_idempotently(self):
        job, _ = self.prepare('google-spark-app')
        first = pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID), first)
        self.assertEqual(first['status'], 'awaiting_result')
        self.assertEqual(first['provider_launches'], 1)

    def test_spark_same_url_with_different_task_id_cannot_replace_job(self):
        job, _ = self.prepare('google-spark-app')
        first = pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        with self.assertRaises(ValueError):
            pilot.register(job, SPARK_PROVIDER, 'goal-c_0123456789abcdef')
        self.assertEqual(pilot.state(job), first)

    def test_spark_cancel_is_local_and_requires_manual_remote_stop(self):
        job, _ = self.prepare('google-spark-app')
        pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        state = pilot.cancel(job)
        self.assertEqual(state['status'], 'canceled')
        self.assertTrue(state['remote_stop_required'])
        self.assertEqual(state['provider_task_id'], SPARK_TASK_ID)
        status = pilot.inspect(job)
        self.assertFalse(status['remote_cancellation_performed'])
        self.assertFalse(status['network_used_by_adapter'])
        self.assertEqual(pilot.cancel(job), state)
        with self.assertRaises(ValueError):
            pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)

    def test_spark_import_requires_registration_then_works_as_draft_only(self):
        job, prepared = self.prepare('google-spark-app')
        path = self.result()
        with self.assertRaises(ValueError):
            pilot.import_result(job, path)
        self.assertEqual(pilot.state(job), prepared)
        self.assertFalse((job / 'result.json').exists())
        pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        state = pilot.import_result(job, path)
        self.assertEqual(state['status'], 'review_required')
        self.assertEqual(state['provider_task_id'], SPARK_TASK_ID)
        self.assertFalse(state['external_writes'])
        self.assertEqual(pilot.import_result(job, path), state)

    def test_spark_timeout_retains_task_id_and_never_reregisters(self):
        job, _ = self.prepare('google-spark-app')
        pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        self.expire(job)
        before = pilot.state(job)
        with self.assertRaises(ValueError):
            pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(pilot.state(job), before)
        status = pilot.inspect(job)
        self.assertTrue(status['expired'])
        self.assertEqual(status['provider_task_id'], SPARK_TASK_ID)
        self.assertEqual(status['provider_launches'], 1)

    def test_spark_cli_roundtrip_keeps_observed_id_across_processes(self):
        code, response = self.cli('prepare', '--case', self.case_path, '--out', self.jobs,
                                  '--mode', 'google-spark-app')
        self.assertEqual(code, 0)
        job = response['data']['job_dir']
        code, response = self.cli('register', '--job', job, '--url', SPARK_PROVIDER,
                                  '--task-id', SPARK_TASK_ID)
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['provider_task_id'], SPARK_TASK_ID)
        code, response = self.cli('status', '--job', job)
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['provider_url'], SPARK_PROVIDER)
        self.assertEqual(response['data']['provider_task_id'], SPARK_TASK_ID)
        code, response = self.cli('import', '--job', job, '--result', self.result())
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['status'], 'review_required')
        self.assertEqual(response['data']['provider_launches'], 1)

    def test_spark_cli_missing_id_returns_structured_error(self):
        job, before = self.prepare('google-spark-app')
        code, response = self.cli('register', '--job', job, '--url', SPARK_PROVIDER)
        self.assertEqual(code, 1)
        self.assertFalse(response['ok'])
        self.assertEqual(pilot.state(job), before)

    def test_spark_matching_chat_link_and_task_id_register_idempotently(self):
        job, _ = self.prepare('google-spark-app')
        state = pilot.register(job, SPARK_CHAT_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(state['provider_url'], SPARK_CHAT_PROVIDER)
        self.assertEqual(state['provider_task_id'], SPARK_TASK_ID)
        self.assertEqual(state['provider_launches'], 1)
        self.assertEqual(pilot.register(job, SPARK_CHAT_PROVIDER, SPARK_TASK_ID), state)
        self.assertEqual(pilot.import_result(job, self.result())['status'], 'review_required')

    def test_spark_matching_chat_link_cli_survives_restart_and_local_cancel(self):
        job, _ = self.prepare('google-spark-app')
        code, response = self.cli('register', '--job', job, '--url', SPARK_CHAT_PROVIDER,
                                  '--task-id', SPARK_TASK_ID)
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['provider_url'], SPARK_CHAT_PROVIDER)
        code, response = self.cli('status', '--job', job)
        self.assertEqual(code, 0)
        self.assertEqual(response['data']['provider_url'], SPARK_CHAT_PROVIDER)
        self.assertEqual(response['data']['provider_task_id'], SPARK_TASK_ID)
        code, response = self.cli('cancel', '--job', job)
        self.assertEqual(code, 0)
        self.assertTrue(response['data']['remote_stop_required'])
        self.assertEqual(response['data']['status'], 'canceled')
        self.assertFalse(pilot.inspect(job)['remote_cancellation_performed'])

    def test_spark_list_link_can_be_refined_to_matching_chat_without_relaunch(self):
        job, _ = self.prepare('google-spark-app')
        first = pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        refined = pilot.register(job, SPARK_CHAT_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(refined['provider_url'], SPARK_CHAT_PROVIDER)
        for key in ('provider_task_id', 'provider_launches', 'registered_at', 'created_at', 'deadline', 'status'):
            self.assertEqual(refined[key], first[key], key)
        self.assertEqual(refined['provider_launches'], 1)
        self.assertEqual(pilot.register(job, SPARK_CHAT_PROVIDER, SPARK_TASK_ID), refined)

    def test_spark_list_link_cannot_be_refined_to_another_task(self):
        job, _ = self.prepare('google-spark-app')
        first = pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        with self.assertRaises(ValueError):
            pilot.register(job, 'https://gemini.google.com/spark/chat/0123456789abcdef', 'goal-c_0123456789abcdef')
        self.assertEqual(pilot.state(job), first)

    def test_spark_chat_link_cannot_be_downgraded_to_task_list(self):
        job, _ = self.prepare('google-spark-app')
        first = pilot.register(job, SPARK_CHAT_PROVIDER, SPARK_TASK_ID)
        with self.assertRaises(ValueError):
            pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(pilot.state(job), first)

    def test_deep_research_rejects_spark_url_or_task_id(self):
        job, before = self.prepare('google-deep-research-app')
        for provider_url, task_id in ((SPARK_PROVIDER, SPARK_TASK_ID), (PROVIDER, SPARK_TASK_ID)):
            with self.subTest(provider_url=provider_url), self.assertRaises(ValueError):
                pilot.register(job, provider_url, task_id)
            self.assertEqual(pilot.state(job), before)

    def test_existing_mode_rejects_spark_registration(self):
        job, before = self.prepare()
        with self.assertRaises(ValueError):
            pilot.register(job, SPARK_PROVIDER, SPARK_TASK_ID)
        self.assertEqual(pilot.state(job), before)


def add_invalid_case_test(name, change):
    def test(self):
        case = synthetic_case()
        if change is None:
            case = None
        else:
            case.update(change)
        self.write_json('case.json', case)
        with self.assertRaises(ValueError):
            pilot.prepare(self.case_path, self.jobs)
        self.assertFalse(self.jobs.exists())
    test.__doc__ = f'Input rejection: {name}.'
    setattr(AdapterTests, 'test_invalid_case_' + name, test)


for case_name, case_change in {
    'null': None, 'wrong_version': {'version': 2}, 'boolean_version': {'version': True},
    'wrong_task': {'task': 'publish-post'}, 'public_opt_in_missing': {'public_only': None},
    'public_opt_in_numeric': {'public_only': 1}, 'empty_prompt': {'prompt': ''},
    'whitespace_prompt': {'prompt': ' ' * 100}, 'short_prompt': {'prompt': 'a' * 29},
    'too_long_prompt': {'prompt': 'a' * 12001}, 'non_string_prompt': {'prompt': []},
    'no_sources': {'sources': []}, 'too_many_sources': {'sources': [f'https://example.org/{n}' for n in range(13)]},
    'duplicate_sources': {'sources': [PUBLIC_SOURCES[0], PUBLIC_SOURCES[0]]},
    'sources_not_list': {'sources': 'https://example.org'},
    'timeout_zero': {'timeout_minutes': 0}, 'timeout_too_large': {'timeout_minutes': 61},
    'timeout_boolean': {'timeout_minutes': True}, 'timeout_string': {'timeout_minutes': '15'},
    'words_too_small': {'max_words': 99}, 'words_too_large': {'max_words': 2001},
    'words_string': {'max_words': '300'},
}.items():
    add_invalid_case_test(case_name, case_change)


def add_invalid_url_test(name, source):
    def test(self):
        with self.assertRaises(ValueError):
            pilot.url(source)
    test.__doc__ = f'Public-source boundary: reject {name}.'
    setattr(AdapterTests, 'test_invalid_source_' + name, test)


for source_name, source_value in {
    'non_string': None, 'http': 'http://example.org/report', 'file': 'file:///C:/private.txt',
    'localhost': 'https://localhost/report', 'dotless_host': 'https://intranet/report',
    'local_suffix': 'https://data.local/report', 'internal_suffix': 'https://data.internal/report',
    'loopback_ip': 'https://127.0.0.1/report', 'private_ip': 'https://192.168.1.10/report',
    'metadata_ip': 'https://169.254.169.254/report', 'ipv6_loopback': 'https://[::1]/report',
    'loopback_short_ipv4': 'https://127.1/report',
    'username': 'https://synthetic@example.org/report',
    'password': 'https://user:SYNTHETIC_NOT_A_SECRET@example.org/report',
    'token_query': 'https://example.org/report?token=SYNTHETIC_NOT_A_SECRET',
    'key_query': 'https://example.org/report?api_key=SYNTHETIC_NOT_A_SECRET',
    'credential_fragment': 'https://example.org/report#access_token=SYNTHETIC_NOT_A_SECRET',
    'invalid_port': 'https://example.org:invalid/report',
    'host_whitespace': 'https://not a valid host.org/report',
}.items():
    add_invalid_url_test(source_name, source_value)


def add_bad_provider_test(name, provider):
    def test(self):
        job, before = self.prepare('google-deep-research-app')
        with self.assertRaises(ValueError):
            pilot.register(job, provider)
        self.assertEqual(pilot.state(job), before)
    setattr(AdapterTests, 'test_invalid_provider_' + name, test)


for provider_name, provider_value in {
    'other_domain': 'https://example.org/app/abcdef',
    'fake_subdomain': 'https://gemini.google.com.example.org/app/abcdef',
    'root': 'https://gemini.google.com/',
    'query': PROVIDER + '?x=1', 'fragment': PROVIDER + '#citation',
    'not_conversation': 'https://gemini.google.com/app/not-real-id',
}.items():
    add_bad_provider_test(provider_name, provider_value)


def add_bad_spark_registration_test(name, provider, task_id):
    def test(self):
        job, before = self.prepare('google-spark-app')
        with self.assertRaises(ValueError):
            pilot.register(job, provider, task_id)
        self.assertEqual(pilot.state(job), before)
    test.__doc__ = f'Spark registration rejection: {name}.'
    setattr(AdapterTests, 'test_invalid_spark_registration_' + name, test)


for spark_name, spark_values in {
    'missing_id': (SPARK_PROVIDER, None), 'empty_id': (SPARK_PROVIDER, ''),
    'numeric_id': (SPARK_PROVIDER, 123), 'wrong_prefix': (SPARK_PROVIDER, 'task-c_abcdef'),
    'non_hex_id': (SPARK_PROVIDER, 'goal-c_nothex'),
    'id_with_path': (SPARK_PROVIDER, 'goal-c_abcdef/other'),
    'conversation_url': (PROVIDER, SPARK_TASK_ID),
    'invented_deep_link': (SPARK_PROVIDER + '/' + SPARK_TASK_ID, SPARK_TASK_ID),
    'other_domain': ('https://example.org/spark/tasks', SPARK_TASK_ID),
    'chat_mismatched_id': (SPARK_CHAT_PROVIDER, 'goal-c_0123456789abcdef'),
    'chat_missing_id': (SPARK_CHAT_PROVIDER, None),
    'chat_path_traversal': ('https://gemini.google.com/spark/chat/../abcdef0123456789', SPARK_TASK_ID),
    'chat_encoded_traversal': ('https://gemini.google.com/spark/chat/%2e%2e/abcdef0123456789', SPARK_TASK_ID),
    'chat_extra_segment': (SPARK_CHAT_PROVIDER + '/extra', SPARK_TASK_ID),
    'chat_query': (SPARK_CHAT_PROVIDER + '?source=test', SPARK_TASK_ID),
    'chat_fragment': (SPARK_CHAT_PROVIDER + '#result', SPARK_TASK_ID),
    'chat_empty_suffix': ('https://gemini.google.com/spark/chat/', SPARK_TASK_ID),
    'chat_fake_subdomain': ('https://gemini.google.com.example.org/spark/chat/abcdef0123456789', SPARK_TASK_ID),
    'chat_nonhex_suffix': ('https://gemini.google.com/spark/chat/nothex', 'goal-c_nothex'),
}.items():
    add_bad_spark_registration_test(spark_name, *spark_values)


def add_bad_result_test(name, body):
    def test(self):
        job, before = self.prepare()
        with self.assertRaises(ValueError):
            pilot.import_result(job, self.result(body))
        self.assertEqual(pilot.state(job), before)
        self.assertFalse((job / 'result.json').exists())
    test.__doc__ = f'Result rejection: {name}.'
    setattr(AdapterTests, 'test_invalid_result_' + name, test)


for result_name, result_body in {
    'empty': '', 'whitespace': ' ' * 1000, 'short': 'summary',
    'nul': synthetic_result() + '\x00', 'no_citations': synthetic_result([]),
    'two_citations': synthetic_result(PUBLIC_SOURCES[:2]),
    'repeated_citation': synthetic_result([PUBLIC_SOURCES[0]] * 3),
    'nonpublic_citation': synthetic_result([*PUBLIC_SOURCES[:2], 'https://127.0.0.1/private']),
    'credential_citation': synthetic_result([*PUBLIC_SOURCES[:2], 'https://example.org/?token=SYNTHETIC_NOT_A_SECRET']),
    'malformed_citation': synthetic_result([*PUBLIC_SOURCES[:2], 'https://.']),
}.items():
    add_bad_result_test(result_name, result_body)


def add_bad_review_test(name, verdict):
    def test(self):
        job, before = self.imported()
        with self.assertRaises(ValueError):
            pilot.review(job, self.write_json('review.json', verdict))
        self.assertEqual(pilot.state(job), before)
    setattr(AdapterTests, 'test_invalid_review_' + name, test)


for review_name, review_value in {
    'empty': {}, 'null': None, 'array': [],
    'wrong_verdict': {'verdict': 'maybe', 'reason': 'undecided'},
    'missing_reason': {'verdict': 'reject'},
    'blank_reason': {'verdict': 'reject', 'reason': '   '},
}.items():
    add_bad_review_test(review_name, review_value)


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def record(self, test, status, detail=None):
        self.records.append({'test': test.id().split('.')[-1], 'status': status,
                             'description': test.shortDescription() or test.id().split('.')[-1],
                             **({'detail': detail} if detail else {})})

    def addSuccess(self, test):
        super().addSuccess(test)
        self.record(test, 'PASS')

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.record(test, 'FAIL', self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self.record(test, 'ERROR', self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.record(test, 'SKIP', reason)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-prefix', type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AdapterTests)
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult).run(suite)
    if args.report_prefix:
        args.report_prefix.parent.mkdir(parents=True, exist_ok=True)
        failures = len(result.failures) + len(result.errors)
        report = {
            'status': 'PASS' if result.wasSuccessful() else 'FAIL',
            'ran_at': datetime.now(timezone.utc).isoformat(), 'adapter': str(ADAPTER),
            'adapter_sha256': hashlib.sha256(ADAPTER.read_bytes()).hexdigest(),
            'tests_run': result.testsRun, 'passed': result.testsRun - failures - len(result.skipped),
            'failed': failures, 'skipped': len(result.skipped), 'cases': result.records,
            'scope': 'Offline stdlib tests, isolated temporary directories, synthetic public fixtures only.',
            'not_verified': [
                'Real Google account/service/quota/cost or output quality.',
                'Browser launch, provider cancellation, cloud scheduling, or computer-off execution.',
                'Unavailable live bridge: this adapter has no network bridge; only local resume semantics were tested.',
            ],
        }
        args.report_prefix.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        lines = ['## Результаты тестирования', f'**Статус: {report["status"]}**',
                 f'**Тестов запущено:** {report["tests_run"]} | **Пройдено:** {report["passed"]} | **Провалено:** {report["failed"]}',
                 '', f'Дата: {report["ran_at"]}', f'Код: `{ADAPTER}`',
                 f'SHA-256 кода: `{report["adapter_sha256"]}`', '', '## Тест-кейсы']
        lines += [f'- [{item["status"]}] {item["test"]}: {item["description"]}' for item in result.records]
        bad = [item for item in result.records if item['status'] in ('FAIL', 'ERROR')]
        if bad:
            lines += ['', '## Провалы']
            for item in bad:
                lines += [f'### {item["test"]}', 'Ожидалось: соблюдение проверяемого контракта.',
                          'Получено: несоответствие ниже.', '```text', item['detail'].rstrip(), '```', '']
        lines += ['', '## Заметки',
                  '- Только локальные тесты стандартной библиотеки; все файлы заданий находятся во временных каталогах и удаляются.',
                  '- Прямые сетевые вызовы адаптера в тестовом процессе запрещены моками.',
                  '- Проверены запуск нового процесса, сохранённое состояние и освобождение системной блокировки после принудительного завершения дочернего процесса.',
                  '- Адаптер не содержит сетевого моста. Проверена локальная инструкция восстановления без повторного запуска, а не доступность живого облачного моста.',
                  '- Проверены три независимых режима existing, google-deep-research-app и google-spark-app; Spark использует синтетический ID, адрес списка задач и ссылку /spark/chat/<hex> с обязательным совпадением ID. Форма ссылки соответствует наблюдению родительского агента в UI; тесты не подтверждают существование синтетического задания в Google.',
                  '- Доступ к аккаунту, квоты, стоимость, качество Deep Research/Spark, фактическая отмена в Google и расписание этими тестами не проверены.',
                  '- Исходный код, пользовательские репозитории, реальные данные и внешние приложения тесты не изменяют.', '']
        args.report_prefix.with_suffix('.md').write_text('\n'.join(lines), encoding='utf-8')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
