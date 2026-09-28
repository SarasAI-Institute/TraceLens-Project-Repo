# Working in one repository

## Start once

Create your own working repository once: fork this repository if course access permits, or download the default-branch ZIP and initialize your own Git repository with a baseline commit. If the instructor enables Use this template, that is also suitable. Clone your own repository and keep using that folder; keep the supplied baseline. Do not push coursework into the instructor's starter repository.

## During a module

Read the module guide and rubric before coding. Commit small, meaningful steps and update EVIDENCE.md with actual results. Push your work to your own repository regularly so the remote copy is current. No weekly capstone upload is required.

In test-first work, commit and record the real failing test before the implementation that makes it pass. Preserve both commits. Do not squash away or reconstruct assessment evidence.

Work on `main` initially. As branching and CI are introduced, create short-lived feature branches from your latest `main` and merge them back, preserving the evidence commits. CI's merge gate is configured in your own GitHub repository during Module 4, not merely by adding a workflow file.

You do not need a permanent branch for every module. Do not restart each module from the teacher's original starter or a completed checkpoint.

## Mark a completed milestone

Update and commit your evidence, then tag the completed project state. For example, after Module 2:

```sh
git status
git tag -a module-2-complete -m "Module 2 milestone"
git push origin main
git push origin module-2-complete
git rev-parse 'module-2-complete^{commit}'
```

Run this from `main` after committing the work and merging any feature branch. The last command prints the exact commit hash. Record it in EVIDENCE.md in your next log update; that update does not change the already-tagged snapshot.

Use `module-3-complete`, `module-4-complete` and `module-5-complete` for later milestones. Tags are bookmarks, not submissions or proof of passing. If you revise a marked milestone, use a new name such as `module-2-revision-1` and record the new hash rather than moving the original tag.

## Evidence

Keep the exact prompts/context, relevant AI output, decisions, checks and commit references as you work. Put longer supporting records in an `evidence/` folder if useful and link them from EVIDENCE.md. Remove credentials and unrelated personal information before committing logs. Only authentic incidents and outcomes count.

## Starter corrections

Continue developing your own application. Your repository created from a template does not automatically receive teacher updates. If the instructor publishes an erratum, apply the specified correction to your existing work, review it and commit it. Do not replace your project with a later completed application.

## Final handoff

Submit through the course's designated channel: repository link and reviewer access, exact final commit hash, working run/deployment instructions, EVIDENCE.md and supporting records, and your final recording link. The instructor selects code from that final commit for the defense; do not silently change the selected version afterwards. Record any permitted revision as a new commit.

See [Module 6](milestones/module-06.md) and [assessment policy](ASSESSMENT.md) for recording and review requirements.
