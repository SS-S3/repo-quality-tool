// halstead_js.js
// Node.js script to compute Halstead metrics for a JS/TS file
const fs = require('fs');
const esprima = require('esprima');

function computeHalsteadMetrics(code) {
    let operators = new Set();
    let operands = new Set();
    let n1 = 0, n2 = 0, N1 = 0, N2 = 0;
    let tokens = esprima.tokenize(code, { loc: false, range: false });
    for (let token of tokens) {
        if (["Punctuator", "Keyword"].includes(token.type)) {
            operators.add(token.value);
            n1++;
        } else if (["Identifier", "String", "Numeric"].includes(token.type)) {
            operands.add(token.value);
            n2++;
        }
    }
    N1 = n1;
    N2 = n2;
    let vocabulary = operators.size + operands.size;
    let length = N1 + N2;
    let volume = null, difficulty = null, effort = null;
    if (vocabulary > 0) {
        volume = length * Math.log2(vocabulary);
        difficulty = (operators.size / 2) * (N2 / (operands.size || 1));
        effort = volume * difficulty;
    }
    return {
        vocabulary,
        length,
        volume: volume ? +volume.toFixed(2) : null,
        difficulty: difficulty ? +difficulty.toFixed(2) : null,
        effort: effort ? +effort.toFixed(2) : null
    };
}

if (process.argv.length < 3) {
    console.error('Usage: node halstead_js.js <file.js>');
    process.exit(1);
}
const file = process.argv[2];
const code = fs.readFileSync(file, 'utf-8');
const metrics = computeHalsteadMetrics(code);
metrics.file = file;
console.log(JSON.stringify(metrics));
