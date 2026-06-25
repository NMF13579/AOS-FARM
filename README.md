<div align="center">
  <h1>AOS-FARM</h1>
  <p><b>Build with AI agents faster — without losing human control.</b></p>

  [![Install / First Run](https://img.shields.io/badge/Install_/_First_Run-000000?style=for-the-badge&logo=github&logoColor=white)](docs/user-guide/installation-clone-first-run-guide.md)
  [![Quickstart](https://img.shields.io/badge/Quickstart-000000?style=for-the-badge&logo=rocket&logoColor=white)](docs/user-guide/quickstart.md)
  [![Templates](https://img.shields.io/badge/Templates-000000?style=for-the-badge&logo=files&logoColor=white)](templates/)
  [![Project Map](https://img.shields.io/badge/Project_Map-000000?style=for-the-badge&logo=map&logoColor=white)](docs/user-guide/project-map.md)
  [![Safety](https://img.shields.io/badge/Safety-000000?style=for-the-badge&logo=shield&logoColor=white)](docs/governance/minimal-safety-floor.md)
  [![Русский](https://img.shields.io/badge/Русский-000000?style=for-the-badge)](README.ru.md)
</div>

---

AOS-FARM is a Markdown-first governance framework for safe AI-assisted / vibe-coding projects. It helps users turn ideas into controlled tasks, evidence, checkpoints, and human-reviewed execution flows.

## ⚠️ What problem does it solve?
AI coding agents are fast but can create risk by:
- silently expanding scope;
- confusing PASS with approval;
- treating reports as decisions;
- pushing risky lifecycle changes before the human understands them;
- mixing evidence, validation, and approval.

AOS-FARM adds **controlled workflow boundaries** so the human always retains absolute authority.

## 🎯 Who is it for?
- vibe-coders;
- non-programmers building with AI agents;
- solo founders;
- product owners;
- users of GPT / Codex / Cursor / Antigravity / Claude Code style agents;
- teams that want lightweight human-controlled AI workflows.

**Not for:**
- fully autonomous production deployment;
- replacing human review;
- blind auto-merge / auto-release workflows.

## ⚙️ How it works
1. **Idea**
2. **Task Brief**
3. **Scope + Forbidden Changes**
4. **Dry Run / Evidence**
5. **Human Checkpoint**
6. **Controlled Execution**
7. **Verification**
8. **Commit / Push** (only after explicit human authorization)

## ⏱️ First 10 minutes
1. Clone the repository.
2. Open it in an IDE.
3. Read [Quickstart](docs/user-guide/quickstart.md).
4. Open [Project Map](docs/user-guide/project-map.md).
5. Open [Installation / First Run Guide](docs/user-guide/installation-clone-first-run-guide.md).
6. Pick a [template](templates/).
7. Ask GPT / IDE agent to act as AOS-FARM Tutor.
8. Run only a dry-run first.
9. Stop before commit / push unless human authorization exists.

## 🎓 Tutor Mode
Paste this prompt to your AI assistant to start safely:
```text
Act as AOS-FARM Tutor.
Guide me through my first dry-run.
Do not execute, stage, commit, push, merge, release, or approve anything.
Explain each approval boundary before risky steps.
```

## 🛡️ Safety boundaries
AOS-FARM enforces a strict Minimal Safety Floor from day one:
- **PASS ≠ approval**
- **Evidence ≠ approval**
- **CI PASS ≠ approval**
- **UNKNOWN ≠ OK**
- **NOT_RUN ≠ PASS**
- **Human approval cannot be simulated**
- **Destructive operations are forbidden by default**

## 🚫 What AOS-FARM does not do
AOS-FARM does **not automatically**:
- approve tasks;
- run agents;
- stage changes;
- commit;
- push;
- merge;
- create releases;
- claim production readiness;
- replace human judgment.

## 🗺️ Documentation map

| Document | Purpose |
|----------|---------|
| [Installation / First Run](docs/user-guide/installation-clone-first-run-guide.md) | How to safely get started |
| [Quickstart](docs/user-guide/quickstart.md) | High-level system overview |
| [Project Map](docs/user-guide/project-map.md) | Where things are located |
| [Glossary](docs/user-guide/glossary.md) | Important terminology |
| [Walkthrough](docs/user-guide/quickstart-example-walkthrough.md) | Example of a controlled task |
| [Templates](templates/) | Task briefs and checkpoints |
| [Approval Boundary](docs/governance/pass-evidence-approval-boundary.md) | Why PASS is not approval |
| [Minimal Safety Floor](docs/governance/minimal-safety-floor.md) | The absolute safety rules |

## 📊 Project status
- **Public onboarding**: preparing
- **Template trial**: preparing
- **Production readiness**: not claimed
- **Release approval**: not granted
- **Runner**: deferred
- **Human approval required for lifecycle actions**
