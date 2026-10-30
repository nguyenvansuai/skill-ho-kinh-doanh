---
name: kiem-tra-hoa-don
description: Hỗ trợ hóa đơn cho hộ kinh doanh Việt Nam — kiểm tra thông tin trước khi xuất hóa đơn điện tử (người mua, mã số thuế, hàng hóa, phép tính), lập bảng chi phí từ ảnh hóa đơn mua vào, đánh dấu khoản từ 5 triệu đồng trả tiền mặt, nhắc ngưỡng bắt buộc hóa đơn điện tử trên 1 tỷ. Dùng khi người dùng nói "kiểm tra hóa đơn", "trước khi xuất hóa đơn", "lập bảng chi phí", "chụp hóa đơn nhập hàng", "có cần hóa đơn điện tử không", "máy tính tiền".
---

# Kiểm tra hóa đơn

Đọc `references/nguyen-tac-chung.md` và `references/quy-dinh-thue-hkd-2026.md` (mục 2, 3).

## 1. Kiểm tra trước khi xuất hóa đơn

Người dùng gửi thông tin định ghi trên hóa đơn. Kiểm tra và trả về bảng `Mục | Hiện tại | Vấn đề | Đề xuất sửa`:

- **Người mua:** tên, địa chỉ; mã số thuế nếu người mua là doanh nghiệp, hộ kinh doanh. Mã số thuế doanh nghiệp: 10 chữ số, đơn vị phụ thuộc thêm 3 chữ số (dạng `0123456789-001`). Cá nhân: số định danh 12 chữ số. Chỉ kiểm tra định dạng, nhắc người dùng tra cứu trên trang của cơ quan thuế.
- **Hàng hóa, dịch vụ:** tên rõ ràng, đơn vị tính, số lượng, đơn giá.
- **Phép tính:** Thành tiền = Số lượng × Đơn giá; tổng cộng; tính bằng code, ghi "Đã kiểm tra phép tính".
- **Số tiền bằng chữ** (nếu có): đọc lại và so với số.
- Không đề xuất ghi thuế suất GTGT kiểu doanh nghiệp (10%, 8%) trên hóa đơn của hộ nộp thuế theo tỷ lệ % trên doanh thu; nếu người dùng hỏi, khuyên hỏi nhà cung cấp phần mềm hóa đơn hoặc cơ quan thuế.

## 2. Bảng chi phí từ hóa đơn mua vào

Từ ảnh hóa đơn: lập bảng `Ngày | Người bán | Số hóa đơn | Mặt hàng | Số tiền | Hình thức thanh toán`. Chữ mờ ghi `[?]`. Cuối bảng liệt kê riêng các khoản **từ 5 triệu đồng trở lên trả bằng tiền mặt**, giải thích: khi tính thuế theo thu nhập, khoản này không được tính vào chi phí (Nghị định 68/2026).

## 3. Có bắt buộc hóa đơn điện tử không?

- Doanh thu năm trên 1 tỷ đồng: bắt buộc hóa đơn điện tử có mã của cơ quan thuế hoặc từ máy tính tiền; đăng ký trong 30 ngày kể từ cuối kỳ có doanh thu lũy kế vượt 1 tỷ (NĐ 141/2026, NĐ 254/2026).
- Bán lẻ, ăn uống, khách sạn, vận tải hành khách, vui chơi giải trí: thuộc nhóm dùng hóa đơn từ máy tính tiền (NĐ 254/2026).
- Từ 1 tỷ trở xuống: không bắt buộc, được tự nguyện đăng ký.
- Luôn kèm: "Kiểm tra văn bản hiện hành và hỏi cơ quan thuế quản lý."
