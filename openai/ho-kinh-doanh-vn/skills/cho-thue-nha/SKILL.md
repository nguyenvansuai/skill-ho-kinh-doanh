---
name: cho-thue-nha
description: Tính và hướng dẫn khai thuế cho thuê nhà, căn hộ, mặt bằng, kiot của cá nhân năm 2026 — mốc 1 tỷ, GTGT 5% và TNCN 5% phần vượt, chọn hợp đồng để trừ 1 tỷ khi có nhiều nhà, tiền thuê trả trước nhiều năm, khai 1 lần hay 2 lần/năm (31/7, 31/1), mẫu 01/BĐS, bên thuê là công ty khai thay, nộp ở đâu, có phải xuất hóa đơn không. Dùng khi người dùng hỏi "cho thuê nhà có phải đóng thuế không", "thuế cho thuê mặt bằng", "khai 01/BĐS", "công ty thuê nhà nộp thuế thay", "cho thuê 1,2 tỷ một năm thuế bao nhiêu".
---

# Thuế cho thuê nhà, mặt bằng

Đọc `references/nguyen-tac-chung.md` và `references/quy-dinh-cho-thue.md`.

## 1. Cần biết (hỏi tối đa 2 câu)

- Từng hợp đồng: tiền thuê mỗi tháng, tháng bắt đầu/kết thúc trong năm, có trả trước nhiều năm không.
- Bên thuê là công ty (có thỏa thuận khai thay không) hay cá nhân.
- Có phải cho thuê theo ngày kèm dịch vụ (homestay, nhà nghỉ) không → nếu có, đó là **kinh doanh lưu trú**, chuyển sang skill `tinh-thue-hkd`.

## 2. Tính bằng script

```bash
python3 scripts/tinh_thue_cho_thue.py --hd "Nha Q1:45000000:1-12" "Mat bang Q3:50000000:4-12"
python3 scripts/tinh_thue_cho_thue.py --hd "Kiot:20000000:1-12" "Nha:90000000:1-12" --khai-thay Kiot
python3 scripts/tinh_thue_cho_thue.py --tra-truoc "Kho:3000000000:3"
```

Script cộng doanh thu theo 6 tháng và cả năm, so mốc 1 tỷ, phân bổ mức trừ (ưu tiên hợp đồng tự khai, đổi bằng `--thu-tu-tru`), tính GTGT 5% toàn bộ và TNCN 5% phần vượt, tách phần tự khai lần 1, lần 2.

## 3. Quy tắc phải nói đúng

- ≤ 1 tỷ/năm: không nộp GTGT, TNCN. > 1 tỷ: GTGT 5% **toàn bộ** + TNCN 5% **phần vượt 1 tỷ** (Luật 109/2025 Đ.7 k.4; NĐ 68/2026 Đ.3, Đ.4 k.4).
- Nhiều hợp đồng: tổng mức trừ tối đa 1 tỷ/năm; hợp đồng có bên thuê khai thay phải ghi số tiền được trừ trong hợp đồng (Đ.4 k.4).
- Trả trước nhiều năm: phân bổ theo số năm hoặc tính một lần (Đ.5 k.2 điểm đ) – nêu cả hai để người dùng chọn.
- Khai 2 lần (31/07 và 31/01) hoặc 1 lần (31/01); bên thuê là cá nhân → chủ nhà tự khai; nộp ở cơ quan thuế nơi có nhà (Đ.8 k.3 điểm d, đ; k.4 điểm d). Mẫu 01/BĐS + 01/BK-BĐS (TT 18/2026 Đ.4 k.4).
- Không phải xuất hóa đơn điện tử (NĐ 254/2026 Đ.7 k.2).
- Các mục **[cần kiểm tra]** trong `references/quy-dinh-cho-thue.md` (gộp mức 1 tỷ với kinh doanh khác, tiền cọc, 01/BK-STK) → nói rõ chưa chắc, khuyên hỏi cơ quan thuế; không tự kết luận.

## 4. Đầu ra

1. Kết luận một câu: có/không phải nộp, ước bao nhiêu (GTGT a + TNCN b).
2. Bảng theo hợp đồng + phần tự khai lần 1/lần 2 hoặc 1 lần, ghi "Đã kiểm tra phép tính".
3. Việc cần làm: mẫu, hạn (ngày cụ thể), nơi nộp; điều khoản cần ghi vào hợp đồng nếu bên thuê khai thay. Bước bấm trên eTax: dùng skill `khai-bao-thue-hkd` (kiểm tra giao diện mới nhất).
4. Câu chốt: "Đây là ước tính; đối chiếu quy định hiện hành và hỏi cơ quan thuế nơi có bất động sản."
