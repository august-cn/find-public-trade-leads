# Project-local continuation and deduplication

Use this workflow on every run, not only when the user explicitly asks for more leads.

## Load the project history

Resolve the current Codex project root, then run:

```bash
python3 <skill-dir>/scripts/lead_history.py \
  --project-root <current-project-root> context
```

The command returns the most recent complete brief, prior batch ID, suggested next batch ID, and history counts. The local history contains only company identity fields, status, batch metadata, and the brief needed for continuation. It does not store contact details or Apollo credentials. Use the `check` command below for each resolved candidate instead of loading a growing history into the conversation.

The history file lives at `<current-project-root>/.find-public-trade-leads/history.json`. The repository's `.gitignore` excludes this directory. Never add, commit, push, or otherwise publish the local history file.

## Recognize continuation requests

Treat phrases such as `继续找`, `再找`, `更多客户`, `下一批`, `沿用上次条件`, or `继续开发这个市场` as continuation mode.

When history exists:

- reuse `last_brief` without asking for the seven fields again;
- apply any changes stated in the current message on top of the saved brief;
- use `suggested_batch_id` as `brief.batch_id` and `previous_batch_id` as `brief.previous_batch_id`;
- set `brief.research_mode` to `continuation`;
- set `brief.history_company_count` before search;
- default the requested new-qualified count to 20 unless the user supplies another number.

When no history exists, explain briefly that this project has no completed batch yet and collect the normal seven-part brief. Do not claim that chat history alone is a durable deduplication database.

The user's shortest supported instruction is:

```text
使用 $find-public-trade-leads，沿用上次条件，再找20家新的客户。
```

## Exclude historical companies

Treat every company from prior qualified, near-match, and excluded rows as already seen. After resolving a candidate's company name, legal name, website, and market—but before the expensive named-contact pass—check it against project history. The script compares normalized domain plus market and normalized company/legal name plus market. Also perform the existing manual review of parent companies, subsidiaries, branches, group companies, brand entities, and marketplace sellers.

For an uncertain candidate, run:

```bash
python3 <skill-dir>/scripts/lead_history.py \
  --project-root <current-project-root> check \
  --company <company> --legal-name <legal-name> \
  --website <website> --market <market>
```

Exit code `3` with `duplicate: true` means the candidate is historical and must be skipped. Exit code `0` with `duplicate: false` means no deterministic history match was found; still perform the manual group-entity review.

Do not put a historical match into the new qualified or near-match sheets. Count it in `brief.duplicates_skipped_count`. A historical company with newly discovered contact information remains skipped from the new batch; mention the update in research notes only when useful.

## Record the completed batch automatically

Pass `--project-root <current-project-root>` to `scripts/run_build.py`. After the workbook builder succeeds, it records qualified, near-match, and excluded company identities plus the current brief automatically.

Do not record an incomplete, failed, or unverified research draft. The recorder rejects historical duplicates or duplicate companies inside the same batch with exit code `4`; remove those rows, replace them with genuinely new qualified prospects when evidence permits, and rebuild. Rebuilding the exact same completed batch is idempotent. If workbook creation succeeds but history recording fails, repair the history step before claiming the batch is complete.

Clearing history is destructive. Run `lead_history.py ... clear --yes` only when the user explicitly asks to forget or reset the project's searched-company history.

## Scope boundary

This continuation memory works only inside the same local Codex project directory. A new project, another device, a deleted history directory, or a fresh clone has no prior customer history. The GitHub repository distributes the automatic-history code and ignore rule, not any user's customer data.
