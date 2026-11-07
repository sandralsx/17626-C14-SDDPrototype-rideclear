# A3 原始作业要求核对

依据：本包 `sources/assignment.pdf`，共 6 页。下述页码指 PDF 的物理页码。本文是要求索引，不是 Learning Log。

## 本轮执行的 Step 1 与 Step 2

| 原文位置 | 必须完成的工作 | 本轮产物位置 |
| --- | --- | --- |
| 第 1 页、Step 1 第 2 页 | 根据 core、user-facing、uncertain 三项优先标准选择 goals 子集，形成两个原型的系统边界 | `goal-model.md` 第 3、4 节 |
| Step 1，第 2 页 | 审查组员 A2 模型，合并并协调细节、差异和分散的信息，形成适合本作业的模型 | 第 1、2 节与附录；`goal-model.json`；`source-crosswalk.csv` |
| Step 1，第 2 页 | 说明选择依据，并考虑被降低优先级的其他目标；选择与取舍最终要进入本人 Learning Log | 第 4 节提供技术评估；Learning Log 尚须学生独立完成 |
| Step 2，第 2 页 | 识别所选需求涉及的有意义的 overlap、dependency、conflict，利用模型解释关系和决定 | 第 5、6 节 |
| Step 2，第 2 页 | 对重叠决定合并、分别实现或不同优先级；对冲突说明权衡，可优先、折中或保留为待澄清 | 第 5 节 |
| Step 2，第 2 页 | 不能直接删除冲突 goals/requirements；保留关系和理由，更新模型以反映 scope、决定与假设 | 第 6、7 节；原模型保存在 `sources/` |

## 整个 A3 后续还要完成什么

| 步骤 | PDF 位置 | 要求 |
| --- | --- | --- |
| Step 3 | 第 2 页 | 创建 GitHub **private repository**，使用 GitHub Spec Kit 和 AI 开发工具。初始 spec 包含所选 goals/requirements、验收场景、假设/依赖/边界案例，以及 overlap/conflict 的决定。用 Spec Kit 生成 plan/tasks 后实现原型。适当使用 mock data 与简化交互。保留初始 model/spec/Spec Kit artifacts/code 为 V1，并部署保留 URL。 |
| Step 4 | 第 2、3 页 | 实际操作 V1，建立 Interview → Goal → Spec requirement ID → Code/behavior → Satisfaction 的 RTM；状态区分 fully/partially/not satisfied。区分 implementation defect 与 requirements issue，说明需要修改或澄清的内容。 |
| Step 5 | 第 3 页 | 根据 V1 评估先改 spec，再更新实现；必要时改 model；保留未解决冲突和取舍。V2 在同一仓库继承 V1 历史，单独部署。至少体现一个由 V1 评估促成的、有意义的 requirements-level improvement。 |
| Step 6 | 第 3、4 页 | 独立撰写单个 `learning-log.md`：Sprint Planning and Requirements Selection、Prototype Evaluation、Revisions and Learning，并回答四个 reflection 问题。具体例子、问题回答和正文作者均不得使用 AI 辅助。 |

## 提交与评分

第 4、5 页：课程网站只提交 **一个 GitHub repository URL**。默认分支的 README 要直接链接五个组件：GitHub V1、GitHub V2、Prototype V1 URL、Prototype V2 URL、Requirements Analysis and Learning Log。两个部署在评分时均须正常可访问。仓库包含完整源码、goal models、Spec Kit artifacts、RTM 和学习文档。建议用 `v1`/`v2` 分支或 tags，保留 V2 建立在 V1 之上的历史。截止日期与时间以课程网站为准，PDF 未给出具体日期。

第 5、6 页的六项评分标准：需求选择与理由、目标关系分析、spec-driven development、traceability、评估与修订、human judgment。重点是需求工程、可追踪性与证据支持的决定，而非界面精美程度或技术复杂度。

## 与旧对话相比需要更正的理解

1. Step 1、2 是工作阶段，PDF 没有要求分别提交 ZIP 或指定名称的分析报告。本包是这两个阶段的技术产物。
2. `frontend/`、`specs/`、`docs/goal-model.md` 等是 **Recommended Repository Structure**；必须存在的是相应内容，不能把推荐路径说成强制文件名。
3. PDF 没有要求必须使用 Python 或 `goalmodeling` 框架；也没有规定选定 goal 的固定数量。因此，本包以可读 Markdown/Mermaid 加带来源的 JSON 表达更新模型，保留原来的 Python 模型供核查。
4. 第 1 页用 “a core feature, a user-facing aspect or an aspect with high uncertainty”；第 2 页要求依据三项标准选择并说明理由。没有“每一个 goal 必须同时满足三个标准”的要求。本方案整体覆盖三项标准。
5. PDF 要审查组员的模型，但没有明确规定每组交一份还是每人交一份，也没有明确写“Step 1–5 小组、Step 6 个人”的分工。不能从措辞推导成正式提交规则。
6. 第 5 页允许 AI 辅助其他部分，明确排除 Learning Log 的作者工作。本包没有生成 `learning-log.md`，也不提供可直接粘贴的 Step 6 回答。学生仍须自行形成并撰写自己的判断。
7. Step 2 明确允许保留需 stakeholder clarification 的未解决冲突；有来源、关系、处理状态和理由的未解决事项不等同于没有完成关系分析。

## 当前完成状态

本包已完成 Step 1、2 的技术建模与关系分析。没有创建仓库、编写 Spec Kit spec/plan/tasks、开发原型、填报实现满意度或执行 V1 评估。不能将这些阶段写成已经发生。

进入 Step 3 时，应将模型中明确标记的原型假设带入 spec，并保持其“假设”身份；不得把模拟渠道、手工 ETA 或未确定的阈值写成访谈事实。Learning Log 的独立写作义务仍由学生完成。
