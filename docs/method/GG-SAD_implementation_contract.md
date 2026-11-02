# GG-SAD — Implementation Contract

**Status:** Normative for the reference implementation only. The method itself does not depend on this document. It holds the automation contract (Section 22) and the state document, content hash, and schema versions (Section 25). A reference to a section other than 22 and 25 names the normative specification (`GG-SAD_normative_method_specification.md`).

---

## 22. Minimal Automation Contract

### 22.1 Contract Operations

A GG-SAD automation contract MUST support these technology-neutral operations:

- initialize a stand-alone GG-SAD project, as the operation `init`: it takes the compliance profile once, creates the configuration, the brief, and the template documents that the profile requires (Section 4.2 of the normative specification), never overwrites an existing file, and reports a difference between the profile of the configuration and the profile of the brief;
- create a goal-bound change;
- validate governing configuration, artifacts, references, and state;
- record a human decision (an approval, a sign-off, an override, or an answer) in the history of a change;
- migrate a schema-governed file to a newer schema version, as an explicit operation whose steps are recorded (Section 25.3);
- record a question of a change (Section 24.8);
- adopt the history of a change (Section 24.4);
- repair a damaged history of a change, as the owner of the project (Section 24.4);
- record a conflict between two documents as a question and a wait (Section 13.1);
- create a follow-up change that is pre-filled from a closed change (Section 23.1);
- report on a change, as the read-only actions `check`, `review`, `guard`, and `check-scope` (Section 22.4) do, with the status report of Section 23.8;
- evaluate and execute one controlled state transition under the transition table of Section 23.4. See AE-067.

The contract specifies observable behavior and compatibility requirements only. It does not prescribe a programming language, module structure, or vendor-specific agent interface.

**AE-067 — Asking a question is an operation of the contract**

- Covers: Section 22.1

Given an implementation of the contract and an `active` change
When a participant records a question
Then the operation is the contract operation that records a question, it appends an entry whose `action` is `ask` to the history of the change, and the transitions of the change are judged under the table of Section 23.4

### 22.2 Minimal Result Envelope

Every contract operation MUST return a result envelope containing three fields present in every response regardless of outcome: `operation`, identifying which contract operation ran; `result`, whose value is one of `success`, `rejected`, `blocked`, or `error` and is never partial; and `changed`, indicating whether persistent state changed.

The four results are exact lowercase names with these meanings:

- `success`: the operation took effect;
- `rejected`: the operation was invalid, or a precondition of the operation was not met; nothing was written, and `changed` is `false`;
- `blocked`: the operation was valid, its evaluation was recorded in the history, and the requested transition did not occur; `changed` is `true`;
- `error`: the operation could not be carried out; nothing was written, and `changed` is `false`.

A `rejected` result with `changed` true and a `blocked` result with `changed` false are invalid. Only the actions `close` and `resume` (Section 23.4) can answer `blocked`. Every other action answers `rejected` when it does not take effect. An action whose evaluation closes the change as failed answers `success` (Section 24.7). See AE-068, AE-069, AE-070.

The `state` field contains the resulting state of the change and is included when applicable to the operation; it is omitted when the operation produces no state result. It contains the state and the outcome (Section 23.2). The `issues` field contains stable codes plus human-readable messages. It is included whenever `result` is `rejected`, `blocked`, or `error`, and it then contains at least one issue; it is omitted whenever `result` is `success`. A result other than `success` without an issue is invalid. The `data` field is always optional operation-specific output and is present only when relevant to the operation.

A goal summary, specification anchor, gate outcome, evidence references, and timestamp are not universally required envelope fields. They MAY appear inside `data` when relevant to a specific operation.

An operation that uses a schema-governed file whose `schema_version` the implementation cannot use is refused with the result `rejected`, `changed` false, and nothing written. The stable issue code is `migration-required` when the version is older and can be migrated, `schema-version-unsupported` for every other unusable value, and `schema-version-mismatch` when the version of a state document differs from the latest recorded one (Section 25.3). See AE-094, AE-095, AE-096, AE-100.

**AE-068 — A blocked result is recorded and changes state**

- Covers: Section 22.2

Given an `active` `core` change with a done gate that is not satisfied  
When the `close` action is requested  
Then the result is `blocked` with `changed` true, the issues name the unsatisfied gate, the evaluation is recorded in the history, and the state remains `active`

**AE-069 — A rejected result writes nothing**

- Covers: Section 22.2

Given an `open` `core` change  
When the `close` action is requested  
Then the result is `rejected` with `changed` false, the issues state that the change is not `active`, and nothing is written to the history

**AE-070 — Reject an envelope whose changed value contradicts its result**

- Covers: Section 22.2

Given an envelope with the result `rejected` and `changed` true, and an envelope with the result `blocked` and `changed` false  
When the two envelopes are validated  
Then both are invalid

### 22.3 Rejection and Output Requirements

An invalid operation MUST be rejected without any partial mutation of persisted state. Its `result` MUST be `rejected` or `error`, and `changed` MUST be `false`.

A valid operation whose evaluation says that the requested transition does not occur is not an invalid operation. When the evaluation is recorded in the history, its result is `blocked` and `changed` is `true`; recording it is what makes the attempts countable under Section 24.2. An operation that is invalid, or whose precondition is not met, stays `rejected` or `error` with `changed` false. Section 23.4 states per action which result applies. See AE-068, AE-069.

For every operation, an implementation MUST emit both an actionable human-readable message and the structured result envelope. It MUST record transition history and relevant evidence under the transition table of Section 23.4 and Section 15 Evidence Model.

### 22.4 The `guard` and `check-scope` Actions

The action `check-scope` is read-only and legal from every state: it measures the paths changed since the base revision (Section 24.5) and reports those outside the allowed path list, without changing the state or the history and without running any command. It reports `not_evaluable` where the scope cannot be measured. The result is `success` with `changed` false when no path is outside the scope, and otherwise `rejected` with `changed` false and the issue code `scope-violation`.

The action `guard` is the verify-only action. It is read-only: it never changes the state or the history of a change, it is legal from every state, and it is not a row of the table of Section 23.4.

The action performs five verifications and reports the result of each:

1. The history is consistent (Section 24.4) and, where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor or an equivalent mechanism (Section 24.4).
2. The gate definitions equal the approved ones (Section 24.1).
3. Every approval is current for the content it names and has the level that the configuration or the gate requires (Section 24.3).
4. The scope, measured against the base revision, holds (Section 24.5).
5. No fail condition of the severity `hard` is active (Section 24.7). This is decided from the results that the history records and from the measurement of the scope, and not by running a command.

The action `guard` MUST NOT execute any command that the change or the project defines, that is the commands of gates, the evidence commands, and the interpreter that the project names (Sections 24.9 and 24.10), and an implementation MUST NOT execute one on its behalf.

The result is `success` with `changed` false when all five verifications hold. Otherwise the result is `rejected` with `changed` false and at least one issue that names each verification that failed, with these stable issue codes: `history-inconsistent` and `anchor-missing` for the first verification (`anchor-missing` is reported when the history has neither an anchor nor an equivalent mechanism, Section 24.4), `gates-changed` (Section 24.1) for the second, `approval-stale` for the third, `scope-violation` for the fourth, and `hard-failure-active` for the fifth. A verification that needs a state document that the change does not have is reported as not enforced, and it makes the result `rejected` (Sections 24.1 and 25.1).

Because the action runs nothing, it proves the record and not the outcome: it cannot confirm that the checks of the change pass, and running them stays a separate task. A pipeline that runs `guard` on a change is the verify-only integration of the method, and enforcement is by the caller, which acts on the result. See AE-071, AE-072, AE-073.

**AE-071 — A guard on a sound change succeeds and starts no program**

- Covers: Section 22.4

Given an `active` `core` change whose approved gate definitions are unchanged, with a consistent history, a scope that holds, no hard failure recorded, and a `check` gate whose program is missing  
When the `guard` action is requested  
Then the result is `success` with `changed` false, and no program is started

**AE-072 — A guard rejects a change whose gate definitions were edited**

- Covers: Section 22.4

Given an `active` `core` change whose gate definitions were edited after their approval and have not been approved again  
When the `guard` action is requested  
Then the result is `rejected` with `changed` false and the issue code `gates-changed`, and the history is unchanged

**AE-073 — A guard accepts an equivalent mechanism in place of an anchor**

- Covers: Section 22.4

Given a project whose configuration requires approvals at the level A2, and a change with a consistent history, no anchor, and an independent append-only record outside the working tree that holds the latest position and hash and is written only after each successful append  
When the `guard` action is requested  
Then the first verification holds, the issue code `anchor-missing` is not reported, and the result is `success` with `changed` false when the other four verifications hold

---

## 25. State, Hashing, and Schema Versions

This section defines the state document, the canonical form and the content hash that the protections of Section 24 rely on, and the versions of the schema-governed files. It applies to the `core` method profile (Section 5.6). The history, the entry hash, and the approvals that Section 24 describes are stored and hashed as this section states.

### 25.1 State Document and Canonical Form

The state document of a change is the JSON file `state.json` in the change directory (Section 4.3). It holds the history of the change (Section 24.4). The implementation owns it, and a human MUST NOT edit it by hand (Section 23.1). The definitions that humans own, such as the change definition and the project configuration, stay YAML documents. Every change has a state document.

The state document is a JSON object with two fields. `schema_version` holds the version of the schema of the document, and Section 25.3 defines its form and the checks on it. `entries` holds the history: a list of entries in ascending order of `n`, each with the four fields `n`, `prev`, `body`, and `hash` that Section 24.4 defines.

The `body` of an entry holds exactly these fields:

- `action`: the name of the operation that the entry records, which is `new`, `approve`, `ask`, `answer`, `adopt`, `repair`, `conflict`, or `migrate` (Section 25.3), or an action of the transition table of Section 23.4. The set of names is closed, and an entry with another name is not valid;
- `actor`: the identity of the participant that performed the action (Section 24.3);
- `account`: the real account of the actor that the implementation reads from version control or from the hosting service, next to the typed identity in `actor`, or `null` when none can be read (Section 24.3);
- `assurance`: the verified assurance level of the claim of the actor, which is `A0`, `A1`, or `A2` (Section 24.3);
- `at`: the instant at which the entry was written, as a string in UTC that is written `YYYY-MM-DDThh:mm:ssZ`;
- `result`: the result of the action, which is `success` or `blocked` (Section 22.2), because an action that is `rejected` or ends in `error` writes no entry;
- `gate_results`: an object from the identifier of each gate that the action evaluated, or skipped as a gate that does not apply, to the value recorded for it, or `null` when the action evaluated no gate. The value is one of the three results of Section 24.2, written in exact lowercase, or the marker `not_applicable` that Section 23.6 prescribes. No other value is valid;
- `gate_detail`: an object from the identifier of a gate that has a value in `gate_results` to the text that the evaluation recorded for it, or `null` when the evaluation recorded none;
- `files`: an object from a path to the content hash of the file (Section 25.2), for the files that the action approved, evaluated, or recorded, or `null` when it concerns no file;
- `note`: the text that the actor gave, or `null`;
- `after`: the record of the state of the change after the action.

A field that does not apply to an action is present with the value `null`. The body holds no other field, except that an action MAY be defined to add fields for itself, and Section 25.3 defines such fields for `migrate`. The `close` action of an agent adds `agent_report` (Section 19.1 of the normative specification: the errors seen, the decisions returned to the owner, and the exceptions recorded). The `repair` action adds `repaired` (Section 24.4 of the normative specification: the damage found, the number of entries lost, the old anchor, the location of the damaged file, and the reason). The first entry of a change that the `new` action created is `new` (the first entry of a state document that was converted from a YAML state document is the `migrate` entry of Section 25.3), the entry of an approval is `approve`, and an entry with a name outside the closed set of `action` is not valid. See AE-079, AE-075, AE-083, AE-084.

The `after` record holds the whole state of the change after the action, and not only what the action changed, so that the state of the change is the `after` record of the last entry (Section 24.4). In `core`, it holds these fields:

- `state` and `outcome` (Section 23.2);
- `approvals`: the approvals recorded so far, in the order of their recording, each naming its target, the identity, the verified assurance level, the `required_level`, and the content hash that was approved (Section 24.3), and for a sign-off, an override, and a re-approval also the fields that Sections 24.1 and 24.7 call for;
- `questions`: the questions recorded so far, with the fields of Section 24.8;
- `wait`: the wait record (Section 23.5), or `null`;
- `base_revision`: the base revision (Section 24.5), or `null` before it is recorded;
- `replaced_by`: the identifier given to `supersede`, or `null`;
- `reason`: `null` unless the outcome is `failed`; when the `fail` action ended the change, the reason text that the actor gave; when a hard fail condition ended the change, a text that names each failing gate and the detail that the evaluation recorded for it, such as the paths outside the scope (Section 24.5); when `cancel` or `supersede` ended a change that awaited the disposition of a soft fail condition, the reason text that the actor gave or, when the actor gave none, a text that names that soft fail condition (Section 23.4);
- `schema_version`: the version of the schema of the document after the action (Section 25.3).

The file is a JSON text in UTF-8. Its layout, that is, indentation and line breaks, is free, and a writer SHOULD pretty-print it so that a human can read it. The file is not the hashed form: a hash is computed over the canonical form defined below and never over the text of the file, so the layout has no effect on a hash. A JSON object that holds the same key twice is not a valid state document. See AE-078.

The values of a state document, and every value that is hashed, belong to a small domain: strings, integers, booleans, `null`, arrays, and objects whose keys are strings. A string is a sequence of Unicode code points that holds no surrogate code point. An integer is a whole number written in decimal digits, without a fraction or an exponent, and its magnitude does not exceed 2 to the power 53, minus 1, so that implementations that store numbers as double-precision values agree. A floating-point number is not in the domain. An implementation that is about to write or hash a value outside the domain MUST stop with the result `error` and MUST write nothing. See AE-077.

The canonical form of a value is the text built by these rules:

- no whitespace is written outside a string, the elements of an array and the members of an object are separated by `,`, and a key is separated from its value by `:`;
- the members of an object are written in ascending order of their keys, compared as sequences of Unicode code points as defined below, and an object does not hold the same key twice;
- a string is enclosed in `"`; the code point `"` is written `\"` and the code point `\` is written `\\`; the code points U+0008, U+0009, U+000A, U+000C, and U+000D are written `\b`, `\t`, `\n`, `\f`, and `\r`; every other code point below U+0020 is written `\u` followed by four lowercase hexadecimal digits; every other code point is written as itself, so that no code point is written as an escape because it is outside ASCII, and the code points U+007F and `/` are written as themselves;
- an integer is written in decimal digits, with a leading `-` when it is negative, without a leading `+`, without a leading zero, and the integer zero is written `0`; the other values are written `true`, `false`, and `null`.

The canonical bytes of a value are the UTF-8 encoding of its canonical form, without a byte order mark and without a final line feed. See AE-074.

Strings are compared as sequences of Unicode code points: the first code point at which two strings differ decides the order by its numeric value, and a string that is a prefix of a longer string comes first. Letter case matters, and nothing is normalized. The comparison is not a comparison by UTF-16 code units, which orders some characters above U+FFFF differently. Every comparison of identifiers, paths, and values that Section 24 makes is made in this way. See AE-076.

A hash is written as a hash string: the prefix `sha256:` followed by the 64 lowercase hexadecimal digits of the SHA-256 digest of some bytes. The hash string of a value is the hash string of its canonical bytes. The hash of an entry is the hash string of the object that holds `prev` and `body` (Section 24.4), and the `prev` of the first entry is the prefix `sha256:` followed by 64 digits 0. A hash string is compared as a string, so that a hash written with an uppercase digit differs from the same hash written with lowercase digits.

An implementation MUST write the state document with an atomic replacement. It writes the whole new document to the temporary file `state.json.tmp` in the change directory, flushes it to storage when the system allows, and then replaces the state document with the temporary file in a single step of the file system. Until that step, the state document is the previous one. An interruption at any moment, such as a crash, a power loss, or a failed write, therefore leaves the previous state document intact, and a file `state.json.tmp` that is left behind is not state: an implementation MUST ignore it and MAY remove it. The scope measurement does not count it (Section 24.5). When the file system cannot replace a file in a single step, the implementation MUST NOT write, and its result is `error`. The creation of the first state document of a change is a replacement in the same way: an interrupted creation leaves no state document. See AE-085, AE-086.

An implementation MUST also protect a write against a second writer. The writer names the version it read, which is the number of entries of the state document at that time, and zero for a change that has no state document yet. It takes an exclusive lock on the lock object `state.json.lock` in the change directory, before it compares and also when the change has no state document yet, and keeps the lock across the comparison and the replacement until the replacement has finished. The lock is one that the system releases when the process that holds it ends, so that a file `state.json.lock` that exists is not by itself a held lock and does not stop a writer. A file `state.json.lock` that is left behind is not state: an implementation MUST ignore it and MAY remove it when no process holds the lock. The scope measurement does not count it (Section 24.5). Under the lock it compares the number of entries that the document holds now with the version it read. When the two differ, the operation MUST write nothing and its result MUST be `error` with the stable issue code `state-conflict`, whose message states that another writer changed the change and that the operation can be repeated after reading it again. A writer that cannot take the lock MUST NOT write, and its result is `error`. This applies to the creation of a change and to every operation that appends an entry, which are all the actions of the transition table of Section 23.4 that record an entry, and `approve`, `ask`, `answer`, `adopt`, and `migrate`. See AE-080, AE-081.

**AE-074 — The canonical form sorts the keys, drops whitespace, and keeps non-ASCII characters**

- Covers: Section 25.1

Given an object with the member `name`, whose value is `café` written with the single code point U+00E9, and the member `count`, whose value is the integer 2, listed in that order  
When its canonical form is built and hashed  
Then the canonical text is `{"count":2,"name":"café"}`, the code point U+00E9 is written as itself and encoded in UTF-8 as the two bytes C3 and A9, and the hash string is `sha256:29775eba68050199f13058db83b4c14ba4b6a6a26666d6373a3cc47481bf6471`

**AE-075 — The marker not_applicable is a value of gate_results and a wrong case is not**

- Covers: Section 25.1

Given a `start` action that evaluated the hard fail gate `no-secrets` to `not_satisfied` and skipped the `check` done gate `docs-built`, which does not apply to `start`
When the entry of the action is built once with `gate_results` that maps `no-secrets` to `not_satisfied` and `docs-built` to `not_applicable`, and once with `gate_results` that maps `no-secrets` to `Not_satisfied`
Then the first entry is accepted, because the marker `not_applicable` is a valid value, and the second is rejected, because a result written in another letter case is not a valid value

**AE-076 — Keys are ordered by code point and not by UTF-16 code unit**

- Covers: Section 25.1

Given an object with two members whose keys are the single code points U+1F600 and U+FF5E, listed with U+1F600 first  
When its canonical form is built  
Then the member with the key U+FF5E is written first, because U+FF5E is the lower code point, although an order by UTF-16 code units would place U+1F600 first

**AE-077 — A value outside the domain is neither written nor hashed**

- Covers: Section 25.1

Given an entry body in which one value is the floating-point number 1.5  
When the implementation is about to write the entry  
Then the operation ends with the result `error`, and nothing is written

**AE-078 — The layout of the file does not change a hash**

- Covers: Section 25.1

Given a state document of three entries, and the same document written again with other indentation and other line breaks but with the same values  
When the history is verified  
Then both documents give the same entry hashes, and both histories are consistent

**AE-079 — Every body field is present and a field that does not apply is null**

- Covers: Section 25.1

Given an `ask` action that evaluates no gate, concerns no file, and gives no note  
When the entry is written  
Then the body holds the ten fields `action`, `actor`, `assurance`, `at`, `result`, `gate_results`, `gate_detail`, `files`, `note`, and `after`, and `gate_results`, `gate_detail`, `files`, and `note` are `null`

**AE-080 — The second of two writers with the same version fails when a change is created**

- Covers: Section 25.1

Given two writers that both read that no state document of the change `c-1` exists, and the first writer has created the state document
When the second writer tries to create it with the version zero
Then the second writer writes nothing, its result is `error` with the issue code `state-conflict`, and the state document is the one that the first writer created

**AE-081 — The lock covers every operation that appends an entry, and a leftover lock file is not a held lock**

- Covers: Section 25.1

Given an `active` `core` change with a state document of six entries, a file `state.json.lock` that a process left behind when it ended, and two writers that both read the version 6  
When both writers request the `ask` action and the first writer takes the lock and records its question as entry 7  
Then the leftover file did not stop the first writer, the second writer writes nothing, its result is `error` with the issue code `state-conflict`, and the state document holds seven entries

**AE-082 — The reason of a failed outcome is recorded in the after record**

- Covers: Section 25.1

Given an `active` `core` change whose `scope.allow` is `lib/**` and in which the file `docs/guide.md` changed, a second change that is `waiting` with a wait record of kind `fail-gate` and receives the `fail` action with the reason `retries exhausted`, and a third change that is `closed` with the outcome `done`  
When the `after` record of the last entry of each change is read, the first one after a `close` action  
Then the `reason` of the first change is a text that names the failing gate and the path `docs/guide.md`, the `reason` of the second change is `retries exhausted`, and the `reason` of the third change is `null`

**AE-083 — The action of an entry is the name of an operation from a closed set**

- Covers: Section 25.1

Given a new change that is created and then approved, and an entry whose `action` is `rewind`
When the entries are written and the entry with that name is validated
Then the first entry of the change has the `action` `new`, the entry of the approval has the `action` `approve`, and the entry whose `action` is not in the closed set is not valid

**AE-084 — The first entry of a converted state document is a migrate entry**

- Covers: Section 25.1

Given a change that the `new` action created, and a change whose state document was converted from a YAML state document
When the first entry of the state document of each change is read
Then the first entry of the first change has the `action` `new`, and the first entry of the second change is the `migrate` entry with `n` 1 (Section 25.3)

**AE-085 — An interrupted creation leaves no state document**

- Covers: Section 25.1

Given a new change whose state document is being created, and the process stops after the temporary file is written and before the replacement
When the project is read again
Then the change has no state document, the temporary file is ignored, and the creation can be repeated

**AE-086 — An interrupted write of an evaluation leaves the previous state intact**

- Covers: Section 25.1

Given an `active` change with a state document of six entries, and the process stops while the entry 7 that records an evaluation is being written
When the state document is read again
Then the document is the previous one of six entries, it is consistent, and no part of the entry 7 is in it

### 25.2 Content Hash

The content hash is the hash string (Section 25.1) that identifies some content. An approval binds the content hash of what it approves (Section 24.3), and the identity of fixed gate definitions is a content hash (Section 24.1). This section defines the content hash of the content that those sections name.

The content hash of a text file is the hash string of the bytes of the file after its line endings are normalized: every pair of a carriage return followed by a line feed, and every carriage return that is not followed by a line feed, is replaced by a line feed. Nothing else is changed. A file with the same text and different line endings therefore has the same content hash. See AE-087.

The content hash of a binary file is the hash string of the bytes of the file, exactly.

A file is text exactly when its bytes are valid UTF-8 and hold no zero byte, and every other file is binary. An implementation MUST classify a file in this way. Valid UTF-8 is a sequence of bytes that encodes Unicode scalar values in the shortest form, with no surrogate code point and no value above U+10FFFF. The decision depends on the bytes only, so that every conforming implementation computes the same content hash for the same bytes. The hash string does not state which kind was applied, and a content hash that one implementation computed can be compared with one that another implementation computed. A content hash that differs from the recorded one is a difference. See AE-088.

The content hash of a parsed definition, such as the gate definitions of a change (Section 24.1), is the hash string of the canonical bytes of the parsed value (Section 25.1) and not of the text of the file. A YAML document is read as YAML 1.2 with its core schema, and an alias is replaced by the value it refers to. Comments, layout, the order of the keys of a mapping, and the quoting of a scalar that reads as the same value therefore have no effect, and the order of the elements of a sequence has an effect. A parsed value that is outside the domain of Section 25.1 has no content hash: this holds for a floating-point number, a mapping key that is not a string, a mapping that repeats a key, and a scalar that the core schema reads as a type that the domain does not hold. An operation that needs the content hash of such a definition MUST be rejected, and its issue states which value is outside the domain. See AE-089, AE-090.

The content hash of a set of files is the hash string of the canonical bytes of an object that maps the path of each file to its content hash. A path is written relative to the root of the repository, with `/` as the separator (Section 24.5). The order in which the files are listed has no effect. See AE-091.

The content hash of the gate definitions together with the identifier of a gate, which binds the sign-off of a gate and an override (Section 24.3), is the hash string of the canonical bytes of an object with the member `definitions`, which holds the content hash of the gate definitions, and the member `gate`, which holds the identifier. See AE-092.

**AE-087 — Text with different line endings has one content hash**

- Covers: Section 25.2

Given two text files that hold the same two lines, the first with the line ending carriage return and line feed and the second with the line ending line feed alone  
When the content hash of each file is computed  
Then the two content hashes are equal

**AE-088 — The kind of a file is decided by its bytes**

- Covers: Section 25.2

Given three files with the line ending carriage return and line feed, of which the first holds text that is valid UTF-8, the second holds the byte 00, and the third holds bytes that are not valid UTF-8, and for each of them a variant with the line ending line feed alone  
When the content hash of each of the six files is computed  
Then the first file has the same content hash as its variant, because it is text, and the second and the third file each have a content hash that differs from the content hash of their variant, because they are binary and are hashed byte for byte

**AE-089 — Layout and comments do not change the hash of a parsed definition, and a list order does**

- Covers: Section 25.2

Given a gate definition file, a copy with an added comment, other indentation, the keys of a mapping in another order, and a quoted scalar that reads as the same string, and a third copy in which the order of two elements of a list is exchanged  
When the content hash of each file is computed as a parsed definition  
Then the first copy has the same content hash as the original, and the third copy has a different content hash

**AE-090 — A definition with a value outside the domain has no content hash**

- Covers: Section 25.2

Given a gate definition in which a retry limit is written as the floating-point number 1.5, and the same definition in which the value is the quoted string `1.5`  
When the approval of the gate definitions is requested for each  
Then the first approval is rejected and its issue names the value outside the domain, and the second definition has a content hash

**AE-091 — The order of the files has no effect on the hash of a set**

- Covers: Section 25.2

Given a set of the two files `lib/a.py` and `docs/b.md`, listed in the first order and then in the reverse order  
When the content hash of the set is computed  
Then both orders give the same content hash, which is the hash string of the canonical bytes of the object that maps `docs/b.md` and `lib/a.py` to their content hashes

**AE-092 — The identifier of the gate is part of the hash of a sign-off**

- Covers: Section 25.2

Given the same gate definitions and two gate identifiers, `review-ok` and `release-ok`  
When the content hash of the gate definitions together with each identifier is computed  
Then the two content hashes differ, because the member `gate` of the hashed object differs

### 25.3 Schema Versions and Migration

Every machine-readable file that a schema governs carries the top-level field `schema_version`. These files are the project configuration (`.ggsad/config.yaml`), the integration mappings, the change definition (Section 23.1), and the state document (Section 25.1). A Markdown document, such as the specification of a change, has no schema and no schema version.

The value of `schema_version` is a string of two non-negative integers that are written in decimal digits and joined by one dot, such as `0.1`. Neither integer has a sign or a leading zero, except that the integer zero is written `0`. Two versions are compared one integer at a time, from left to right, by the numeric value of each integer, so that `0.9` is older than `0.10` and `0.10` is older than `1.0`. A value that is not a string, for example the number 0.1 that a YAML file holds when the value is not quoted, is not a version.

An implementation supports one or more versions of each kind of file: it reads and writes a file of a supported version as it is. It MAY also hold migration steps, and each step converts a file from one version to the next higher version. A version is migratable when it is not supported, when it is lower than the highest supported version, and when a chain of steps leads from it to a supported version. See AE-097.

Before an implementation uses a governed file for an operation, it MUST check the `schema_version` of the file. For a state document, the comparison with the latest recorded version that is described below is made first, and only a document that matches it is checked against the supported versions:

- a version that equals a supported version is accepted;
- a migratable version is refused until the file is migrated explicitly: the operation answers `rejected` with the stable issue code `migration-required`;
- every other value is refused with the result `rejected` and the stable issue code `schema-version-unsupported`: a version that is newer than every supported version, a version that is unknown, a missing field, the value `null`, an empty string, a value that is not a string, and a string that is not a version.

A refusal writes nothing and leaves `changed` false (Section 22.2). It applies to every operation that uses the file, including a read-only operation and the validation of the file, and it applies to the state document of a change in the same way as to the other files. The one exception is the `migrate` operation, which accepts a migratable version. An implementation MUST NOT guess the content of a file of a version that it does not support, and MUST NOT write such a file. See AE-093, AE-094, AE-095, AE-096.

The `migrate` operation (Section 22.1) is the only way to change the version of a file. It is explicit and it is never carried out silently as a part of another operation. It takes the file and optionally a target version, which is a supported version that is higher than the version of the file and which is the highest supported version when it is not given. It applies the steps of the chain one at a time in ascending order of version, so that no step is skipped and no step is applied twice, and it records each step. When a step cannot be applied, the operation writes nothing and answers `error`; the steps that were applied before it are not kept. A file that already has the target version, or a higher one, is not migrated, and the operation answers `rejected`. See AE-098.

A migration of the state document appends one entry to the history for each step. The body of the entry has the action `migrate` and the result `success`, and in addition to the fields of Section 25.1 it holds `source_version`, the version before the step, `target_version`, the version after the step, and `source_hash`, the source content hash, which is the content hash (Section 25.2) of the state document before the step, taken as a parsed value for a state document written in JSON and as a text file for a state document written in YAML. The `after` record of the entry holds the target version in `schema_version`, and the field `schema_version` of the state document is set to the version after the last step. The entries that the history already holds are kept as they are: a migration appends to the history and MUST NOT rewrite an entry, and the `n`, `prev`, `body`, and `hash` of every earlier entry are unchanged. See AE-098, AE-099.

The version of the state document MUST equal the latest recorded version, which is the `schema_version` of the `after` record of the last entry. A state document whose version differs from it, whether lower or higher, is not consistent in the sense of Section 24.4. An implementation MUST NOT act on it, and its result is `rejected` with the stable issue code `schema-version-mismatch`. This detects a state document whose version was lowered by hand in order to run a migration again, or to make a refusal disappear. Because the comparison is made first, such a document is refused with `schema-version-mismatch` even when the lowered version is a migratable one. See AE-100.

A project-level artifact, that is, the project configuration or the integration mappings, is migrated inside a change: the `migrate` operation names a change that is not `closed`, and the migration is recorded in the history of that change, in an entry whose `files` field maps the path of the artifact to its content hash after the step, and whose `source_hash` is its content hash before the step. The change definition and the state document of a change are migrated as part of that change. A migration that changes the parsed gate definitions of a change makes them differ from the approved ones, and Section 24.1 then requires that a human approves them again. The `migrate` operation does not change the state or the outcome of a change. Applied to the state document or the change definition of a change, it is therefore legal from every state of that change, and it is not a row of a transition table. See AE-101, AE-102.

A state document that an earlier version of this method wrote as a YAML document named `state.yaml` is migrated by the `migrate` operation, which converts it to `state.json` as a step of the chain. The first entry of the new state document is a `migrate` entry with `n` 1 and the `prev` of Section 25.1, whose `source_hash` is the content hash of the old file as a text file and whose `after` record holds the state that was taken over from the old document. The operation neither changes nor deletes the old file, and once `state.json` exists the old file is not read. The chain of hashes starts at that entry: the earlier history is not covered by it, and an anchor that exists for the change makes a history that was restarted in this way detectable (Section 24.4). See AE-103.

**AE-093 — A version that equals a supported version is accepted**

- Covers: Section 25.3

Given an implementation that supports the version `0.1`, and a project configuration with `schema_version` set to `"0.1"`  
When an operation reads the project configuration  
Then the version is accepted, and the operation goes on

**AE-094 — An older migratable version is refused until it is migrated**

- Covers: Section 25.3

Given an implementation that supports only the version `1.0` and holds a step from `0.1` to `1.0`, and a change definition with `schema_version` set to `"0.1"`  
When the `validate` operation is requested for the change  
Then the result is `rejected` with `changed` false and the issue code `migration-required`, nothing is written, and after an explicit `migrate` the same operation accepts the change definition

**AE-095 — A newer version is refused**

- Covers: Section 25.3

Given an implementation that supports only the version `1.0`, and a state document with `schema_version` set to `"1.1"`  
When any operation, including a read-only one, uses the state document  
Then the result is `rejected` with `changed` false and the issue code `schema-version-unsupported`, and nothing is written

**AE-096 — A missing, null, or empty version is refused**

- Covers: Section 25.3

Given three project configurations, the first without the field `schema_version`, the second with `schema_version` set to `null`, and the third with `schema_version` set to the empty string  
When an operation reads each of them  
Then each read is refused with the result `rejected` and the issue code `schema-version-unsupported`, and nothing is written

**AE-097 — Versions are compared one integer at a time**

- Covers: Section 25.3

Given an implementation that supports only the version `0.10` and holds a step from `0.9` to `0.10`, and two change definitions with the versions `"0.9"` and `"0.100"`  
When an operation reads each of them  
Then the version `0.9` is migratable and is refused with the issue code `migration-required`, and the version `0.100` is newer than the supported version and is refused with the issue code `schema-version-unsupported`

**AE-098 — A migration applies its steps in ascending order and records each**

- Covers: Section 25.3

Given an implementation that supports only the version `2.0` and holds the steps `1.0` to `1.1` and `1.1` to `2.0`, and a state document of six entries with `schema_version` set to `"1.0"`  
When the `migrate` operation is requested for the state document without a target version  
Then the step from `1.0` to `1.1` is applied and recorded as entry 7, the step from `1.1` to `2.0` is applied and recorded as entry 8, each entry names its source version, its target version, and its source content hash, and the version of the state document is `"2.0"`

**AE-099 — A migration appends and does not rewrite an entry**

- Covers: Section 25.3

Given a state document of six entries that is consistent, and a migration of it to a newer version  
When the history is read again after the migration  
Then the entries 1 to 6 have the same `prev`, `body`, and `hash` as before, the entries 7 and later are the migration entries, and the history is consistent

**AE-100 — A lowered version of the state document is detected**

- Covers: Section 25.3

Given an implementation that supports only the version `1.1` and holds a step from `1.0` to `1.1`, and a state document whose last entry records the version `"1.1"`, and a hand edit that sets the field `schema_version` of the document to `"1.0"`  
When any operation is requested for the change  
Then the result is `rejected` with the issue code `schema-version-mismatch` and not `migration-required`, nothing is written, and the implementation does not act on the change

**AE-101 — A project-level artifact is migrated inside a change and recorded in it**

- Covers: Section 25.3

Given a migratable project configuration, an `active` change `c-1`, and a `closed` change `c-0`  
When the `migrate` operation for the project configuration names `c-1`, and then another `migrate` operation names `c-0`, and then a third names no change  
Then the first migration succeeds and the history of `c-1` gets an entry whose `files` field maps the path of the project configuration to its content hash after the step and whose `source_hash` is its content hash before the step, and the second and the third operation are rejected and write nothing

**AE-102 — A migration that changes the gate definitions needs a new approval**

- Covers: Section 25.3

Given an `active` `core` change whose gate definitions were approved, and a change definition whose migration changes its parsed gate definitions  
When the change definition is migrated and then the `close` action is requested  
Then the migration is recorded, and the `close` action is rejected with the issue code `gates-changed` until a human approves the gate definitions again

**AE-103 — A YAML state document is converted by an explicit migration**

- Covers: Section 25.3

Given a change directory with a YAML state document named `state.yaml` and no `state.json`  
When the `migrate` operation is requested for the change  
Then `state.json` is created with a first entry that is a `migrate` entry with `n` 1 and the `prev` of the first entry, whose `source_hash` is the content hash of the old file as a text file, the old file is neither changed nor deleted, and later operations read only `state.json`

