# Hệ thống Agent của công ty

Tài liệu này giải thích toàn bộ cấu trúc hệ thống AI Agent tại công ty — dành cho người mới muốn hiểu "bức tranh lớn".

---

## 1. Tại sao có hệ thống Agent?

Mỗi team (Finance, HR, BD, Product...) có **một AI Agent riêng** — đóng vai trò như một chuyên gia AI cho team đó. Thay vì chat ngẫu hứng với AI, agent được "lập trình" trước bằng:
- **Skills**: Kỹ năng chuyên biệt (phân tích tài chính, phỏng vấn ứng viên...)
- **Rules**: Quy tắc luôn áp dụng (bảo mật, định dạng output...)
- **Vaults**: Kho dữ liệu kiến thức của team

Và tất cả được kết nối qua một **hub trung tâm** là `Humaner-Agent`.

---

## 2. Cấu trúc tổng thể

```
{workspace-root}/          ← Monorepo (tên folder tuỳ bạn đặt, VD: TheHumanTeam)
│
├── Humaner-Agent/           ← HUB TRUNG TÂM
│   ├── ONBOARDING.md        ← Đọc đầu tiên khi onboard
│   ├── shared/              ← Data tổng hợp (tự động sync)
│   │   ├── finance/         ← Từ Finance-Agent
│   │   ├── hr/              ← Từ HR-Agent  
│   │   ├── product/         ← Từ Product Agent
│   │   ├── bd/              ← Từ BD-Agent
│   │   └── compliance/      ← Từ Compliance Agent
│   └── .agent/skills/
│       ├── agent-builder/   ← Tạo agent mới
│       └── AskAgent/        ← File này
│
├── Finance-Agent/           ← Agent của Finance team
├── HR-Agent/                ← Agent của HR team
├── {Product-Agent}/         ← Agent của Product team
├── BD-Agent/                ← Agent của BD/Sales team
└── {Compliance-Agent}/      ← Agent của Compliance team
```

---

## 3. Vault — Kho kiến thức 4 tầng

Mỗi Agent có cấu trúc vault chuẩn. **Luôn đọc vault-1-core trước**.

| Vault | Tên | Nội dung | Ai sửa? |
|-------|-----|---------|---------|
| `vault-1-core/` | Constitution | Mục tiêu team, glossary, rules cứng | Team lead khi onboard |
| `vault-2-live/` | Live State | Sprint hiện tại, data sync | Agent cập nhật thường xuyên |
| `vault-3-standards/` | Standards | SOPs, playbooks, specs | Team lead theo sprint |
| `vault-4-strategy/` | Strategy | Roadmap, OKR dài hạn | Leadership theo quarter |

### Rule quan trọng nhất về vault

```
vault-2-live/data/ → shared/{team}/
```

**Chỉ** files trong `vault-2-live/data/` mới được sync ra `shared/`. Đây là "cửa sổ" mà team chia sẻ data với công ty.

---

## 4. Shared Data — Trung tâm dữ liệu chung

`shared/` trong Humaner-Agent là nơi **tất cả teams chia sẻ data** với nhau.

**Cách hoạt động:**

```
[Finance-Agent]           [HR-Agent]           [BD-Agent]
vault-2-live/data/    vault-2-live/data/    vault-2-live/data/
       ↓                      ↓                     ↓
       └──────────────────────┴─────────────────────┘
                    GitHub Actions (00:00 daily)
                              ↓
              Humaner-Agent/shared/
              ├── finance/fee-structure.md
              ├── hr/org-chart.md
              └── bd/customer-insights.md
```

**Ai đọc shared/?**
- Nhân viên mới đọc `shared/hr/` để biết về tổ chức
- Finance đọc `shared/product/` để biết roadmap khi định giá
- BD đọc `shared/finance/` để biết fee structure khi báo giá

**Lưu ý:** Không sửa file trong `shared/` thủ công — sẽ bị ghi đè bởi sync tiếp theo.

---

## 5. Sync tự động — Cách hoạt động

File: `Humaner-Agent/.github/workflows/sync.yml`

- Chạy **hàng ngày lúc 00:00** (UTC+7)
- Clone mỗi agent repo
- Copy files từ `vault-2-live/data/` → `shared/{team}/`
- Commit tự động vào Humaner-Agent

**Để thêm file sync mới:** Sửa `sync-config.md` và `.github/workflows/sync.yml`

---

## 6. Tạo Agent mới cho team

```
@agent-builder create {Team}-Agent
```

Agent sẽ hỏi bạn 3 câu:
1. Tên team và mục tiêu?
2. Loại team: Squad / Chapter / Back-office?
3. Team muốn share data gì ra `shared/`?

Sau đó tự động tạo full cấu trúc và cập nhật `sync-config.md`.

---

## 7. Câu hỏi thường gặp

**"Tôi cần xem data của Finance thì xem ở đâu?"**
→ `Humaner-Agent/shared/finance/`

**"Tại sao file của tôi trong shared/ bị mất?"**
→ Sync tự động đã ghi đè. Luôn sửa trong `vault-2-live/data/` của agent gốc.

**"Ai có quyền sửa vault-1-core?"**
→ Team lead — đây là "constitution" bất biến của team.

**"Sync chưa chạy, tôi muốn update shared/ ngay?"**
→ Vào GitHub Actions → `sync.yml` → "Run workflow" để chạy thủ công.
