import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname,join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const base='x-content-engine/operations/trend-radar';
const files=['RESTORE-SPARK.md','verification-2026-10-03.md','verification-2026-10-07-linkedin.md','setup-state.json','spark-skills/x-radar-analysis.md','spark-skills/x-radar-feed.md','spark-skills/x-linkedin-adapt.md','spark-skills/analysis-schedule.txt','assets/linkedin-app-km.png'].map(p=>({from:`${base}/${p}`,to:p}));
for(const n of ['creator-profile','audience-and-goals','brand-voice','content-strategy','privacy-and-approval','proof-and-claims','context-storytelling','post-formatting'])files.push({from:`x-content-engine/knowledge/${n}.md`,to:`knowledge/${n}.md`});
files.push({from:'x-content-engine/operations/notion-schema.md',to:'knowledge/notion-schema.md'});
files.push({from:'x-content-engine/operations/dots/feed-calibration-2026-10-03.md',to:'feed-calibration-2026-10-03.md'});
const backup=join(root,'local-backups','spark');await mkdir(backup,{recursive:true});await writeFile(join(backup,'.gitignore'),'*\n');
const folder=join(backup,new Date().toISOString().replace(/[:.]/g,'-'),'x-content-engine-spark');await mkdir(folder,{recursive:true});
const manifest=[];
for(const f of files){const bytes=await readFile(join(root,f.from));await mkdir(dirname(join(folder,f.to)),{recursive:true});await writeFile(join(folder,f.to),bytes);manifest.push({path:f.to,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')});}
await writeFile(join(folder,'manifest.json'),JSON.stringify({schemaVersion:1,createdAt:new Date().toISOString(),containsSecrets:false,files:manifest},null,2));
const zip=folder+'.zip';const r=spawnSync('powershell.exe',['-NoProfile','-NonInteractive','-Command','Compress-Archive -LiteralPath $env:X_SPARK_PACK -DestinationPath $env:X_SPARK_ZIP'],{env:{...process.env,X_SPARK_PACK:folder,X_SPARK_ZIP:zip},encoding:'utf8'});
if(r.status!==0)throw new Error('spark_pack_zip_failed');console.log(JSON.stringify({folder,zip,files:manifest.length,containsSecrets:false}));
