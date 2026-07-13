# Integration Boundary Contract

The AOS integration contract records what is proposed for integration and the exact `dev` state it is proposed against. It verifies technical freshness and consistency. It does not authorize integration, merge, release, or lifecycle change.

## Boundary

Active contracts must be tracked regular files under `aos/integration/contracts/` and use `.json` or `.yaml`. A `.yaml` file is accepted only when the payload is strict JSON. Temporary files, `.aos-tmp/`, test fixtures, repository root files, and templates are not active contracts.

`aos/templates/execution-artifacts/aos-integration-contract-template.yaml` is a template only. It is not Source of Truth, not approval, and not integration authorization.

## Structure

An active contract binds:

- repository identity and remote URL;
- source build branch, source commit, parent, and tree;
- target branch `dev` and expected target head;
- candidate file entries with path, state, mode, and SHA-256;
- integration method `GITHUB_PR_MERGE_COMMIT`;
- exact commit preservation rule `REQUIRED_AS_MERGE_PARENT_OR_ANCESTOR`;
- shadow required check policy version 1;
- invalidation triggers;
- authorization boundary fields that must remain false except `human_decision_required`.

Candidate paths must be repository-relative, unique, lexicographically sorted, and must not use traversal, backslashes, `.git/`, `.aos-tmp/`, symlink modes, or duplicate previous paths.

## Bindings

`candidate.manifest_binding` is SHA-256 over:

```json
{
  "binding_version": 1,
  "repository_identity": "<repository.identity>",
  "source_commit_oid": "<source.commit_oid>",
  "source_tree_oid": "<source.tree_oid>",
  "files": "<candidate.files>"
}
```

`contract_binding` protects every authoritative contract field except the two derived top-level fields:

```text
contract_id
contract_binding
```

The verifier deep-copies the contract, removes only those two fields, serializes with JSON `sort_keys=true`, `separators=(",", ":")`, `ensure_ascii=false`, and `allow_nan=false`, then computes SHA-256.

`contract_binding` is the full 256-bit content binding. `contract_id` is a shortened reference identifier derived as `integration-<first-16-of-contract_binding>`. Security-sensitive comparisons use `contract_binding`; display and lookup may use `contract_id`.

Both derived fields are excluded from the binding payload to avoid a self-referential hash. Fixed-point iteration is not used. The verifier separately checks that the full binding matches and that the short ID derives from that binding.

## Validation

The verifier checks strict JSON parsing, duplicate keys, schema shape, binding derivation, path safety, tracked active contract location, remote URL, source parent and tree, observed source and target OIDs, target ancestry, candidate diff state, file modes, and blob SHA-256.

Protected or canonical paths require human review. The contract can be technically valid while returning `HUMAN_REVIEW_REQUIRED`; this still grants no approval.

Required check policy version 1 defines these exact shadow checks:

- `aos-integration / candidate-binding`
- `aos-integration / contract`
- `aos-integration / focused-tests`
- `aos-integration / full-pytest`
- `aos-integration / protected-paths`
- `aos-integration / semantic-guard`

The verifier defines policy only. It does not claim the checks exist on GitHub and does not enable platform enforcement.

## Aggregate Usage

The aggregate validator can forward explicit context:

```bash
python3 -B aos/scripts/aos_validate.py all \
  --integration-contract aos/integration/contracts/example.yaml \
  --integration-source-oid <40-hex> \
  --integration-target-oid <40-hex> \
  --json
```

All three integration options are required together. Without explicit context the integration checker is not run, and the template is not validated automatically.

## Human Boundary

`PASS` means only `technical_contract_valid: true`. It does not approve integration. It does not approve merge. It does not approve release. It does not authenticate human approval.

For non-programmers: the contract freezes the proposed change and the current `dev` baseline so reviewers can see whether the proposal changed. It checks the proposal. It does not say yes to merging it.

## Limitations

This stage does not implement GitHub branch protection, required status checks, pull request creation, check-run publishing, external attestation, signed commits, or cross-machine single-use enforcement. Administrator bypass prevention and trusted executor isolation are deferred.
