# Examples

Three small projects that were built with the real `ggsad` command line. Each one has a finished
change (created, approved, started, implemented, closed) and a second change that waits for a
human answer, so `ggsad check <change-id>` shows both a closed and an open change.

| Example | Profile | Mode | What it shows |
| --- | --- | --- | --- |
| `lean-startup` | lean | team | The lightest setup: brief, constitution, one approver. |
| `solo-developer` | standard | solo | One person in every role; all project documents. |
| `governed-enterprise` | governed | team | A separate approver and minimum assurance level A1. |

The examples keep only the record files. They are not Git repositories and carry no anchors, so
`ggsad doctor` reports a warning about the missing anchor. To try one, copy it, then run:

```
git init && git add -A && git commit -m example
ggsad doctor
ggsad check <change-id>
```

Regenerate them with `uv run python scripts/build_examples.py`. A test
(`tests/unit/core/test_examples.py`) runs `doctor` and `check` on every example.
