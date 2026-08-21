'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');

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
