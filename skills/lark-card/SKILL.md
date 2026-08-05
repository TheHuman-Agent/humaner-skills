---
name: lark-card
khoi: ai
description: Soạn và gửi thẻ (card) Lark đẹp — có nút bấm ẩn/hiện phần dài, dải thông tin nhiều cột, màu và icon, gửi qua Lark MCP. Kích hoạt khi user muốn gửi thông báo Lark cho đẹp, gửi card message, làm tin nhắn có nút thu gọn / xem thêm, thông báo hàng loạt cho nhiều người, thiết kế lại tin nhắn Lark đang xấu hoặc quá dài, hoặc gọi @lark-card. Dùng kèm skill lark (xác thực, tra open_id, MCP setup).
---

# lark-card — Thẻ Lark đẹp, có nút ẩn/hiện

Tin nhắn Lark dài là tin nhắn không ai đọc. Thẻ giải quyết đúng chuyện đó: **phần
quan trọng hiện sẵn, phần dài gấp lại sau một nút bấm.**

> Skill này lo phần **soạn thẻ**. Phần **xác thực, tra `open_id`, cài Lark MCP**
> nằm ở skill `lark` — đọc nó trước nếu chưa gửi được tin nào.

---

## Nguyên tắc số 1 — mặc định là GẤP

Người nhận mở Lark trên điện thoại. Cái họ thấy đầu tiên phải vừa một màn hình.

- **Hiện sẵn:** họ là ai, việc gì, cần làm gì, hạn khi nào. Tối đa ~5 dòng.
- **Gấp lại:** hướng dẫn từng bước, FAQ, điều khoản, ví dụ, thông tin nhạy cảm.

Mọi `collapsible_panel` phải có **`"expanded": false`**. Bỏ trường này là thẻ mở
toang, và bạn vừa gửi đi một bức tường chữ.

> 🔒 Nội dung nhạy cảm (chìa khoá, mã, số tiền) **luôn** nằm trong panel gấp, kèm
> một dòng nhắc *"đang share màn hình thì đừng mở vội"*. Thẻ Lark hiện trong
> preview thông báo — cái gì không muốn nhảy lên màn hình khoá thì đừng để ngoài.

---

## Khi nào KHÔNG dùng thẻ

| Tình huống | Dùng gì |
|---|---|
| Một câu ngắn, không cần cấu trúc | `msg_type: text` |
| Cần người khác reply vào nội dung | text — thẻ khó quote lại |
| Nội dung > 30 KB | Cắt bớt, hoặc gửi kèm file |

Thẻ cho **thông báo có cấu trúc**. Đừng bọc một câu "họp lúc 3h" vào thẻ.

---

## Bộ khung tối thiểu

```json
{
  "schema": "2.0",
  "config": { "wide_screen_mode": true, "update_multi": true },
  "header": {
    "title":    { "tag": "plain_text", "content": "🔑 Tiêu đề ngắn, có 1 emoji" },
    "subtitle": { "tag": "plain_text", "content": "Tên người · bối cảnh" },
    "template": "turquoise"
  },
  "body": {
    "elements": [
      { "tag": "markdown", "content": "Câu mở đầu nói thẳng việc cần làm." }
    ]
  }
}
```

Ba chỗ hay sai ngay từ khung:

1. **`schema: "2.0"`** — thiếu thì các tag mới (`collapsible_panel`, `standard_icon`) không render.
2. **`body.elements`**, không phải `elements` ở gốc. Đây là khác biệt lớn nhất so với schema 1.0.
3. **`update_multi: true`** — cho phép **sửa lại thẻ đã gửi** mà không phải gửi tin mới. Luôn bật; ngày mai phát hiện viết sai là còn đường lùi.

---

## ⭐ Nút ẩn/hiện — `collapsible_panel`

Đây là thứ bạn tới đây để lấy. Markup dưới đã chạy thật, không phải ví dụ trong tài liệu:

```json
{
  "tag": "collapsible_panel",
  "expanded": false,
  "background_color": "yellow-50",
  "border": { "color": "yellow", "corner_radius": "6px" },
  "vertical_spacing": "8px",
  "padding": "8px 12px 12px 12px",
  "header": {
    "title": { "tag": "markdown", "content": "**🔑 Bấm vào đây để hiện chìa khoá**" },
    "vertical_align": "center",
    "padding": "4px 0px 4px 8px",
    "icon": {
      "tag": "standard_icon",
      "token": "down-small-ccm_outlined",
      "color": "yellow",
      "size": "16px 16px"
    },
    "icon_position": "right",
    "icon_expanded_angle": -180
  },
  "elements": [
    { "tag": "markdown", "content": "*Đang share màn hình thì đừng mở vội nhé.*" },
    { "tag": "markdown", "content": "```\nNỘI DUNG DÀI Ở ĐÂY\n```" }
  ]
}
```

**Đọc kỹ mấy trường này:**

| Trường | Vì sao cần |
|---|---|
| `expanded: false` | Gấp sẵn. **Bỏ là hỏng cả mục đích.** |
| `header.title` | Phải là **câu mời bấm**, không phải nhãn. *"Bấm để xem 3 bước cài"* tốt hơn *"Hướng dẫn"*. |
| `icon_expanded_angle: -180` | Mũi tên xoay khi mở. Thiếu thì mũi tên đứng im, người dùng không biết đã mở hay chưa. |
| `background_color` + `border` | Cho khối nổi khỏi nền. Cùng tông màu (`yellow-50` + `yellow`). |
| `icon_position: "right"` | Mũi tên bên phải giống mọi accordion khác — đừng sáng tạo chỗ này. |

**Đặt tiêu đề panel cho đúng.** Người ta chỉ bấm khi biết bên trong có gì:

- ❌ "Thông tin thêm" · "Chi tiết" · "Ghi chú"
- ✅ "Bấm để xem 3 bước cài (2 phút)" · "Em vào web nó đòi đăng nhập?" · "Lỡ làm mất thì sao?"

Nhiều panel liên tiếp thì **mỗi panel một câu hỏi người dùng thật sự hỏi**. Thẻ
biến thành FAQ gấp gọn — đó là bố cục dễ đọc nhất cho hướng dẫn.

---

## Dải thông tin ngang — `column_set`

Lark **không render bảng markdown**. Cần bảng thì dùng cột:

```json
{
  "tag": "column_set",
  "horizontal_spacing": "8px",
  "columns": [
    {
      "tag": "column", "width": "weighted", "weight": 1,
      "background_style": "grey-50", "padding": "8px", "vertical_spacing": "2px",
      "elements": [ { "tag": "markdown", "content": "**Đội**\nOTC" } ]
    },
    {
      "tag": "column", "width": "weighted", "weight": 1,
      "background_style": "grey-50", "padding": "8px", "vertical_spacing": "2px",
      "elements": [ { "tag": "markdown", "content": "**Cấp đọc**\nNội bộ" } ]
    }
  ]
}
```

**Tối đa 4 cột.** Trên điện thoại 5 cột trở lên là chữ vỡ vụn. Nhiều hơn thì tách
hai `column_set` chồng lên nhau.

Mẫu nội dung mỗi ô: `**Nhãn**\nGiá trị` — nhãn đậm, giá trị xuống dòng.

---

## Bảng tra nhanh

**Màu header (`template`):** `blue` `wathet` `turquoise` `green` `yellow` `orange`
`red` `carmine` `violet` `purple` `indigo` `grey`

Chọn theo **ý nghĩa**, không theo sở thích: `turquoise`/`green` = tin vui, hướng
dẫn · `yellow`/`orange` = cần chú ý · `red`/`carmine` = sự cố, hạn chót · `grey` = báo cáo định kỳ.

**Nền & viền:** `<màu>-50` cho nền nhạt (`yellow-50`, `grey-50`, `blue-50`), tên
màu trơn cho viền.

**Icon hay dùng (`standard_icon.token`):**
`down-small-ccm_outlined` (mũi tên panel) · `warning_outlined` · `done_outlined`
· `time_outlined` · `lock_outlined` · `chat_outlined` · `file_outlined`

**Element cơ bản:** `markdown` · `plain_text` · `hr` (đường kẻ) · `column_set` ·
`collapsible_panel` · `button` · `img`

**Markdown Lark hỗ trợ:** `**đậm**` · `*nghiêng*` · `~~gạch~~` · `` `mã` `` ·
` ```khối mã``` ` · `[chữ](url)` · `<at id=open_id></at>` · xuống dòng bằng `\n`.
**Không** hỗ trợ bảng, tiêu đề `#`, danh sách lồng sâu.

---

## Nút bấm

```json
{
  "tag": "button",
  "text": { "tag": "plain_text", "content": "💬 Nhắn Kiên" },
  "type": "primary",
  "width": "default",
  "behaviors": [ { "type": "open_url", "default_url": "https://..." } ]
}
```

> ⚠️ **Đừng đặt nút trỏ tới trang người nhận không vào được.** Đây là lỗi thật đã
> xảy ra: thẻ phát chìa khoá có nút *"Mở Data-Center"* trỏ vào trang quản trị, nhân
> viên bấm vào gặp form đăng nhập rồi tưởng mình thiếu quyền, đi hỏi vòng vòng.
> Trước khi gắn nút, tự hỏi: **người nhận bấm vào có dùng được không?**

Tối đa **2 nút**. Nhiều hơn là không nút nào được bấm.

---

## Gửi đi

### Qua Lark MCP (đường chính)

```
mcp__lark-openapi__im_v1_message_create
  params: { receive_id_type: "open_id" }
  data: {
    receive_id: "ou_xxx",
    msg_type:   "interactive",
    content:    "<CHUỖI JSON CỦA THẺ>"
  }
```

> 🚨 **Lỗi số 1, ai cũng dính:** `content` phải là **chuỗi**, không phải object.
> Thẻ của bạn là JSON, và nó phải được **serialize lần nữa** thành chuỗi rồi mới
> nhét vào `content`. Truyền object vào là lỗi ngay.

```python
content = json.dumps(card, ensure_ascii=False)   # đúng
content = card                                    # SAI
```

`msg_type` là `"interactive"` — không phải `"card"`.

### Qua REST (khi MCP chưa nạp)

```bash
curl -s -X POST "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TENANT_TOKEN" -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json;print(json.dumps({"receive_id":"ou_xxx","msg_type":"interactive","content":json.dumps(CARD,ensure_ascii=False)}))')"
```

Dựng payload bằng `json.dumps` chứ đừng nối chuỗi tay — tiếng Việt có dấu và ký
tự xuống dòng sẽ phá cú pháp.

### Sửa thẻ ĐÃ gửi

`config.update_multi: true` cho phép cập nhật tại chỗ qua
`PATCH /open-apis/im/v1/messages/{message_id}`. Viết sai thì sửa, **đừng gửi tin
đính chính** — người nhận đọc tin cũ trước.

---

## Gửi hàng loạt

1. **Gửi thử cho chính mình trước.** Luôn luôn. Thẻ render khác hẳn giữa lúc soạn và lúc nhận.
2. **Chạy thử (dry-run) in ra màn hình** toàn bộ danh sách người nhận trước khi bắn.
3. **Giãn ~0.4s mỗi tin.** Bắn song song là dính giới hạn tần suất.
4. **Bắt lỗi từng người**, đừng để một người hỏng làm chết cả vòng lặp.
5. **Lỗi `230013`** = bot chưa được phép nhắn người đó (ngoài phạm vi ứng dụng). Không phải lỗi thẻ — xem skill `lark`.

---

## Bẫy hay gặp

| Triệu chứng | Nguyên nhân |
|---|---|
| API trả OK nhưng thẻ hiện trống | `elements` đặt ở gốc thay vì trong `body` |
| Tag `collapsible_panel` không nhận | Thiếu `"schema": "2.0"` |
| Panel mở toang khi vừa nhận | Quên `"expanded": false` |
| Lỗi parse `content` | Truyền object thay vì chuỗi JSON |
| Xuống dòng thành chữ `\n` | Escape hai lần — để `json.dumps` lo, đừng tự thay |
| Bảng markdown ra một cục | Lark không có bảng, phải dùng `column_set` |
| Chữ vỡ trên điện thoại | Quá 4 cột trong một `column_set` |
| `400` khi gửi | Thẻ vượt 30 KB |
| Mũi tên panel không xoay | Thiếu `icon_expanded_angle: -180` |

---

## Checklist trước khi bấm gửi

- [ ] Đã gửi thử cho chính mình và **mở trên điện thoại**?
- [ ] Mọi panel dài đều `expanded: false`?
- [ ] Tiêu đề panel là **câu mời bấm**, không phải nhãn chung chung?
- [ ] Nội dung nhạy cảm nằm trong panel gấp?
- [ ] Nút bấm trỏ tới chỗ người nhận **thật sự vào được**?
- [ ] `content` đã `json.dumps` thành chuỗi?
- [ ] `update_multi: true` để còn đường sửa?
- [ ] Màn hình đầu tiên đọc xong trong 10 giây?

---

## Mẫu dùng ngay

`resources/mau-the-thong-bao.json` — thẻ thông báo hoàn chỉnh: header màu, câu mở
đầu, dải 3 cột, 3 panel gấp, 1 nút. Thay chỗ `{{...}}` là gửi được.

Cách dùng: đọc file, `json.dumps`, thay placeholder, gửi. **Đừng viết thẻ từ số
không** — sửa mẫu nhanh hơn và ít lỗi hơn nhiều.
