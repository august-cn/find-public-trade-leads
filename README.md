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
- 自动排除不符合要求的公司并合并重复主体
- 使用透明的 100 分模型对客户进行评分和分级
- 为每家公司生成基于真实公开信息的个性化开发信
- 导出经过排版和公式检查的 Excel 工作簿

本项目默认可完全使用公开网页，不把 Apollo 作为必需依赖。首次调用时，Agent会让用户选择一次Apollo状态并保存在当前Codex用户设备；以后不再重复询问。公开搜索会按客户类型覆盖相关决策角色，并补查LinkedIn或当地职业网络；任何记录缺少公开个人邮箱时，工作簿都会给出“需尝试Apollo积分深度背调”提示。即使选择了允许积分，Agent也只记住“可逐次申请”，每次真正耗分前仍会说明操作、数量和积分风险并等待单独批准。

所有默认来源必须无需用户注册、无需安装浏览器扩展或插件。遇到登录墙、付费墙、反复验证码或禁止目标自动访问的条款时，Agent会跳过该来源、记录限制并继续，不要求用户绕过访问控制。

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

## 首次 Apollo 状态选择

首次使用本技能时只提示一次。用户选择后，状态保存在当前设备的Codex用户目录中；不保存Apollo账号、密码、令牌、积分余额或其他凭据。技能没有内置共享Apollo账号，两个“已连接”选项只表示当前用户已经用自己的账号完成连接。换设备、使用不同Codex用户目录或清除本地状态后会重新提示。

| 选择 | 适用情况 | 技能行为 |
| --- | --- | --- |
| 未注册、未安装、未连接或不可用（推荐默认） | 没有Apollo账号、没有连接，或不想使用Apollo | 完整执行免注册公开网页调查；不中断、不调用Apollo；缺失个人邮箱时写入“需尝试Apollo积分深度背调” |
| 已连接，但不使用积分 | 已使用自己的Apollo账号连接Codex，但不允许耗分 | 只调用官方当前明确标为零积分的People Search等免费动作，补姓名、职位、现任公司和职业主页；不调用邮箱、电话、公司搜索或任何增强动作 |
| 已连接，允许逐次审批积分 | 愿意在公开搜索和免费搜索不足时考虑付费增强 | 先完成公开与免费搜索；每次耗分前列出动作、人数、字段和积分风险，取得该次明确批准后才执行；默认不查电话、不启用waterfall |

可以随时在对话中修改：

```text
更改 Apollo 状态为未注册、未安装或仅公开搜索
更改 Apollo 状态为已连接但不使用积分
更改 Apollo 状态为已连接并允许逐次审批积分
忘记 Apollo 状态
```

修改后立即按新模式继续当前调查。`这次不要用 Apollo`只限制当前任务，不会改写长期选择；任何一次性指令都不能代替耗分调用的逐次批准。

## 工作流程

1. 解析产品文字、网址或上传文件，提取用途、材料、规格、认证、包装和差异点。
2. 生成产品同义词、本地语言关键词、目标客户类型和多组搜索式。
3. 广泛发现候选公司，并按照用户的硬性条件初步筛选。
4. 优先使用公司官网核实主体、业务范围、地址、联系方式和产品证据。
5. 对每家公司执行独立的联系人检索，按客户类型覆盖采购、品类、产品、项目、运营、管理层或市场商务负责人，并补查公开职业网络。
6. 对公司规模、渠道匹配、合作方式、证据质量和真实可联系路径进行评分。
7. 合并重复公司，将证据不足但可能相关的公司放入“待探索”名单。
8. 根据每家公司已经核实的事实撰写开发信。
9. 生成并检查最终 Excel 文件。

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
- 所有相关角色均无法核实时，Excel 显示“未找到可核实具名联系人”，同时填写联系人状态、检索说明和最佳转交渠道。
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
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-form.md
│   ├── apollo-preference.md
│   ├── research-workflow.md
│   ├── data-contract.md
│   ├── public-contact-playbook.md
│   └── example-input.json
└── scripts/
    ├── apollo_preference.py
    ├── run_build.py
    └── build_lead_workbook.mjs
```

## License

本项目使用 [MIT License](LICENSE)。

## English summary

Find Public Trade Leads is a reusable Codex skill for public-web B2B prospecting. It collects a seven-part product and ideal-customer brief, dynamically maps no-registration public sources for the requested country and industry, discovers and verifies companies, adapts decision-maker roles to each customer type, scores and deduplicates prospects, drafts evidence-based outreach, and exports a polished Excel workbook. Workbook titles, labels, statuses, and research analysis default to Simplified Chinese, while source-original identifiers and target-market outreach remain unchanged.

It works across products and markets without requiring Apollo or another paid sales-intelligence service. Every retained prospect receives a dedicated named-contact search; unresolved contacts are labeled explicitly with the search scope and best fallback route instead of unexplained blank cells. Product fit remains a prospecting hypothesis rather than proof of active purchasing demand.
