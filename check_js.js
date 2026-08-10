const fs = require('fs');
const html = fs.readFileSync('templates/admin_dashboard.html', 'utf8');
const scriptRegex = /<script.*?>([\s\S]*?)<\/script>/gi;
let match;
let hasError = false;
while ((match = scriptRegex.exec(html)) !== null) {
    const code = match[1];
    if (code.trim() === '') continue;
    try {
        require('vm').Script(code);
    } catch (e) {
        console.error("Syntax Error found in script block!");
        console.error(e.message);
        const lines = code.split('\n');
        // print around the error
        console.log(code);
        hasError = true;
    }
}
if (!hasError) console.log("All JS scripts are syntax valid.");
