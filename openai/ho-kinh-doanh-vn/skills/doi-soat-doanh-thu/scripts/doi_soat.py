#!/usr/bin/env python3
"""Đối soát doanh thu hộ kinh doanh từ sao kê + báo cáo sàn, cộng theo quý, so mốc.

Ví dụ:
  python3 doi_soat.py sao_ke.xlsx --cot-ngay "Ngày GD" --cot-noi-dung "Nội dung" --cot-tien "Ghi có" \
      --bao-cao-san doanh_thu_san.csv --cot-ngay-san "Ngày" --cot-tien-san "Doanh thu" --ra ket_qua.xlsx

- Chỉ xét tiền vào (số tiền > 0).
- Nếu file sao kê đã có cột "Nhóm" (do người dùng sửa sau lần chạy trước), giữ nguyên nhóm đó.
- Có báo cáo sàn: doanh thu sàn lấy theo báo cáo; tiền sàn chuyển về trong sao kê bị loại để tránh cộng trùng.
Cần: pip install pandas openpyxl
"""
import argparse
import re
import unicodedata

import pandas as pd

MOC_1, MOC_2 = 1_000_000_000, 3_000_000_000  # NĐ 141/2026, NĐ 68/2026 — kiểm tra hiện hành

NHOM = {
    "san": ("Tiền sàn chuyển về", ["shopee", "tiktok", "lazada", "tiki", "sendo"]),
    "noi_bo": ("Chuyển nội bộ", ["noi bo", "tu tk ca nhan", "chuyen tien tu tk", "tk cua toi", "chuyen tu tai khoan"]),
    "vay_no": ("Vay hoặc trả nợ", ["vay", "tra no", "gop von", "hoan tien", "hoan tra", "tra lai tien"]),
    "ban_hang": ("Tiền bán hàng", ["mua hang", "thanh toan don", "tt don", "don hang", "tien hang", "thanh toan hd", "coc don"]),
}
CHUA_RO = "Chưa rõ"


def khong_dau(s):
    s = unicodedata.normalize("NFD", str(s).lower()).replace("đ", "d")
    return re.sub(r"\s+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def so_tien(v):
    if pd.isna(v):
        return 0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(" ", "")
    if re.fullmatch(r"-?[\d.]+(,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0


def doc(path):
    return pd.read_csv(path) if path.lower().endswith(".csv") else pd.read_excel(path)


def phan_loai(noi_dung):
    nd = khong_dau(noi_dung)
    for key, (ten, tu_khoa) in NHOM.items():
        for t in tu_khoa:
            if t in nd:
                return ten, f'Nội dung có "{t}"'
    return CHUA_RO, "Không đủ thông tin trong nội dung chuyển khoản"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sao_ke")
    ap.add_argument("--cot-ngay", required=True)
    ap.add_argument("--cot-noi-dung", required=True)
    ap.add_argument("--cot-tien", required=True)
    ap.add_argument("--bao-cao-san")
    ap.add_argument("--cot-ngay-san")
    ap.add_argument("--cot-tien-san")
    ap.add_argument("--nam", type=int)
    ap.add_argument("--ra", default="ket_qua_doi_soat.xlsx")
    a = ap.parse_args()

    df = doc(a.sao_ke)
    df["_ngay"] = pd.to_datetime(df[a.cot_ngay], dayfirst=True, errors="coerce")
    df["_tien"] = df[a.cot_tien].map(so_tien)
    df = df[df["_tien"] > 0].copy()
    if "Nhóm" in df.columns:
        df["Lý do"] = df.get("Lý do", "Người dùng xác nhận")
    else:
        kq = df[a.cot_noi_dung].map(phan_loai)
        df["Nhóm"] = kq.map(lambda x: x[0])
        df["Lý do"] = kq.map(lambda x: x[1])
    nam = a.nam or int(df["_ngay"].dt.year.mode().iloc[0])
    df = df[df["_ngay"].dt.year == nam]
    df["Quý"] = df["_ngay"].dt.quarter

    truc_tiep = df[df["Nhóm"] == "Tiền bán hàng"].groupby("Quý")["_tien"].sum()
    if a.bao_cao_san:
        san = doc(a.bao_cao_san)
        san["_ngay"] = pd.to_datetime(san[a.cot_ngay_san], dayfirst=True, errors="coerce")
        san["_tien"] = san[a.cot_tien_san].map(so_tien)
        san = san[san["_ngay"].dt.year == nam]
        dt_san = san.groupby(san["_ngay"].dt.quarter)["_tien"].sum()
        ghi_chu_san = "Doanh thu sàn lấy theo báo cáo sàn; tiền sàn chuyển về trong sao kê đã loại để tránh cộng trùng."
    else:
        dt_san = df[df["Nhóm"] == "Tiền sàn chuyển về"].groupby("Quý")["_tien"].sum()
        ghi_chu_san = ("CHƯA có báo cáo sàn: tạm dùng tiền sàn chuyển về (đã trừ phí sàn, thấp hơn doanh thu thật). "
                       "Nên bổ sung báo cáo doanh thu từ sàn.")

    rows, luy_ke, vuot = [], 0, None
    for q in range(1, 5):
        a1, a2 = float(truc_tiep.get(q, 0)), float(dt_san.get(q, 0))
        luy_ke += a1 + a2
        if vuot is None and luy_ke > MOC_1:
            vuot = q
        rows.append({"Quý": f"Quý {q}", "Bán hàng trực tiếp": a1, "Doanh thu sàn": a2,
                     "Cộng quý": a1 + a2, "Lũy kế": luy_ke})
    theo_quy = pd.DataFrame(rows)
    if luy_ke > MOC_2:
        trang_thai = "Trên 3 tỷ: thuế TNCN tính theo thu nhập tính thuế (NĐ 68/2026)."
    elif luy_ke > MOC_1:
        trang_thai = f"Trên 1 tỷ từ Quý {vuot}: khai thuế từ quý này; bắt buộc hóa đơn điện tử (NĐ 141/2026)."
    else:
        trang_thai = f"Từ 1 tỷ trở xuống: còn {MOC_1 - luy_ke:,.0f} đồng nữa đến mốc 1 tỷ.".replace(",", ".")

    chua_ro = df[df["Nhóm"] == CHUA_RO]
    giao_dich = df.drop(columns=["_ngay", "_tien"])
    with pd.ExcelWriter(a.ra, engine="openpyxl") as w:
        theo_quy.to_excel(w, sheet_name="Theo quý", index=False)
        pd.DataFrame({"Ghi chú": [f"Năm {nam}", trang_thai, ghi_chu_san,
                                  "Chỉ để tham khảo. Đối chiếu quy định hiện hành và hỏi cơ quan thuế."]}).to_excel(
            w, sheet_name="Theo quý", index=False, startrow=7)
        giao_dich.to_excel(w, sheet_name="Giao dịch", index=False)
        chua_ro.drop(columns=["_ngay", "_tien"]).to_excel(w, sheet_name="Chưa rõ", index=False)
        for ws in w.book.worksheets:
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = 22
        for row in w.book["Theo quý"].iter_rows(min_row=2, max_row=5, min_col=2, max_col=5):
            for c in row:
                c.number_format = "#,##0"

    print(theo_quy.to_string(index=False, float_format=lambda x: f"{x:,.0f}".replace(",", ".")))
    print(trang_thai)
    print(ghi_chu_san)
    print(f"Giao dịch chưa rõ: {len(chua_ro)} (xem tab 'Chưa rõ'). Đã lưu {a.ra}")


if __name__ == "__main__":
    main()
