#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const optimist = require('optimist');
const gzip = require('../lib/gzip.js');

const argv = optimist
  .usage('Usage: $0 --level [1-9] --file [filename] --output [filename]')
  .alias({
    f: 'file',
    o: 'output',
    l: 'level',
  })
  .default('level', gzip.DEFAULT_LEVEL)
  .demand(['file']).argv;

const fileName = path.basename(argv.file);

const stat = fs.statSync(argv.file);
const out = gzip.zip(fs.readFileSync(argv.file), {
  name: fileName,
  level: argv.level,
  timestamp: Math.round(stat.mtime.getTime() / 1000),
});

fs.writeFileSync(argv.output || `${argv.file}.gz`, Buffer.from(out));
