#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const optimist = require('optimist');
const gzip = require('../lib/gzip.js');

const argv = optimist
  .usage('Usage: $0 --file [filename] --output [filename]')
  .alias({
    f: 'file',
    o: 'output',
  })
  .demand(['file']).argv;

const fileName = path.basename(argv.file);

const stat = fs.statSync(argv.file);
const out = gzip.unzip(fs.readFileSync(argv.file), {
  name: fileName,
  timestamp: Math.round(stat.mtime.getTime() / 1000),
});

const outputFile = argv.output || argv.file.replace(/\.gz$/, '');
fs.writeFileSync(outputFile, Buffer.from(out));
