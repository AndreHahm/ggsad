# Third-Party Notices

This document identifies third-party software intentionally used by or integrated with the GG-SAD
reference implementation.

It is provided for attribution and license-notice purposes. It does not replace the license files
distributed by the respective third-party projects.

## GSD Core

- Component: GSD Core
- Package: `@opengsd/gsd-core`
- Project: `open-gsd/gsd-core`
- Copyright: Copyright (c) 2026 Open GSD
- License: MIT License
- Usage in GG-SAD: Optional project-local execution and context-engineering companion
- Installation:

  ```bash
  npx @opengsd/gsd-core@latest --claude --local
  ```

### Relationship to GG-SAD

GSD Core is not part of the GG-SAD Method Core.

GG-SAD may use GSD Core to support:

- implementation discussion;
- subordinate execution planning;
- context engineering;
- implementation execution;
- verification support;
- shipping or pull-request preparation.

GG-SAD remains authoritative for:

- goals and approved scope;
- governing documents;
- specifications;
- architecture and ADR precedence;
- workflow state;
- Definition of Ready, Done, Wait, and Fail;
- evidence requirements;
- approvals;
- Pair Review policy;
- change closure.

GSD-generated files under `.planning/` are third-party-tool execution artifacts and remain
subordinate to GG-SAD artifacts.

### Distribution and Generated Files

The GSD installer may install runtime-specific commands, agents, skills, hooks, configuration, or
other files into project-local tool directories.

Before redistributing installed or generated GSD files:

1. identify the exact installed GSD version;
2. retain applicable copyright and license notices;
3. inspect the installed package and generated files for additional notices;
4. ensure that modifications are identified where required by project policy;
5. do not imply endorsement by Open GSD;
6. update this document when the package name, project ownership, license, or usage changes.

The package version should be recorded in the repository lockfile, installation evidence, or
project documentation when GSD is installed.

## GSD Core MIT License

```text
MIT License

Copyright (c) 2026 Open GSD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Other Dependencies

The Python package declares runtime and development dependencies in `pyproject.toml`. Their
transitive licenses are not reproduced in this initial notice.

Before publishing a source distribution, wheel, binary bundle, container image, hosted service, or
other distributable artifact, the project must:

- generate an exact dependency inventory from the resolved lockfile;
- identify direct and transitive licenses;
- verify license compatibility with the project license and distribution model;
- include required notices and license texts;
- review bundled assets, templates, schemas, generated files, and documentation;
- record the review as release evidence.

This file must be updated when the repository begins distributing third-party code or assets beyond
the project-local GSD integration described above.

## Notice Maintenance

Update this document when:

- a third-party component is added, removed, renamed, forked, or replaced;
- a component's license or copyright notice changes;
- third-party source or substantial portions are copied into the repository;
- generated files are committed and require attribution;
- a new distribution format introduces bundled dependencies;
- a release-license review identifies additional notice obligations.

Where this document conflicts with an upstream third-party license, the upstream license text
distributed with that component governs that component.
