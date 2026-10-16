#!/usr/bin/env node
// Resolve already installed CDP dependencies without installing or launching a browser.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const Module = require('node:module');

const root = path.resolve(__dirname, '..');
const candidates = [
  path.join(root, 'browser', 'node_modules'),
  path.join(root, 'node_modules'),
  path.join(root, 'modules', 'cdp', 'browser', 'node_modules'),
  path.join(os.homedir(), '.agents', 'skills', 'browser', 'browser', 'node_modules'),
  ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean),
].filter(p => fs.existsSync(path.join(p, 'ws', 'package.json')));
process.env.NODE_PATH = [...new Set(candidates)].join(path.delimiter);
Module._initPaths();

let websocket;
try { websocket = require.resolve('ws'); }
catch { console.error('CDP dependency ws is unavailable. Inspect the existing browser runtime package before installing dependencies.'); process.exit(1); }

if (process.argv[2] === '--check') {
  console.log(JSON.stringify({ status: 'resolved', websocket, browser_started: false }));
  process.exit(0);
}
const command = process.argv[2];
if (!['start', 'nav', 'eval', 'pick', 'screenshot', 'viewport'].includes(command)) {
  console.error('Usage: node run-cdp.cjs <start|nav|eval|pick|screenshot|viewport> [helper arguments], or --check');
  process.exit(2);
}
const helper = path.join(__dirname, command + '.cjs');
process.argv.splice(1, 2, helper);
require(helper);
