# Find Public Trade Leads

一个面向外贸业务的公开网页客户开发 Agent。输入产品和目标客户条件后，它会从公开来源发现、筛选并验证潜在 B2B 客户，生成个性化开发信，并导出结构化 Excel 客户清单。

[English summary](#english-summary)

## 主要能力

- 适用于任意产品和目标国家，不内置特定行业或市场
- 通过 7 项表单收集产品、市场和理想客户画像
- 使用公司官网、公开目录、协会、展会名单和公共登记信息开展研究
- 根据目标国家、语言、行业和客户类型，动态发现当地登记机构、监管目录、采购平台、协会、展会和职业网络，不写死某个国家或行业
- 识别进口商、经销商、批发商、品牌商、制造商、零售商等 B2B 客户
- 核实公司网站、地址、规模线索、产品匹配证据、公开邮箱和电话
- 根据进口商、零售商、品牌商、制造商、项目方、运营商等客户类型动态调整联系人优先级
- 即使没有采购负责人，也尽量填入可核实的管理层、产品或市场负责人
- 为每家公司单独补查LinkedIn或当地职业网络，记录准确个人主页、联系人专属来源和检索说明
- 没有公开个人邮箱时自动给出“需尝试Apollo积分深度背调”提示
- 首次未检测到Apollo插件时，边执行公开调查边给出一次非阻塞的注册、安装和连接建议
- 检测到Apollo插件后不再重复安装提示；积分补全仍按每次调用单独授权
- 自动排除不符合要求的公司并合并重复主体
- 在同一Codex项目内自动保存已查企业，后续批次无需上传旧Excel即可跨批次查重
- 使用透明的 100 分模型对客户进行评分和分级
- 为每家公司生成基于真实公开信息的个性化开发信
- 导出经过排版和公式检查的 Excel 工作簿

本项目始终先执行公开网页调查，不把Apollo设置作为开始研究的前置问题。首次未检测到Apollo插件时，Agent会在调查已经进行的同时建议用户注册Apollo并安装、连接Apollo插件；该提示不要求用户停下来选择或确认。连接Apollo MCP后，可用官方当前明确为零积分的People Search补充姓名、职位和职业主页；需要完整联系人信息时，可在逐次授权后使用Apollo积分调查个人或商务邮箱和电话。检测到Apollo插件后，Agent不再重复注册或安装提示；任何真正耗分的调用仍必须说明动作、数量、字段和积分上限，并等待该次明确批准。

公开调查层的所有默认来源必须无需用户注册、无需安装浏览器扩展或插件。Apollo是可选的联系人补全层，只使用用户自行注册、安装和连接的账号。遇到其他登录墙、付费墙、反复验证码或禁止目标自动访问的条款时，Agent会跳过该来源、记录限制并继续，不要求用户绕过访问控制。

## 适合谁

- 外贸公司、工厂和出口销售团队
- 希望开拓新国家或新渠道的业务负责人
- 需要批量整理潜在客户并保留证据来源的研究人员
- 希望把可复核的公开调查与可选Apollo联系人补全结合使用的用户

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

## 同一项目继续查找更多客户

第一次调查完成后，技能会把合格、待探索和已排除企业的域名、公司名称、市场和批次信息自动写入当前Codex项目的本地历史。以后无需上传旧Excel，只需输入：

```text
使用 $find-public-trade-leads，沿用上次条件，再找20家新的客户。
```

技能会自动读取上一次Brief，排除所有已经调查过的企业，并为新结果建立下一批次。用户也可以在同一句话里修改数量或条件，例如：

```text
沿用上次条件，再找30家新的客户；这次优先法国南部经销商。
```

历史文件保存在当前项目的 `.find-public-trade-leads/history.json`，并由仓库的 `.gitignore` 排除。GitHub只发布查重代码，不会上传任何用户的客户历史。此功能只在同一个本地Codex项目目录中生效；换项目、换设备、删除历史目录或重新克隆后会重新建立历史。

## 首次 Apollo 建议与后续补全

技能不会在调查前要求用户选择Apollo模式。公开网页研究会立即开始，并按客户类型完成公司核实、联系人角色检索和职业网络检查。

当当前会话未检测到Apollo插件/MCP工具，而且安装建议从未显示过时，Agent会在研究进度消息中提示一次：

```text
公开网页调查已开始。若希望补充更多具名联系人，建议注册Apollo并安装、连接Apollo插件。
连接Apollo MCP后，可用零积分People Search补充姓名、职位和职业主页；经逐次积分授权，
还可进一步调查完整联系人信息，包括个人或商务邮箱和电话。
```

该建议不会暂停调查，也不会要求用户立即注册。技能只在当前Codex项目的git忽略目录中保存“建议已经显示”这一布尔状态，不保存Apollo账号、密码、令牌、余额或其他凭据，也不会上传到GitHub。检测到Apollo插件后，不再显示注册或安装建议。

Apollo连接后的规则：

- 官方当前明确为零积分的People Search可在公开调查之后自动使用，用于补姓名、职位、现任公司和职业主页；
- 公司搜索、联系人增强、个人邮箱、电话、waterfall或任何正积分/未知成本动作都必须逐次披露；
- 披露内容包括具体动作、记录数量、请求字段、已知或最大积分影响，以及是否包含个人邮箱、电话或waterfall；
- 安装插件、连接账号或以前批准过其他调用，都不等于本次积分授权；
- 用户拒绝某次调用时，技能继续导出最佳公开/免费结果，不降低证据标准。

## 工作流程

1. 解析产品文字、网址或上传文件，提取用途、材料、规格、认证、包装和差异点。
2. 生成产品同义词、本地语言关键词、目标客户类型和多组搜索式。
3. 广泛发现候选公司，并按照用户的硬性条件初步筛选。
4. 优先使用公司官网核实主体、业务范围、地址、联系方式和产品证据。
5. 对每家公司执行独立的联系人检索，按客户类型覆盖采购、品类、产品、项目、运营、管理层或市场商务负责人，并补查公开职业网络。
6. 对公司规模、渠道匹配、合作方式、证据质量和真实可联系路径进行评分。
7. 合并重复公司，将证据不足但可能相关的公司放入“待探索”名单。
8. 根据每家公司已经核实的事实撰写开发信。
9. 生成并检查最终 Excel 文件，成功后自动写入项目本地历史供下一批查重。

## 跨国家、跨行业的公开联系人来源

Agent固定执行八类来源，但每次根据Brief动态确定具体网站和当地语言关键词：

1. 公司官网的团队、管理层、联系、新闻、供应商、合作伙伴、产品、招聘和法律声明页面；
2. 搜索引擎收录的站内页面、PDF、目录、新闻稿、演示文稿和历史展会资料；
3. 目标市场公开可访问的公司登记、监管、许可、认证和上市公司披露；
4. 行业协会、商会、产业集群、会员名单和加盟网络；
5. 展会展商、会议嘉宾、讲者、赞助商、网络研讨会和活动手册；
6. 与目标客户类型相关的公共采购、招标和合同授予文件；
7. 新闻、采访、播客、视频、招聘、合作公告、经销商和服务伙伴网络；
8. LinkedIn及当地职业网络的公开页面或搜索摘要；遇到登录墙时只保留公开证据。

每家公司都必须在结构化的 `public_source_lane_results` 中记录八类来源的结果；没有结果时填写“未找到”，与该客户类型无关时填写“不适用”，遇到登录墙或访问限制时写明限制，不能静默跳过。

联系人优先级也会随客户类型变化：进口商优先采购、进口和品类负责人；零售商优先Buyer、Category和Merchandising；品牌商优先Sourcing、Private Label和Product；制造商优先采购、供应链和技术运营；项目客户优先项目采购、工程、设施和运营；小型企业可优先创始人或总经理。市场、品牌、渠道和商务负责人仅在合作模式相关或更高优先角色不可核实时作为有效后备，不会冒充采购负责人。

## Excel 输出

默认工作簿的界面和研究分析使用简体中文，包含以下工作表：

| 工作表 | 内容 |
| --- | --- |
| `需求与说明` | 用户输入、研究口径、评分规则和使用说明 |
| `合格客户` | 合格客户、联系方式、匹配理由、风险和综合评分 |
| `开发信` | 每家公司的个性化开发信 |
| `证据与评分` | 来源链接、事实与推断边界、分项评分 |
| `待探索客户` | 证据不足或部分符合条件的候选公司，仅在需要时出现 |
| `已排除` | 不符合硬性条件的候选公司，仅在需要时出现 |

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

- `高优先级`：85–100
- `中优先级`：70–84
- `待探索`：低于 70

### 中文输出规则

- 工作表名称、标题行、列标题、字段标签、评分、分级、状态、图例、备注和说明文字全部使用中文。
- 客户类型、规模说明、产品证据、匹配理由、风险、可信度、证据边界、下一步和排除原因尽量使用中文。
- 公司及法定名称、联系人姓名、邮寄地址、邮箱、电话、网址、LinkedIn、来源链接和注册品牌保留原文，避免破坏身份识别和联系方式。
- 联系人职位默认翻译成中文；有助于核实时，可在中文后用括号保留原职位。
- 开发信标题和正文按照目标市场的商务语言输出。
- 需要引用来源原话时，先给出中文概括，再附简短原文。

## 数据与合规原则

- 只收集公开可访问的企业和商务联系信息。
- 不猜测姓名、职位、邮箱格式、LinkedIn、电话、员工数或营业收入。
- 找不到第一优先角色时，继续搜索该客户类型对应的产品、品类、项目、运营、管理层或市场商务负责人，不因单一职位缺失而过早停止。
- 所有相关角色均无法核实时，Excel 联系人栏显示“需通过Apollo插件优化搜索具名联系人”；联系人状态同时保留“当前仅提供部门渠道”“当前仅提供公司渠道”或“公开网页暂无可用联系人”等事实说明。
- LinkedIn或当地职业网络必须逐家公司搜索；只有精确匹配姓名、现任公司和职位的公开主页才能写入。
- 找不到公开个人邮箱时，不猜测邮箱格式；Excel自动写入“需尝试Apollo积分深度背调”提示。
- 公司通用邮箱或总机不能获得最高可联系评分；只有已核实具名联系人及直接联系方式才能获得最高分。
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
├── .gitignore
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-form.md
│   ├── apollo-routing.md
│   ├── continuation-search.md
│   ├── research-workflow.md
│   ├── data-contract.md
│   ├── public-contact-playbook.md
│   └── example-input.json
└── scripts/
    ├── apollo_onboarding.py
    ├── lead_history.py
    ├── run_build.py
    └── build_lead_workbook.mjs
```

## License

本项目使用 [MIT License](LICENSE)。

## English summary

Find Public Trade Leads is a reusable Codex skill for public-web B2B prospecting. It collects a seven-part product and ideal-customer brief, dynamically maps no-registration public sources for the requested country and industry, discovers and verifies companies, adapts decision-maker roles to each customer type, scores and deduplicates prospects, drafts evidence-based outreach, and exports a polished Excel workbook. Workbook titles, labels, statuses, and research analysis default to Simplified Chinese, while source-original identifiers and target-market outreach remain unchanged.

It works across products and markets by starting with public-web research immediately. When the Apollo plugin is not detected, the skill shows one non-blocking recommendation to register, install, and connect it while research continues. Once the plugin is detected, setup prompts stop. Verified zero-credit People Search may supplement names and roles; credit-consuming email, personal-email, phone, company-search, or enrichment actions require exact per-call approval. In the same local Codex project, completed batches are recorded in a git-ignored history so a simple “use the previous criteria and find another 20” request automatically excludes every previously qualified, near-match, and excluded company without re-uploading an old workbook. Every retained prospect receives a dedicated named-contact search; unresolved contacts are labeled explicitly with the search scope and best fallback route instead of unexplained blank cells. Product fit remains a prospecting hypothesis rather than proof of active purchasing demand.
