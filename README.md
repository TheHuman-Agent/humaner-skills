# Humaner Plugin — Bộ skill onboarding cho The Human Inc / Wealify

Plugin đóng gói sẵn cho **Cowork / Claude Code**, dành cho nhân viên The Human Inc. Cài 1 lần là có ngay **3 cửa hỏi-đáp** + **hướng dẫn dùng Cowork cho người không phải dev**.

> 🎯 Mục tiêu: người mới mở Cowork lên là tự hỏi-đáp được về **hệ thống/công cụ**, **công ty/chính sách**, và **thao tác Lark** — không cần lục tài liệu, không cần biết code.

---

## ⚡ Cài đặt (làm 1 lần)

### Cách 1 — Claude Cowork (khuyến nghị cho người không phải dev)

1. Mở **Customize** (góc dưới bên trái).
2. Vào **Browse plugins → Personal → +**.
3. Chọn **Add marketplace from GitHub**.
4. Nhập: **`thehuman-agent/humaner-skills`**
5. Marketplace **humaner-skills** xuất hiện → chọn plugin **humaner** → **Install**.

### Cách 2 — Dòng lệnh (Claude Code CLI)

```
/plugin marketplace add thehuman-agent/humaner-skills
/plugin install humaner@humaner-skills
```

Cài xong, plugin tự nạp (cần thì gõ `/reload-plugins`).

> 👉 Người mới chưa quen Cowork: gõ **`/huong-dan-cowork`** để được hướng dẫn từng bước bằng tiếng Việt.

---

## 📦 Trong plugin có gì

### 3 cửa hỏi-đáp (skills)

| Skill | Hỏi về | Ví dụ câu hỏi |
|-------|--------|----------------|
| **`ask-agent`** | Hệ thống Agent & công cụ AI (Antigravity, Claude Code/Cowork, Codex, vault, skill, shared/) | "Antigravity là gì?", "vault để làm gì?", "tôi mới vào bắt đầu từ đâu?" |
| **`ask-hr`** | Công ty & chính sách (Wealify, 4 sản phẩm, Squad-Chapter, AI-First, onboarding 7 ngày, nghỉ phép/WFH) | "Wealify làm gì?", "Squad vs Chapter?", "xin WFH thế nào?" |
| **`lark`** | Thao tác Lark/Feishu (gửi message, task, calendar, Bitable, Drive) | "gửi tin cho team...", "đặt lịch họp...", "thêm record vào Bitable..." |

**Cách gọi:** cứ **hỏi tự nhiên** bằng tiếng Việt — skill phù hợp tự kích hoạt theo nội dung. Hoặc gõ `/` rồi chọn `humaner:ask-agent` / `humaner:ask-hr` / `humaner:lark`.

### Slash command

| Lệnh | Tác dụng |
|------|----------|
| **`/huong-dan-cowork`** | Hướng dẫn người KHÔNG phải dev dùng Cowork: cài plugin, gọi 3 cửa, làm việc an toàn. Có thể kèm câu hỏi: `/huong-dan-cowork gửi lark thế nào`. |

---

## 🧭 Dùng nhanh (cho người mới)

1. Mở **Cowork** → chọn **thư mục** dự án/agent của bạn (góc dưới trái).
2. Để chế độ **Ask** khi mới làm quen (AI chỉ trả lời, không sửa file).
3. Gõ câu hỏi bằng tiếng Việt. Ví dụ:
   - *"Wealify có những sản phẩm gì?"* → `ask-hr` trả lời.
   - *"Skill là gì, gọi sao?"* → `ask-agent` trả lời.
   - *"Gửi tin chúc mừng team vào Lark"* → `lark` xử lý.
4. Khi AI hỏi xác nhận trước hành động quan trọng → đọc kỹ rồi mới đồng ý.

---

## 🔒 Bảo mật & phạm vi

- Plugin này **không chứa dữ liệu thật**: không roster nhân sự, không App ID/Secret, không Calendar/Group ID nội bộ. `lark` dùng **placeholder** — workspace tự cấu hình credentials qua env file riêng (mode 600, ngoài repo).
- `ask-hr` dùng **kiến thức nền tĩnh** (mức sổ tay onboarding). Thông tin **cá nhân/pháp lý** (lương, hợp đồng, số phép còn lại) → skill sẽ **không bịa** mà chỉ user tới Lark / HR Manager / bot `@hr-agent`.
- `ask-agent` giữ nhẹ: nhúng tài liệu Antigravity (42 file) + tổng quan hệ thống; tài liệu Claude Code đầy đủ được **fetch on-demand** từ web (không nhúng file ~58MB).

---

## 🛠 Cấu trúc plugin (cho người bảo trì)

```
Humaner-Plugin/
├── .claude-plugin/
│   ├── plugin.json          ← Manifest plugin (name: humaner)
│   └── marketplace.json     ← Marketplace (name: humaner-skills) trỏ plugin ở repo root
├── README.md
├── commands/
│   └── huong-dan-cowork.md  ← /humaner:huong-dan-cowork
└── skills/
    ├── ask-agent/
    │   ├── SKILL.md
    │   └── resources/       ← antigravity-docs/, antigravity-guide.md, ai-tools-comparison.md, thehuman-agent-system.md
    ├── ask-hr/
    │   ├── SKILL.md
    │   └── resources/       ← company-overview.md, onboarding-7-ngay.md, faq-hr.md
    └── lark/
        ├── SKILL.md
        └── resources/       ← lark-mcp-setup.md
```

### Thêm / cập nhật skill
1. Tạo thư mục `skills/<ten-skill>/SKILL.md` với frontmatter `name` + `description` (description quyết định khi nào skill tự bật → viết rõ trigger).
2. Resource đi kèm để trong `skills/<ten-skill>/resources/`.
3. **Không** đưa secret/PII (roster, App Secret, ID nội bộ) vào skill — đây là plugin chia sẻ.
4. Bump `version` trong `plugin.json` khi muốn user nhận update ổn định; rồi `git push`.
5. Người dùng cập nhật: `/plugin marketplace update humaner-skills`.

---

## ❓ Hỏi thêm

- Không phải dev → `/huong-dan-cowork`.
- Về hệ thống/công cụ → hỏi `ask-agent`.
- Về công ty/chính sách → hỏi `ask-hr`.
- Thao tác Lark → hỏi `lark`.

*The Human Inc · Wealify — Rev 1.0*
