---
name: ask-agent
description: Hướng dẫn người mới về công cụ AI Agent (Google Antigravity, Claude Code, Codex) và cấu trúc hệ thống Agent của công ty (vault, shared data, skills, rules, workflows). Tự động kích hoạt khi user hỏi — kể cả hỏi bằng lời thường — về: Antigravity/Claude Code/Cowork là gì và dùng sao, skill/rule/workflow là gì, vault là gì, shared/ hoạt động thế nào, cách tạo agent mới, "tôi mới vào bắt đầu từ đâu", hoặc bất kỳ câu hỏi onboarding nào về hệ thống AI của công ty.
---

# ask-agent — Cửa hỏi về Hệ thống & Công cụ AI

Skill này dành cho **người mới gia nhập công ty**. Nó giúp bạn hiểu và sử dụng hệ thống AI Agent — gồm công cụ (Antigravity, Claude Code, Cowork, Codex), các khái niệm cốt lõi (vault, shared data, skills, rules, workflows), và cách hệ thống Agent của công ty được tổ chức.

> **Đây là 1 trong 3 "cửa hỏi-đáp":** `ask-agent` (hệ thống & công cụ) · `ask-hr` (công ty & chính sách) · `lark` (thao tác app Lark). Nếu câu hỏi nghiêng về chính sách/công ty → nhường cho `ask-hr`; nếu về gửi tin/lịch/Bitable trên Lark → nhường cho `lark`.

---

## Khi nào dùng skill này

- User hỏi Antigravity / Claude Code / Cowork / Codex là gì, cài & dùng ra sao.
- User hỏi skill, rule, workflow là gì; cách gọi một skill.
- User hỏi vault, `shared/`, sync data hoạt động thế nào.
- User mới onboard, chưa biết bắt đầu từ đâu.
- User so sánh các công cụ AI Agent.

## Cách trả lời

Trả lời **ngắn gọn, có ví dụ thực tế**, tránh lý thuyết dài. Luôn kết thúc bằng:
- **Bước tiếp theo** rõ ràng (1 hành động cụ thể).
- Gợi ý **file nên đọc thêm** trong `resources/` của skill này.

---

## Phần 1 — Google Antigravity (tài liệu chính thức đầy đủ)

Toàn bộ docs gốc nằm tại `resources/antigravity-docs/` (42 file). **Luôn đọc đúng file liên quan** thay vì chỉ dùng summary.

### Index — câu hỏi nào → đọc file nào

| Câu hỏi về | Đọc file |
|-----------|---------|
| Tổng quan, bắt đầu từ đâu | `Getting-Started.md`, `Home.md`, `FAQ.md` |
| Skills là gì, cách tạo | `Skills.md` ← **quan trọng nhất** |
| Rules & Workflows | `Rules-Workflows.md` |
| Agent hoạt động thế nào | `Agent.md`, `Agent-Manager.md`, `Agent-Modes-Settings.md` |
| Browser / subagent | `Browser.md`, `Browser-Subagent.md` |
| MCP integration | `MCP.md` |
| Artifacts, Plans | `Artifacts.md`, `Plans.md`, `Implementation-Plan.md` |
| Sandbox, security | `Sandboxing.md`, `Strict-Mode.md`, `Allowlist-Denylist.md` |
| Models (Gemini, Claude...) | `Models.md` |
| Workspace, Editor | `Workspaces.md`, `Editor.md`, `Panes.md` |
| Terminal | `Terminal.md` |
| Knowledge items | `Knowledge.md` |
| Task management | `Task-List.md`, `Task-Groups.md` |
| Chrome extension | `Chrome-Extension.md`, `Separate-Chrome-Profile.md` |
| FAQ tổng hợp | `FAQ.md` (đọc khi chưa rõ chủ đề) |

### Tóm tắt nhanh (khi user hỏi overview)

```
Antigravity = IDE + AI Agent (Google Gemini)
├── Chat với Agent → Agent đọc code, chạy lệnh, viết file
├── Skills (.agent/skills/)   → Dạy Agent làm một việc cụ thể
├── Rules (.agent/rules/)     → Quy tắc luôn áp dụng
└── Workflows (.agent/workflows/) → /lệnh để chạy quy trình
```

Đọc thêm: `resources/antigravity-guide.md` (hướng dẫn nhanh, tiếng Việt).

---

## Phần 2 — Claude Code & Cowork (Anthropic)

Bản thân bạn (Agent đang chạy) chính là **Claude Code / Cowork**. Khi user hỏi về Claude Code/Cowork:

- **Trả lời trực tiếp** từ hiểu biết của bạn về CLI/Cowork cho các câu cơ bản (mở folder, chọn model, Ask vs Code mode, gọi skill bằng `/`, cài plugin).
- Với câu hỏi **chi tiết/chuyên sâu** (hooks, settings.json, permissions, MCP, slash commands nâng cao) cần tài liệu chính thức cập nhật → dùng **WebFetch** lấy docs:

  ```
  WebFetch https://code.claude.com/docs/en/  (hoặc trang con tương ứng)
  ```

  Một số trang hữu ích:
  - Tổng quan & cài đặt: `https://code.claude.com/docs/en/overview`
  - Skills: `https://code.claude.com/docs/en/skills`
  - Plugins & marketplace: `https://code.claude.com/docs/en/plugins`
  - Settings & hooks: `https://code.claude.com/docs/en/settings`, `.../hooks`
  - MCP: `https://code.claude.com/docs/en/mcp`

> Lưu ý: bản đóng gói này **không nhúng** file `llms-full.txt` (~58MB) để giữ plugin nhẹ. Khi cần spec đầy đủ, fetch từ web như trên hoặc tải `https://platform.claude.com/llms-full.txt`.

### Tóm tắt nhanh Claude Code / Cowork

```
Claude Code = công cụ Agent của Anthropic (Claude), chạy trong terminal/IDE.
Cowork      = ứng dụng desktop của Claude Code — giao diện thân thiện cho NON-DEV.
              Chọn folder → chọn mode (Ask/Code) → chọn model → gõ yêu cầu.
Hỗ trợ: Skills (/ten-skill), Plugins, MCP (Model Context Protocol).
```

> Người không phải dev nên dùng **Cowork**. Hướng dẫn chi tiết: chạy lệnh `/humaner:huong-dan-cowork`.

---

## Phần 3 — Hệ thống Agent của công ty

Đọc `resources/thehuman-agent-system.md` để trả lời:
- Vault là gì, tại sao có 4 tầng.
- `shared/` hoạt động ra sao.
- Sync data giữa các Agent bằng cách nào.
- Cách tạo Agent mới cho team.

### Tóm tắt nhanh

```
{workspace-folder}/ (monorepo — tên folder tuỳ công ty đặt)
├── Humaner-Agent/         ← Hub trung tâm
│   └── shared/            ← Data tổng hợp từ tất cả agents (KHÔNG sửa tay)
├── Finance-Agent/
├── HR-Agent/
└── ...

Mỗi Agent có:
├── .claude/skills/   ← Kỹ năng chuyên biệt
├── .claude/rules/    ← Rules luôn on
└── vaults/
    ├── vault-1-core/      ← Bất biến: mục tiêu, glossary, rules — đọc trước
    ├── vault-2-live/data/ ← Sync ra shared/ hàng ngày
    ├── vault-3-standards/ ← SOPs, playbooks
    └── vault-4-strategy/  ← Roadmap, OKR dài hạn
```

---

## Phần 4 — Các công cụ AI Agent khác

Đọc `resources/ai-tools-comparison.md` để so sánh chi tiết.

| Công cụ | Công ty | Ghi chú |
|---------|---------|---------|
| **Antigravity** | Google (Gemini) | Đang dùng tại công ty |
| **Claude Code / Cowork** | Anthropic (Claude) | Terminal + app desktop; mạnh về coding & skills |
| **Codex** | OpenAI (ChatGPT) | Web + terminal |

> Cấu trúc `skills/`, `rules/`, `workflows/` là tương đương về concept — chỉ khác tên file & cú pháp nhỏ.

---

## Câu hỏi thường gặp

**"Tôi bắt đầu từ đâu?"**
→ Đọc sổ tay onboarding 7 ngày (hỏi `ask-hr`) → Clone agent của team → Mở bằng Cowork/Claude Code → Hỏi Agent.

**"Skill là gì?"**
→ File hướng dẫn dạy Agent làm một việc cụ thể. Trong Cowork/Claude Code gọi bằng `/ten-skill` (hoặc cứ hỏi tự nhiên, skill tự kích hoạt).

**"Vault dùng để làm gì?"**
→ Kho kiến thức theo 4 tầng. Đọc `vault-1-core` trước.

**"shared/ là gì?"**
→ Thư mục chứa data sync từ tất cả agents. **Không sửa tay** — GitHub Actions tự cập nhật.

**"Tôi muốn tạo Agent cho team mới?"**
→ Dùng skill `agent-builder` (nếu có trong workspace) hoặc hỏi đội hệ thống.
