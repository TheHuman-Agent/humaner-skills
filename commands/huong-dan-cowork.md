---
description: Hướng dẫn người KHÔNG PHẢI DEV cách dùng Cowork (app desktop của Claude Code) — cài plugin Humaner, gọi 3 cửa hỏi-đáp, và làm việc an toàn.
argument-hint: "[câu hỏi cụ thể, vd: cài plugin / gửi lark / nghỉ phép]"
---

Bạn đang hướng dẫn một **người mới, KHÔNG phải lập trình viên** cách dùng **Cowork** (ứng dụng desktop của Claude Code) tại The Human Inc / Wealify. Giọng văn: thân thiện, tiếng Việt, ngắn gọn, từng bước, không thuật ngữ khó. Dùng bảng/emoji vừa phải cho dễ nhìn.

Nếu user có truyền câu hỏi cụ thể trong `$ARGUMENTS` → trả lời thẳng phần liên quan trước, rồi mới tóm tắt phần còn lại. Nếu không có gì → trình bày toàn bộ hướng dẫn theo thứ tự dưới đây.

Trình bày các phần sau (rút gọn cho dễ đọc, đừng dán nguyên si):

## 1. Cowork là gì
- Là **app desktop** để bạn nói chuyện với AI Agent (Claude) làm việc giúp bạn — không cần biết code.
- Bạn chỉ cần: **chọn thư mục làm việc → chọn chế độ → chọn model → gõ yêu cầu bằng tiếng Việt**.

## 2. Màn hình chính (3 nút quan trọng)
| Nút | Là gì | Cho người mới |
|-----|-------|---------------|
| **Thư mục** (góc dưới trái) | Chỗ AI làm việc & lưu file | Chọn đúng folder dự án / agent của bạn |
| **Ask / Code** | Chế độ trả lời | **Ask** = hỏi-đáp, đọc, tư vấn (an toàn). **Code** = cho AI sửa/tạo file |
| **Model** (góc dưới phải) | "Bộ não" AI | Cứ để mặc định / chọn bản mới nhất |

> Mẹo: cứ gõ yêu cầu bằng **tiếng Việt như nhắn tin**. AI tự hiểu.

## 3. Cài plugin Humaner (làm 1 lần)
**Trong Cowork (khuyến nghị):**
1. Mở **Customize** (góc dưới bên trái).
2. Vào **Browse plugins → Personal → +**.
3. Chọn **Add marketplace from GitHub**.
4. Nhập: **`thehuman-agent/humaner-skills`**
5. Chọn plugin **humaner** → **Install**.

**Hoặc bằng lệnh (Claude Code CLI):**
```
/plugin marketplace add thehuman-agent/humaner-skills
/plugin install humaner@humaner-skills
```
Sau khi cài, plugin tự nạp (nếu cần thì gõ `/reload-plugins`).

## 4. 3 cửa hỏi-đáp (tính năng chính của plugin)
Bạn **không cần nhớ lệnh** — cứ hỏi tự nhiên, đúng skill sẽ tự bật. Hoặc gõ `/` để chọn:

| Hỏi về | Cứ hỏi kiểu | Skill bật |
|--------|-------------|-----------|
| Công cụ AI, hệ thống, vault, skill | "Antigravity là gì?", "vault để làm gì?" | `/humaner:ask-agent` |
| Công ty, sản phẩm, chính sách, nghỉ phép | "Wealify làm gì?", "xin WFH thế nào?" | `/humaner:ask-hr` |
| Thao tác Lark: gửi tin, lịch, task, Bitable | "gửi tin cho team...", "đặt lịch họp..." | `/humaner:lark` |

## 5. Làm việc an toàn (NON-DEV nhớ 4 điều)
1. **Mới dùng thì để chế độ Ask** — AI chỉ trả lời, không tự sửa file.
2. **AI hỏi xác nhận** trước khi làm việc quan trọng (gửi tin, xóa, thay đổi) → đọc kỹ rồi mới đồng ý.
3. **Không dán mật khẩu / App Secret / thông tin nhạy cảm** vào chat.
4. **Bí chỗ nào** → hỏi ngay 1 trong 3 cửa, hoặc nhắn buddy/leader.

## 6. Bước tiếp theo gợi ý cho user
Kết thúc bằng 1 câu rủ user thử ngay, ví dụ: *"Thử gõ: «Wealify có những sản phẩm gì?» để xem cửa ask-hr trả lời nhé."*
