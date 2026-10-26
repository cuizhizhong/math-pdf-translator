# 覆盖清单约定

覆盖文件推荐使用 JSON。字段可适应项目，但必须保留可验证事实和状态流转。

## 推荐骨架

```json
{
  "document_kind": "book_chapter",
  "source_format": "pdf-text",
  "workflow": {
    "model_route": {
      "planner": "gpt-5.6-sol",
      "planner_write_access": false,
      "executor": "gpt-5.6-luna",
      "executor_reasoning": "max",
      "sole_writer": true,
      "independent_acceptance": "primary_agent"
    },
    "loaded_constraints": {
      "load_scope": "task_once",
      "loaded_by": "primary_coordinator",
      "nature_reader_entrypoint": "nature-reader/SKILL.md",
      "nature_reader_manifest": "nature-reader/manifest.yaml",
      "always_load": [],
      "source_fragments": [],
      "on_demand_references": [],
      "pdf_skill_loaded": true,
      "fingerprints": [],
      "constraint_packet": {
        "version": 1,
        "created": true,
        "reused_by": ["planner", "executor", "primary_agent_qa"],
        "invalidated": false,
        "invalidation_events": []
      }
    },
    "template": {
      "mode": "preserve_existing",
      "existing_project": true,
      "existing_document_class": "elegantbook",
      "preserved_existing_class": true,
      "template_invariants_source": "existing_project",
      "master_skill_loaded": null,
      "master_load_reason": "not_required_for_verified_existing_project",
      "final_document_class": "elegantbook"
    },
    "delivery": {
      "primary": "complete_chinese_latex_pdf",
      "bilingual_reader_requested": false,
      "paper_md_required": false
    }
  },
  "chapter": 4,
  "title_en": "The Maximum Principle",
  "title_zh": "极大值原理",
  "status": "pending",
  "source": {
    "file": "source.pdf",
    "printed_pages": "102-155",
    "pdf_physical_pages": "121-174",
    "page_count": 54,
    "mapping_rule": "pdf_physical_page = printed_page + 19"
  },
  "expected": {
    "sections": 6,
    "subsections": 17,
    "equations": 70,
    "figures": 18,
    "examples": 4,
    "exercises": 16,
    "lemmas": 2,
    "named_statements": 2,
    "numbered_theorems": 1,
    "source_footnotes": 8,
    "citation_keys": 33
  },
  "stages": [],
  "pages": [],
  "figures": [],
  "validation": {}
}
```

`document_kind` 推荐使用稳定值，如 `book`、`book_chapter`、`monograph`、`long_lecture_notes`、`thesis_like`、`journal_paper`、`conference_paper`、`preprint`、`working_paper` 或 `short_academic_report`。若项目已有自己的枚举，可以保留项目命名，但须能明确推导模板路线。

`loaded_constraints` 必须记录本次实际读取的文件，而不是预期读取清单。`load_scope` 默认为 `task_once`，并记录首次加载者、文件指纹、约束包版本、复用角色和失效事件。PDF 输入的 `pdf_skill_loaded` 必须为 `true`；非 PDF 输入可为 `false`。公式或图表存在时，对应 `on_demand_references` 不得缺失。同一任务的后续阶段不得把复用误记为再次完整加载。

`template.mode` 只允许：

- `new_elegantbook`：新建书籍类项目；`master_skill_loaded` 为 `elegantbook-master`。
- `new_elegantpaper`：新建论文类项目；`master_skill_loaded` 为 `elegantpaper-master`。
- `preserve_existing`：已有项目；`preserved_existing_class` 必须为 `true`。记录模板不变量来自实际项目。已有 Elegant 类在模板信息充分时 `master_skill_loaded` 可为 `null`；仅在确实读取 Master 时记录技能名与原因。其他类同样不得迁移模板。

已有覆盖文件不要求追溯迁移到新字段；新任务及仍在进行的任务采用任务级加载记录。

用户明确指定其他模板时仍使用 `preserve_existing` 或项目自定义的显式模式，并在 `notes` 中记录用户指令，不能伪装成 Elegant 默认路由。

## 页面记录

每个源页至少包含：

```json
{
  "printed_page": 102,
  "pdf_physical_page": 121,
  "target_anchor": "section:4.1",
  "objects": ["eq:4.1", "source footnote 1"],
  "status": "pending",
  "notes": ""
}
```

`objects` 应按实际页内容记录，不要为了满足总数而虚构归属。跨页公式、脚注或段落可在相邻两页都登记，并在 `notes` 中说明。

## 图片记录

```json
{
  "id": "fig4.1",
  "source_pdf_page": 127,
  "file": "image/fig4.1.png",
  "action": "recrop",
  "caption_checked": false,
  "render_checked": false,
  "status": "pending"
}
```

图片在源裁剪、LaTeX 图注和最终 PDF 渲染均核对后才能完成。

## 状态流转

- `pending`：尚未翻译或核查。
- `partial_translated_checked_pending_render`：跨阶段对象只完成一部分。
- `translated_checked_pending_render`：已翻译并与源文核对，尚未完成最终 PDF 视觉复核。
- `complete_verified`：源文、译文、编译和最终渲染全部通过。

顶层 `status` 只能在所有页面和对象均为 `complete_verified`、编译成功且视觉检查完成后更新为 `complete_verified`。最终 `validation` 应记录：

- 路由与加载检查结果，包括 `document_kind`、`source_format`、约束技能和模板模式；
- 完整编译顺序和退出码；
- 最终 PDF 总页数；
- 译文章节 PDF 页范围和页数；
- 下一章起始页；
- 最终结构计数；
- 已核查的公式组；
- 实际视觉检查页数；
- 已修复问题和仍存在的不确定项。
