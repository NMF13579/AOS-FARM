# Review Package Output Policy

## Purpose

This policy defines when review package generation is read-only and when it mutates files.

## Modes

`stdout` mode is read-only review mode. Running `aos_review_package.py` without `--output` prints the package and does not write a review package file.

`--output` is file mutation. It writes a markdown review package to the requested path.

## Required Authorization for File Output

Using `--output` requires explicit file creation scope from the human owner. The exact output path must be authorized before the command is run.

Reports, Evidence, approvals, checkpoints, protected/canonical files, and lifecycle artifacts must not be written to `/.aos-tmp/`.

Temporary command output in `/.aos-tmp/` is local-only and disposable. It is not Source of Truth, not Evidence storage, not approval storage, and not checkpoint storage.

## Safety Semantics

Review package generation is not approval.

Review package generation is not Evidence.

Review package generation is not lifecycle mutation.

Review package generation is not commit authorization.

Review package generation is not push authorization.

Review package generation is not release authorization.

PASS is not approval. Evidence is not approval. CI PASS is not approval. UNKNOWN is not OK. NOT_RUN is not PASS.

## CLI Warning

The CLI help for `--output` must warn:

`WARNING: --output writes a file. Do not use --output during read-only audit unless file creation is explicitly authorized.`
