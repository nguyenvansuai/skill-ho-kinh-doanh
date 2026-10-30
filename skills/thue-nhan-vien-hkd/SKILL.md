---
name: thue-nhan-vien-hkd
description: Hỗ trợ hộ kinh doanh thuê nhân viên năm 2026 — tính lương thực nhận, thuế TNCN (giảm trừ 15,5 triệu, 6,2 triệu/người phụ thuộc, biểu lũy tiến 5 bậc), bảo hiểm bắt buộc phần nhân viên và phần hộ phải đóng, tổng chi phí thuê một người; kiểm tra lương tối thiểu vùng; khi nào phải đóng BHXH (hợp đồng từ 1 tháng), chủ hộ có phải đóng không; chi phí lương được trừ thuế; khung hợp đồng lao động, bảng lương. Dùng khi người dùng hỏi "thuê nhân viên phải đóng gì", "lương 8 triệu thực nhận bao nhiêu", "có phải đóng bảo hiểm cho nhân viên", "khấu trừ thuế lương", "làm bảng lương", "chủ hộ có phải đóng BHXH".
---

# Nhân viên của hộ kinh doanh: lương, bảo hiểm, thuế TNCN

Đọc `references/nguyen-tac-chung.md` và `references/lao-dong-tncn.md`.

## 1. Cần biết (hỏi tối đa 2 câu)

Lương tháng (gồm phụ cấp chịu thuế) · lương ghi trong hợp đồng để đóng bảo hiểm · thời hạn hợp đồng (dưới 1 tháng, 1–3 tháng, dài hơn) · số người phụ thuộc đã đăng ký · tỉnh/thành, quận/huyện (để biết vùng lương tối thiểu).

## 2. Tính bằng script

```bash
python3 scripts/tinh_luong.py --luong 9000000 --vung I
python3 scripts/tinh_luong.py --luong 30000000 --npt 1 --vung I
python3 scripts/tinh_luong.py --luong 4000000 --thoi-vu
```

Nhiều nhân viên → chạy cho từng người, lập **bảng lương** (Excel nếu người dùng cần): họ tên, lương, bảo hiểm NLĐ, thuế TNCN, thực nhận, bảo hiểm hộ đóng, tổng chi phí; dòng cộng tính bằng công thức.

## 3. Quy tắc phải nói đúng

- TNCN: giảm trừ 15,5 triệu/tháng + 6,2 triệu/người phụ thuộc; biểu 5%–35% (Luật 109/2025 Đ.9, Đ.10), áp dụng từ kỳ tính thuế 2026 (Đ.29 k.2). Lương sau bảo hiểm ≤ 15,5 triệu (không người phụ thuộc) → không có thuế.
- Hộ trả lương là bên **khấu trừ, khai, nộp** thuế của nhân viên (Luật 108/2025 Đ.12 k.3 điểm a). Mẫu, kỳ khai, quyết toán thay → **[cần kiểm tra]**, nói rõ chưa xác minh.
- Bảo hiểm: hợp đồng từ đủ 1 tháng → bắt buộc. Tỷ lệ mặc định hộ 21,5% / nhân viên 10,5% → **[cần kiểm tra với cơ quan BHXH]**.
- Chủ hộ: trên 1 tỷ thuộc diện BHXH bắt buộc; từ 1 tỷ trở xuống không bắt buộc (nguồn báo chí, công văn BHXH) → **[cần kiểm tra]**.
- Lương không thấp hơn lương tối thiểu vùng (NĐ 293/2025) với công việc làm đủ giờ.
- Lương nhân viên **có đóng bảo hiểm** là chi phí được trừ khi hộ tính TNCN theo thu nhập; lương chủ hộ, thành viên hộ không được trừ (NĐ 68/2026 Đ.6). Nhắc chuyển khoản lương, lưu bảng lương có chữ ký.
- Không khuyên ký hợp đồng ngắn liên tục hoặc ghi lương thấp trong hợp đồng để né bảo hiểm: nói rõ rủi ro pháp lý.

## 4. Đầu ra

1. Kết luận: nhân viên thực nhận X, hộ chi tổng Y/tháng; có phải đóng bảo hiểm, có thuế TNCN không.
2. Bảng chi tiết (script), ghi "Đã kiểm tra phép tính".
3. Việc hộ phải làm: ký hợp đồng, đăng ký BHXH cho nhân viên, khấu trừ và khai thuế (nếu có), lưu chứng từ. Có thể soạn **khung hợp đồng lao động** đơn giản theo mục 4 của `references/lao-dong-tncn.md` (để trống chỗ cần người dùng quyết định).
4. Ghi rõ phần nào **[cần kiểm tra]**.
5. Câu chốt: "Đối chiếu quy định hiện hành; hỏi cơ quan BHXH và cơ quan thuế quản lý."
