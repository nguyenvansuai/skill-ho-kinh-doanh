#!/usr/bin/env python3
"""Đối chiếu SỔ DOANH THU với sao kê (ngân hàng, ví) và báo cáo sàn: tìm chỗ sổ ghi sót, ghi thừa, lệch sàn.

Ví dụ:
  python3 doi_chieu_so.py so.csv sao_ke.xlsx --cot-ngay "Ngày GD" --cot-noi-dung "Nội dung" --cot-tien "Ghi có" \
      --bao-cao-san shopee.csv --cot-ngay-san "Ngày" --cot-tien-san "Doanh thu" --tu 01/07/2026 --den 30/09/2026

Sổ: cột ngay, dien_giai, so_tien (file CSV của skill ghi-so-hkd hoặc tab sổ xuất ra CSV).
     Diễn giải mở đầu bằng mã nguồn [TM], [CK], [MoMo], [Sàn].
Cách khớp: dòng sổ [CK]/[MoMo] khớp giao dịch sao kê cùng số tiền, lệch ngày tối đa --lech-ngay ngày.
Sao kê đã loại trước khi khớp: chuyển nội bộ, vay/trả nợ, tiền sàn chuyển về (doanh thu sàn so theo báo cáo sàn).
Kết quả chỉ là danh sách cần kiểm tra – người dùng xác nhận trước khi sửa sổ.
Cần: pip install pandas openpyxl
"""
import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doi_soat import CHUA_RO, MOC_1, doc, khong_dau, phan_loai, so_tien  # noqa: E402

LOAI_TRUOC = {"Chuyển nội bộ", "Vay hoặc trả nợ", "Tiền sàn chuyển về"}


def dong(x):
    return f"{x:,.0f}".replace(",", ".")


def nguon(dien_giai):
    d = khong_dau(dien_giai)
    for ma, key in (("CK", "[ck]"), ("MoMo", "[momo]"), ("Sàn", "[san]"), ("TM", "[tm]")):
        if d.startswith(key):
            return ma
    return "?"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("so")
    ap.add_argument("sao_ke")
    ap.add_argument("--cot-ngay", required=True)
    ap.add_argument("--cot-noi-dung", required=True)
    ap.add_argument("--cot-tien", required=True)
    ap.add_argument("--bao-cao-san")
    ap.add_argument("--cot-ngay-san")
    ap.add_argument("--cot-tien-san")
    ap.add_argument("--tu")
    ap.add_argument("--den")
    ap.add_argument("--lech-ngay", type=int, default=3)
    ap.add_argument("--ra", default="ket_qua_doi_chieu.xlsx")
    a = ap.parse_args()

    tu = pd.to_datetime(a.tu, dayfirst=True) if a.tu else None
    den = pd.to_datetime(a.den, dayfirst=True) if a.den else None

    def loc(df):
        if tu is not None:
            df = df[df["_ngay"] >= tu]
        if den is not None:
            df = df[df["_ngay"] <= den]
        return df

    so = doc(a.so)
    so["_ngay"] = pd.to_datetime(so["ngay"], dayfirst=True, errors="coerce")
    so["_tien"] = so["so_tien"].map(so_tien)
    so["Nguồn"] = so["dien_giai"].map(nguon)
    so_all = so.copy()
    so = loc(so)

    sk = doc(a.sao_ke)
    sk["_ngay"] = pd.to_datetime(sk[a.cot_ngay], dayfirst=True, errors="coerce")
    sk["_tien"] = sk[a.cot_tien].map(so_tien)
    sk = loc(sk[sk["_tien"] > 0].copy())
    kq = sk[a.cot_noi_dung].map(phan_loai)
    sk["Nhóm"] = kq.map(lambda x: x[0])
    ung_vien = sk[~sk["Nhóm"].isin(LOAI_TRUOC)].copy()
    ung_vien["_khop"] = False

    lech = []
    so_ck = so[so["Nguồn"].isin(["CK", "MoMo"])]
    for _, r in so_ck.iterrows():
        cand = ung_vien[(~ung_vien["_khop"]) & (ung_vien["_tien"] == r["_tien"])
                        & ((ung_vien["_ngay"] - r["_ngay"]).abs().dt.days <= a.lech_ngay)]
        if len(cand):
            ung_vien.loc[cand.index[0], "_khop"] = True
        else:
            lech.append({"Ngày": r["_ngay"].strftime("%d/%m"), "Loại lệch": "Sổ ghi chuyển khoản/ví, sao kê không có",
                         "Nội dung": r["dien_giai"], "Số tiền": r["_tien"],
                         "Gợi ý": "Khách trả tiền mặt (đổi nguồn [TM])? Ghi trùng? Hỏi người dùng"})
    for _, r in ung_vien[~ung_vien["_khop"]].iterrows():
        ro = r["Nhóm"] == CHUA_RO
        lech.append({"Ngày": r["_ngay"].strftime("%d/%m"), "Loại lệch": "Tiền vào tài khoản/ví, sổ chưa ghi",
                     "Nội dung": r[a.cot_noi_dung], "Số tiền": r["_tien"],
                     "Gợi ý": "Chưa rõ: hỏi có phải tiền bán hàng không" if ro else "Bổ sung vào sổ ([CK]/[MoMo])"})

    if a.bao_cao_san:
        san = doc(a.bao_cao_san)
        san["_ngay"] = pd.to_datetime(san[a.cot_ngay_san], dayfirst=True, errors="coerce")
        san["_tien"] = san[a.cot_tien_san].map(so_tien)
        san = loc(san)
        t_bc, t_so = san["_tien"].sum(), so[so["Nguồn"] == "Sàn"]["_tien"].sum()
        if abs(t_bc - t_so) >= 1:
            lech.append({"Ngày": "cả kỳ", "Loại lệch": "Doanh thu sàn: sổ khác báo cáo sàn",
                         "Nội dung": f"Sổ {dong(t_so)} · báo cáo {dong(t_bc)}", "Số tiền": t_bc - t_so,
                         "Gợi ý": "Thiếu đơn → bổ sung [Sàn]" if t_bc > t_so else "Sổ ghi thừa → kiểm tra đơn hủy/hoàn"})

    bang = pd.DataFrame(lech, columns=["Ngày", "Loại lệch", "Nội dung", "Số tiền", "Gợi ý"])
    so_all["Quý"] = so_all["_ngay"].dt.quarter
    theo_quy = so_all.groupby("Quý")["_tien"].sum()
    luy_ke = theo_quy.sum()

    with pd.ExcelWriter(a.ra, engine="openpyxl") as w:
        bang.to_excel(w, sheet_name="Chênh lệch", index=False)
        theo_quy.rename("Doanh thu trên sổ").to_frame().to_excel(w, sheet_name="Theo quý (sổ)")
        for ws in w.book.worksheets:
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = 26

    print(f"Đã khớp {int(ung_vien['_khop'].sum())} giao dịch sao kê với sổ. Chỗ lệch: {len(bang)}")
    for _, r in bang.iterrows():
        print(f"  {r['Ngày']:>6} | {r['Loại lệch']} | {r['Nội dung']} | {dong(r['Số tiền'])} | {r['Gợi ý']}")
    print("Doanh thu trên sổ theo quý: " + " · ".join(f"Q{q} {dong(v)}" for q, v in theo_quy.items())
          + f" · lũy kế {dong(luy_ke)}")
    print("Trên 1 tỷ" if luy_ke > MOC_1 else f"Chưa vượt 1 tỷ, còn {dong(MOC_1 - luy_ke)} (lũy kế theo sổ, trước khi sửa chỗ lệch).")
    print(f"Đã lưu {a.ra}. Người dùng xác nhận từng dòng trước khi sửa sổ.")


if __name__ == "__main__":
    main()
