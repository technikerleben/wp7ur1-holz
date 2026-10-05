import {build} from '../holzexpress/node_modules/esbuild/lib/main.js';
import {readFile,writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
process.chdir(fileURLToPath(new URL('.',import.meta.url)));
const result=await build({absWorkingDir:process.cwd(),entryPoints:['game.js'],bundle:true,minify:true,format:'iife',write:false,nodePaths:['../holzexpress/node_modules'],legalComments:'inline'});
execFileSync(process.execPath,['../holzexpress/node_modules/tailwindcss/lib/cli.js','-i','tailwind.css','-o','compiled.css','--content','shell.html,game.js','--minify']);
const html=(await readFile('shell.html','utf8')).replace('__TAILWIND__',await readFile('compiled.css','utf8')).replace('__GAME__',result.outputFiles[0].text);
await writeFile('../../holzdetektive.html',html+'\n<!-- Three.js license:\n'+await readFile('../holzexpress/node_modules/three/LICENSE','utf8')+'\n-->');
