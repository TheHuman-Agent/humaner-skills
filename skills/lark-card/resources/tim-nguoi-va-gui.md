# Gửi cho ai — tìm người không sót

Mọi số liệu dưới **đo thật** trên workspace The Human Inc ngày 05/08/2026, không
phải chép tài liệu.

---

## ⛔ Đọc cái này trước: email công ty ≠ email Lark

Lark có **hai** trường email và chúng khác nhau:

| Trường | Có ở | Tra được người? |
|---|---|---|
| `email` | **12/43** | ✅ có |
| `enterprise_email` | **43/43** | ❌ **KHÔNG** |
| `mobile` | **43/43** | ✅ có |

Cái ai cũng biết (`kiennt@thehumaninc.com`) nằm ở **`enterprise_email`** — và Lark
**không tra được bằng trường đó**.

Hậu quả đo thật:

- `receive_id_type=email` gửi cho `kiennt@thehumaninc.com` → **HTTP 400**, không gửi được
- `batch_get_id` với `enterprise_email` → **trả `code: 0` "success" nhưng danh sách rỗng**

Cái thứ hai mới nguy: **báo thành công mà không ra ai.** Vòng lặp gửi hàng loạt
sẽ chạy êm ru, cuối cùng in "đã gửi xong", trong khi 31/43 người không nhận được gì.

---

## Đường gửi nên dùng

**1. Có sẵn `open_id`** → tốt nhất, dùng luôn.

```
params: { receive_id_type: "open_id" }
data:   { receive_id: "ou_xxx", msg_type: "interactive", content: "<CHUỖI JSON>" }
```

**2. Chỉ có email công ty** → **đừng** gửi thẳng bằng email. Tra `open_id` trước
(mục dưới), rồi gửi bằng `open_id`.

**3. `receive_id_type: "email"`** chỉ dùng khi **chắc chắn** người đó có trường
`email` trong Lark. Với workspace này là 12/43 người. Không chắc thì đừng dùng.

---

## Tra `open_id` — thứ tự ưu tiên

### Cách 1 — quét danh bạ rồi tự ghép (đáng tin nhất)

```python
seen = {}                                    # open_id -> user, tự khử trùng
deps = get("/contact/v3/departments/0/children?fetch_child=true&page_size=50")
for d in deps + [{"open_department_id": "0"}]:     # ⬅ ĐỪNG QUÊN "0"
    tok = None
    while True:                                     # ⬅ ĐỪNG QUÊN PHÂN TRANG
        q = f"/contact/v3/users?department_id={d['open_department_id']}&page_size=50"
        if tok: q += "&page_token=" + tok
        r = get(q)
        for u in r["items"]: seen[u["open_id"]] = u
        tok = r.get("page_token")
        if not r.get("has_more"): break

def khoa(u):                                  # ghép bằng CẢ HAI trường email
    return (u.get("enterprise_email") or u.get("email") or "").strip().lower()
```

**Hai chỗ sót người, cả hai đều đã cắn thật:**

- **Người chưa gán phòng ban.** Duyệt cây ra 43. Gọi thêm `department_id=0` ra
  1 người nữa không nằm trong phòng nào (người mới, cộng tác viên, người sắp
  nghỉ hay rơi vào đây). Tổng thật **44**.
- **Phân trang.** `has_more: true` mà không đi tiếp `page_token` là mất cả trang.
  Áp dụng cho **cả** danh sách phòng ban **lẫn** danh sách người.

### Cách 2 — `batch_get_id`

`POST /open-apis/contact/v3/users/batch_get_id?user_id_type=open_id`

- `{"emails": [...]}` → chỉ ăn trường `email` (12/43)
- `{"mobiles": [...]}` → ăn `mobile` (**43/43**, phủ tốt nhất)

> 🚨 Không khớp thì trả về phần tử **thiếu `user_id`** chứ **không báo lỗi**, và
> `code` vẫn là `0`. **Bắt buộc** đếm lại: gửi đi bao nhiêu, ra bao nhiêu ID, ai
> không tra được — in tên ra, đừng nuốt.

### Cách 3 — ghép bằng mã nhân viên hoặc tên

`employee_no` có ở **39/43**. Hết cách thì ghép theo **tên bỏ dấu + hạ chữ
thường**, nhưng **phải bắt người xác nhận** — ghép nhầm tên là gửi nhầm người.

---

## Đối chiếu trước khi bắn

Trước mỗi lượt gửi hàng loạt:

1. Số người tra được **phải khớp** danh sách gốc (HR, bảng lương). Lệch một người
   cũng phải truy ra tên.
2. In danh sách người nhận ra màn hình, **chạy thử không gửi** trước.
3. Gửi thử cho chính mình một bản.

Sau khi gửi:

- Bắt lỗi **từng người**, đừng để một người hỏng làm chết cả vòng lặp
- Cuối vòng in rõ **ai chưa nhận được**
- **Đừng báo "đã gửi xong" khi còn người trượt**

Lỗi `230013` = bot chưa được phép nhắn người đó (ngoài phạm vi ứng dụng). Không
phải lỗi email, không phải lỗi thẻ — admin phải mở phạm vi trong Lark Admin.
