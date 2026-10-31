# GG-SAD — Signing Extension

**Status:** Optional extension. A project MAY adopt it. It extends Section 24.3 of the normative specification (`GG-SAD_normative_method_specification.md`) with the assurance levels `A1` and `A2` and the signed approval. A reference to a section of the normative specification names that document.

---

### 24.3 Assurance Levels and Signed Approval

This extension defines the assurance levels above `A0` of Section 24.3 of the normative specification, the statement that a signed approval signs, and the limit of what any level proves. A project MAY adopt it. A project that does not adopt it treats every claim as `A0`.

There are three assurance levels. In order from the lowest to the highest they are `A0`, `A1`, and `A2`, and these exact strings are their names:

- `A0`, self-declared: no check of the claim exists. Every claim is worth exactly A0 unless a verifier establishes a higher level;
- `A1`, platform review: the latest review by the platform account that the project configuration maps to the claimed identity is an approval of the revision that is checked out, and none of the files that are approved has an uncommitted change. The review is recorded by the platform that hosts the project, on the review object of the change, for example a pull request;
- `A2`, signature: the claim carries a valid signature over exactly the statement that the implementation builds for the action, made with a key that is listed for the claimed identity in a signers file. The signers file is kept outside the repository of the project, so that a participant who can change the repository cannot add a key for itself.

The levels, their order, and the statement defined below are normative. The verifiers are not: an implementation MAY verify `A1`, `A2`, or both. An implementation that verifies neither treats every claim as A0. An implementation that verifies A2 MUST verify it over the statement defined below and over no other statement.

Verification MUST fail closed. A claim whose level cannot be established is A0, whatever the reason: no verifier exists, the platform does not answer, the signers file cannot be read, the signature is not valid, the key is not listed for the identity, or the statement that was signed differs from the statement that the implementation builds. An action whose required level is higher than the verified level of its claim MUST be rejected, with `changed` false (Section 22.2). A claim that carries no signature and no review is not malformed: it is a claim at A0, and it is rejected only where the required level is higher. See AE-104, AE-106, AE-107, AE-041.

The statement of a signed approval is built by the implementation from the action that it is about to perform. A statement that the participant supplies is not accepted, so that what is signed cannot differ from what is verified. The statement is text in lines, each ended by a line feed, and the bytes that are signed are its UTF-8 encoding. It contains, in this order:

1. a first line that holds the format identifier and the format version of the statement;
2. the operation, which is the name of the action;
3. the change, which is the identifier of the change;
4. the version, which is the number of entries that the history of the change holds when the statement is built (Section 24.4), so that the statement names the history that the action extends;
5. the identity of the signer;
6. the details of the action, one line for each detail field, in ascending order of the field names compared as Section 24 states. The details of an approval include its target and the content hash of the content that is approved.

Each line after the first has the form `name: value`, and each value is encoded as JSON, in the way that Section 25.1 encodes a value, so that no value can contain a line feed and no value can inject a line of its own. A statement with a format identifier or a format version that the verifier does not support is not verified. The specification fixes that the format identifier and the format version are part of the statement, and it does not fix their spelling. An illustration, not normative:

```text
<format identifier> <format version>
operation: "approve"
change: "c-1"
version: 4
identity: "human:ada"
content_hash: "sha256:<64 hexadecimal digits>"
target: "spec"
```

A signature made for a statement is valid only for that statement. A signature made at another position of the history, for another change, for another operation, or over other content is not valid for the statement that the implementation builds now. See AE-107.

A private key that is not protected by a passphrase, or by an equivalent protection, lets every process and every participant that can read the key sign as its holder. An implementation that creates signatures SHOULD refuse such a key unless a human explicitly allows its use. The signers file lists public keys only, and a participant that can write the signers file can list its own key for any identity. See AE-109.

No level proves that a human is present. An agent that is able to use a human's credentials can act as that human, and this holds at every level. At A0, any participant can write any identity. At A1, the platform sees the account and not the participant that operates it, so an agent that holds the login of the account can approve as the account holder; and a platform commonly does not let the author of a review object approve it, so A1 does not serve a participant who works alone. At A2, an agent that can read an unprotected private key, or that can use a key which a running process holds, can sign as the signer. The levels raise the cost of a false claim, and they do not exclude it. See AE-109.

**AE-104 — Reject an A0 claim where A2 is required**

- Covers: Section 24.3

Given an `open` `core` change in a project whose configuration sets the minimum level A2 for the approval of the specification  
When a participant that claims the identity `human:ada` approves the target `spec` and carries no signature  
Then the verified level is A0, which is below the required level A2, the approval is rejected with `changed` false, and no approval is recorded

**AE-105 — Accept a valid signature at A2**

- Covers: Section 24.3

Given the same change and configuration, and a signers file outside the repository that lists a key for `human:ada`  
When the approval of the target `spec` carries a valid signature by that key over the statement that the implementation builds  
Then the approval is recorded with the verified level A2 and with the content hash of the specification that was approved

**AE-106 — A forged signature fails closed**

- Covers: Section 24.3

Given the same change and configuration, and a signers file that lists a key for `human:ada`  
When the approval of the target `spec` carries a signature made with a key that is not listed for `human:ada`  
Then the claim is A0, the approval is rejected, and no approval is recorded

**AE-107 — A signature replayed at another history position fails**

- Covers: Section 24.3

Given a signature that is valid for an approval of `spec` whose statement names the version 4, and a `core` change whose history now holds five entries, in a project whose configuration sets the minimum level A2  
When the approval is presented again with that signature  
Then the statement that the implementation builds names the version 5, the signature is not valid for it, the claim is A0, and the approval is rejected

**AE-108 — A1 requires that the approved files have no uncommitted change**

- Covers: Section 24.3

Given a project whose configuration sets the minimum level A1 for the approval of the specification, a platform account mapped to `human:ada` whose latest review approves the checked-out revision, and an uncommitted change in the specification of the change  
When `human:ada` approves the target `spec`  
Then the claim is A0, because an approved file has an uncommitted change, and the approval is rejected

**AE-109 — An agent with a human's key can sign as that human**

- Covers: Section 24.3

Given a private key of `human:ada` without a passphrase that an AI agent can read, a signers file that lists the matching key for `human:ada`, and a configuration that sets the minimum level A2  
When the AI agent signs an approval of the target `spec` as `human:ada`  
Then the approval is valid and is recorded at A2, and this specification offers no detection of it, because an agent that is able to use a human's credentials can act as that human

