# Harness

WHAT A HARNESS IS
Everything outside the model weights, in five subsystems. Missing one makes it incomplete.
- Instructions: one short root file plus docs it points to.
- Tools: enough access to work, least privilege.
- Environment: reproducible and self-describing (pinned runtime and dependency versions, one-command setup, one-command check).
- State: progress file, feature list, decision log, git history.
- Feedback: runnable verification commands. Highest return of the five.
When something fails, do not blame the model first. Attribute the failure to a layer (task specification, context, environment, verification, state), fix that layer, and log it (task, pass/fail, layer) so it never repeats.

PRINCIPLES
1. The repository is the system of record. Decisions, plans, status and conventions live in files next to the code.
2. The root instruction file (AGENTS.md) is a map of about 100 lines: purpose, startup steps, verification commands, a few hard invariants, definition of done, end-of-session rules, links to docs/ with "read when...". Critical rules go at the top or bottom, never the middle. Each rule records why it exists and when it can be deleted. Delete stale or contradictory rules.
3. One feature at a time. No second feature before the first is verified. No extras, no drive-by refactors.
4. Done means runnable evidence (command and result), never belief. You may not set a feature to passing yourself; only a recorded successful verification run does. Never edit or reword the feature list to hide unfinished work.
5. Enforce rules mechanically (tests, linters, scripts, git hooks) instead of prose reminders.
6. Every session starts from a verified baseline and ends in a restartable state.
7. Add the smallest artifact that fixes an observed failure. Do not pre-build large systems.
8. Important work gets a separate check pass with fresh context. Authors are lenient judges of their own work.
9. Commits are records. One commit per verified logical unit, never mixed unrelated changes. The message says what changed, why, and what evidence verified it. Never commit failing or unverified work; discard failed attempts.
10. Write decisions down when you make them. Every choice of language, framework, library, tool, directory layout or approach goes in docs/DECISIONS.md with reason, rejected alternatives, constraints and date. A commit that introduces such a choice references the entry. Never switch a tool silently.
11. Error messages from check scripts and code say ERROR (what failed), WHY, FIX (concrete command or path).
12. Observability belongs in the harness: log lifecycle (start, ready, running), key-path execution and errors with full context. Judge from what you ran, not from reading code.

SESSION ROUTINE (store this in docs/HARNESS.md; AGENTS.md links to it)
Start: confirm repo root. Read AGENTS.md, docs/PROGRESS.md, docs/DECISIONS.md, docs/feature_list.json and the recent git log. Run the init script and a baseline smoke path. If the baseline is broken, fix it first.
Select: exactly one unfinished, unblocked feature by priority and dependencies. Mark it in_progress. For non-trivial features, write a short sprint contract first: scope, verification standards, exclusions.
Execute: implement only that feature. Verify in order, never skipping a level: L1 static (lint, types); L2 runtime (unit and integration tests, app starts, critical path works); L3 end-to-end run of the real user-visible path whenever components interact. Fix and rerun until it passes. Correctness first, then performance, then style; no refactoring before core behavior is verified. Record evidence.
Commit: one commit for the verified unit, with the what and why message and any decision recorded.
Wrap up: status becomes passing only via scripts/verify_feature.py. Update PROGRESS.md (verified, broken or unverified, next best action). Clean state means all five: build passes, all tests pass (including pre-existing), progress and feature state recorded in files, no stale artifacts (debug code, temp files, commented-out code, stray TODOs), startup path still works. If you cannot reach clean state, roll back to the last consistent commit. Never claim completion with failing or unrun checks.
Context: if a long task nears about 60% of the context window, persist state to PROGRESS.md and hand off instead of rushing. Write conclusions to files, read files on demand, delegate side tasks to an isolated context or branch.
Failure handling: a recurring failure or review comment becomes an automated check or a short rule in docs/ with its reason and expiry, never a pile in AGENTS.md. A blocked feature is marked blocked with the reason; do not fake progress.
Review: at milestones, a separate pass with fresh context scores 0-2 on correctness, verification, scope discipline, reliability, maintainability, handoff readiness, citing evidence; outcome accept, revise or block. Keep a quality document grading each module; fix the lowest first. Run a periodic cleanup sweep; cleanup scripts must be safe to repeat.
Scale only when needed: stay with single-agent sessions until manual driving is the bottleneck. Then a goal loop (goal, machine-checkable stop condition, independent judge, markdown memory file), a timer loop, or maker-checker. Watch verification debt, comprehension rot, cognitive surrender, token blowout. Use multi-agent graphs only when independent units, rollback paths and checkable results justify the cost. Periodically disable one harness component and keep only what measurably helps.

PROJECT-SPECIFIC USER-RUN EVIDENCE
Paid and device-dependent verification commands must never execute automatically. Once the
user actually supplies their run output, record a sanitized JSON file with feature_id, command
(the exact command without 'user runs' / 'and pastes output'), source='user', exit_code=0,
stdout (nonempty actual output), reviewed_result='accepted', and acceptance_notes explaining
how all feature criteria were checked. Never fabricate these fields or treat exit 0 alone as
acceptance: T3 must satisfy the go/no-go decision and T8 requires native-speaker review.
Run `.venv/bin/python scripts/verify_feature.py T2 --user-evidence /path/to/record.json`.
The script validates the record, requires passing dependencies and make check, and records
supplied evidence without executing the paid command. The format cannot authenticate origin;
reviewer responsibility is to use only output actually supplied by the user and remove secrets.
No such output exists at initialization; all user-run features remain blocked.
