# Hướng dẫn Google Antigravity

Tài liệu này tóm tắt những gì người mới cần biết để bắt đầu với Antigravity tại The Human.

> Tài liệu đầy đủ: thư mục `resources/antigravity-docs/` chứa toàn bộ docs gốc.

---

## 1. Antigravity là gì?

**Google Antigravity** = IDE + AI Agent (chạy trên Google Gemini).

Thay vì chỉ gợi ý code, Agent trong Antigravity có thể:
- Đọc và hiểu toàn bộ codebase của bạn
- Chạy lệnh terminal, tạo/sửa file
- Dùng browser, search web
- Thực hiện workflows nhiều bước tự động

---

## 2. Cài đặt

**Download:** [antigravity.google/download](https://antigravity.google/download)

| Hệ điều hành | Yêu cầu |
|-------------|---------|
| macOS | Monterey (12) trở lên, Apple Silicon hoặc Intel |
| Windows | Windows 10 64-bit trở lên |
| Linux | glibc ≥ 2.28 (Ubuntu 20+, Debian 10+) |

**Đăng nhập:** Dùng tài khoản Gmail cá nhân (cá nhân/được cấp)

---

## 3. Workspace — Nơi Agent làm việc

Antigravity hoạt động theo **workspace** = một thư mục/repo cụ thể.

**Cách mở workspace:**
1. Mở Antigravity
2. Bấm `Cmd + E` để toggle giữa Agent Manager và Editor
3. Chọn workspace cần làm việc (VD: `Humaner-Agent/`)

**Tip:** Mỗi Folder Agent (HR-Agent, Finance-Agent...) là một workspace riêng. Mở đúng workspace để Agent đọc đúng context.

---

## 4. Skills — Dạy Agent làm việc chuyên biệt

Skills là package hướng dẫn cho Agent. Đặt trong `.agent/skills/`.

```
.agent/skills/
└── ten-skill/
    ├── SKILL.md       ← Hướng dẫn chính (BẮT BUỘC)
    ├── resources/     ← Tài liệu tham khảo
    ├── scripts/       ← Scripts chạy được
    └── examples/      ← Ví dụ mẫu
```

**Cách gọi skill:** Gõ `@ten-skill` trong chat, hoặc để Agent tự nhận dạng khi phù hợp.

**Ví dụ tại công ty:**
- `@agent-builder` → Tạo Agent mới cho team
- `@cbi-interviewer` → Tạo bộ câu hỏi phỏng vấn (trong HR-Agent)
- `@ke-toan` → Hỗ trợ nghiệp vụ kế toán (trong Finance-Agent)

---

## 5. Rules — Quy tắc luôn áp dụng

Rules là file `.md` định nghĩa hành vi Agent phải luôn tuân theo.

```
.agent/rules/
└── onboarding.md    ← Ví dụ: luôn giới thiệu vault structure
```

**Các chế độ activation:**
| Chế độ | Mô tả |
|--------|-------|
| `always_on` | Luôn áp dụng mọi conversation |
| `manual` | Kích hoạt bằng @mention |
| Model Decision | Agent tự quyết có áp dụng không |
| Glob | Áp dụng khi mở file theo pattern |

---

## 6. Workflows — Quy trình nhiều bước

Workflows = chuỗi bước tự động, có thể chạy chuỗi skill. Gọi bằng `/ten-workflow`.

```markdown
---
description: Mô tả ngắn
---

# /ten-workflow

**Bước 1: ...**
// turbo
Hướng dẫn cho Agent làm gì

**Bước 2: ...**
Hướng dẫn tiếp theo
```

**`// turbo`**: đánh dấu step này Agent tự chạy không cần hỏi.

**Ví dụ tại công ty:**
- `/phong-van` → Quy trình phỏng vấn A-Z (HR-Agent)
- `/register-agent` → Đăng ký Agent mới vào hệ thống

---

## 7. Artifacts — File kết quả

Agent có thể tạo "artifacts" (file quan trọng như plan, report) lưu vào thư mục đặc biệt. Artifacts hiển thị trong sidebar với preview và history.

---

## 8. Phím tắt hữu ích

| Phím tắt | Chức năng |
|----------|----------|
| `Cmd + E` | Toggle Editor ↔ Agent Manager |
| `@skill-name` | Gọi skill cụ thể |
| `/workflow-name` | Chạy workflow |
| `@filename` | Đính kèm file vào chat |

---

## 9. Troubleshooting thường gặp

**"Skill không kích hoạt?"**
→ Gọi trực tiếp: `@ten-skill làm việc X`

**"Agent không hiểu context?"**
→ Chỉ mở workspace đúng (không mở nhiều workspace cùng lúc)

**"Chạy quá lâu không kết thúc?"**
→ Click "Stop" và thử chia nhỏ task hơn

**"Token limit exceeded?"**
→ Bắt đầu conversation mới, cung cấp ít context hơn
