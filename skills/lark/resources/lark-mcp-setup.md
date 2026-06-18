# Lark MCP — Hướng dẫn cài

Cài Lark MCP server chính thức để Cowork/Claude Code gọi Lark API qua MCP tools thay vì curl thủ công.

> 🔒 Mọi App ID/Secret/ID ở đây là **placeholder** — thay bằng giá trị thật của bạn và **đọc từ env file private** (mode 600, ngoài repo). Không hardcode, không commit secret.

---

## 1. Verify đã có chưa

```bash
claude mcp list 2>&1 | grep lark-mcp
```

- Có `lark-mcp: ... ✓ Connected` → bỏ qua, sang phần "Sau khi cài".
- Không có → tiếp bước 2.

## 2. Lệnh cài (user scope)

```bash
source ~/.config/agent-cron/env   # nạp $LARK_APP_ID, $LARK_APP_SECRET (đặt tên tuỳ app của bạn)
claude mcp add lark-mcp --scope user -- npx -y @larksuiteoapi/lark-mcp mcp \
  -a "$LARK_APP_ID" \
  -s "$LARK_APP_SECRET" \
  -d https://open.larksuite.com \
  -t preset.base.default,preset.im.default,preset.calendar.default,preset.task.default
```

| Flag | Ý nghĩa |
|------|---------|
| `--scope user` | Chỉ user hiện tại dùng (không commit vào repo) |
| `-a` / `-s` | App ID / Secret — đọc từ env, KHÔNG hardcode |
| `-d` | Domain: `https://open.larksuite.com` (Lark SG/Global — KHÔNG dùng `feishu.cn` nếu workspace ở SG) |
| `-t` | 4 nhóm tool: Bitable + Message + Calendar + Task |

Token mode mặc định = `tenant_access_token` (bot identity), không cần OAuth user.

## 3. Verify & restart

```bash
claude mcp list 2>&1 | grep lark-mcp
# mong đợi: lark-mcp: npx ... - ✓ Connected
```

MCP tools chỉ load ở session mới → `/exit` rồi mở lại Cowork/Claude Code. Sau restart có:

| Nhóm | Tool prefix |
|------|-------------|
| Bitable | `mcp__lark-mcp__bitable.v1.*` |
| Message | `mcp__lark-mcp__im.v1.*` |
| Calendar | `mcp__lark-mcp__calendar.v4.*` |
| Task | `mcp__lark-mcp__task.v2.*` |

## 4. Sau khi cài — share resource với bot

Bot dùng `tenant_access_token` → KHÔNG tự thấy Larkbase/Calendar/Doc cá nhân. Phải share thủ công:

| Resource | Cách share |
|----------|-----------|
| **Larkbase (Bitable)** | Mở Base → Share → search tên app của bạn → add role Editor/Viewer |
| **Calendar** | Grant ACL qua `POST /calendar/v4/calendars/{cal_id}/acls`; người dùng subscribe calendar_id tương ứng |
| **Doc/Sheet/Drive** | `POST /drive/v1/permissions/{file_token}/members` với `member_type=openid`, `member_id={bot_open_id}` |
| **Chat group** | Add bot vào group như add member |

## 5. Troubleshooting

- **`✗ Failed` sau cài:** test token còn live? `POST /open-apis/auth/v3/tenant_access_token/internal`. Nếu `code != 0` → App Secret đã reset → lấy secret mới ở Lark Developer Console → `claude mcp remove lark-mcp` rồi add lại.
- **`permission denied` khi gọi tool:** app thiếu scope → Lark Console → app → Permissions → add scope → **Publish version mới**.
- **Không tìm thấy user/email:** thiếu scope `contact:user.base:readonly`. Workaround: lookup open_id qua `GET /im/v1/chats/{chat_id}/members` của group bot là member.

## 6. Giới hạn đã biết

Lark MCP **KHÔNG hỗ trợ:** upload/download file (dùng REST `POST /drive/v1/medias/upload_all`); edit cloud docs trực tiếp (chỉ read/import); một số non-preset API không ổn định với AI calls. Các case này → fallback REST API curl với `tenant_access_token`.

## 7. Reference

- npm: https://www.npmjs.com/package/@larksuiteoapi/lark-mcp
- GitHub: https://github.com/larksuite/lark-openapi-mcp
- Docs MCP: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/mcp_integration/mcp_introduction
- Tool presets: https://github.com/larksuite/lark-openapi-mcp/blob/main/docs/reference/tool-presets/presets.md
