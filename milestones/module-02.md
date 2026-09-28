# Module 2 - Brownfield Challenge

C1 - Codebase Comprehension & AI-Assisted Debugging. **C1.1-C1.6 | Completes C1 when all six are Met.**

Understand and repair the inherited TraceLens backend; verify AI-assisted changes against observable behavior.

This is the optional TraceLens capstone track. Follow PromptLab's demonstrated methods independently; no TraceLens walkthrough is required. Continue your own repository rather than restarting from another starter.

## Work and evidence

1. Create docs/SYSTEM_MODEL.md: routes, request/storage flow, project/trace relationship, cost units, dependencies and context strategy.

2. Close TL-1 through TL-6 against CONTRACT.md, retaining passing behavior and adding regression checks. Document your deletion policy and hand calculation.

3. Keep docs/prompt-log.md with at least two substantive iterations and docs/ai-verification-note.md with one real, traceable AI error.

4. Write accurate Google-style docstrings on changed/added functions and verify README setup from a clean copy.

## Task detail

Start with a committed baseline and record the actual diagnostic failures. Understand the code before changing it; do not substitute an AI summary for your system model. Explain why whole-repository or file-level context fits each exploration stage.

Repair all five defects and implement PATCH. Test missing traces, per-million costs including unknown models, page boundaries and combined filters, empty-project stats, your chosen project-deletion policy and partial updates. The existing tests are a starting point, not proof of exhaustive correctness. Do not weaken them. Record actual commands and results.

Use precise Args, Returns and Raises in changed-function docstrings. The model and prompt log must agree with the actual implementation and your real exploration process. Do not invent an AI mistake for the evidence note.

## Milestone review

Use the [Module 2 rubric](../rubrics/TraceLens_Module_2_Project_Rubric.pdf) and [full criterion text](../rubrics/CRITERIA.md). Update [EVIDENCE.md](../EVIDENCE.md), commit your real results and mark a milestone as described in [STUDENT_WORKFLOW.md](../STUDENT_WORKFLOW.md). No weekly capstone upload is required; all evidence feeds the final review. Tags are bookmarks, not passing grades.

Both tracks use the same Met/Not Yet standard, 80% coverage threshold and defense rules. Optional extensions carry no bonus credit. [ASSESSMENT.md](../ASSESSMENT.md) explains policy and MUST PASS returns.
