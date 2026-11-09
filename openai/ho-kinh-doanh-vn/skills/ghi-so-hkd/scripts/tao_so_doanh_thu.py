from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
"""Tạo file Excel sổ doanh thu hộ kinh doanh (S1a-HKD, S2a-HKD, Tổng hợp).

Dùng:
  python3 tao_so_doanh_thu.py so_doanh_thu.xlsx                      # sổ trống
  python3 tao_so_doanh_thu.py so.xlsx --csv du_lieu.csv --so S1a --nam 2026
CSV S1a: ngay,dien_giai,so_tien   (ngay dạng dd/mm/yyyy hoặc yyyy-mm-dd)
CSV S2a: so_hieu,ngay,dien_giai,nhom_nganh,so_tien
Cần: pip install openpyxl
"""
import argparse, csv, datetime as _dt

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--csv")
ap.add_argument("--so", choices=["S1a", "S2a"], default="S1a")
ap.add_argument("--nam", type=int, default=_dt.date.today().year)
ARGS = ap.parse_args()
OUT = ARGS.out
N = 500  # data rows per book

F = "Arial"
def font(**k): return Font(name=F, size=k.pop("size", 11), **k)
YELLOW = PatternFill("solid", fgColor="FFF4C2")
HEAD = PatternFill("solid", fgColor="12304A")
SUB = PatternFill("solid", fgColor="E7F7F5")
GREY = PatternFill("solid", fgColor="F1F5F8")
thin = Side(style="thin", color="CBD5E1")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
MONEY = '#,##0;-#,##0;"-"'

wb = Workbook()

# ------------------------------------------------------------------ Hướng dẫn
hd = wb.active
hd.title = "Hướng dẫn"
hd.column_dimensions["A"].width = 26
hd.column_dimensions["B"].width = 90
r = 1
def line(a, b="", bold=False, fill=None, size=11, color="102A43"):
    global r
    hd.cell(r, 1, a).font = font(bold=True, size=size, color=color)
    c = hd.cell(r, 2, b); c.font = font(bold=bold, size=size, color=color); c.alignment = WRAP
    if fill:
        hd.cell(r, 1).fill = fill; hd.cell(r, 2).fill = fill
    r += 1

line("SỔ DOANH THU HỘ KINH DOANH – MẪU EXCEL", size=16, color="12304A")
line("Quà tặng từ Sự AI · Chuyên đề Thuế HKD 2026 · MBV Tây Sài Gòn", size=10, color="52606D")
r += 1
line("1. DÙNG SỔ NÀO?", bold=True, fill=SUB)
line("Doanh thu từ 1 tỷ đồng/năm trở xuống", "Ghi vào tab S1a-HKD. Không phải nộp thuế GTGT, TNCN (Nghị định 141/2026/NĐ-CP).")
line("Trên 1 tỷ, nộp thuế theo tỷ lệ % trên doanh thu", "Ghi vào tab S2a-HKD, chọn nhóm ngành nghề cho từng dòng.")
line("Trên 3 tỷ, hoặc tính TNCN theo thu nhập", "Phải dùng bộ sổ S2b, S2c, S2d, S2e-HKD. File này chưa bao gồm các sổ đó.")
r += 1
line("2. CÁCH GHI", bold=True, fill=SUB)
line("Bước 1", "Điền thông tin hộ kinh doanh ở các ô màu vàng đầu sổ (tên, địa chỉ, mã số thuế, năm).")
line("Bước 2", "Mỗi lần bán hàng hoặc cuối ngày: ghi 1 dòng gồm ngày, diễn giải, số tiền. Ngày nhập dạng dd/mm/yyyy.")
line("Bước 3", "Xem tab Tổng hợp: doanh thu theo tháng, theo quý, lũy kế cả năm và trạng thái so với mốc 1 tỷ, 3 tỷ.")
line("Ô màu vàng", "Là ô bạn được điền. Các ô khác có công thức, không cần sửa.")
r += 1
line("3. DÒNG VÍ DỤ", bold=True, fill=SUB)
ex = [("Ngày, tháng", "01/10/2026"), ("Diễn giải", "Bán sữa rửa mặt (3 hộp)"), ("Số tiền", "450.000")]
for a, b in ex:
    line(a, b, color="52606D")
r += 1
line("4. DÙNG CÙNG AI", bold=True, fill=SUB)
line("Câu lệnh gợi ý", "“Đây là ảnh sổ bán hàng của tôi. Hãy chuyển thành bảng gồm 3 cột: Ngày, Diễn giải, Số tiền, để tôi dán vào sổ S1a-HKD. Chỗ nào chữ mờ hoặc không chắc, đánh dấu [?], không được tự đoán.”")
line("Lưu ý", "Che số tài khoản, số CCCD trước khi chụp gửi cho AI. Luôn kiểm lại số liệu AI trả về.")
r += 1
line("5. CĂN CỨ VÀ GIỚI HẠN", bold=True, fill=SUB)
line("Căn cứ", "Mẫu sổ S1a-HKD, S2a-HKD theo Thông tư 152/2025/TT-BTC (hiệu lực 01/01/2026). Mốc 1 tỷ theo Nghị định 141/2026/NĐ-CP (hiệu lực 01/01/2026). Mốc 3 tỷ theo Nghị định 68/2026/NĐ-CP.")
line("Giới hạn", "Đây là mẫu tham khảo do Sự AI dựng lại theo cấu trúc sổ của Thông tư 152/2025; tab S2a có thêm cột Nhóm ngành nghề để cộng riêng từng nhóm. File không tính số thuế phải nộp: số thuế khai theo tờ khai của cơ quan thuế. Đối chiếu phụ lục Thông tư 152/2025 và hỏi cơ quan thuế quản lý trước khi sử dụng chính thức.")
hd.sheet_view.showGridLines = False


def book_header(ws, code, title, cols):
    ws.sheet_view.showGridLines = False
    labels = ["HỘ, CÁ NHÂN KINH DOANH:", "Địa chỉ:", "Mã số thuế:"]
    for i, lb in enumerate(labels, 1):
        ws.cell(i, 1, lb).font = font(bold=True)
        c = ws.cell(i, 2); c.fill = YELLOW; c.border = BOX; c.font = font(color="0000FF")
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=cols)
    ws.merge_cells(start_row=5, start_column=1, end_row=5, end_column=cols)
    c = ws.cell(5, 1, "SỔ DOANH THU BÁN HÀNG HÓA, DỊCH VỤ"); c.font = font(bold=True, size=14, color="12304A"); c.alignment = CENTER
    ws.merge_cells(start_row=6, start_column=1, end_row=6, end_column=cols)
    c = ws.cell(6, 1, f"Mẫu số {code} (tham khảo Thông tư 152/2025/TT-BTC)"); c.font = font(italic=True, size=10, color="52606D"); c.alignment = CENTER
    ws.cell(7, 1, "Địa điểm kinh doanh:").font = font(bold=True)
    c = ws.cell(7, 2); c.fill = YELLOW; c.border = BOX; c.font = font(color="0000FF")
    ws.merge_cells(start_row=7, start_column=2, end_row=7, end_column=cols)
    ws.cell(8, 1, "Năm:").font = font(bold=True)


def head_row(ws, row, names, syms):
    for j, (n, s) in enumerate(zip(names, syms), 1):
        c = ws.cell(row, j, n); c.font = font(bold=True, color="FFFFFF"); c.fill = HEAD; c.alignment = CENTER; c.border = BOX
        c = ws.cell(row + 1, j, s); c.font = font(italic=True, size=9, color="52606D"); c.fill = GREY; c.alignment = CENTER; c.border = BOX
    ws.row_dimensions[row].height = 32


def sign(ws, row, cols):
    ws.merge_cells(start_row=row, start_column=cols - 1, end_row=row, end_column=cols)
    c = ws.cell(row, cols - 1, "Ngày ..... tháng ..... năm ......"); c.font = font(italic=True); c.alignment = CENTER
    ws.merge_cells(start_row=row + 1, start_column=cols - 1, end_row=row + 1, end_column=cols)
    c = ws.cell(row + 1, cols - 1, "NGƯỜI ĐẠI DIỆN HỘ KINH DOANH / CÁ NHÂN KINH DOANH"); c.font = font(bold=True); c.alignment = CENTER
    ws.merge_cells(start_row=row + 2, start_column=cols - 1, end_row=row + 2, end_column=cols)
    c = ws.cell(row + 2, cols - 1, "(Ký, họ tên, đóng dấu nếu có)"); c.font = font(italic=True, size=10, color="52606D"); c.alignment = CENTER


# ------------------------------------------------------------------ S1a-HKD
s1 = wb.create_sheet("S1a-HKD")
book_header(s1, "S1a-HKD", "", 3)
c = s1.cell(8, 2, ARGS.nam); c.fill = YELLOW; c.border = BOX; c.font = font(color="0000FF"); c.alignment = Alignment(horizontal="left")
for col, w in zip("ABC", (18, 64, 22)):
    s1.column_dimensions[col].width = w
head_row(s1, 10, ["Ngày, tháng", "Diễn giải", "Số tiền (đồng)"], ["A", "B", "1"])
D0, D1 = 12, 12 + N - 1
for rr in range(D0, D1 + 1):
    for j in range(1, 4):
        c = s1.cell(rr, j); c.border = BOX; c.font = font(color="0000FF")
    s1.cell(rr, 1).number_format = "dd/mm/yyyy"
    s1.cell(rr, 3).number_format = MONEY
T1 = D1 + 1
s1.cell(T1, 1, "").border = BOX
c = s1.cell(T1, 2, "Tổng cộng"); c.font = font(bold=True); c.border = BOX; c.fill = SUB
c = s1.cell(T1, 3, f"=SUM(C{D0}:C{D1})"); c.font = font(bold=True); c.number_format = MONEY; c.border = BOX; c.fill = SUB
sign(s1, T1 + 2, 3)
s1.freeze_panes = "A12"
s1["C10"].comment = Comment("Tổng số tiền thanh toán của hàng hóa, dịch vụ bán ra.", "Sự AI")

# ------------------------------------------------------------------ S2a-HKD
s2 = wb.create_sheet("S2a-HKD")
book_header(s2, "S2a-HKD", "", 5)
c = s2.cell(8, 2, "='S1a-HKD'!B8"); c.font = font(color="008000"); c.alignment = Alignment(horizontal="left")
for col, w in zip("ABCDE", (14, 16, 48, 44, 20)):
    s2.column_dimensions[col].width = w
head_row(s2, 10, ["Số hiệu chứng từ", "Ngày, tháng", "Diễn giải", "Nhóm ngành nghề", "Số tiền (đồng)"], ["A", "B", "C", "(bổ sung)", "1"])
GROUPS = [
    "Phân phối, cung cấp hàng hóa",
    "Dịch vụ, xây dựng không bao thầu nguyên vật liệu",
    "Sản xuất, vận tải, dịch vụ gắn với hàng hóa, xây dựng có bao thầu nguyên vật liệu",
    "Cho thuê tài sản",
    "Hoạt động kinh doanh khác",
]
# group list lives on Tổng hợp (validation source)
for rr in range(D0, D1 + 1):
    for j in range(1, 6):
        c = s2.cell(rr, j); c.border = BOX; c.font = font(color="0000FF")
    s2.cell(rr, 2).number_format = "dd/mm/yyyy"
    s2.cell(rr, 5).number_format = MONEY
T2 = D1 + 1
for j in range(1, 6):
    s2.cell(T2, j).border = BOX; s2.cell(T2, j).fill = SUB
s2.cell(T2, 3, "Tổng cộng").font = font(bold=True)
c = s2.cell(T2, 5, f"=SUM(E{D0}:E{D1})"); c.font = font(bold=True); c.number_format = MONEY
g0 = T2 + 2
s2.cell(g0, 3, "Cộng theo nhóm ngành nghề").font = font(bold=True, color="12304A")
for i, g in enumerate(GROUPS):
    rr = g0 + 1 + i
    c = s2.cell(rr, 4, g); c.border = BOX; c.font = font(); c.alignment = WRAP
    c = s2.cell(rr, 5, f'=SUMIFS($E${D0}:$E${D1},$D${D0}:$D${D1},D{rr})'); c.number_format = MONEY; c.border = BOX; c.font = font()
s2.cell(g0 + 7, 3, "Thuế GTGT, TNCN phải nộp: khai theo tờ khai 01/CNKD (Thông tư 18/2026/TT-BTC), không tính trong file này.").font = font(italic=True, size=10, color="52606D")
sign(s2, g0 + 9, 5)
s2.freeze_panes = "A12"
dv = DataValidation(type="list", formula1=f"=$D${g0+1}:$D${g0+5}", allow_blank=True)
dv.error = "Chọn một nhóm ngành nghề trong danh sách"; dv.errorTitle = "Nhóm ngành nghề"
s2.add_data_validation(dv); dv.add(f"D{D0}:D{D1}")
s2["D10"].comment = Comment("Cột bổ sung để cộng riêng từng nhóm ngành có cùng tỷ lệ thuế (Thông tư 152/2025 cho phép bổ sung nội dung vào mẫu sổ).", "Sự AI")

# ------------------------------------------------------------------ Tổng hợp
th = wb.create_sheet("Tổng hợp")
th.sheet_view.showGridLines = False
for col, w in zip("ABCDEF", (14, 20, 20, 20, 20, 10)):
    th.column_dimensions[col].width = w
th["A1"] = "TỔNG HỢP DOANH THU THEO THÁNG, QUÝ"; th["A1"].font = font(bold=True, size=14, color="12304A")
th["A2"] = "Năm:"; th["A2"].font = font(bold=True)
th["B2"] = "='S1a-HKD'!B8"; th["B2"].font = font(color="008000"); th["B2"].alignment = Alignment(horizontal="left")
th["A3"] = "Mốc 1:"; th["A3"].font = font(bold=True)
th["B3"] = 1_000_000_000; th["B3"].number_format = MONEY; th["B3"].fill = YELLOW; th["B3"].font = font(color="0000FF")
th["C3"] = "Nghị định 141/2026/NĐ-CP: từ 1 tỷ trở xuống không nộp thuế GTGT, TNCN; trên 1 tỷ bắt buộc hóa đơn điện tử."
th["A4"] = "Mốc 2:"; th["A4"].font = font(bold=True)
th["B4"] = 3_000_000_000; th["B4"].number_format = MONEY; th["B4"].fill = YELLOW; th["B4"].font = font(color="0000FF")
th["C4"] = "Nghị định 68/2026/NĐ-CP: trên 3 tỷ tính thuế TNCN theo thu nhập tính thuế × thuế suất."
for a in ("C3", "C4"):
    th[a].font = font(size=9, color="52606D")

hr = 6
heads = ["Tháng", "Doanh thu S1a", "Doanh thu S2a", "Cộng tháng", "Lũy kế năm", "Vượt mốc 1"]
for j, h in enumerate(heads, 1):
    c = th.cell(hr, j, h); c.font = font(bold=True, color="FFFFFF"); c.fill = HEAD; c.alignment = CENTER; c.border = BOX
S1D, S1A = f"'S1a-HKD'!$A${D0}:$A${D1}", f"'S1a-HKD'!$C${D0}:$C${D1}"
S2D, S2A = f"'S2a-HKD'!$B${D0}:$B${D1}", f"'S2a-HKD'!$E${D0}:$E${D1}"
for m in range(1, 13):
    rr = hr + m
    th.cell(rr, 1, m)
    th.cell(rr, 2, f'=SUMIFS({S1A},{S1D},">="&DATE($B$2,A{rr},1),{S1D},"<"&DATE($B$2,A{rr}+1,1))')
    th.cell(rr, 3, f'=SUMIFS({S2A},{S2D},">="&DATE($B$2,A{rr},1),{S2D},"<"&DATE($B$2,A{rr}+1,1))')
    th.cell(rr, 4, f"=B{rr}+C{rr}")
    th.cell(rr, 5, f"=D{rr}" if m == 1 else f"=E{rr-1}+D{rr}")
    th.cell(rr, 6, f"=IF(E{rr}>$B$3,1,0)")
    for j in range(1, 7):
        c = th.cell(rr, j); c.border = BOX; c.font = font()
        if 2 <= j <= 5: c.number_format = MONEY
        if j in (1, 6): c.alignment = Alignment(horizontal="center")
M0, M1 = hr + 1, hr + 12

qr = M1 + 2
for j, h in enumerate(["Quý", "Doanh thu quý", "Lũy kế đến hết quý"], 1):
    c = th.cell(qr, j, h); c.font = font(bold=True, color="FFFFFF"); c.fill = HEAD; c.alignment = CENTER; c.border = BOX
for q in range(1, 5):
    rr = qr + q
    a, b = M0 + (q - 1) * 3, M0 + q * 3 - 1
    th.cell(rr, 1, f"Quý {q}")
    th.cell(rr, 2, f"=SUM(D{a}:D{b})")
    th.cell(rr, 3, f"=E{b}")
    for j in range(1, 4):
        c = th.cell(rr, j); c.border = BOX; c.font = font()
        if j > 1: c.number_format = MONEY

sr = qr + 6
th.cell(sr, 1, "Tổng cả năm:").font = font(bold=True)
c = th.cell(sr, 2, f"=E{M1}"); c.number_format = MONEY; c.font = font(bold=True)
th.cell(sr + 1, 1, "Vượt 1 tỷ từ:").font = font(bold=True)
th.cell(sr + 1, 2, f'=IFERROR("Tháng "&MATCH(1,F{M0}:F{M1},0)&" (Quý "&ROUNDUP(MATCH(1,F{M0}:F{M1},0)/3,0)&")","Chưa vượt")').font = font(bold=True)
th.cell(sr + 2, 1, "Trạng thái:").font = font(bold=True)
th.merge_cells(start_row=sr + 2, start_column=2, end_row=sr + 3, end_column=6)
c = th.cell(sr + 2, 2, (f'=IF(B{sr}>$B$4,"Trên 3 tỷ: tính thuế TNCN theo thu nhập tính thuế, dùng bộ sổ S2b–S2e-HKD.",'
                         f'IF(B{sr}>$B$3,"Trên 1 tỷ: khai thuế từ quý phát sinh vượt mốc; bắt buộc hóa đơn điện tử (đăng ký trong 30 ngày).",'
                         f'"Từ 1 tỷ trở xuống: không phải nộp thuế GTGT, TNCN; vẫn thông báo doanh thu theo hướng dẫn của cơ quan thuế."))'))
c.font = font(bold=True, color="12304A"); c.fill = SUB; c.alignment = WRAP
th.row_dimensions[sr + 2].height = 22
th.cell(sr + 5, 1, "Trạng thái chỉ để tham khảo nhanh. Nghĩa vụ cụ thể: đối chiếu Nghị định 68/2026, Nghị định 141/2026 và hỏi cơ quan thuế quản lý.").font = font(italic=True, size=9, color="52606D")

for ws in wb.worksheets:
    ws.sheet_properties.tabColor = {"Hướng dẫn": "18A7A0", "S1a-HKD": "1B6BC0", "S2a-HKD": "7B61FF", "Tổng hợp": "F08A24"}[ws.title]
    for row in ws.iter_rows():
        for c in row:
            if c.font is None or c.font.name != F:
                c.font = Font(name=F, size=c.font.size if c.font else 11, bold=c.font.bold if c.font else False,
                              italic=c.font.italic if c.font else False, color=c.font.color if c.font else None)
def _ngay(s):
    s = s.strip()
    for f in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return _dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    raise SystemExit(f"Ngày không đọc được: {s!r} (dùng dd/mm/yyyy)")

def _tien(s):
    return int(round(float(str(s).replace(".", "").replace(",", ".").replace(" ", "") or 0)))

if ARGS.csv:
    with open(ARGS.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) > N:
        raise SystemExit(f"Tối đa {N} dòng mỗi sổ, file có {len(rows)} dòng")
    for i, row in enumerate(rows):
        r = D0 + i
        if ARGS.so == "S1a":
            s1.cell(r, 1, _ngay(row["ngay"])); s1.cell(r, 2, row["dien_giai"]); s1.cell(r, 3, _tien(row["so_tien"]))
        else:
            s2.cell(r, 1, row.get("so_hieu", "")); s2.cell(r, 2, _ngay(row["ngay"])); s2.cell(r, 3, row["dien_giai"])
            s2.cell(r, 4, row.get("nhom_nganh", "")); s2.cell(r, 5, _tien(row["so_tien"]))
    print(f"Đã ghi {len(rows)} dòng vào {ARGS.so}-HKD")

wb.save(OUT)
print("Đã lưu", OUT)
