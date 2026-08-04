# Apollo preference and routing

Resolve this preference before collecting the seven-part brief or starting research.

## Read the saved choice

Run:

```bash
python3 <skill-dir>/scripts/apollo_preference.py get --json
```

Exit code `0` means a valid saved choice exists. Use it without asking again. Exit code `2` means no choice exists. If the current user message already states one of the three modes clearly, save that mode and continue without asking. Otherwise ask once using the three options below. The preference is local to the current Codex user profile and device. A new device, a different `CODEX_HOME`, or deleted local state requires a new choice.

If a tappable-choice UI is available, use it. Otherwise show the same three choices as a numbered list. Explain the effect of each choice before asking the user to select one.

1. `public_only` — **未注册、未安装、未连接或不可用（推荐默认）**
   - No Apollo registration, installation, or connection is required.
   - Complete the full no-registration public-web workflow without interruption.
   - Never call an Apollo tool.
   - When no public personal business email is supported, preserve the row and mark it `需尝试Apollo积分深度背调`.
2. `connected_free` — **已连接，但不使用积分**
   - The user's own Apollo account or connector is already available.
   - Use only Apollo People Search, and only when current official documentation still marks that exact action as zero-credit. If the exact People Search action is unavailable or its credit status cannot be verified, stay on public web research.
   - Use free results to supplement a person's name, title, current company, and public professional profile when returned.
   - Do not claim that People Search supplies email or phone; those fields require enrichment when they are not already public elsewhere.
   - Block People Enrichment, Bulk People Enrichment, Company Search, Company Enrichment, phone retrieval, waterfall enrichment, and any action whose current credit status is unknown or credit-consuming.
3. `credit_per_call` — **已连接，允许逐次审批积分**
   - Remember only that the user is willing to consider a credit-consuming enrichment pass.
   - Finish public-web research and zero-credit search first.
   - Before every credit-consuming call, show the planned Apollo action, record count, requested fields, known or maximum estimated credit impact, and whether phone or waterfall enrichment is included.
   - When available, check Apollo credit-usage statistics before and after the approved call. If the cost cannot be bounded from current official information, say so explicitly rather than presenting a guessed number.
   - Wait for explicit approval for that exact call. Never interpret this saved choice as blanket spending permission.
   - Default to email-only enrichment with no phone and no waterfall unless the user explicitly requests and approves them.
   - If the user declines a call, continue and export the best public/free result.

After the user chooses, save it and immediately continue the original task:

```bash
python3 <skill-dir>/scripts/apollo_preference.py set <public_only|connected_free|credit_per_call> --json
```

Do not store Apollo credentials, tokens, credit balances, or account identifiers in this file.

## Change or forget the choice

Treat explicit instructions such as these as preference updates:

- `更改 Apollo 状态为未注册、未安装或仅公开搜索` → `set public_only`
- `更改 Apollo 状态为已连接但不使用积分` → `set connected_free`
- `更改 Apollo 状态为已连接并允许逐次审批积分` → `set credit_per_call`
- `忘记 Apollo 状态` or `重新选择 Apollo 状态` → `clear`

Persist an explicit change immediately, switch to the matching workflow, and continue the current task. After `clear`, ask the three-choice question the next time the skill is invoked.

A one-off instruction can narrow the saved mode for the current action, such as `这次不要用 Apollo`. Do not rewrite the saved preference unless the user says to change or remember it. A one-off instruction cannot broaden credit authority: every paid call still requires exact-call approval.

## Availability mismatch

If the saved mode says Apollo is connected but no Apollo tool is available or authentication fails, fall back to `public_only` for the current task, state the mismatch in the handoff, and continue. Do not install a plugin, start registration, or silently change the saved preference unless the user asks.
