const fs = require('fs');
const path = require('path');
const vsctm = require('vscode-textmate');
const oniguruma = require('vscode-oniguruma');

/**
 * Utility to read a file as a promise
 */
function readFile(path) {
    return new Promise((resolve, reject) => {
        fs.readFile( path, ( error, data ) => {
            error ? reject( error ) : resolve( data )
        } );
    })
}

const wasmBin = fs.readFileSync(path.join(__dirname, './node_modules/vscode-oniguruma/release/onig.wasm')).buffer;
const vscodeOnigurumaLib = oniguruma.loadWASM(wasmBin).then(() => {
    return {
        createOnigScanner(patterns) { return new oniguruma.OnigScanner(patterns); },
        createOnigString(s) { return new oniguruma.OnigString(s); }
    };
});

// Create a registry that can create a grammar from a scope name.
const registry = new vsctm.Registry({
    onigLib: vscodeOnigurumaLib,
    loadGrammar: ( scopeName ) => {
        if (scopeName === 'source1.js') {
            // https://github.com/textmate/javascript.tmbundle/blob/master/Syntaxes/JavaScript.plist
            return readFile('./JavaScript.plist').then(data => vsctm.parseRawGrammar(data.toString()))
        } 
        if (scopeName === 'source.matlab') {
            // https://github.com/textmate/javascript.tmbundle/blob/master/Syntaxes/JavaScript.plist
            return readFile('./assets/m.tmLanguage').then(data => vsctm.parseRawGrammar(data.toString()))
        } 
        console.log(`Unknown scope name: ${scopeName}`);
        return null;
    }
});

// Load the JavaScript grammar and any other grammars included by it async.
// registry.loadGrammar('source.matlab').then(grammar => {
//     let flags = fs.readFileSync( "options.txt",
//         { encoding: 'utf8', flag: 'r' } ).split( " " );
//     const filename = flags[0];
//     const output_file = flags[1];
//     let content = fs.readFileSync('test.m',
//         { encoding: 'utf8', flag: 'r' } ).split( '\r\n' );
    
//     let ruleStack = vsctm.INITIAL;
//     fs.writeFile(output_file, `line,start,end,token,scopes`, err => {})
//     for (let i = 0; i < content.length; i++) {
//         const line = content[i];
//         const lineTokens = grammar.tokenizeLine( line, ruleStack );
//         for (let j = 0; j < lineTokens.tokens.length; j++) {
//             const token = lineTokens.tokens[j];
//             fs.writeFile(output_file, `\n${i}_,_${token.startIndex}_,_${token.endIndex}_,_${line.substring(token.startIndex, token.endIndex)}_,_${token.scopes.join(', ')}`, { flag: 'a+' }, err => {})
//             // fs.writeFile(output_file, `\n - token from ${token.startIndex} to ${token.endIndex} ` +
//             //   `(${line.substring(token.startIndex, token.endIndex)}) ` +
//             //   `with scopes ${token.scopes.join(', ')}`, { flag: 'a+' }, err => {}
//             // );
//         }
//         ruleStack = lineTokens.ruleStack;
//     }

// } );
const filename = process.argv[2];
const output_file = process.argv[3];

// Load the JavaScript grammar and any other grammars included by it async.
registry.loadGrammar('source.matlab').then(grammar => {
    let content = fs.readFileSync(filename,
        { encoding: 'utf8', flag: 'r' } ).split( '\r\n' );
    
    let ruleStack = vsctm.INITIAL;
    fs.writeFile(output_file, `line_,_start_,_end_,_token_,_scopes`, err => {})
    for (let i = 0; i < content.length; i++) {
        const line = content[i];
        const lineTokens = grammar.tokenizeLine( line, ruleStack );
        for (let j = 0; j < lineTokens.tokens.length; j++) {
            const token = lineTokens.tokens[j];
            fs.writeFile(output_file, `\n${i}_,_${token.startIndex}_,_${token.endIndex}_,_${line.substring(token.startIndex, token.endIndex)}_,_["${token.scopes.join('", "')}"]`, { flag: 'a+' }, err => {})
        }
        ruleStack = lineTokens.ruleStack;
    }
} );

