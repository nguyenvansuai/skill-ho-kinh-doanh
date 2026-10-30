# Skill AI cho Hộ kinh doanh (Việt Nam 2026)

Bộ skill giúp Claude (và ChatGPT) hỗ trợ **chủ hộ kinh doanh, tiểu thương** làm việc sổ sách và thuế **theo quy định năm 2026**: ghi sổ doanh thu S1a/S2a-HKD theo Thông tư 152/2025/TT-BTC, đối soát sao kê với doanh thu sàn, so mốc **1 tỷ đồng** (Nghị định 141/2026/NĐ-CP), hỏi đáp thuế có dẫn nguồn văn bản, kiểm tra hóa đơn điện tử.

Mọi skill tuân theo cùng nguyên tắc: **không bịa, không đoán số** (chữ mờ thì đánh dấu `[?]`), tính toán bằng code, viện dẫn pháp luật luôn kèm số hiệu văn bản và lưu ý kiểm tra văn bản hiện hành, **không tự khai, nộp, ký thay**.

> Quà tặng từ chương trình **Chuyên đề Thuế HKD 2026 · MBV Tây Sài Gòn** – Sự AI (suai.vn).

## Tải nhanh – không cần cài

| File | Dùng để |
|---|---|
| [`qua-tang/10_cau_lenh_AI_cho_Ho_kinh_doanh.pdf`](qua-tang/10_cau_lenh_AI_cho_Ho_kinh_doanh.pdf) | 10 câu lệnh sao chép dán vào ChatGPT, Gemini, Claude, NotebookLM |
| [`qua-tang/So_doanh_thu_HKD_S1a_S2a.xlsx`](qua-tang/So_doanh_thu_HKD_S1a_S2a.xlsx) | Sổ doanh thu S1a-HKD, S2a-HKD có tổng hợp theo tháng, quý, mốc 1 tỷ và 3 tỷ |
| [`van-ban/`](van-ban/) | Văn bản pháp luật gốc để tải lên NotebookLM làm nguồn |

Trên điện thoại: bấm vào tên file → nút **Download** (biểu tượng tải xuống) góc phải.

## Danh sách skill

| # | Skill | Lệnh | Làm gì |
|---|---|---|---|
| 01 | Ghi sổ doanh thu | `/ghi-so-hkd` | Ảnh sổ tay, hóa đơn → sổ S1a/S2a-HKD; đánh dấu `[?]` chỗ mờ; xuất Excel có công thức |
| 02 | Đối soát doanh thu | `/doi-soat-doanh-thu` | Sao kê + báo cáo sàn → tách tiền bán hàng, nội bộ, vay; cộng theo quý; so mốc 1 tỷ, 3 tỷ |
| 03 | Hỏi đáp thuế | `/hoi-dap-thue-hkd` | Trả lời có dẫn nguồn; đọc thông báo thuế; soạn câu hỏi cho cán bộ thuế; checklist theo quý |
| 04 | Kiểm tra hóa đơn | `/kiem-tra-hoa-don` | Kiểm tra trước khi xuất hóa đơn; bảng chi phí từ hóa đơn mua vào; ngưỡng hóa đơn điện tử |

## Cài đặt

### Claude.ai (web / app) – dễ nhất

1. Bật **Settings → Capabilities → Code execution and file creation**.
2. Vào **Settings → Capabilities → Skills → Upload skill**.
3. Tải lên từng file trong thư mục [`dist/`](dist/) (ví dụ `dist/ghi-so-hkd.zip`).

Sau đó cứ nói tự nhiên: "ghi sổ giúp tôi từ ảnh này", "doanh thu tôi đã vượt 1 tỷ chưa", Claude tự chọn skill.

### Claude Code – cài qua plugin marketplace

Bước 1 làm một lần:

```
/plugin marketplace add nguyenvansuai/skill-ho-kinh-doanh
```

Bước 2: cài skill cần dùng, ví dụ:

```
/plugin install ghi-so-hkd@skill-ho-kinh-doanh
```

Hoặc cài cả bộ:

```
/plugin install tron-bo-skill-hkd@skill-ho-kinh-doanh
```

Tên để cài chính là cột **Lệnh** trong bảng trên (bỏ dấu `/`). Cập nhật bản mới: `/plugin marketplace update skill-ho-kinh-doanh`.

### Claude Code – chép thủ công

```bash
git clone https://github.com/nguyenvansuai/skill-ho-kinh-doanh.git
mkdir -p ~/.claude/skills && cp -r skill-ho-kinh-doanh/skills/* ~/.claude/skills/
```

### ChatGPT

Mỗi skill có một file hướng dẫn trong [`chatgpt/`](chatgpt/): tạo Custom GPT (hoặc Project), dán phần **Instructions**, tải các file `references/` lên mục **Knowledge**.

### NotebookLM (trợ lý thuế có trích dẫn)

Làm theo [`skills/hoi-dap-thue-hkd/references/huong-dan-notebooklm.md`](skills/hoi-dap-thue-hkd/references/huong-dan-notebooklm.md): tạo notebook, tải các file trong [`van-ban/`](van-ban/) lên làm nguồn.

## Văn bản pháp luật dùng trong bộ skill

Tóm tắt có nguồn: [`shared/quy-dinh-thue-hkd-2026.md`](shared/quy-dinh-thue-hkd-2026.md) (cập nhật đến 10/2026).

| Văn bản | Nội dung |
|---|---|
| Luật Quản lý thuế 108/2025/QH15 | Hiệu lực 01/07/2026; phần khai thuế, hóa đơn của hộ kinh doanh từ 01/01/2026 |
| Luật Thuế TNCN 109/2025/QH15 | Thuế TNCN của cá nhân, hộ kinh doanh |
| Luật Thuế GTGT 48/2024/QH15 | Sửa đổi bởi Luật 149/2025/QH15 |
| Luật 09/2026/QH16 | Ngưỡng doanh thu chịu thuế do Chính phủ quy định |
| Nghị định 68/2026/NĐ-CP | Chính sách thuế và quản lý thuế với hộ, cá nhân kinh doanh |
| Nghị định 141/2026/NĐ-CP | Nâng ngưỡng lên 1 tỷ đồng/năm từ 01/01/2026 |
| Nghị định 254/2026/NĐ-CP | Hóa đơn, chứng từ điện tử từ 01/07/2026 |
| Nghị định 117/2025/NĐ-CP | Thuế với kinh doanh trên sàn TMĐT, nền tảng số |
| Thông tư 18/2026/TT-BTC | Hồ sơ, thủ tục, mẫu tờ khai (sửa đổi bởi Thông tư 50/2026/TT-BTC) |
| Thông tư 152/2025/TT-BTC | Chế độ kế toán, mẫu sổ hộ kinh doanh |

## Script đi kèm

| Script | Chức năng |
|---|---|
| `skills/ghi-so-hkd/scripts/tao_so_doanh_thu.py` | Tạo file Excel sổ S1a/S2a-HKD + tab Tổng hợp; nạp dữ liệu từ CSV |
| `skills/doi-soat-doanh-thu/scripts/doi_soat.py` | Phân loại giao dịch sao kê, cộng doanh thu theo quý, so mốc, tránh cộng trùng tiền sàn |

Thư viện Python: `pip install pandas openpyxl`.

## Cấu trúc repo

```
skills/<tên-skill>/SKILL.md        # hướng dẫn chính (frontmatter name + description)
skills/<tên-skill>/references/     # nguyên tắc chung, tóm tắt quy định
skills/<tên-skill>/scripts/        # script hỗ trợ
shared/                            # nguồn gốc tài liệu dùng chung -> build chép vào từng skill
qua-tang/                          # PDF 10 câu lệnh + Excel sổ doanh thu (tải về dùng ngay)
van-ban/                           # văn bản pháp luật gốc
chatgpt/                           # bản hướng dẫn cho ChatGPT (sinh tự động)
dist/                              # file zip để upload claude.ai (sinh tự động)
.claude-plugin/marketplace.json    # danh mục plugin cho Claude Code (sinh tự động)
scripts/build.py                   # đồng bộ shared, sinh chatgpt/, dist/, marketplace, kiểm tra lỗi
```

Sửa tài liệu dùng chung ở `shared/` rồi chạy `python3 scripts/build.py`.

## Lưu ý pháp lý

Tóm tắt quy định trong bộ skill tổng hợp đến tháng 10/2026 từ các nguồn ghi trong `shared/quy-dinh-thue-hkd-2026.md` và **có thể đã thay đổi**. Mốc doanh thu, tỷ lệ thuế, hạn nộp phải được đối chiếu văn bản hiện hành và hỏi cơ quan thuế quản lý. Skill không thay thế tư vấn của kế toán, cơ quan thuế.

## Giấy phép

MIT – xem [LICENSE](LICENSE). Văn bản quy phạm pháp luật trong `van-ban/` không thuộc đối tượng bảo hộ quyền tác giả.
