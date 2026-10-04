import {build} from 'esbuild';
import {readFile,writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
process.chdir(fileURLToPath(new URL('.',import.meta.url)));
const result=await build({entryPoints:['game.js'],bundle:true,minify:true,format:'iife',write:false,legalComments:'inline'});
execFileSync(process.execPath,['node_modules/tailwindcss/lib/cli.js','-i','tailwind.css','-o','compiled.css','--content','shell.html,game.js','--minify']);
const html=(await readFile('shell.html','utf8')).replace('__TAILWIND__',await readFile('compiled.css','utf8')).replace('__GAME__',result.outputFiles[0].text);
await writeFile('../../holzexpress.html',html+'\n<!-- Three.js license:\n'+await readFile('node_modules/three/LICENSE','utf8')+'\n-->');
