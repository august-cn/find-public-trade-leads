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
  "contact_status": "已公开核实 | 仅二手来源 | 待核实 | 未找到具名联系人；已提供部门渠道 | 未找到具名联系人；已提供公司渠道 | 公开网页未找到可用联系人",
  "email": "",
  "email_type": "公开个人邮箱 | 部门邮箱 | 公司通用邮箱 | 联系表单 | 未找到",
  "phone": "",
  "phone_type": "直线电话 | 部门电话 | 公司总机 | 未找到",
  "linkedin": "",
  "contact_source_urls": ["https://example.com/team-or-profile"],
  "contact_search_note": "中文记录已检查的官网页面、职位关键词、职业网络、PDF或行业来源及结果",
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

`contact_status` and `contact_search_note` are required for every qualified lead and near match. When `contact_name` is populated, also require `contact_title` and at least one `contact_source_urls` entry. When no person is found, keep `contact_name` empty in JSON; the workbook builder will display `未找到具名采购联系人` without treating it as a real person.

The workbook builder derives `scores.reachability` from the actual named contact and contact route. It does not trust an inflated input score.

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
- Never use guessed values.
- Keep URLs as plain text so the workbook remains auditable.
