# Find Public Trade Leads

一个面向外贸业务的公开网页客户开发 Agent。输入产品和目标客户条件后，它会从公开来源发现、筛选并验证潜在 B2B 客户，生成个性化开发信，并导出结构化 Excel 客户清单。

[English summary](#english-summary)

## 主要能力

- 适用于任意产品和目标国家，不内置特定行业或市场
- 通过 7 项表单收集产品、市场和理想客户画像
- 使用公司官网、公开目录、协会、展会名单和公共登记信息开展研究
- 识别进口商、经销商、批发商、品牌商、制造商、零售商等 B2B 客户
- 核实公司网站、地址、规模线索、产品匹配证据、公开邮箱和电话
- 在有公开证据时记录联系人姓名、职位和 LinkedIn
- 自动排除不符合要求的公司并合并重复主体
- 使用透明的 100 分模型对客户进行评分和分级
- 为每家公司生成基于真实公开信息的个性化开发信
- 导出经过排版和公式检查的 Excel 工作簿

本项目只使用公开网页信息，不依赖 Apollo、付费销售情报平台或消耗积分的数据增强插件。

## 适合谁

- 外贸公司、工厂和出口销售团队
- 希望开拓新国家或新渠道的业务负责人
- 需要批量整理潜在客户并保留证据来源的研究人员
- 不使用付费获客数据库，但仍希望获得可复核结果的用户

## 使用方式

将本仓库作为 Codex Skill 安装，然后在对话中调用：

```text
Use $find-public-trade-leads to find qualified B2B prospects for my product
and export a verified Excel workbook.
```

也可以直接使用中文：

```text
使用 $find-public-trade-leads，根据我的产品和目标市场寻找 20 家合格客户，
核实联系方式，为每家公司写开发信，并导出 Excel。
```

Agent 会先要求填写以下 7 项信息；信息完整后才开始搜索。

```text
1. 产品
   输入产品说明、公开网址，或上传产品文件。

2. 目标市场
   国家、地区，或需要覆盖的语言市场。

3. 合作方式
   例如 OEM、ODM、客户自有品牌、经销或批发。

4. 供货能力
   例如混装柜、整柜、MOQ、交期、认证和包装能力。

5. 客户规模
   例如本地中型企业，并排除大型跨国集团。

6. 参考品牌或竞争对手
   用于识别产品类别和销售渠道，不代表只寻找这些品牌。

7. 排除条件
   例如纯施工公司、单店零售商或终端消费者。
```

目标客户数量为可选项，默认寻找 20 家。

## 工作流程

1. 解析产品文字、网址或上传文件，提取用途、材料、规格、认证、包装和差异点。
2. 生成产品同义词、本地语言关键词、目标客户类型和多组搜索式。
3. 广泛发现候选公司，并按照用户的硬性条件初步筛选。
4. 优先使用公司官网核实主体、业务范围、地址、联系方式和产品证据。
5. 对公司规模、渠道匹配、合作方式和证据质量进行评分。
6. 合并重复公司，将证据不足但可能相关的公司放入“待探索”名单。
7. 根据每家公司已经核实的事实撰写开发信。
8. 生成并检查最终 Excel 文件。

## Excel 输出

默认工作簿包含以下工作表：

| 工作表 | 内容 |
| --- | --- |
| `Brief & Guide` | 用户输入、研究口径、评分规则和使用说明 |
| `Qualified Leads` | 合格客户、联系方式、匹配理由、风险和综合评分 |
| `Outreach Drafts` | 每家公司的个性化开发信 |
| `Evidence & Scoring` | 来源链接、事实与推断边界、分项评分 |
| `Near Matches` | 证据不足或部分符合条件的候选公司，仅在需要时出现 |

评分总计 100 分：

| 维度 | 分值 |
| --- | ---: |
| 产品或品类重合度 | 30 |
| 客户类型与渠道匹配 | 20 |
| 合作方式匹配 | 15 |
| 供应与物流匹配 | 10 |
| 公司规模匹配 | 10 |
| 证据质量 | 10 |
| 可联系程度 | 5 |

- `High`：85–100
- `Medium`：70–84
- `Explore`：低于 70

## 数据与合规原则

- 只收集公开可访问的企业和商务联系信息。
- 不猜测姓名、职位、邮箱格式、LinkedIn、电话、员工数或营业收入。
- 找不到公开采购负责人时，保留空值并提供采购部门或公司官方渠道。
- 搜索摘要和第三方目录主要用于发现线索，关键结论优先由官网验证。
- 每条客户记录保留来源链接，并区分事实、合理推断和未知信息。
- 产品与渠道匹配只代表潜在合作可能，不证明对方正在采购。
- 不自动发送邮件，也不把联系人加入营销活动。

公开信息的完整度因国家、行业和企业而异。Agent 不会为了凑够目标数量而用低质量或虚构数据填充结果。

## 安装

### 从 GitHub 克隆

```bash
git clone https://github.com/august-cn/find-public-trade-leads.git
```

将 `find-public-trade-leads` 文件夹放入你的 Codex skills 目录，然后重新打开 Codex。

### 下载 ZIP

在仓库页面点击 **Code → Download ZIP**，解压后将整个文件夹放入 Codex skills 目录。

> Excel 构建脚本使用 Codex 工作区提供的 Node.js 和表格依赖，不需要单独安装 npm 包。

## 项目结构

```text
find-public-trade-leads/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-form.md
│   ├── research-workflow.md
│   ├── data-contract.md
│   └── example-input.json
└── scripts/
    ├── run_build.py
    └── build_lead_workbook.mjs
```

## License

本项目使用 [MIT License](LICENSE)。

## English summary

Find Public Trade Leads is a reusable Codex skill for public-web B2B prospecting. It collects a seven-part product and ideal-customer brief, discovers and verifies companies using public sources, scores and deduplicates prospects, drafts evidence-based outreach, and exports a polished Excel workbook.

It works across products and markets without requiring Apollo or another paid sales-intelligence service. Unsupported contact fields remain empty, every retained prospect includes source evidence, and product fit is treated as a prospecting hypothesis rather than proof of active purchasing demand.
