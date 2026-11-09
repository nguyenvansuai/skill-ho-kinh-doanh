---
name: hoa-don-dien-tu-hkd
description: Hướng dẫn hộ kinh doanh dùng hóa đơn điện tử theo Nghị định 254/2026 (từ 01/07/2026) — có phải dùng không, chọn hóa đơn có mã hay hóa đơn từ máy tính tiền, hạn đăng ký 30 ngày khi vượt 1 tỷ, khi nào phải lập, ghi những nội dung gì, gửi khách thế nào, xử lý hóa đơn viết sai (thông báo 04/SS-HĐĐT, hóa đơn điều chỉnh, thay thế), trường hợp cấp theo từng lần phát sinh; kiểm tra giao diện mới nhất trước khi chỉ bước bấm. Dùng khi người dùng hỏi "có phải xuất hóa đơn không", "đăng ký hóa đơn điện tử", "máy tính tiền", "xuất hóa đơn sai", "hóa đơn điều chỉnh", "khách đòi hóa đơn".
---

# Hóa đơn điện tử cho hộ kinh doanh

Đọc `references/nguyen-tac-chung.md`, `references/quy-dinh-thue-hkd-2026.md` và `references/quy-dinh-hoa-don.md`.

Khác skill `kiem-tra-hoa-don`: skill đó soát **từng tờ** hóa đơn (trước khi xuất, hóa đơn mua vào). Skill này hướng dẫn **có dùng không, đăng ký, lập, sửa**.

## 1. Có phải dùng không? Dùng loại nào?

Hỏi: doanh thu năm (ước tính, lũy kế đến quý gần nhất) · bán cho ai (người tiêu dùng tại quầy, doanh nghiệp, qua sàn) · ngành (bán lẻ, ăn uống, dịch vụ, cho thuê nhà).

1. Cho thuê bất động sản; đại lý xổ số/bảo hiểm/đa cấp đã được khấu trừ → **không phải** dùng (NĐ 254 Đ.7 k.2, k.3).
2. Doanh thu > 1 tỷ → **bắt buộc**; vượt mốc trong năm → đăng ký trong **30 ngày** từ cuối quý vượt (NĐ 68/2026 Đ.8 k.5). Nêu ngày hạn cụ thể (tính bằng code).
3. ≤ 1 tỷ → không bắt buộc; được tự nguyện (khách là doanh nghiệp hay đòi hóa đơn thì nên đăng ký).
4. Chọn loại: bán trực tiếp người tiêu dùng (bán lẻ, quán ăn, khách sạn, dịch vụ cá nhân…) → **máy tính tiền** (in/gửi ngay tại quầy, không cần chữ ký số); bán cho doanh nghiệp, giao hàng xa, hợp đồng → **hóa đơn có mã**. Có thể dùng cả hai (NĐ 254 Đ.6 k.1 điểm c).
5. Loại hóa đơn của hộ: **hóa đơn bán hàng** (không phải hóa đơn GTGT) (NĐ 254 Đ.8 k.2).

## 2. Kiểm tra giao diện và mẫu mới nhất (bắt buộc trước khi chỉ bước bấm)

Có công cụ tìm kiếm: tìm "đăng ký hóa đơn điện tử hộ kinh doanh [tháng/năm hiện tại]", "Thông tư 91/2026 mẫu đăng ký hóa đơn". Ưu tiên gdt.gov.vn, Cục Thuế, rồi bài hướng dẫn có ngày trong 60 ngày gần nhất. Mở được trang công khai `hoadondientu.gdt.gov.vn` thì chỉ xem menu, **không đăng nhập, không nhập mã số thuế, mật khẩu, OTP, không bấm gửi**. Không kiểm tra được → nói rõ "chưa kiểm tra được giao diện hiện tại, tên nút có thể đã đổi".

## 3. Lập hóa đơn đúng

- Thời điểm: giao hàng (dù chưa thu tiền); dịch vụ xong, hoặc lúc thu tiền trước (không tính tiền cọc); giao nhiều lần → mỗi lần một hóa đơn (NĐ 254 Đ.9).
- Đủ nội dung bắt buộc (`references/quy-dinh-hoa-don.md` mục 3). Người mua là cá nhân không có mã số thuế → ghi số định danh cá nhân nếu có.
- Gửi khách ngay sau khi có mã; máy tính tiền: cuối ngày dữ liệu tự gửi cơ quan thuế (Đ.15 k.3).
- Tạo **bảng kiểm** cho người dùng điền trước khi bấm lập: người mua, mã số thuế/định danh, hàng, số lượng, đơn giá, thành tiền (cộng bằng code), ngày.

## 4. Hóa đơn sai

Hỏi sai ở đâu → tra bảng mục 5 của `references/quy-dinh-hoa-don.md`:
- Sai không ảnh hưởng thuế (tên, địa chỉ người mua…) → thông báo 04/SS-HĐĐT, không lập lại.
- Sai mã số thuế, hàng, số lượng, giá, tiền thuế → hóa đơn điều chỉnh **hoặc** thay thế; soạn sẵn dòng ghi chú "Điều chỉnh cho / Thay thế cho hóa đơn Mẫu số… ký hiệu… số… ngày…" với số liệu của người dùng.
- Ghi rõ phần này theo TT 91/2026 qua nguồn thứ cấp → **[cần kiểm tra]** trên hệ thống hoặc với nhà cung cấp hóa đơn.

## 5. Đầu ra

1. Kết luận: phải dùng / không phải dùng / nên dùng + loại phù hợp + căn cứ.
2. Hạn đăng ký (nếu có), các bước làm (đã kiểm tra giao diện ngày nào, nguồn).
3. Bảng kiểm lập hóa đơn hoặc cách sửa hóa đơn sai.
4. **Anh/chị tự làm:** đăng nhập, ký số, bấm lập/gửi. Skill không làm thay, không hỏi mật khẩu, OTP.
5. Câu chốt: "Đối chiếu quy định hiện hành và hỏi cơ quan thuế quản lý hoặc nhà cung cấp hóa đơn."
