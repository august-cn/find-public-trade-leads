# Apollo setup and runtime routing

Public-web research always starts first and never waits for Apollo setup.

## Detect the plugin before prompting

At the start of each invocation, inspect the available tools for Apollo plugin or MCP capabilities.

- If Apollo tools are present, do not recommend registering or installing the plugin. This rule applies even if an old onboarding state file is missing.
- If Apollo tools are present but authentication fails, continue with public research and record the connection issue. Do not repeat the installation recommendation.
- If Apollo tools are absent, check whether the one-time setup recommendation has already been shown:

```bash
python3 <skill-dir>/scripts/apollo_onboarding.py \
  --project-root <current-project-root> get --json
```

Exit code `0` means the recommendation was already shown. Exit code `2` means it has not been shown.

## First-use recommendation

When Apollo tools are absent and the recommendation has not been shown, send one concise, non-blocking commentary update while public research is already running. Do not ask the user to choose a mode and do not wait for a reply.

Use this meaning in the user's language:

> 公开网页调查已开始。若希望补充更多具名联系人，建议注册 Apollo 并安装、连接 Apollo 插件。连接 Apollo MCP 后，可用零积分 People Search 补充姓名、职位和职业主页；经逐次积分授权，还可进一步调查完整联系人信息，包括个人或商务邮箱和电话。

After showing the recommendation, record it:

```bash
python3 <skill-dir>/scripts/apollo_onboarding.py \
  --project-root <current-project-root> mark-shown --json
```

This project-local, git-ignored state stores only that the recommendation was shown. It must not store credentials, account identifiers, tokens, balances, or contact data. To test the first-use experience again:

```bash
python3 <skill-dir>/scripts/apollo_onboarding.py \
  --project-root <current-project-root> clear --json
```

If the user explicitly declines Apollo registration, installation, connection, or use, do not show the recommendation again during that task. Continue publicly without interruption.

## Runtime routes after public research

Do not persist or ask for a three-mode preference. Resolve the route from current tool availability, current official credit documentation, the user's instructions, and exact-call approvals.

### Apollo unavailable

- Complete the public-web workbook normally.
- Preserve row-level `需尝试Apollo积分深度背调` prompts for unresolved personal contact data.
- Record `apollo_mode: public_only` and `apollo_usage: not_available` unless the user explicitly disabled Apollo, in which case use `apollo_usage: public_only`.

### Apollo connected: zero-credit search

- Use People Search only when current official Apollo documentation still marks that exact endpoint zero-credit.
- Use returned names, titles, current companies, and public professional-profile URLs only after company-role verification.
- Do not claim People Search returns email or phone.
- Do not call company search, enrichment, email reveal, phone retrieval, waterfall enrichment, record-writing, or any unknown-cost action without exact-call approval.
- Record `apollo_mode: connected_free` and `apollo_usage: free_search_used` when free search is used.

### Apollo connected: credit-consuming completion

- Finish public and verified zero-credit passes first.
- Before every credit-consuming call, state the exact action, exact record count, requested fields, known or maximum credit effect, and whether personal-email reveal, phone retrieval, or waterfall enrichment is included.
- Wait for explicit approval for that exact call. Installation or connection is not spending permission.
- Check credit usage before and after an approved call when the connector supports it.
- Default to business-email enrichment only. Include personal email, phone, or waterfall only when the user requests or approves those disclosed fields.
- Verify every returned person against the exact company and commercially relevant role. Do not silently merge conflicts.
- Record `apollo_mode: credit_per_call` only when a credit-consuming call was approved for the current run. Record `apollo_usage: paid_approved_used`, `paid_declined`, or `paid_available_not_needed` according to what happened.

If the user declines a credit call or Apollo returns no useful result, continue with the best public/free workbook and preserve unresolved status honestly.
