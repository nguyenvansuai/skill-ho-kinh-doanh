---
name: tinh-thue-hkd
description: Tính, ước tính số thuế GTGT và TNCN hộ kinh doanh, cá nhân kinh doanh phải nộp năm 2026 theo từng nhóm ngành, theo quý và cả năm; so sánh 2 cách tính TNCN (tỷ lệ % trên doanh thu vượt 1 tỷ hay 15% trên thu nhập), tìm mức chi phí hòa vốn, phân bổ mức trừ 1 tỷ có lợi nhất khi nhiều ngành; trừ số thuế sàn đã khấu trừ. Dùng khi người dùng hỏi "tôi phải đóng thuế bao nhiêu", "tính thuế giúp", "nên chọn cách tính nào", "doanh thu 1,5 tỷ thuế bao nhiêu", "thuế quý này", "so sánh tính theo doanh thu và theo thu nhập".
---

# Tính thuế hộ kinh doanh

Đọc `references/nguyen-tac-chung.md` và `references/quy-dinh-thue-hkd-2026.md` (mục 2, 3a).

## 1. Cần biết (hỏi tối đa 2 câu nếu thiếu)

- Doanh thu năm (hoặc từng quý) **theo nhóm ngành**: hàng hóa · dịch vụ · cho thuê tài sản/đại lý · sản xuất, vận tải · nội dung số · khác. Bán nhiều ngành → hỏi tách.
- Có bán trên sàn có thanh toán (Shopee, TikTok Shop, Lazada) không, sàn đã khấu trừ bao nhiêu (xem báo cáo thuế trên trang quản lý shop).
- Nếu doanh thu trên 1 tỷ đến 3 tỷ và muốn so cách tính: tổng chi phí có hóa đơn, chứng từ.
- Cho thuê nhà, mặt bằng → dùng skill `cho-thue-nha`. Lương nhân viên → `thue-nhan-vien-hkd`.

## 2. Tính bằng script (không tính nhẩm)

```bash
python3 scripts/tinh_thue.py --nganh hang_hoa=1200000000
python3 scripts/tinh_thue.py --nganh hang_hoa=900000000 dich_vu=400000000 --chi-phi 1000000000
python3 scripts/tinh_thue.py --quy hang_hoa=250000000,300000000,320000000,330000000 --san-da-khau-tru 4000000
```

Script tự: so mốc 1 tỷ, 3 tỷ, 50 tỷ; trừ 1 tỷ vào ngành thuế suất cao nhất trước (NĐ 68/2026 Đ.4 k.3); tính GTGT trên **toàn bộ** doanh thu; tính Cách 2 khi có chi phí; chỉ ra quý vượt mốc.

## 3. Quy tắc phải nói đúng

| Doanh thu năm | Cách tính TNCN | Căn cứ |
|---|---|---|
| ≤ 1 tỷ | Không nộp GTGT, TNCN | NĐ 68/2026 Đ.3 k.1, Đ.4 k.1 |
| > 1 tỷ đến 3 tỷ | Mặc định Cách 1: (doanh thu − 1 tỷ) × thuế suất ngành. **Được chọn** Cách 2: (doanh thu − chi phí) × 15% | Luật 109/2025 Đ.7 k.2, k.3; NĐ 68/2026 Đ.4 k.5 |
| > 3 tỷ đến 50 tỷ | **Bắt buộc** Cách 2 × 17%, quyết toán năm | Luật 109/2025 Đ.7 k.2 điểm c |
| > 50 tỷ | Cách 2 × 20%; GTGT khai theo tháng | Luật 109/2025 Đ.7 k.2 điểm d; NĐ 68/2026 Đ.10 k.1 |

- Chọn Cách 2: giữ ổn định **2 năm liên tục**; đang dùng Cách 1 mà cả năm vượt 3 tỷ → năm sau phải chuyển Cách 2 (NĐ 68/2026 Đ.4 k.5 điểm d).
- Chi phí được trừ phải có hóa đơn, chứng từ; khoản từ 5 triệu đồng trở lên phải chuyển khoản; không trừ lương của chính chủ hộ, thành viên hộ, chi phí gia đình, tiền phạt (NĐ 68/2026 Đ.6).
- Thuế sàn đã khấu trừ, nộp thay: không nộp lại (Luật 108/2025 Đ.12 k.3 điểm c); cả năm ≤ 1 tỷ thì được bù trừ, hoàn (NĐ 68/2026 Đ.12 k.1).
- Cách 2 tạm nộp theo quý thiếu so với quyết toán: nộp bổ sung, **không** tính tiền chậm nộp (NĐ 68/2026 Đ.10 k.2 điểm b).

## 4. Đầu ra

1. Một câu kết luận: "Năm nay anh/chị ước nộp khoảng X đồng (GTGT a + TNCN b)".
2. Bảng theo ngành (doanh thu, GTGT, mức trừ, TNCN) và bảng theo quý nếu có số quý. Ghi "Đã kiểm tra phép tính".
3. Doanh thu 1–3 tỷ: so 2 cách, cách nào thấp hơn, **chi phí hòa vốn**, và điều kiện đi kèm khi chọn Cách 2 (sổ sách, hóa đơn chi phí, giữ 2 năm). Không khuyên Cách 2 nếu người dùng không có đủ hóa đơn chi phí.
4. Việc cần làm tiếp: mẫu, hạn nộp (skill `khai-bao-thue-hkd`, `lich-thue-hkd`).
5. Câu chốt: "Đây là ước tính; số chính thức do eTax tính trên tờ khai. Đối chiếu quy định hiện hành và hỏi cơ quan thuế quản lý."
