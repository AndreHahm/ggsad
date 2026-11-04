# Third-Party Notices

This document identifies third-party software intentionally used by or integrated with the GG-SAD
reference implementation.

It is provided for attribution and license-notice purposes. It does not replace the license files
distributed by the respective third-party projects.

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

This file must be updated when the repository begins distributing third-party code or assets.

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
