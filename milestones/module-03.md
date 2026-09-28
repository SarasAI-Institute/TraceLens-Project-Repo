# Module 3 - Documentation & Spec Sprint

C2 - Specification-Driven Development & Automated Quality Engineering. **C2.1-C2.3 | C2.1/C2.2 provisional until Module 4.**

Document the repaired backend and specify both features before implementation; demonstrate useful project-specific AI instructions.

This is the optional TraceLens capstone track. Follow PromptLab's demonstrated methods independently; no TraceLens walkthrough is required. Continue your own repository rather than restarting from another starter.

## Work and evidence

1. Write specs/evaluations.md and specs/alert-rules.md: goals, stories, acceptance criteria, data, endpoint shapes and errors/edge cases.

2. Create docs/API_REFERENCE.md for implemented endpoints; document every function/class in models, API, storage and utilities.

3. Create AGENTS.md or CLAUDE.md with TraceLens-specific standards and docs/agent-effect-note.md showing genuine before/after output.

4. Keep setup, examples and seed instructions accurate. Commit both specs before feature code; build the features in Modules 4 and 5.

## Task detail

Expand each specification brief into a complete implementable contract. Evaluation Scores must support add/list-by-trace/project summary. Alert Rules must support create/list/delete per project and on-demand evaluation for cost, error rate and latency. Choose score range, threshold operators, units, error semantics, empty behavior and deletion relationships explicitly. Both features are mandatory; their order is your choice.

Your API reference covers every implemented route, including PATCH, with methods, query defaults/limits, requests, success responses and error formats. Identify the absence of authentication and the in-memory reset behavior. Keep unimplemented routes in specs, not in a misleading current API inventory.

Agent instructions must name actual project patterns and testing/error conventions. Capture a real before/after effect of adding them. The provided spec prompts and course instructions do not constitute your own agent file or completed evidence. C2.1/C2.2 are reviewed again after Module 4 implementation and refactoring.

## Milestone review

Use the [Module 3 rubric](../rubrics/TraceLens_Module_3_Project_Rubric.pdf) and [full criterion text](../rubrics/CRITERIA.md). Update [EVIDENCE.md](../EVIDENCE.md), commit your real results and mark a milestone as described in [STUDENT_WORKFLOW.md](../STUDENT_WORKFLOW.md). No weekly capstone upload is required; all evidence feeds the final review. Tags are bookmarks, not passing grades.

Both tracks use the same Met/Not Yet standard, 80% coverage threshold and defense rules. Optional extensions carry no bonus credit. [ASSESSMENT.md](../ASSESSMENT.md) explains policy and MUST PASS returns.
