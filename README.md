# Skill AI cho Hộ kinh doanh (Việt Nam 2026)

Bộ **12 skill** giúp Claude (và ChatGPT) hỗ trợ **chủ hộ kinh doanh, cá nhân kinh doanh, người cho thuê nhà** làm sổ sách và thuế **theo quy định năm 2026**: ghi sổ S1a/S2a-HKD (Thông tư 152/2025/TT-BTC), đối soát sao kê, so mốc **1 tỷ đồng** (Nghị định 141/2026/NĐ-CP), tính thuế và so 2 cách tính TNCN, lịch hạn nộp đưa vào Google Calendar, khai báo trên eTax Mobile, hóa đơn điện tử (Nghị định 254/2026), đăng ký – tạm ngừng – đóng hộ, thuế cho thuê nhà, xử lý chậm nộp và phạt, lương – bảo hiểm – thuế TNCN của nhân viên.

Mọi skill tuân theo cùng nguyên tắc: **không bịa, không đoán số** (chữ mờ thì đánh dấu `[?]`), tính toán bằng code, viện dẫn pháp luật luôn kèm số hiệu văn bản và lưu ý kiểm tra văn bản hiện hành, **không tự khai, nộp, ký thay**.

> Quà tặng từ chương trình **Chuyên đề Thuế HKD 2026 · MBV Tây Sài Gòn** – Sự AI (suai.vn).

## Tải nhanh – không cần cài

| File | Dùng để |
|---|---|
| [`qua-tang/10_cau_lenh_AI_cho_Ho_kinh_doanh.pdf`](qua-tang/10_cau_lenh_AI_cho_Ho_kinh_doanh.pdf) | 10 câu lệnh sao chép dán vào ChatGPT, Claude |
| [`qua-tang/So_doanh_thu_HKD_S1a_S2a.xlsx`](qua-tang/So_doanh_thu_HKD_S1a_S2a.xlsx) | Sổ doanh thu S1a-HKD, S2a-HKD có tổng hợp theo tháng, quý, mốc 1 tỷ và 3 tỷ |
| [`van-ban/`](van-ban/) | Văn bản pháp luật gốc (bản chữ) để đối chiếu hoặc nạp vào Claude/ChatGPT Project |

Trên điện thoại: bấm vào tên file → nút **Download** (biểu tượng tải xuống) góc phải.

## Danh sách skill

| # | Skill | Lệnh | Làm gì |
|---|---|---|---|
| 01 | Ghi sổ doanh thu | `/ghi-so-hkd` | Ảnh sổ tay, hóa đơn → sổ S1a/S2a-HKD; đánh dấu `[?]` chỗ mờ; xuất Excel có công thức |
| 02 | Đối soát doanh thu | `/doi-soat-doanh-thu` | Sao kê + báo cáo sàn → tách tiền bán hàng, nội bộ, vay; cộng theo quý; so mốc 1 tỷ, 3 tỷ |
| 03 | Hỏi đáp thuế | `/hoi-dap-thue-hkd` | Trả lời có dẫn nguồn; đọc thông báo thuế; soạn câu hỏi cho cán bộ thuế; checklist theo quý |
| 04 | Kiểm tra hóa đơn | `/kiem-tra-hoa-don` | Kiểm tra trước khi xuất hóa đơn; bảng chi phí từ hóa đơn mua vào; ngưỡng hóa đơn điện tử |
| 05 | Khai báo thuế | `/khai-bao-thue-hkd` | Đúng trường hợp → mẫu, hạn nộp, ô cần điền; các bước trên eTax Mobile và Cổng dịch vụ công, **kiểm tra lại giao diện mới nhất** trước khi hướng dẫn |
| 06 | Tính thuế | `/tinh-thue-hkd` | Thuế GTGT, TNCN theo ngành, theo quý; so cách tính % doanh thu với 15% thu nhập, chi phí hòa vốn; trừ 1 tỷ có lợi nhất |
| 07 | Lịch thuế | `/lich-thue-hkd` | Hạn nộp cả năm đúng trường hợp, tự lùi ngày nghỉ; file .ics nhập Google Calendar, iPhone có nhắc trước |
| 08 | Hóa đơn điện tử | `/hoa-don-dien-tu-hkd` | Có phải dùng không, hóa đơn có mã hay máy tính tiền, hạn đăng ký 30 ngày, lập đúng, sửa hóa đơn sai (NĐ 254/2026) |
| 09 | Đăng ký hộ kinh doanh | `/dang-ky-ho-kinh-doanh` | Thành lập, thay đổi, mở thêm cửa hàng, tạm ngừng, chấm dứt + việc phía thuế đi kèm; kiểm tra thủ tục mới nhất |
| 10 | Cho thuê nhà | `/cho-thue-nha` | Thuế cho thuê nhà, mặt bằng: mốc 1 tỷ, GTGT 5% + TNCN 5%, nhiều hợp đồng, trả trước, 01/BĐS, bên thuê khai thay |
| 11 | Chậm nộp, phạt | `/xu-ly-cham-nop-phat` | Tiền chậm nộp 0,03%/ngày, khung phạt trễ tờ khai, mốc 90 ngày, khai bổ sung, bất khả kháng, soạn giải trình |
| 12 | Nhân viên | `/thue-nhan-vien-hkd` | Lương thực nhận, thuế TNCN, bảo hiểm phần nhân viên và hộ, lương tối thiểu vùng, bảng lương, khung hợp đồng |

## Cài đặt

### Claude.ai (web / app) – dễ nhất

1. Bật **Settings → Capabilities → Code execution and file creation**.
2. Vào **Settings → Capabilities → Skills → Upload skill**.
3. Tải lên từng file trong thư mục [`dist/`](dist/) (ví dụ `dist/ghi-so-hkd.zip`).

Sau đó cứ nói tự nhiên: "ghi sổ giúp tôi từ ảnh này", "doanh thu tôi đã vượt 1 tỷ chưa", "cho thuê nhà 1,2 tỷ thuế bao nhiêu", Claude tự chọn skill.

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

Mỗi skill có một file hướng dẫn trong [`chatgpt/`](chatgpt/). Bản miễn phí: tạo **Project**, dán phần **Instructions** vào hướng dẫn của Project, tải các file `references/` lên. Bản trả phí có thể tạo Custom GPT tương tự.

### Tra cứu nguyên văn văn bản (Claude/ChatGPT Project)

Làm theo [`skills/hoi-dap-thue-hkd/references/huong-dan-nap-van-ban.md`](skills/hoi-dap-thue-hkd/references/huong-dan-nap-van-ban.md): tạo Project, tải các file trong [`van-ban/`](van-ban/) lên làm tài liệu.

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
| Thông tư 91/2026/TT-BTC | Hướng dẫn NĐ 254/2026 về hóa đơn (xử lý hóa đơn sai) – tóm tắt từ nguồn thứ cấp |
| Nghị định 168/2025/NĐ-CP, 296/2026/NĐ-CP; QĐ 1995/QĐ-BTC | Đăng ký hộ kinh doanh – tóm tắt từ nguồn thứ cấp |
| Nghị định 125/2020/NĐ-CP (sửa đổi đến NĐ 291/2026) | Xử phạt vi phạm hành chính về thuế, hóa đơn – tóm tắt từ nguồn thứ cấp |
| Luật BHXH 41/2024/QH15; NĐ 293/2025/NĐ-CP | Bảo hiểm bắt buộc; lương tối thiểu vùng 2026 – tóm tắt từ nguồn thứ cấp |

## Script đi kèm

| Script | Chức năng |
|---|---|
| `skills/ghi-so-hkd/scripts/tao_so_doanh_thu.py` | Tạo file Excel sổ S1a/S2a-HKD + tab Tổng hợp; nạp dữ liệu từ CSV |
| `skills/doi-soat-doanh-thu/scripts/doi_soat.py` | Phân loại giao dịch sao kê, cộng doanh thu theo quý, so mốc, tránh cộng trùng tiền sàn |
| `skills/tinh-thue-hkd/scripts/tinh_thue.py` | Ước tính GTGT, TNCN theo ngành/quý; so 2 cách tính TNCN |
| `skills/lich-thue-hkd/scripts/tao_lich_thue.py` | Lịch hạn nộp + file .ics |
| `skills/cho-thue-nha/scripts/tinh_thue_cho_thue.py` | Thuế cho thuê BĐS theo hợp đồng, 2 lần khai |
| `skills/xu-ly-cham-nop-phat/scripts/tinh_cham_nop.py` | Tiền chậm nộp, khung phạt chậm nộp tờ khai |
| `skills/thue-nhan-vien-hkd/scripts/tinh_luong.py` | Lương thực nhận, bảo hiểm, TNCN, chi phí của hộ |

Thư viện Python: `pip install pandas openpyxl` (2 script đầu); các script còn lại chỉ cần Python 3.

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
