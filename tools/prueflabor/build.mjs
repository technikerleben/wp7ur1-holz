import {build} from '../holzexpress/node_modules/esbuild/lib/main.js';
import {execFileSync} from 'node:child_process';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
process.chdir(fileURLToPath(new URL('.',import.meta.url)));
await build({absWorkingDir:process.cwd(),entryPoints:['film.js'],bundle:true,minify:true,format:'iife',outfile:'../../prueflabor-film.js',nodePaths:['../holzexpress/node_modules'],legalComments:'inline'});
execFileSync(process.execPath,['../holzexpress/node_modules/tailwindcss/lib/cli.js','-i','tailwind.css','-o','compiled.css','--content','../../pruefstation.html,film.js','--minify']);
await writeFile('../../prueflabor-film.css',await readFile('compiled.css','utf8'));
