#!/usr/bin/env python3
"""gui_lark.py — gửi tin Lark theo EMAIL công ty, không sót người.

Vì sao cần file này: `receive_id_type="email"` chỉ ăn trường `email` của Lark,
mà email công ty ai cũng biết lại nằm ở `enterprise_email` — gửi thẳng là 400.
Tệ hơn, `batch_get_id` với `enterprise_email` trả `code: 0` "success" nhưng
danh sách RỖNG, nên vòng gửi chạy êm rồi báo xong trong khi không ai nhận được.

Module này giải quyết đúng chỗ đó: quét danh bạ một lần, dựng bảng tra từ CẢ HAI
trường email + mã nhân viên + số điện thoại, rồi gửi bằng `open_id`.

Dùng:
    from gui_lark import Lark
    lark = Lark(app_id, app_secret)
    kq = lark.gui_hang_loat(["a@ct.com", "b@ct.com"], card_dict)
    print(kq["truot"])          # ⬅ LUÔN kiểm cái này trước khi báo "đã gửi xong"

Chạy thử:  python3 gui_lark.py --thu you@congty.com
"""
from __future__ import annotations

import json
import sys
import time
import unicodedata
import urllib.error
import urllib.request

BASE = "https://open.larksuite.com"


def _bo_dau(s: str) -> str:
    s = (s or "").replace("đ", "d").replace("Đ", "D")
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if not unicodedata.combining(c)).lower().strip()


class Lark:
    def __init__(self, app_id: str, app_secret: str):
        self._id, self._secret = app_id, app_secret
        self._token: str | None = None
        self._danh_ba: dict[str, dict] | None = None

    # ── hạ tầng ──────────────────────────────────────────────────────────
    def _call(self, path: str, body=None, method="GET") -> dict:
        h = {"Content-Type": "application/json"}
        if self._token:
            h["Authorization"] = "Bearer " + self._token
        req = urllib.request.Request(
            BASE + path, method=method,
            data=json.dumps(body).encode() if body is not None else None, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode())

    def token(self) -> str:
        if not self._token:
            r = self._call("/open-apis/auth/v3/tenant_access_token/internal",
                           {"app_id": self._id, "app_secret": self._secret}, "POST")
            if r.get("code"):
                raise RuntimeError(f"Lấy token hỏng: {r}")
            self._token = r["tenant_access_token"]
        return self._token

    # ── quét danh bạ ─────────────────────────────────────────────────────
    def danh_ba(self, lam_lai=False) -> dict[str, dict]:
        """open_id -> user. Quét CẢ người chưa gán phòng ban."""
        if self._danh_ba is not None and not lam_lai:
            return self._danh_ba
        self.token()
        phong = ["0"]                      # ⬅ "0" = người chưa gán phòng. ĐỪNG BỎ.
        tok = None
        while True:
            q = "/open-apis/contact/v3/departments/0/children?fetch_child=true&page_size=50"
            if tok:
                q += "&page_token=" + tok
            d = self._call(q).get("data", {})
            phong += [x["open_department_id"] for x in d.get("items", [])]
            tok = d.get("page_token")
            if not d.get("has_more"):
                break

        seen: dict[str, dict] = {}
        for p in phong:
            tok = None
            while True:
                q = f"/open-apis/contact/v3/users?department_id={p}&page_size=50"
                if tok:
                    q += "&page_token=" + tok
                d = self._call(q).get("data", {})
                for u in d.get("items", []):
                    seen[u["open_id"]] = u
                tok = d.get("page_token")
                if not d.get("has_more"):
                    break
        self._danh_ba = seen
        return seen

    def bang_tra(self) -> dict[str, str]:
        """Mọi khoá tra được → open_id. Gộp cả 2 trường email, mã NV, SĐT, tên."""
        b: dict[str, str] = {}
        for oid, u in self.danh_ba().items():
            for k in (u.get("enterprise_email"), u.get("email"),
                      u.get("employee_no"), u.get("mobile")):
                if k:
                    b[str(k).strip().lower()] = oid
            if u.get("name"):
                b.setdefault(_bo_dau(u["name"]), oid)
        return b

    def tra(self, khoas: list[str]) -> tuple[dict[str, str], list[str]]:
        """→ ({khoá: open_id}, [khoá không tra được]). KHÔNG nuốt cái trượt."""
        b = self.bang_tra()
        ra, truot = {}, []
        for k in khoas:
            oid = b.get(str(k).strip().lower()) or b.get(_bo_dau(str(k)))
            (ra.setdefault(k, oid) if oid else truot.append(k))
        return ra, truot

    # ── gửi ──────────────────────────────────────────────────────────────
    def gui(self, open_id: str, noi_dung, msg_type="interactive") -> dict:
        self.token()
        return self._call(
            "/open-apis/im/v1/messages?receive_id_type=open_id",
            {"receive_id": open_id, "msg_type": msg_type,
             "content": json.dumps(noi_dung, ensure_ascii=False)
                        if isinstance(noi_dung, dict) else noi_dung}, "POST")

    def gui_hang_loat(self, khoas: list[str], card: dict, *, that=False,
                      nghi=0.4) -> dict:
        """Mặc định CHẠY THỬ. Phải truyền that=True mới gửi thật."""
        ra, truot = self.tra(khoas)
        dat, loi = [], []
        for k, oid in ra.items():
            ten = self.danh_ba()[oid].get("name", "?")
            if not that:
                dat.append((k, ten, "(chạy thử)"))
                continue
            r = self.gui(oid, card)
            if r.get("code"):
                loi.append((k, ten, r.get("msg")))
            else:
                dat.append((k, ten, r["data"]["message_id"]))
            time.sleep(nghi)
        return {"dat": dat, "loi": loi, "truot": truot,
                "tom_tat": f"{len(dat)} đạt · {len(loi)} lỗi · {len(truot)} không tra được"}


if __name__ == "__main__":
    import os
    import re
    env = {}
    p = os.path.expanduser("~/.config/lark/env")
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r'(?:export\s+)?([A-Z_]+)=["\']?([^"\'\n]+)', line)
            if m:
                env[m.group(1)] = m.group(2)
    lark = Lark(env.get("LARK_APP_ID") or env.get("APP_ID"),
                env.get("LARK_APP_SECRET") or env.get("APP_SECRET"))
    if "--thu" in sys.argv:
        who = sys.argv[sys.argv.index("--thu") + 1]
        card = {"schema": "2.0", "config": {"wide_screen_mode": True, "update_multi": True},
                "header": {"title": {"tag": "plain_text", "content": "✉️ gui_lark.py chạy được"},
                           "template": "green"},
                "body": {"elements": [{"tag": "markdown",
                         "content": "Tra từ **email công ty** → `open_id` → gửi. Không dùng `receive_id_type=email`."}]}}
        print(lark.gui_hang_loat([who], card, that=True))
    else:
        db = lark.danh_ba()
        print(f"danh bạ: {len(db)} người")
        co = sum(1 for u in db.values() if u.get("email"))
        print(f"  có trường `email` (gửi thẳng bằng email được): {co}/{len(db)}")
        print(f"  có `enterprise_email` (KHÔNG gửi thẳng được):  "
              f"{sum(1 for u in db.values() if u.get('enterprise_email'))}/{len(db)}")
