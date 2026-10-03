/** Explicit allowlist: reproducible instructions and context, never credential files. */
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const base = 'x-content-engine/operations/dots';
const files = [
  'README.md','START-HERE.txt','schedules.json','references.json','installation-state.json',
  'editorial-brief.md','feed-calibration-2026-10-03.md','SKILL.md',
  'prompts/feed.md','prompts/analysis.md','prompts/sync.md',
].map(p => ({ from: `${base}/${p}`, to: p }));
for (const name of ['creator-profile','audience-and-goals','brand-voice','content-strategy','privacy-and-approval','proof-and-claims','context-storytelling','post-formatting']) {
  files.push({ from:`x-content-engine/knowledge/${name}.md`, to:`knowledge/${name}.md` });
}
files.push({from:'x-content-engine/operations/notion-schema.md',to:'knowledge/notion-schema.md'});
const stamp = new Date().toISOString().replace(/[:.]/g,'-');
const backupRoot = join(root,'local-backups','dots');
await mkdir(backupRoot,{recursive:true});
await writeFile(join(backupRoot,'.gitignore'),'*\n');
const destination = join(backupRoot,stamp,'x-content-engine-dot');
await mkdir(destination,{recursive:true});
const checksums = [];
for (const file of files) {
  const bytes = await readFile(join(root,file.from));
  const target=join(destination,file.to);
  await mkdir(dirname(target),{recursive:true});
  await writeFile(target,bytes);
  checksums.push({path:file.to,sha256:createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length});
}
await writeFile(join(destination,'manifest.json'),JSON.stringify({schemaVersion:1,createdAt:new Date().toISOString(),containsSecrets:false,files:checksums},null,2));
const zip=destination+'.zip';
const result=spawnSync('powershell.exe',['-NoProfile','-NonInteractive','-Command','Compress-Archive -LiteralPath $env:DOTS_PACK_SOURCE -DestinationPath $env:DOTS_PACK_ZIP'],{env:{...process.env,DOTS_PACK_SOURCE:destination,DOTS_PACK_ZIP:zip},encoding:'utf8'});
if(result.status!==0) throw new Error('dots_pack_zip_failed: '+result.stderr);
console.log(JSON.stringify({directory:destination,zip,files:checksums.length,containsSecrets:false}));
