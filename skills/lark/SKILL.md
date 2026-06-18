---
name: lark
description: Thao tác Lark / Feishu — gửi message, tạo task, tạo calendar event, CRUD Larkbase (Bitable) records, query data, upload file Drive. Tự cài / verify Lark MCP server (@larksuiteoapi/lark-mcp) nếu chưa có. Kích hoạt khi user muốn thông báo team, gửi update Lark, tạo lịch họp, tạo / sửa / query Larkbase, Bitable, base record, hoặc gọi @lark / /lark.
---

# lark — Cửa thao tác Lark / Feishu

Dùng Lark API để gửi message, tạo task, tạo calendar event, query thông tin, CRUD Larkbase (Bitable).

> **1 trong 3 "cửa hỏi-đáp":** `ask-agent` (hệ thống & công cụ) · `ask-hr` (công ty & chính sách) · **`lark` (thao tác app Lark)**.
>
> 🔒 **Bản đóng gói này KHÔNG chứa dữ liệu thật** (không roster nhân sự, không App ID/Secret, không Calendar/Group ID nội bộ). Mọi ID/email/secret ở dưới là **placeholder** — thay bằng giá trị thật của workspace bạn, và **luôn đọc từ env / nguồn riêng**, không hardcode vào repo.

---

## ⚡ Pre-flight — kiểm tra Lark MCP (chạy đầu mỗi lần invoke)

Trước khi gọi bất kỳ Lark API nào, chạy check:

```bash
claude mcp list 2>&1 | grep lark-mcp
```

- **`lark-mcp: ... ✓ Connected`** → dùng MCP tools (`mcp__lark-mcp__*`) làm đường chính. Bỏ qua xuống "Lệnh hỗ trợ".
- **Không có dòng nào / `✗ Failed`** → MCP chưa cài hoặc lỗi. **Đọc `resources/lark-mcp-setup.md` và làm theo**, rồi bảo user `/exit` restart Claude Code/Cowork và quay lại.
- **Vừa cài trong session, chưa restart** → fallback dùng REST API curl với credentials env (xem dưới), đồng thời nhắc user restart để load tool.

## Credentials — KHÔNG hardcode

> 🔐 Lưu App ID/Secret trong **env file private ngoài repo** (mode 600), ví dụ `~/.config/agent-cron/env`. Source trước khi gọi API:

```bash
source ~/.config/agent-cron/env
# dùng biến: $LARK_APP_ID, $LARK_APP_SECRET   (đặt tên tuỳ app của bạn)
# Domain Lark SG: https://open.larksuite.com   (KHÔNG dùng feishu.cn nếu workspace ở SG/Global)
```

Lấy `tenant_access_token`:

```bash
curl -s -X POST "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$LARK_APP_ID\",\"app_secret\":\"$LARK_APP_SECRET\"}"
# → { "tenant_access_token": "t-..." }
```

---

## Lệnh hỗ trợ (cú pháp gọi tự nhiên)

```
gửi "{nội dung}" tới {tên người / group chat}
tạo task "{tiêu đề}" giao cho {người} deadline {ngày}
tạo lịch "{tiêu đề}" ngày {YYYY-MM-DD} {HH:MM}-{HH:MM} mời {người/email}
tìm chat/doc "{keyword}"
query / thêm / sửa record Bitable {tên bảng}
```

## Tra cứu người nhận (open_id / email) — không bịa

Để DM / mời họp / tag user cần `open_id` (hoặc email). **Quy ước an toàn:**

1. **Ưu tiên roster riêng của workspace** nếu có (file JSON map `tên ↔ open_id ↔ email ↔ employee_no`). *(Bản plugin này không kèm roster — bạn tự duy trì trong workspace.)*
2. Không có roster → lookup bằng email qua Contact API:
   ```bash
   curl -s -X POST "https://open.larksuite.com/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id" \
     -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
     -d '{"emails":["nguoinhan@example.com"]}'
   # → data.user_list[].user_id chính là open_id
   ```
3. **Vẫn không có → HỎI user**, đừng đoán email/ID.

> ⚠️ **`open_id` khác nhau giữa các Lark App.** DM bằng open_id sai-scope → HTTP 400. Luôn dùng open_id thuộc scope của chính app/bot đang chạy.

---

## ⚠️ Guards — không tái phạm

### 1. Message: chọn format theo độ dài — KHÔNG spam nhiều tin

| Độ dài / cấu trúc | Format | Ghi chú |
|---|---|---|
| **≤ 280 chars** (~50 từ, 2-3 dòng mobile) | `msg_type=text` plain | Đọc 1 nhịp, không cần scroll |
| **280–800 chars** HOẶC có structure (bullet, link, status, CTA) | `msg_type=interactive` (Lark card) | Header + 1-2 div + button. Gọn, không nhồi nhét |
| **> 800 chars** HOẶC > 150 từ HOẶC nhiều section | Upload `.md` lên Drive → gửi **1 card** chứa link | Không dump report dài vào text/card |

**Cấm:** gửi 3+ tin text liên tiếp cùng chủ đề; paste nguyên report/log dài vào plain text; dùng card cho 1 câu ngắn (overkill). Mẹo: đếm `len(text)` trước khi gửi.

Flow khi nội dung dài (> 5 dòng): tạo file `.md` → `POST /im/v1/files` (multipart, `file_type=stream`) lấy `file_key` → gửi `msg_type=file`. Hoặc upload Drive (`POST /drive/v1/files/upload_all`, `parent_type=explorer`) rồi gửi card chứa link, nhớ cấp `perm=view` cho người nhận.

### 2. Calendar timestamp: luôn dùng `datetime`, verify năm

```python
import datetime
dt = datetime.datetime(2026, 3, 26, 15, 0, 0,
        tzinfo=datetime.timezone(datetime.timedelta(hours=7)))  # ICT (UTC+7)
ts = int(dt.timestamp())
print(datetime.datetime.fromtimestamp(ts))  # verify năm đúng trước khi dùng
# ❌ KHÔNG hardcode số epoch (dễ ra sai năm)
```

### 3. Lịch lặp (recurring): field là `recurrence`, KHÔNG phải `rrule`

- Lark Calendar V4 dùng `"recurrence"` (string RRULE), vd `"FREQ=MONTHLY;BYMONTHDAY=6"`.
- ⚠️ Gửi nhầm `rrule` → API trả `code:0` (OK) nhưng **âm thầm bỏ qua**, lịch KHÔNG lặp. **Luôn GET lại event verify `recurrence` khác rỗng.**

### 4. Email/ID người nhận: chỉ dùng nguồn xác thực

- Lấy từ roster workspace hoặc Contact API. Dùng field **`enterprise_email`** (field `email` thường rỗng).
- Không có nguồn → hỏi user. KHÔNG bịa email kiểu `ten@congty.com`.

### 5. Lỗi 230013 — Bot has no availability to this user

App chưa bật "All Employees" trong Lark Developer Console. Fix (1 lần, do Admin): Permissions & Scopes → Data Scope → **All Employees**; Version Management & Release → Availability → **All Employees** → publish. Workaround tạm: gửi vào group chat có người đó rồi tag `@tên`.

---

## Quy trình tạo Calendar Event

1. **Parse**: tiêu đề, ngày giờ, múi giờ ICT (UTC+7), người dự.
2. **Timestamp đúng** (Guard #2), verify năm.
3. **Check slot trống** (nếu không chỉ định giờ): `GET /calendar/v4/calendars/{CAL_ID}/events?start_time=...&end_time=...`.
4. **Tìm email người dự** (roster / Contact API). Không có → hỏi.
5. **Tạo event**: `POST /calendar/v4/calendars/{CAL_ID}/events` (dùng calendar ID đích đã định, KHÔNG dùng `primary` nếu primary là lịch bot).
6. **Add attendees**: Lark user → `type:"user"` + `user_id_type=open_id`; email ngoài → `type:"third_party"` + `third_party_email`.
7. **Cấp quyền file đính kèm** (nếu có): `POST /drive/v1/permissions/{file_token}/members` với `member_type=openid`, `perm=view`.
8. **Confirm**: báo kết quả + event ID + giờ thực tế.

## Quy trình gửi Message

1. **Preview** & xác nhận với user trước khi gửi.
2. **Chọn format theo độ dài** (Guard #1).
3. **Reply Guard**: nếu là reply ai đó, GET list message, check `create_time` để chỉ reply **tin mới nhất** đúng người.
4. Get `tenant_access_token` → execute (1 lần gửi) → confirm.

---

## Resources

- `resources/lark-mcp-setup.md` — Hướng dẫn cài Lark MCP server (`@larksuiteoapi/lark-mcp`), grant scope, troubleshooting.

Spec API chi tiết (IM, Contact, Bitable, Calendar, Task, Docs, Cards, Approval...) → tra trực tiếp tại **https://open.larksuite.com/document/server-docs**.
