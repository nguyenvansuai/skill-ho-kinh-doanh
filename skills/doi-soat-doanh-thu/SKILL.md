---
name: doi-soat-doanh-thu
description: Đối soát doanh thu hộ kinh doanh từ sao kê ngân hàng, ví điện tử và báo cáo doanh thu sàn (Shopee, TikTok Shop, Lazada) — phân loại tiền bán hàng, chuyển nội bộ, vay/trả nợ, chưa rõ; tránh cộng trùng tiền sàn; cộng theo quý, lũy kế và so mốc 1 tỷ, 3 tỷ. Dùng khi người dùng nói "đối soát", "sao kê", "cộng doanh thu theo quý", "tôi đang ở mốc nào", "doanh thu đã vượt 1 tỷ chưa", "kiểm tra tiền vào tài khoản".
---

# Đối soát doanh thu

Đọc `references/nguyen-tac-chung.md` và `references/quy-dinh-thue-hkd-2026.md` (mục 2, 3).

## 1. Đầu vào

- Sao kê tài khoản kinh doanh, ví điện tử: ưu tiên Excel/CSV; PDF nhiều trang dễ đọc sót → khuyên xuất lại dạng Excel.
- Báo cáo doanh thu từ sàn (file tải từ trang quản lý shop).
- Nhắc người dùng che số tài khoản đầy đủ trước khi gửi.

## 2. Phân loại từng giao dịch

| Nhóm | Ví dụ nội dung chuyển khoản |
|---|---|
| Tiền bán hàng | Khách chuyển khoản mua hàng, thanh toán đơn |
| Tiền sàn chuyển về | SHOPEE, TIKTOK, LAZADA thanh toán doanh thu |
| Chuyển nội bộ | Chuyển từ tài khoản cá nhân, chuyển giữa các tài khoản của chủ hộ |
| Vay hoặc trả nợ | Vay, trả nợ, góp vốn, hoàn tiền |
| Chưa rõ | Nội dung trống, chỉ có tên người chuyển, nộp tiền mặt tại quầy |

- Nhóm **Chưa rõ** không tự xếp vào doanh thu: liệt kê để người dùng xác nhận.
- **Tránh cộng trùng:** doanh thu bán trên sàn lấy theo **báo cáo của sàn** (sàn đã khấu trừ, nộp thay thuế). Khoản "sàn chuyển về" trong sao kê là tiền sau phí của chính các đơn đó → không cộng thêm lần nữa.
- Mỗi dòng ghi lý do phân loại.

## 3. Tính toán

Chạy `scripts/doi_soat.py` (phân loại theo từ khóa + cộng theo quý). Ví dụ:

```bash
python3 scripts/doi_soat.py sao_ke.xlsx --cot-ngay "Ngày GD" --cot-noi-dung "Nội dung" --cot-tien "Ghi có" \
  --bao-cao-san doanh_thu_san.csv --cot-ngay-san "Ngày" --cot-tien-san "Doanh thu" --ra ket_qua.xlsx
```

Kết quả: tab Giao dịch (có cột Nhóm, Lý do), Theo quý, Chưa rõ. Người dùng sửa nhóm của dòng "Chưa rõ" rồi chạy lại.

## 4. Đầu ra

1. Bảng doanh thu theo quý: tiền bán hàng trực tiếp, doanh thu sàn, cộng quý, lũy kế.
2. Trạng thái so mốc: đã vượt 1 tỷ chưa, từ quý nào; còn bao nhiêu nữa đến mốc kế tiếp.
3. Danh sách giao dịch **Chưa rõ** và các khoản đã loại (nội bộ, vay) để người dùng kiểm tra.
4. **Việc cần làm** theo trạng thái: chưa vượt 1 tỷ → danh sách A; đã vượt hoặc dự báo vượt trong năm → danh sách B, nêu rõ quý bắt đầu khai thuế và hạn đăng ký hóa đơn điện tử (mục 3a của `references/quy-dinh-thue-hkd-2026.md`), giữ nguyên căn cứ.
5. Câu chốt: "Đối chiếu quy định hiện hành và hỏi cơ quan thuế quản lý trước khi thực hiện."

Người dùng chỉ cần gửi file và nói "đối soát doanh thu năm nay"; skill tự phân loại, cộng, so mốc, dự báo quý vượt mốc theo tốc độ quý gần nhất.
