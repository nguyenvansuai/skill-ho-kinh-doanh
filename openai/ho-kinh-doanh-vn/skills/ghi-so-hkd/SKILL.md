---
name: ghi-so-hkd
description: Ghi sổ doanh thu đủ 3 nguồn cho hộ kinh doanh Việt Nam — tiền mặt (ảnh sổ ghi tay, hóa đơn), sao kê ngân hàng và ví MoMo, báo cáo doanh thu sàn TMĐT — loại tiền nội bộ, tiền vay và tiền sàn chuyển về để không cộng trùng, chuyển thành sổ S1a-HKD (doanh thu từ 1 tỷ trở xuống) hoặc S2a-HKD (trên 1 tỷ, theo nhóm ngành) theo Thông tư 152/2025/TT-BTC, đánh dấu [?] chỗ chữ mờ, cộng theo tháng/quý, xuất file Excel có công thức. Dùng khi người dùng nói "ghi sổ", "chụp sổ bán hàng", "làm sổ doanh thu", "sổ S1a", "sổ S2a", "chuyển sổ tay sang Excel", "sổ sách hộ kinh doanh", "ghi sổ từ sao kê".
---

# Ghi sổ doanh thu hộ kinh doanh

Đọc `references/nguyen-tac-chung.md` và `references/quy-dinh-thue-hkd-2026.md` (mục 4: sổ kế toán).

## 1. Chọn sổ

| Doanh thu năm (ước tính) | Sổ |
|---|---|
| Từ 1 tỷ đồng trở xuống | S1a-HKD |
| Trên 1 tỷ, nộp thuế theo tỷ lệ % trên doanh thu | S2a-HKD, mỗi dòng gắn nhóm ngành nghề |
| Trên 3 tỷ, hoặc tính TNCN theo thu nhập | Bộ S2b–S2e-HKD: báo người dùng skill này chưa hỗ trợ, khuyên dùng phần mềm kế toán |

Người dùng chưa nói doanh thu năm → hỏi một câu: "Doanh thu cả năm của anh/chị khoảng bao nhiêu?" Nếu không trả lời được, mặc định S1a và ghi rõ giả định.

Câu lệnh ngắn là đủ, ví dụ "Ghi sổ giúp tôi từ 3 file này, cả năm khoảng 500 triệu" kèm ảnh sổ tay, sao kê, báo cáo sàn. Không yêu cầu người dùng gõ lại quy tắc: skill tự áp dụng mục 2–3 dưới đây.

## 2. Đọc dữ liệu đầu vào – đủ 3 nguồn

Sổ doanh thu phải ghi **toàn bộ** tiền bán hàng (NĐ 68/2026 Đ.5 k.1). Hỏi người dùng còn thiếu nguồn nào:

| Nguồn | Dữ liệu | Mã nguồn trong Diễn giải |
|---|---|---|
| 1. Tiền mặt | Ảnh sổ ghi tay, hóa đơn, phiếu bán hàng | `[TM]` |
| 2. Tài khoản bán lẻ | Sao kê ngân hàng và lịch sử ví MoMo/ZaloPay (file Excel/CSV) | `[CK]`, `[MoMo]` |
| 3. Sàn TMĐT | **Báo cáo doanh thu của sàn** (giá bán, đơn hoàn thành) | `[Sàn]` |

Quy tắc **không cộng trùng, không sót**:
- Doanh thu sàn lấy theo **báo cáo sàn**, không lấy tiền sàn chuyển về (tiền về là tiền đã trừ phí, thuế sàn khấu trừ, gộp nhiều đơn).
- Tài khoản nhận tiền sàn **gộp chung** tài khoản bán lẻ → các dòng sao kê "SHOPEE/TIKTOK/LAZADA thanh toán" phải **loại ra**, ghi lý do "tiền sàn về, đã ghi theo báo cáo sàn". Khuyên người dùng dùng 1 tài khoản riêng nhận tiền sàn.
- Loại khỏi doanh thu: chuyển từ tài khoản cá nhân, chuyển giữa các tài khoản của chủ hộ, tiền vay, góp vốn, hoàn tiền. Dòng không rõ → để "Chưa rõ", hỏi người dùng, **không tự cộng**.
- Khoản chuyển khoản đã được ghi trong sổ tay (cùng ngày, cùng số tiền) → chỉ ghi một lần, đánh dấu "nghi trùng" để người dùng xác nhận.
- Bán chịu: ghi doanh thu ngày giao hàng dù chưa thu tiền (NĐ 68/2026 Đ.5 k.3); hỏi nếu người dùng có bán chịu.
- Sao kê nhiều giao dịch: dùng `scripts` của skill `doi-soat-doanh-thu` nếu có, hoặc tự phân loại bằng Python.

Đọc từng nguồn:
- Ảnh sổ tay, hóa đơn, bảng kê: đọc **từng dòng theo đúng thứ tự**, không gộp, không sắp lại.
- Mỗi dòng lấy: ngày, diễn giải (ngắn gọn, giữ tên hàng), số tiền. S2a lấy thêm số hiệu chứng từ nếu có.
- Chữ hoặc số mờ, bị che, viết tắt khó hiểu → ghi `[?]` ngay tại ô đó (ví dụ `2?0.000 [?]`), **không đoán**.
- Năm không ghi trên sổ → dùng năm người dùng nói; chưa nói thì hỏi.
- Dòng không phải doanh thu (tiền nhập hàng, chi phí, ghi chú cá nhân) → để riêng ở mục "Dòng đã bỏ ra", nêu lý do.

## 3. Tính toán

- Cộng theo tháng, theo quý và lũy kế năm bằng Python (`scripts/tao_so_doanh_thu.py` khi xuất file). Dòng có `[?]` không đưa vào tổng; báo "Tổng các dòng đọc rõ" và số dòng chờ xác nhận.
- So lũy kế với mốc 1 tỷ và 3 tỷ (`references/quy-dinh-thue-hkd-2026.md`, mục 2). Chỉ nêu trạng thái, không tính số thuế phải nộp.

## 4. Đầu ra

1. Bảng Markdown: `Ngày | Diễn giải | Số tiền`, Diễn giải mở đầu bằng mã nguồn (`[TM]`, `[CK]`, `[MoMo]`, `[Sàn]`); S2a thêm `Số hiệu | Nhóm ngành`. Giữ đúng 3 cột của mẫu sổ, không thêm cột.
2. Tổng theo tháng, lũy kế, **tổng theo từng nguồn**, trạng thái so với mốc doanh thu.
3. Bảng **Cần anh/chị kiểm tra**: các ô `[?]`, dòng nghi trùng, dòng Chưa rõ, dòng đã loại (nội bộ, vay, tiền sàn về) kèm lý do.
4. Khi đã biết doanh thu năm: thêm mục **Việc anh/chị cần làm** lấy đúng danh sách A hoặc B ở mục 3a của `references/quy-dinh-thue-hkd-2026.md`, giữ nguyên căn cứ (văn bản, điều, khoản). Không thêm việc ngoài danh sách.
5. Người dùng cần file Excel: lưu dữ liệu đã xác nhận ra CSV (cột `ngay,dien_giai,so_tien` cho S1a; thêm `so_hieu,nhom_nganh` cho S2a), rồi chạy:

```bash
python3 scripts/tao_so_doanh_thu.py so_doanh_thu.xlsx --csv du_lieu.csv --so S1a --nam 2026
```

Không có dữ liệu thì bỏ `--csv` để tạo sổ trống. File có các tab Hướng dẫn, S1a-HKD, S2a-HKD, Tổng hợp với công thức Excel thật.

## 5. Lưu ý

- Sổ do hộ kinh doanh tự lập theo mẫu Thông tư 152/2025; skill chỉ hỗ trợ ghi chép. Người đại diện hộ kiểm tra, ký.
- Ngày định dạng `dd/mm/yyyy`, số tiền `1.250.000`.
