# Workbook input contract

Pass one UTF-8 JSON object to `scripts/run_build.py`.

## Top-level shape

```json
{
  "brief": {},
  "sender": {},
  "leads": [],
  "near_matches": [],
  "excluded": [],
  "generated_at": "YYYY-MM-DD"
}
```

## `brief`

Required string fields:

- `product`
- `target_market`
- `cooperation_model`
- `supply_capability`
- `customer_size`
- `reference_brands`
- `exclusions`

Optional:

- `target_count` number, default 20
- `product_sources` array of URLs or uploaded file names
- `research_notes` string
- `outreach_language` string
- `apollo_mode` string: `public_only`, `connected_free`, or `credit_per_call`
- `apollo_usage` string: `not_available`, `public_only`, `free_search_used`, `paid_declined`, `paid_approved_used`, or `paid_available_not_needed`
- `research_mode` string: `initial` or `continuation`
- `batch_id` string from the project-history context, such as `batch-0002`
- `previous_batch_id` string, empty for the first batch
- `history_company_count` number loaded before the current search
- `duplicates_skipped_count` number of historical candidates omitted from this batch

Set `brief.apollo_mode` from the current run: `public_only` when Apollo was unavailable or disabled, `connected_free` when only verified zero-credit search was available or used, and `credit_per_call` when a credit-consuming call was approved for this run. Use `brief.apollo_usage` to record what actually happened. Plugin installation or connection alone does not mean credits were used.

Copy the project-local continuation context into the five history fields. These values make the workbook auditable; the actual deduplication state remains in the git-ignored project history rather than inside GitHub.

## Workbook language policy

Keep JSON keys in English because they are machine-readable. Write the workbook-facing values in Simplified Chinese unless the field must remain source-original.

Write these values in Chinese:

- `brief` narrative values and `research_notes`;
- `customer_type`, `size_band`, `size_evidence`, `country`, and `product_evidence`;
- `contact_title`, `contact_status`, `contact_search_note`, `email_type`, and `phone_type`;
- `fit_reason`, `risks`, `confidence`, `evidence_boundary`, and `next_step`;
- `near_match_reason` and excluded `reason`.

Keep these values source-original:

- `company`, `legal_name`, `contact_name`, and `address`;
- `email`, `phone`, `website`, `linkedin`, and every URL;
- registered brand or product names;
- `outreach_subject` and `outreach_body` in the requested target-market language.

When a job title or source phrase needs its original wording for identification, write the Chinese translation first and place the original in parentheses. Do not translate or alter identifiers and contact routes.

## `sender`

Optional strings:

- `name`
- `title`
- `company`
- `email`
- `phone`
- `website`

Use placeholders in drafts when sender contact details are absent.

## `leads`

Each lead supports:

```json
{
  "priority": 1,
  "company": "Company name",
  "legal_name": "Legal name",
  "customer_type": "经销商",
  "size_band": "中型",
  "size_evidence": "事实或明确标注的规模代理指标",
  "address": "Full address",
  "country": "Country",
  "website": "https://example.com",
  "product_evidence": "已核实的产品或品类重合证据",
  "contact_name": "",
  "contact_title": "采购经理，或建议转交的部门",
  "contact_status": "已公开核实 | 仅二手来源 | 待核实 | 需通过Apollo插件优化搜索；当前仅提供部门渠道 | 需通过Apollo插件优化搜索；当前仅提供公司渠道 | 需通过Apollo插件优化搜索；公开网页暂无可用联系人",
  "email": "",
  "email_type": "公开个人邮箱 | 部门邮箱 | 公司通用邮箱 | 联系表单 | 未找到",
  "phone": "",
  "phone_type": "直线电话 | 部门电话 | 公司总机 | 未找到",
  "professional_profile_url": "",
  "professional_network": "",
  "linkedin": "",
  "apollo_deep_research_prompt": "需尝试Apollo积分深度背调：...",
  "contact_source_urls": ["https://example.com/team-or-profile"],
  "public_source_lane_results": {
    "official_company": "已检查：...",
    "indexed_documents": "已检查：...",
    "registries_regulators": "已检查 / 不适用 / 访问限制：...",
    "associations_chambers": "已检查 / 不适用 / 访问限制：...",
    "events_speakers": "已检查 / 不适用 / 访问限制：...",
    "procurement_awards": "已检查 / 不适用 / 访问限制：...",
    "commercial_signals": "已检查 / 不适用 / 访问限制：...",
    "professional_profiles": "已检查 / 不适用 / 登录墙已跳过：..."
  },
  "contact_search_note": "中文记录八类公开来源、客户类型对应角色阶梯、当地语言关键词、LinkedIn或当地职业网络结果及访问限制",
  "fit_reason": "中文匹配推断，不写成采购需求事实",
  "risks": "中文描述不确定性或合作障碍",
  "confidence": "高 | 中 | 低",
  "verified_date": "YYYY-MM-DD",
  "source_urls": ["https://example.com/page"],
  "evidence_boundary": "事实 / 推断 / 未知",
  "next_step": "建议的下一步核实或联系动作",
  "outreach_subject": "Subject",
  "outreach_body": "Personalized draft",
  "scores": {
    "product_overlap": 0,
    "channel_fit": 0,
    "cooperation_fit": 0,
    "supply_fit": 0,
    "size_fit": 0,
    "evidence_quality": 0,
    "reachability": 0
  }
}
```

Score maxima are 30, 20, 15, 10, 10, 10, and 5.

`contact_status`, `contact_search_note`, and all eight `public_source_lane_results` keys are required for every newly researched qualified lead and near match. Use a short Chinese result, `不适用`, or an access limitation for every lane. When `contact_name` is populated, also require `contact_title` and at least one `contact_source_urls` entry. When no person is found, keep `contact_name` empty in JSON; the workbook builder will display `需通过Apollo插件优化搜索具名联系人` without treating it as a real person. The builder remains backward-compatible with older JSON and automatically converts old `未找到具名联系人` statuses to the new Apollo optimization wording.

Build a runtime source map for the actual country, language, industry, and customer type. Do not hard-code a country registry, trade fair, association, procurement portal, or professional network as a universal source. Record the result or access limitation for every source category required by `public-contact-playbook.md` in `contact_search_note`.

Adapt the contact role order to `customer_type` using `public-contact-playbook.md`. Populate the highest-priority supported person for that customer type instead of applying one procurement-to-executive sequence to every company.

Populate `professional_profile_url` with an exact public LinkedIn or local professional-network profile only when the person-company-role match is supported, and set `professional_network` to the source name. `linkedin` remains accepted for backward compatibility. Record an explicit public-professional-profile-not-found or login-wall result in `contact_search_note` when no exact accessible profile is available.

`apollo_deep_research_prompt` is optional in input. The workbook builder fills it automatically for every row without a public personal business email. The prompt must begin exactly `需尝试Apollo积分深度背调`. A company-general or department mailbox does not count as a person's email.

The workbook builder derives `scores.reachability` from the actual named contact and contact route. It does not trust an inflated input score.

A qualified lead must have a reachable public company channel and therefore must not use the unresolved `E` state (`需通过Apollo插件优化搜索；公开网页暂无可用联系人`). Put an otherwise plausible but unreachable company in `near_matches`; exclude it when other required qualification evidence is also insufficient.

## `near_matches`

Use the same lead shape. Include `near_match_reason`.

## `excluded`

Each item supports:

```json
{
  "company": "Company name",
  "website": "https://example.com",
  "reason": "中文说明硬性排除原因或主体冲突",
  "source_url": "https://example.com/page"
}
```

## Empty data

- Use empty strings or empty arrays for unknown values.
- Do not use an empty string for `contact_status` or `contact_search_note`.
- Never use guessed values, inferred email patterns, or approximate professional-profile URLs.
- Keep URLs as plain text so the workbook remains auditable.
