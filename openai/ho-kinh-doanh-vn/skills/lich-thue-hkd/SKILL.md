---
name: lich-thue-hkd
description: Lập lịch hạn nộp thuế cả năm cho hộ kinh doanh, cá nhân kinh doanh, người cho thuê nhà theo đúng trường hợp (từ 1 tỷ trở xuống, mới ra kinh doanh, trên 1 tỷ khai quý, trên 3 tỷ quyết toán, khai tháng, cho thuê BĐS 1 hay 2 lần/năm); tự lùi hạn khi trùng thứ Bảy, Chủ nhật, ngày lễ; xuất file .ics để nhập Google Calendar, iPhone, Outlook có nhắc trước 7 ngày và 1 ngày. Dùng khi người dùng hỏi "hạn nộp thuế khi nào", "lịch thuế năm nay", "nhắc tôi hạn nộp tờ khai", "đưa hạn thuế vào Google Calendar", "quý này hạn ngày mấy".
---

# Lịch thuế hộ kinh doanh

Đọc `references/nguyen-tac-chung.md` và `references/quy-dinh-thue-hkd-2026.md` (mục 2, 3a).

## 1. Xác định trường hợp (hỏi tối đa 2 câu)

Doanh thu năm ước tính · mới ra kinh doanh (6 tháng đầu hay cuối năm) · có cho thuê nhà không, khai 1 hay 2 lần · đã vượt 1 tỷ từ quý nào · có chọn TNCN theo thu nhập không.

| Mã | Trường hợp | Hạn | Căn cứ |
|---|---|---|---|
| A | ≤ 1 tỷ | 31/01 năm sau: thông báo doanh thu 01/TKN-CNKD | NĐ 68/2026 Đ.8 k.1 điểm a |
| moi-6t-dau | Bắt đầu kinh doanh trong 6 tháng đầu năm, ≤ 1 tỷ | 31/07 (doanh thu đến 30/6) và 31/01 năm sau (6 tháng cuối) | NĐ 68/2026 Đ.9 k.1 |
| moi-6t-cuoi | Bắt đầu trong 6 tháng cuối năm, ≤ 1 tỷ | 31/01 năm sau | NĐ 68/2026 Đ.9 k.1 |
| B | > 1 tỷ, khai quý | Ngày cuối tháng đầu quý sau: 30/4, 31/7, 31/10, 31/1; từ quý vượt mốc. Đăng ký hóa đơn điện tử trong 30 ngày từ cuối quý vượt mốc | NĐ 68/2026 Đ.8 k.1, k.3 điểm a, k.5 điểm c; Đ.9 k.2 |
| C | > 3 tỷ hoặc chọn TNCN theo thu nhập | Như B + quyết toán 02/CNKD-TNCN-QTT trước 31/03 năm sau | NĐ 68/2026 Đ.8 k.3 điểm c |
| thang | > 50 tỷ | GTGT ngày 20 tháng sau | NĐ 68/2026 Đ.8 k.3 điểm b, Đ.10 k.1 điểm b |
| cho-thue-2 / cho-thue-1 | Cá nhân tự khai cho thuê BĐS | 2 lần: 31/07 và 31/01 năm sau; 1 lần: 31/01 năm sau | NĐ 68/2026 Đ.8 k.3 điểm d |

- Hạn nộp **tiền** thuế = hạn nộp tờ khai (Đ.8 k.3 điểm e).
- Hạn trùng ngày nghỉ → ngày làm việc tiếp theo (Bộ luật Dân sự 2015 Đ.148 k.5). Script tự lùi theo thứ Bảy, Chủ nhật, 1/1, 30/4, 1/5, 2/9; **Tết âm lịch và ngày nghỉ bù** người dùng thêm bằng `--nghi`, script cảnh báo hạn gần Tết.
- Việc phát sinh không cố định ngày: địa điểm kinh doanh mới, thay đổi, tạm ngừng, chấm dứt → trong 10 ngày làm việc (Đ.8 k.4 điểm đ); tài khoản ngân hàng, ví mới → 01/BK-STK (Đ.13 k.4).

## 2. Tạo lịch

```bash
python3 scripts/tao_lich_thue.py --nam 2026 --truong-hop B --quy-vuot 3 --ra lich_thue_2026.ics
python3 scripts/tao_lich_thue.py --nam 2027 --truong-hop A cho-thue-2 --nghi 2028-01-31
```

Nhập vào lịch:
- **Google Calendar (máy tính):** calendar.google.com → bánh răng → Cài đặt → Nhập và xuất → Nhập → chọn file .ics.
- **iPhone:** mở file .ics trong Tệp/Mail → Thêm tất cả.
- Nếu có công cụ Google Calendar được kết nối: **hỏi người dùng xác nhận** danh sách sự kiện trước, rồi mới tạo.

## 3. Đầu ra

1. Bảng hạn: ngày (đã lùi nếu trùng ngày nghỉ), việc, mẫu, căn cứ. Đánh dấu hạn gần nhất kể từ hôm nay.
2. File .ics (gửi cho người dùng) + cách nhập.
3. Câu chốt: "Hạn theo NĐ 68/2026 tại thời điểm lập lịch; đối chiếu quy định hiện hành và thông báo của cơ quan thuế."
