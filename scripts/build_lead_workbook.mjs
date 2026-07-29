import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

function readArg(name) {
  const index = process.argv.indexOf(name);
  if (index === -1 || !process.argv[index + 1]) {
    throw new Error(`Missing required argument: ${name}`);
  }
  return process.argv[index + 1];
}

function asText(value) {
  if (value === undefined || value === null) return "";
  return String(value);
}

function asDate(value) {
  const text = asText(value);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return text;
  return new Date(`${text}T12:00:00Z`);
}

function clampScore(value, max) {
  const number = Number(value ?? 0);
  if (!Number.isFinite(number)) return 0;
  return Math.max(0, Math.min(max, number));
}

function sourceText(value) {
  if (!Array.isArray(value)) return asText(value);
  return value.filter(Boolean).join("\n");
}

function categoryText(value, translations) {
  const text = asText(value).trim();
  if (!text) return "";
  return translations[text.toLowerCase()] ?? text;
}

const sizeBandZh = {
  micro: "微型",
  small: "小型",
  medium: "中型",
  large: "大型",
};

const contactStatusZh = {
  "verified public": "已公开核实",
  "secondary-source only": "仅二手来源",
  "not found": "未找到",
};

const emailTypeZh = {
  "named public": "公开个人邮箱",
  department: "部门邮箱",
  "company general": "公司通用邮箱",
  form: "联系表单",
  "not found": "未找到",
};

const phoneTypeZh = {
  direct: "直线电话",
  department: "部门电话",
  switchboard: "公司总机",
  "not found": "未找到",
};

const confidenceZh = {
  high: "高",
  medium: "中",
  low: "低",
};

function requireBrief(brief) {
  const fields = [
    "product",
    "target_market",
    "cooperation_model",
    "supply_capability",
    "customer_size",
    "reference_brands",
    "exclusions",
  ];
  const missing = fields.filter((field) => !asText(brief?.[field]).trim());
  if (missing.length) {
    throw new Error(`Missing required brief fields: ${missing.join(", ")}`);
  }
}

function validateLead(lead, index) {
  if (!asText(lead?.company).trim()) {
    throw new Error(`Lead ${index + 1} is missing company`);
  }
  const maxima = {
    product_overlap: 30,
    channel_fit: 20,
    cooperation_fit: 15,
    supply_fit: 10,
    size_fit: 10,
    evidence_quality: 10,
    reachability: 5,
  };
  for (const [field, max] of Object.entries(maxima)) {
    const value = Number(lead?.scores?.[field] ?? 0);
    if (!Number.isFinite(value) || value < 0 || value > max) {
      throw new Error(`Lead ${index + 1} has invalid score ${field}; expected 0-${max}`);
    }
  }
}

function styleTitle(sheet, range, title) {
  sheet.mergeCells(range);
  const cell = range.split(":")[0];
  sheet.getRange(cell).values = [[title]];
  sheet.getRange(range).format = {
    fill: "#17365D",
    font: { bold: true, color: "#FFFFFF", size: 16 },
    verticalAlignment: "center",
  };
  sheet.getRange(range).format.rowHeight = 34;
}

function styleHeader(range) {
  range.format = {
    fill: "#17365D",
    font: { bold: true, color: "#FFFFFF" },
    wrapText: true,
    verticalAlignment: "center",
  };
  range.format.rowHeight = 30;
}

function setWidths(sheet, widths, lastRow) {
  for (const [column, width] of Object.entries(widths)) {
    sheet.getRange(`${column}1:${column}${lastRow}`).format.columnWidth = width;
  }
}

function setLeadValues(sheet, leads, startRow) {
  const scoreFields = [
    ["product_overlap", 30],
    ["channel_fit", 20],
    ["cooperation_fit", 15],
    ["supply_fit", 10],
    ["size_fit", 10],
    ["evidence_quality", 10],
    ["reachability", 5],
  ];
  for (let index = 0; index < leads.length; index += 1) {
    const lead = leads[index];
    const row = startRow + index;
    const scores = scoreFields.map(([field, max]) => clampScore(lead.scores?.[field], max));
    sheet.getRange(`A${row}:AC${row}`).values = [[
      Number(lead.priority ?? index + 1),
      asText(lead.company),
      asText(lead.legal_name),
      asText(lead.customer_type),
      categoryText(lead.size_band, sizeBandZh),
      asText(lead.size_evidence),
      asText(lead.address),
      asText(lead.country),
      asText(lead.website),
      asText(lead.product_evidence),
      asText(lead.contact_name),
      asText(lead.contact_title),
      categoryText(lead.contact_status, contactStatusZh),
      asText(lead.email),
      categoryText(lead.email_type, emailTypeZh),
      asText(lead.phone),
      categoryText(lead.phone_type, phoneTypeZh),
      asText(lead.linkedin),
      asText(lead.fit_reason),
      asText(lead.risks),
      categoryText(lead.confidence, confidenceZh),
      asDate(lead.verified_date),
      ...scores,
    ]];
    sheet.getRange(`AD${row}`).formulas = [[`=SUM(W${row}:AC${row})`]];
    sheet.getRange(`AE${row}`).formulas = [[
      `=IF(AD${row}>=85,"高优先级",IF(AD${row}>=70,"中优先级","待探索"))`,
    ]];
    sheet.getRange(`AF${row}:AH${row}`).values = [[
      sourceText(lead.source_urls),
      asText(lead.evidence_boundary),
      asText(lead.next_step),
    ]];
  }
}

function configureLeadSheet(sheet, leads, tableName) {
  const headers = [[
    "优先序号", "公司名称", "法定名称", "客户类型", "规模档位", "规模依据",
    "地址（保留原文）", "国家或地区", "公司官网", "产品或品类证据", "联系人", "职位或部门",
    "联系人状态", "邮箱（保留原文）", "邮箱类型", "电话（保留原文）", "电话类型", "LinkedIn",
    "匹配理由", "风险与疑点", "可信度", "核实日期", "产品重合度（30）",
    "渠道匹配（20）", "合作方式匹配（15）", "供货匹配（10）", "规模匹配（10）",
    "证据质量（10）", "可联系程度（5）", "总分", "分级", "来源链接",
    "证据边界", "下一步建议",
  ]];
  const startRow = 3;
  const endRow = startRow + leads.length;
  styleTitle(sheet, "A1:AH1", sheet.name);
  sheet.getRange("A3:AH3").values = headers;
  styleHeader(sheet.getRange("A3:AH3"));
  setLeadValues(sheet, leads, 4);
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(2);

  const body = sheet.getRange(`A4:AH${endRow}`);
  body.format = {
    font: { size: 10 },
    wrapText: true,
    verticalAlignment: "top",
    borders: {
      insideHorizontal: { style: "thin", color: "#D9E2F3" },
      bottom: { style: "thin", color: "#D9E2F3" },
    },
  };
  body.format.rowHeight = 76;
  sheet.getRange(`A4:A${endRow}`).format.horizontalAlignment = "center";
  sheet.getRange(`W4:AE${endRow}`).format.horizontalAlignment = "center";
  sheet.getRange(`V4:V${endRow}`).format.numberFormat = "yyyy-mm-dd";

  sheet.getRange(`AE4:AE${endRow}`).conditionalFormats.add("containsText", {
    text: "高优先级",
    format: { fill: "#E2F0D9", font: { color: "#375623", bold: true } },
  });
  sheet.getRange(`AE4:AE${endRow}`).conditionalFormats.add("containsText", {
    text: "中优先级",
    format: { fill: "#FFF2CC", font: { color: "#7F6000", bold: true } },
  });
  sheet.getRange(`AE4:AE${endRow}`).conditionalFormats.add("containsText", {
    text: "待探索",
    format: { fill: "#FCE4D6", font: { color: "#C00000" } },
  });

  setWidths(sheet, {
    A: 8, B: 27, C: 28, D: 20, E: 15, F: 30, G: 32, H: 14, I: 30,
    J: 38, K: 20, L: 25, M: 20, N: 28, O: 20, P: 20, Q: 16, R: 38,
    S: 38, T: 34, U: 13, V: 14, W: 14, X: 14, Y: 15, Z: 13, AA: 12,
    AB: 15, AC: 13, AD: 10, AE: 12, AF: 44, AG: 48, AH: 42,
  }, endRow);

  const table = sheet.tables.add(`A3:AH${endRow}`, true, tableName);
  table.style = "TableStyleMedium2";
  table.showBandedRows = true;
  table.showFilterButton = true;
}

const inputPath = path.resolve(readArg("--input"));
const outputPath = path.resolve(readArg("--output"));
const previewDir = path.resolve(readArg("--preview-dir"));
const data = JSON.parse(await fs.readFile(inputPath, "utf8"));

requireBrief(data.brief);
if (!Array.isArray(data.leads) || data.leads.length === 0) {
  throw new Error("At least one qualified lead is required");
}
data.leads.forEach(validateLead);
if (Array.isArray(data.near_matches)) data.near_matches.forEach(validateLead);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const workbook = Workbook.create();
const guide = workbook.worksheets.add("需求与说明");
const leadsSheet = workbook.worksheets.add("合格客户");
const outreach = workbook.worksheets.add("开发信");
const evidence = workbook.worksheets.add("证据与评分");
const nearMatches = Array.isArray(data.near_matches) && data.near_matches.length
  ? workbook.worksheets.add("待探索客户")
  : null;
const excluded = Array.isArray(data.excluded) && data.excluded.length
  ? workbook.worksheets.add("已排除")
  : null;

workbook.comments.setSelf({
  displayName: asText(data.sender?.name) || "用户",
});

styleTitle(guide, "A1:H1", "公开网页外贸客户开发报告");
guide.showGridLines = false;
guide.getRange("A3:B13").values = [
  ["项目", "内容"],
  ["产品", asText(data.brief.product)],
  ["目标市场", asText(data.brief.target_market)],
  ["合作方式", asText(data.brief.cooperation_model)],
  ["供货能力", asText(data.brief.supply_capability)],
  ["客户规模", asText(data.brief.customer_size)],
  ["参考品牌", asText(data.brief.reference_brands)],
  ["排除条件", asText(data.brief.exclusions)],
  ["目标客户数量", Number(data.brief.target_count ?? 20)],
  ["产品资料来源", sourceText(data.brief.product_sources)],
  ["研究说明", asText(data.brief.research_notes)],
];
styleHeader(guide.getRange("A3:B3"));
guide.getRange("A4:B13").format = {
  wrapText: true,
  verticalAlignment: "top",
  borders: { insideHorizontal: { style: "thin", color: "#D9E2F3" } },
};
guide.getRange("A4:A13").format = { fill: "#D9EAF7", font: { bold: true, color: "#17365D" } };
guide.getRange("D3:H3").values = [[
  "合格客户", "待探索客户", "已排除", "具名联系人", "公司公共渠道",
]];
styleHeader(guide.getRange("D3:H3"));
const qualifiedEnd = data.leads.length + 3;
guide.getRange("D4").formulas = [[`=COUNTA('合格客户'!B4:B${qualifiedEnd})`]];
guide.getRange("E4").values = [[nearMatches ? data.near_matches.length : 0]];
guide.getRange("F4").values = [[excluded ? data.excluded.length : 0]];
guide.getRange("G4").formulas = [[
  `=COUNTIF('合格客户'!K4:K${qualifiedEnd},"?*")`,
]];
guide.getRange("H4").formulas = [[`=D4-G4`]];
guide.getRange("D4:H4").format = {
  fill: "#F2F7FB",
  font: { bold: true, color: "#17365D", size: 15 },
  horizontalAlignment: "center",
};
guide.mergeCells("D6:H8");
guide.getRange("D6").values = [[
  "公开信息显示的产品与渠道匹配只是一项客户开发假设，不能证明对方存在当前需求、正在采购、对现有供应商不满或具有明确购买意向。"
]];
guide.getRange("D6:H8").format = {
  fill: "#FFF2CC",
  font: { color: "#7F6000" },
  wrapText: true,
  verticalAlignment: "center",
};
guide.mergeCells("D10:H13");
guide.getRange("D10").values = [[
  "联系人规则：只有在公开证据能够支持身份和职责时，才使用具名联系人；否则使用部门邮箱、公司通用邮箱、公开联系表单或公司总机。禁止推测邮箱格式。"
]];
guide.getRange("D10:H13").format = {
  fill: "#E2F0D9",
  font: { color: "#375623" },
  wrapText: true,
  verticalAlignment: "center",
};
setWidths(guide, { A: 23, B: 66, C: 4, D: 17, E: 17, F: 15, G: 18, H: 20 }, 13);

configureLeadSheet(leadsSheet, data.leads, "QualifiedLeadTable");

styleTitle(outreach, "A1:G1", "个性化开发信草稿");
outreach.getRange("A3:G3").values = [[
  "优先序号", "公司名称", "收件人", "邮箱或联系渠道", "邮件主题", "开发信正文", "联系说明",
]];
styleHeader(outreach.getRange("A3:G3"));
for (let index = 0; index < data.leads.length; index += 1) {
  const lead = data.leads[index];
  const row = index + 4;
  outreach.getRange(`A${row}:G${row}`).values = [[
    Number(lead.priority ?? index + 1),
    asText(lead.company),
    asText(lead.contact_name) || asText(lead.contact_title) || "公司团队",
    asText(lead.email) || asText(lead.website),
    asText(lead.outreach_subject),
    asText(lead.outreach_body),
    `${categoryText(lead.contact_status, contactStatusZh)} | ${categoryText(lead.email_type, emailTypeZh)}`,
  ]];
}
const outreachEnd = data.leads.length + 3;
outreach.getRange(`A4:G${outreachEnd}`).format = {
  wrapText: true,
  verticalAlignment: "top",
  borders: { insideHorizontal: { style: "thin", color: "#D9E2F3" } },
};
outreach.getRange(`A4:G${outreachEnd}`).format.rowHeight = 150;
outreach.showGridLines = false;
outreach.freezePanes.freezeRows(3);
setWidths(outreach, { A: 8, B: 27, C: 23, D: 30, E: 42, F: 92, G: 28 }, outreachEnd);
const outreachTable = outreach.tables.add(`A3:G${outreachEnd}`, true, "OutreachDraftTable");
outreachTable.style = "TableStyleMedium2";
outreachTable.showBandedRows = true;
outreachTable.showFilterButton = true;

styleTitle(evidence, "A1:M1", "证据边界与评分明细");
evidence.getRange("A3:M3").values = [[
  "优先序号", "公司名称", "来源链接", "证据边界", "下一步建议",
  "产品重合度（30）", "渠道匹配（20）", "合作方式匹配（15）", "供货匹配（10）",
  "规模匹配（10）", "证据质量（10）", "可联系程度（5）", "总分 / 分级",
]];
styleHeader(evidence.getRange("A3:M3"));
for (let index = 0; index < data.leads.length; index += 1) {
  const lead = data.leads[index];
  const row = index + 4;
  const sourceRow = index + 4;
  evidence.getRange(`A${row}:E${row}`).values = [[
    Number(lead.priority ?? index + 1),
    asText(lead.company),
    sourceText(lead.source_urls),
    asText(lead.evidence_boundary),
    asText(lead.next_step),
  ]];
  evidence.getRange(`F${row}:M${row}`).formulas = [[
    `='合格客户'!W${sourceRow}`,
    `='合格客户'!X${sourceRow}`,
    `='合格客户'!Y${sourceRow}`,
    `='合格客户'!Z${sourceRow}`,
    `='合格客户'!AA${sourceRow}`,
    `='合格客户'!AB${sourceRow}`,
    `='合格客户'!AC${sourceRow}`,
    `='合格客户'!AD${sourceRow}&" / "&'合格客户'!AE${sourceRow}`,
  ]];
}
const evidenceEnd = data.leads.length + 3;
evidence.getRange(`A4:M${evidenceEnd}`).format = {
  wrapText: true,
  verticalAlignment: "top",
  borders: { insideHorizontal: { style: "thin", color: "#D9E2F3" } },
};
evidence.getRange(`A4:M${evidenceEnd}`).format.rowHeight = 86;
evidence.getRange(`F4:M${evidenceEnd}`).format.horizontalAlignment = "center";
evidence.showGridLines = false;
evidence.freezePanes.freezeRows(3);
setWidths(evidence, {
  A: 8, B: 28, C: 50, D: 54, E: 42, F: 13, G: 13, H: 15, I: 12,
  J: 12, K: 13, L: 14, M: 15,
}, evidenceEnd);
const evidenceTable = evidence.tables.add(`A3:M${evidenceEnd}`, true, "EvidenceScoreTable");
evidenceTable.style = "TableStyleMedium2";
evidenceTable.showBandedRows = true;
evidenceTable.showFilterButton = true;

if (nearMatches) {
  configureLeadSheet(nearMatches, data.near_matches, "NearMatchTable");
}

if (excluded) {
  styleTitle(excluded, "A1:D1", "已排除的候选公司");
  excluded.getRange("A3:D3").values = [["公司名称", "公司官网", "排除原因", "来源链接"]];
  styleHeader(excluded.getRange("A3:D3"));
  for (let index = 0; index < data.excluded.length; index += 1) {
    const item = data.excluded[index];
    const row = index + 4;
    excluded.getRange(`A${row}:D${row}`).values = [[
      asText(item.company),
      asText(item.website),
      asText(item.reason),
      asText(item.source_url),
    ]];
  }
  const excludedEnd = data.excluded.length + 3;
  excluded.getRange(`A4:D${excludedEnd}`).format = {
    wrapText: true,
    verticalAlignment: "top",
    borders: { insideHorizontal: { style: "thin", color: "#D9E2F3" } },
  };
  excluded.getRange(`A4:D${excludedEnd}`).format.rowHeight = 55;
  excluded.showGridLines = false;
  excluded.freezePanes.freezeRows(3);
  setWidths(excluded, { A: 30, B: 34, C: 58, D: 48 }, excludedEnd);
  const excludedTable = excluded.tables.add(`A3:D${excludedEnd}`, true, "ExcludedCandidateTable");
  excludedTable.style = "TableStyleMedium2";
  excludedTable.showBandedRows = true;
}

workbook.comments.addThread(
  { cell: leadsSheet.getRange("AF3") },
  "为便于逐行核查，请保留纯文本来源链接；多个来源用换行分隔。"
);
workbook.comments.addThread(
  { cell: leadsSheet.getRange("S3") },
  "说明公开证据为何支持潜在匹配。除非来源明确证明，否则不得描述该公司正在采购。"
);

const keyInspect = await workbook.inspect({
  kind: "table",
  sheetId: "合格客户",
  range: `A3:AH${qualifiedEnd}`,
  include: "values,formulas",
  tableMaxRows: Math.min(data.leads.length + 1, 10),
  tableMaxCols: 34,
  maxChars: 10000,
});
console.log(keyInspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

for (const [index, sheet] of workbook.worksheets.items.entries()) {
  const preview = await workbook.render({
    sheetName: sheet.name,
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  const safeName = sheet.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  await fs.writeFile(
    path.join(previewDir, `${safeName || `sheet-${index + 1}`}.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(JSON.stringify({
  outputPath,
  qualified: data.leads.length,
  nearMatches: data.near_matches?.length ?? 0,
  excluded: data.excluded?.length ?? 0,
  sheets: workbook.worksheets.items.map((sheet) => sheet.name),
}));
