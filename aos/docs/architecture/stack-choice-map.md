# Stack Choice Map

Stack Choice Map is not approval.
Stack Choice Map does not select a default stack.
Stack Choice Map does not authorize implementation.
Stack Choice Map does not authorize installer changes.
Stack Choice Map does not authorize execution, commit, push, or release.
Human review is required before any stack preset becomes ACTIVE or default.
This document is referenced during Architecture Fixed Interview when stack questions arise.

Note: Silent stack selection is tracked in aos/docs/architecture/architecture-anti-pattern-catalog.md

Stack recommendation ≠ approval.
Stack Choice Map ≠ default stack selection.
Stack preset PASS ≠ implementation authorization.
Human approval cannot be simulated.

| Stack element | Plain-language meaning | Typical options | Needed immediately? | Can be deferred? | Human review needed? | Risk notes |
|---|---|---|---|---|---|---|
| Frontend | What the user sees and interacts with. | React, Vue, HTML/CSS | Varies | Yes, if API first | Yes | High visibility, dictates UI structure |
| Backend | The core logic and data processing layer. | Node.js, Python, Go | Yes | No | Yes | Contains core logic and secrets |
| Database | Where permanent structured data is kept. | PostgreSQL, MySQL, SQLite | Yes | No | Yes | Data loss risk, high schema lock-in |
| Auth | How users log in and get permissions. | OAuth, JWT, Session | Varies | Yes | Yes | High security risk if misconfigured |
| File storage | Where uploads and assets are saved. | S3, Local, GCS | Varies | Yes | Yes | Privacy and cost risks |
| Deployment | Where the application runs live. | AWS, Vercel, Heroku | No | Yes | Yes | Infrastructure lock-in, billing risks |
| Background jobs | Tasks that run behind the scenes. | Celery, Redis, Cron | No | Yes | Yes | Can fail silently if unmonitored |
| Payments | How money is collected. | Stripe, PayPal | No | Yes | Yes | Compliance and financial risk |
| Admin panel | The dashboard for staff to manage data. | Custom, Retool, Django Admin | No | Yes | Yes | Exposes sensitive operational data |
| Search/RAG | How complex data is searched or queried. | Elasticsearch, Pinecone | No | Yes | Yes | Costly and complex to maintain |
| Runtime | The environment that executes the code. | Node, Python 3.9+, Docker | Yes | No | Yes | Upgrades can break compatibility |
