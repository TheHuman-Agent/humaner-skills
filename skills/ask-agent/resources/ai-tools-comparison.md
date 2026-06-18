# AI Agent Tools — So Sánh

Ngoài Google Antigravity đang dùng tại công ty, có 2 công cụ AI Agent phổ biến khác với concept tương tự. Biết về chúng giúp bạn hiểu rộng hơn về hệ sinh thái AI Agent.

---

## Tổng quan

| Tiêu chí | Antigravity (Google) | Claude Code (Anthropic) | Codex (OpenAI) |
|----------|---------------------|------------------------|----------------|
| AI Model | Gemini | Claude | GPT-4o |
| Loại | Desktop IDE App | Terminal CLI | Web + CLI |
| Skills/Rules | ✅ `.agent/skills/`, `.agent/rules/` | ✅ Tương đương concept | ✅ Tương đương concept |
| Sandbox | ✅ Docker sandbox | ✅ Có | ✅ Có |
| Browser tool | ✅ Built-in | ❌ | ❌ |
| Đang dùng? | ✅ **Đang dùng** | Tùy chọn | Tùy chọn |

---

## Google Antigravity (đang dùng)

**Điểm mạnh:**
- Tích hợp với GitHub, IDE đầy đủ tính năng
- Browser subagent built-in (lướt web, điền form)
- Skills/Rules/Workflows rất linh hoạt
- Sandboxing an toàn (Docker)

**Phù hợp với:** Làm việc trên codebase, tạo agents, quản lý dữ liệu

---

## Claude Code (Anthropic)

**Điểm mạnh:**
- Claude 3.5/3.7 rất mạnh về reasoning và coding
- Terminal-native, không cần GUI
- Autonomous mode: tự chạy nhiều bước dài

**Concept tương đương:**
```
Antigravity          Claude Code
─────────────────────────────────
.agent/skills/    ≈  Custom instructions / CLAUDE.md
.agent/rules/     ≈  CLAUDE.md (project rules)
.agent/workflows/ ≈  Slash commands
vaults/           ≈  Context files
```

**Khi nào dùng:** Khi cần coding agent thuần túy, không cần GUI  
**Tài liệu:** [docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code)

---

## Codex (OpenAI)

**Điểm mạnh:**
- Tích hợp với ChatGPT ecosystem
- Web-based, không cần cài đặt
- GPT-4o mạnh về multi-modal (image, code)

**Concept tương đương:**
```
Antigravity          Codex / ChatGPT
─────────────────────────────────────
.agent/skills/    ≈  GPT Instructions / System prompt
.agent/rules/     ≈  Memory / Persistent instructions
vaults/           ≈  Knowledge files upload
```

**Khi nào dùng:** Quick tasks, khi đã quen ChatGPT interface  
**Tài liệu:** [platform.openai.com/codex](https://platform.openai.com/codex)

---

## Tóm lại

**Concept "Agent với Skills/Rules/Vaults" là universal** — không phụ thuộc vào tool cụ thể.

Khi bạn học cách dùng Antigravity tại công ty, bạn đang học:
1. Cách define context cho AI (vaults)
2. Cách viết instructions cho AI (skills)
3. Cách tự động hóa workflow (rules + workflows)

→ Kiến thức này áp dụng được cho Claude Code và Codex với adjustment nhỏ.

> **Lưu ý:** Không dùng tài khoản Antigravity của công ty với Claude Code/Codex. Nếu muốn thử, dùng API key riêng.
