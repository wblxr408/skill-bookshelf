#!/usr/bin/env node
// Launch Edge with remote debugging on port 9222
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const useProfile = process.argv.includes('--profile');
const port = 9222;

// Find Edge executable first, then fall back to Chrome
const browserPaths = {
  darwin: [
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ],
  linux: [
    '/usr/bin/microsoft-edge',
    '/usr/bin/microsoft-edge-stable',
    '/usr/bin/google-chrome',
  ],
  win32: [
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ],
};
const browserPath = (browserPaths[process.platform] || browserPaths.win32).find((candidate) =>
  fs.existsSync(candidate),
);

if (!browserPath) {
  throw new Error('No supported browser executable found. Install Microsoft Edge or Chrome.');
}

// Build args
const args = [
  `--remote-debugging-port=${port}`,
  '--no-first-run',
  '--no-default-browser-check'
];

if (useProfile) {
  const profileDir = path.join(os.homedir(), '.edge-debug-profile');
  args.push(`--user-data-dir=${profileDir}`);
} else {
  args.push(`--user-data-dir=${path.join(os.tmpdir(), 'edge-debug-' + Date.now())}`);
}

console.log(`Starting Edge on port ${port}${useProfile ? ' (with profile)' : ''}...`);
const browser = spawn(browserPath, args, { detached: true, stdio: 'ignore' });
browser.unref();
console.log(`Edge launched (PID: ${browser.pid})`);
