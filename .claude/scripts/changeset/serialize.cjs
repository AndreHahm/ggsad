'use strict';

/**
 * Markdown serializer + parser for the changelog IR. The two are inverses
 * over the well-formed subset; tests assert via round-trip (parse(serialize(ir)))
 * rather than by inspecting serialized text — see CONTRIBUTING.md
 * "Prohibited: Raw Text Matching on Test Outputs".
 *
 * Serialized form (Keep a Changelog):
 *
 *   ## [1.42.0] - 2026-05-01
 *
 *   ### Fixed
 *
 *   - body of the bullet (#NNNN)
 *
 *   <priorChangelog appended verbatim>
 */

function serializeChangelog(ir) {
  const lines = [];
  const { version, date } = ir.releaseHeader;
  lines.push(`## [${version}] - ${date}`);
  lines.push('');
  for (const section of ir.sections) {
    lines.push(`### ${section.type}`);
    lines.push('');
    for (const b of section.bullets) {
      // Prefix every logical continuation line with exactly two spaces. The
      // parser removes this transport prefix and preserves the remaining
      // Markdown indentation and line breaks verbatim.
      const bodyLines = b.body.split('\n').map((line, index) =>
        index === 0 ? `- ${line}` : `  ${line}`
      );
      bodyLines[bodyLines.length - 1] += ` (#${b.pr})`;
      lines.push(...bodyLines);
    }
    lines.push('');
  }
  let out = lines.join('\n');
  if (ir.priorChangelog) {
    out += '\n' + ir.priorChangelog;
  }
  return out;
}

/**
 * Inverse parser: extracts the structured releases from a CHANGELOG.md
 * text. Returns { releases: [{ version, date, sections: [{ type, bullets:
 * [{ pr, body }] }] }] }. Tolerates the actual repo's CHANGELOG dialect.
 *
 * Multi-line bullets are supported: a bullet opens on a line starting with
 * `- ` and continues on lines starting with two or more spaces (or a tab).
 * The `(#NNNN)` PR trailer may appear on any continuation line.  Single-line
 * bullets (entire entry on one `- ` line) are still handled as before.
 *
 * Fix for #3496: the previous implementation only matched single-line bullets
 * whose `(#NNNN)` suffix was on the same line as the opening `- `.  Long
 * bullets — which wrap onto indented continuation lines — returned 0 entries
 * for their section even when the markdown was well-formed.
 */
function parseChangelog(text) {
  const releases = [];
  const lines = text.split(/\r?\n/);
  let cur = null;
  let curSection = null;
  // Accumulates lines belonging to the current in-flight bullet (may span
  // multiple lines).  Flushed when a new block-level element is encountered.
  let bulletLines = null;

  function flushBullet() {
    if (bulletLines === null || !curSection) return;
    const joined = bulletLines.join('\n');
    // Locate the (# pr) trailer anywhere in the joined text.  The trailer is
    // expected to be at the very end, but we tolerate trailing whitespace.
    const trailMatch = joined.match(/^([\s\S]*?)\s*\(#(\d+)\)\s*$/);
    if (trailMatch) {
      curSection.bullets.push({ body: trailMatch[1], pr: Number(trailMatch[2]) });
    } else {
      // Bullet has no PR trailer — preserve it with pr: null so callers
      // (e.g. cmdExtract) do not silently drop authored content.
      curSection.bullets.push({ body: joined, pr: null });
    }
    bulletLines = null;
  }

  for (const line of lines) {
    // F3: match linked headers: ## [1.42.1](url) - 2026-05-15
    //     The (?:\([^)]*\))? group skips an optional (url) after the closing ]
    //     before looking for the optional date suffix.
    // F6: strip a leading `v` from the captured version so `## [v1.0.0]`
    //     parses as version "1.0.0" instead of "v1.0.0".
    const releaseMatch = line.match(/^##\s+\[([^\]]+)\](?:\([^)]*\))?\s*(?:-\s*(\S+))?/);
    if (releaseMatch) {
      flushBullet();
      const rawVersion = releaseMatch[1];
      const version = rawVersion.replace(/^v/, '');
      cur = { version, date: releaseMatch[2] || null, sections: [] };
      curSection = null;
      releases.push(cur);
      continue;
    }
    if (!cur) continue;
    const sectionMatch = line.match(/^###\s+(.+?)\s*$/);
    if (sectionMatch) {
      flushBullet();
      curSection = { type: sectionMatch[1], bullets: [] };
      cur.sections.push(curSection);
      continue;
    }
    if (!curSection) continue;

    // New bullet: line begins with `- ` (after optional leading spaces that
    // would indicate a nested list — we only handle top-level bullets here).
    if (/^-\s+/.test(line)) {
      flushBullet();
      bulletLines = [line.replace(/^-\s+/, '')];
      continue;
    }

    // Continuation line: remove only the Markdown transport indentation.
    // Content indentation after that prefix is significant (for example,
    // nested lists and indented code blocks) and must survive round trips.
    if (bulletLines !== null && /^[ \t]+/.test(line)) {
      const content = line.startsWith('  ')
        ? line.slice(2)
        : line.slice(1);
      bulletLines.push(content);
      continue;
    }

    // Any other line (blank, heading, etc.) terminates a pending bullet.
    flushBullet();
  }
  flushBullet();

  return { releases };
}

module.exports = { serializeChangelog, parseChangelog };
