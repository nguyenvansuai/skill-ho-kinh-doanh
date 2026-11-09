# Nạp văn bản pháp luật gốc để tra cứu sâu

Skill đã có sẵn bản tóm tắt `quy-dinh-thue-hkd-2026.md`. Khi cần trích nguyên văn điều khoản, nạp thêm văn bản gốc (thư mục `van-ban/` của repo, bản chữ lấy từ vbpl.vn).

## Claude (khuyên dùng)

1. Cài skill `hoi-dap-thue-hkd`: Settings › Capabilities › bật **Code execution and file creation**, rồi Customize › Skills › tải lên `dist/hoi-dap-thue-hkd.zip`.
2. Câu hỏi thông thường: hỏi luôn, skill tự dùng bản tóm tắt.
3. Cần nguyên văn: tạo **Project**, tải các file trong `van-ban/` vào phần Project knowledge (ưu tiên file 01 và 03 là văn bản hợp nhất), rồi hỏi trong Project đó.

## ChatGPT (bản miễn phí dùng Project)

Bản miễn phí không tạo được Custom GPT, nhưng dùng được **Project**:

1. Tạo Project mới, mở phần hướng dẫn (instructions) của Project.
2. Dán khối Instructions trong `chatgpt/hoi-dap-thue-hkd.md`.
3. Tải lên `quy-dinh-thue-hkd-2026.md`, `nguyen-tac-chung.md` và các file văn bản cần tra trong `van-ban/`.

## Câu hỏi mẫu

```
Tôi là hộ kinh doanh [ngành hàng], bán qua [cửa hàng, sàn, Facebook...], doanh thu khoảng [số tiền]/năm.
Tôi cần làm gì về hóa đơn, sổ sách và kê khai? Trả lời ngắn gọn, ghi rõ căn cứ (văn bản, điều, khoản) cho từng ý.
Nếu tài liệu không đề cập, hãy nói là không có thông tin.
```

## Lưu ý

- Không trộn tài liệu cũ còn ghi mốc 500 triệu đồng (đã thay bằng 1 tỷ từ 01/01/2026 theo Nghị định 141/2026).
- Văn bản ban hành sau 30/10/2026: tải thêm từ https://vbpl.vn.
- Luôn mở văn bản gốc để đối chiếu điều khoản AI dẫn trước khi làm theo.
