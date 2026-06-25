# Problem Intake Methodology

The Problem Intake phase is the foundational stage of defining work in AOS. It ensures that the core problem is deeply understood before any technical architecture is proposed.

## 1. Interview Mechanics
- **One Question at a Time**: To avoid overwhelming the user, the agent must ask only one primary question per conversational turn.
- **Adaptive Follow-up**: If a user's answer is brief or vague, the agent must probe deeper.
- **Skip Handling**: Users can skip questions, but skipped blocking items must be logged as `UNKNOWN` and flagged as risks.
- **UNKNOWN Capture**: The agent must explicitly record missing or ambiguous data as `UNKNOWN`. `UNKNOWN ≠ OK`.

## 2. Modes of Intake
- **EXPRESS Mode**: Designed for lean scoping of simple, low-risk tasks or MVPs. It collects minimal context to proceed quickly.
- **FULL Mode**: Designed for complex, sensitive, or high-risk tasks. It dives deeply into edge cases, security constraints, and broader workflows.
- **Escalation**: The agent must automatically recommend escalating from EXPRESS to FULL mode if it detects high-risk signals (e.g., medical data, financial impact, severe security implications).

## 3. Discovery Frameworks
The agent leverages established frameworks to extract deep context:
- **Five Whys**: Iterative questioning to discover the root cause of a stated problem rather than treating its symptoms.
- **Jobs to be Done (JTBD)**: Understanding what underlying "job" the user is "hiring" the software to perform.
- **Entity Process Traversal**: Mapping out how core data entities flow through the system and who interacts with them.
- **Scenario Walkthrough**: Simulating specific edge cases or failure modes with the user to discover grey zones.

## 4. Output
The culmination of this methodology is the `Problem Intake Summary` template, which strictly separates the business context from the eventual implementation.
