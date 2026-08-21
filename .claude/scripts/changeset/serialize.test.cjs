'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { cmdExtract } = require('./cli.cjs');
const { parseChangelog, serializeChangelog } = require('./serialize.cjs');

function roundTripBody(body) {
  const changelog = serializeChangelog({
    releaseHeader: { version: '1.2.3', date: '2026-08-21' },
    sections: [{ type: 'Fixed', bullets: [{ pr: 42, body }] }],
    priorChangelog: '',
  });

  return parseChangelog(changelog).releases[0].sections[0].bullets[0].body;
}

test('round trip preserves nested list items and trailing paragraphs', () => {
  const body = 'Summary\n\n- nested item\n\nTrailing paragraph';

  assert.equal(roundTripBody(body), body);
});

test('round trip preserves indented code blocks', () => {
  const body = 'Example:\n\n    const answer = 42;\n\nAfter code';

  assert.equal(roundTripBody(body), body);
});

test('extract indents every multiline bullet continuation', () => {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ggsad-extract-'));
  const changelogPath = path.join(tempDir, 'CHANGELOG.md');
  fs.writeFileSync(
    changelogPath,
    '# Changelog\n\n## [1.2.3] - 2026-08-21\n\n### Fixed\n\n- Summary\n  continued (#42)\n',
  );

  const result = cmdExtract({
    fromRef: '1.2.2',
    toRef: '1.2.3',
    changelog: changelogPath,
    repo: tempDir,
  });

  assert.equal(result.exitCode, 0);
  assert.match(result.textOutput, /- Summary\n  continued \(#42\)/);
});
