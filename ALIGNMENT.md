# TraceLens v1.1 course alignment

Revision date: 2026-09-28. Sources: the supplied TraceLens Course & Project Guide, five module project documents and TraceLens Grading Rubric v1.0; the current six-module course and published PromptLab starter/assessment package. Original user documents remain unchanged outside this repository.

## Intent

TraceLens is an optional independently built capstone **instead of PromptLab**. PromptLab remains the walkthrough project. This revision preserves the same 22 criterion IDs, three competencies and five MUST PASS gates while adapting project-specific evidence. It is a student starter, not an instructor solution.

## Changes from the old TraceLens handouts

- Old project Modules 1-5 become current course Modules 2-6; Module 1 TokenScope remains common and ungraded.
- Replace five weekly submissions with one continuing repository and final delivery. Keep five evidence groups and their separate attempt accounts, matching PromptLab.
- Local setup replaces old Continue/provider configuration. Codex/Claude instruction files replace legacy tool examples. No provider key is required by the app.
- Clarify TL-3: pages have **at most** limit items; short/empty pages are valid. Total counts all filtered matches.
- Clarify that both Evaluation Scores and Alert Rules are required and usable in the final UI. The old brief required both backend features but its UI criterion ambiguously said “evaluations or alert rules.”
- Align C2.5 to implemented endpoints (the second feature is implemented in Module 5); meaningful documented failure paths are required where defined. Coverage remains 80%.
- Make the PromptLab CI failure/recovery, separate required merge-check proof, Compose hot reload and spec-before-frontend expectations explicit.
- Apply PromptLab's timing calibration caveat to C3.5. Record honest timing; do not enforce the old unvalidated four-hour placeholder before calibration and a versioned published budget. Pending calibration is not automatic Met.
- Align defense to an instructor-selected backend function and React component, 48-hour issue window, 12-20 continuous minutes, up to three written clarifications in two business days and fresh files on re-attempts.

These clarifications are explicitly versioned in the canonical criterion text and PDFs; they are not presented as a verbatim reproduction of v1.0. The Syllabus remains authoritative for course policy.

## Starter quality corrections

Use an import string for Uvicorn reload; explicit local CORS origins; UTC-aware timestamps; bounded list queries and the existing tag-validation rule; separate runtime/development dependency files; synthetic seeding that checks failed writes. Prices are fixed teaching fixtures rather than live pricing claims.

The TL-5 diagnostic now rejects dangling references while accepting cascade, detach or reject policies. Add missing PATCH diagnostics and use deterministic ordering fixtures. Keep all five inherited defects and the missing PATCH implementation for students to repair. Feature implementations, complete docs, agent instructions, CI, containers and React remain student work.

Future rubric edits should update CRITERIA.md and the module PDFs together. Do not mix this version with old module-numbered handouts.
