// Static syntax and key-UI contract test; does not require a browser.
const fs=require('fs');
const vm=require('vm');
const path=require('path');
const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
if(scripts.length!==1)throw new Error('Expected a single inline script');
new vm.Script(scripts[0][1],{filename:'DynaCPI-inline.js'});
for(const id of ['smiles','protein','support','chemBtn','runBtn','molecule','prediction','seed','chart','resultsTable','davisExample']){
 if(!html.includes('id="'+id+'"'))throw new Error('Missing UI element: '+id);
}
if(!html.includes('Development demo — not scientific validation'))throw new Error('Missing research limitation');
console.log('UI SCRIPT SYNTAX + 12 ELEMENTS: PASS');
