# AOS Package Changelog

## Product Package Change Summary

### [Unreleased / Pre-merge]
- Restructured `llms.txt` to safely bootstrap consumer agents.
- Sanitized `problem-intake.md` prompt to remove internal `agentos/` dependencies.
- Updated `problem_intake_runner.py` to route output to `.aos-tmp/`.
- Hardened task quality check schema to enforce boolean constants.
- Rewrote skeleton metadata docs to consumer-facing language.

*Note: This is a pre-merge/pre-release changelog. There is no fake release maturity.*
