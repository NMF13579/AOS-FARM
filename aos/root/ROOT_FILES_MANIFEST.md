# AOS Root Files Manifest

| file | source path | target path | required/optional | purpose | overwrite policy | expected status | Source of Truth role |
|---|---|---|---|---|---|---|---|
| AGENTS.md | /aos/root/AGENTS.md | /AGENTS.md | required | Primary agent entrypoint | Do not overwrite | Deployed | Runtime Entrypoint |
| llms.txt | /aos/root/llms.txt | /llms.txt | required | Secondary agent entrypoint | Do not overwrite | Deployed | Runtime Entrypoint |
| .gitignore | /aos/root/.gitignore.template | /.gitignore | optional | Ignore temporary AOS files | Do not overwrite, merge snippet | Deployed/Merged | Ignore Rules |
| README block | /aos/root/README_AOS_SECTION.md | /README.md | optional | Warn human/agent readers | Do not overwrite, merge manually | Merged | Advisory |
| advisory workflow | /aos/root/.github/workflows/aos-advisory.yml | /.github/workflows/aos-advisory.yml | optional | CI advisory checks | Do not overwrite | Deployed | CI config |
