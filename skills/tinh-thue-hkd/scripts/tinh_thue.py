#!/usr/bin/env python3
"""Ước tính thuế GTGT, TNCN của hộ kinh doanh năm 2026 và so sánh 2 cách tính TNCN.

Căn cứ: Luật 48/2024/QH15 Đ.12 k.2 (tỷ lệ GTGT); Luật 109/2025/QH15 Đ.7 k.2, k.3 (TNCN);
NĐ 68/2026/NĐ-CP (VBHN 25/2026) Đ.3, Đ.4 k.3, k.5; mức 1 tỷ theo NĐ 141/2026/NĐ-CP.

Cách dùng:
  python3 tinh_thue.py --nganh hang_hoa=1200000000
  python3 tinh_thue.py --nganh hang_hoa=900000000 dich_vu=400000000 --chi-phi 950000000
  python3 tinh_thue.py --quy hang_hoa=250000000,300000000,320000000,330000000
  python3 tinh_thue.py --json dau_vao.json      # {"doanh_thu": {...}, "chi_phi": ..., "san_da_khau_tru": ...}

Nhóm ngành: hang_hoa, dich_vu, cho_thue_dai_ly, san_xuat_van_tai, noi_dung_so, khac.
Kết quả là ƯỚC TÍNH để đối chiếu; số chính thức do eTax tính trên tờ khai.
"""
import argparse
import json
import sys

MUC_TRU = 1_000_000_000      # NĐ 141/2026: mức doanh thu không chịu thuế, mức trừ TNCN
MOC_3_TY = 3_000_000_000
MOC_50_TY = 50_000_000_000

# (tên hiển thị, tỷ lệ GTGT, thuế suất TNCN trên doanh thu vượt mức trừ)
NGANH = {
    "hang_hoa": ("Phân phối, cung cấp hàng hóa", 0.01, 0.005),
    "dich_vu": ("Dịch vụ, xây dựng không bao thầu NVL", 0.05, 0.02),
    "cho_thue_dai_ly": ("Cho thuê tài sản (trừ BĐS), đại lý BH/xổ số/đa cấp", 0.05, 0.05),
    "san_xuat_van_tai": ("Sản xuất, vận tải, dịch vụ gắn hàng hóa, xây dựng bao thầu NVL", 0.03, 0.015),
    "noi_dung_so": ("Nội dung số (giải trí, game, phim, ảnh, nhạc, quảng cáo số)", 0.05, 0.05),
    "khac": ("Hoạt động kinh doanh khác", 0.02, 0.01),
}
CAN_KIEM_TRA = {
    "noi_dung_so": "Tỷ lệ GTGT 5% cho nội dung số là giả định xếp vào nhóm dịch vụ – cần kiểm tra.",
    "cho_thue_dai_ly": "Đại lý bán đúng giá: doanh nghiệp giao đại lý khấu trừ thuế (NĐ 68/2026 Đ.8 k.7) – kiểm tra trước khi tự khai.",
}


def dong(so):
    return f"{round(so):,}".replace(",", ".")


def phan_bo_muc_tru(dt):
    """Trừ 1 tỷ vào ngành có thuế suất TNCN cao nhất trước (phương án có lợi nhất, NĐ 68 Đ.4 k.3)."""
    con_lai = MUC_TRU
    tru = {k: 0 for k in dt}
    for k in sorted(dt, key=lambda k: NGANH[k][2], reverse=True):
        t = min(dt[k], con_lai)
        tru[k] = t
        con_lai -= t
    return tru


def tinh_nam(dt, chi_phi=None):
    tong = sum(dt.values())
    kq = {"tong_dt": tong, "dong": []}
    if tong <= MUC_TRU:
        kq["dien"] = "A"
        return kq
    tru = phan_bo_muc_tru(dt)
    gtgt = tncn_a = 0
    for k, v in dt.items():
        ten, r_gtgt, r_tncn = NGANH[k]
        g = v * r_gtgt
        t = (v - tru[k]) * r_tncn
        gtgt += g
        tncn_a += t
        kq["dong"].append((ten, v, r_gtgt, g, tru[k], r_tncn, t))
    kq.update(gtgt=gtgt, tncn_a=tncn_a)
    ts_b = 0.15 if tong <= MOC_3_TY else (0.17 if tong <= MOC_50_TY else 0.20)
    kq["ts_b"] = ts_b
    if chi_phi is not None:
        kq["thu_nhap"] = max(tong - chi_phi, 0)
        kq["tncn_b"] = kq["thu_nhap"] * ts_b
        # điểm hòa vốn: chi phí để 2 cách bằng nhau
        kq["chi_phi_hoa"] = tong - tncn_a / ts_b
    kq["dien"] = "B" if tong <= MOC_3_TY else "C"
    return kq


def tinh_quy(quy):
    """Thuế từng quý khi biết doanh thu từng quý (cách A, mức trừ trừ dần theo lũy kế)."""
    so_quy = max(len(v) for v in quy.values())
    luy_ke = {k: 0 for k in quy}
    da_tinh_tncn = 0
    ra = []
    vuot_tu = None
    for q in range(so_quy):
        for k, v in quy.items():
            luy_ke[k] += v[q] if q < len(v) else 0
        tong_lk = sum(luy_ke.values())
        if tong_lk > MUC_TRU and vuot_tu is None:
            vuot_tu = q + 1
        tru = phan_bo_muc_tru(luy_ke)
        tncn_lk = sum((luy_ke[k] - tru[k]) * NGANH[k][2] for k in quy)
        dt_q = sum((v[q] if q < len(v) else 0) for v in quy.values())
        gtgt_q = sum((v[q] if q < len(v) else 0) * NGANH[k][1] for k, v in quy.items()) if vuot_tu else 0
        ra.append((q + 1, dt_q, tong_lk, gtgt_q, tncn_lk - da_tinh_tncn))
        da_tinh_tncn = tncn_lk
    return ra, vuot_tu


def doc_cap(ds, nhieu=False):
    out = {}
    for s in ds or []:
        k, _, v = s.partition("=")
        if k not in NGANH:
            sys.exit(f"Nhóm ngành không hợp lệ: {k}. Dùng: {', '.join(NGANH)}")
        out[k] = [float(x) for x in v.split(",")] if nhieu else float(v)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nganh", nargs="*", help="nhom=doanh_thu_nam")
    ap.add_argument("--quy", nargs="*", help="nhom=q1,q2,q3,q4")
    ap.add_argument("--chi-phi", type=float, help="tổng chi phí được trừ cả năm (để so cách tính theo thu nhập)")
    ap.add_argument("--san-da-khau-tru", type=float, default=0, help="tổng thuế sàn TMĐT đã khấu trừ, nộp thay")
    ap.add_argument("--json")
    a = ap.parse_args()

    dt, quy, chi_phi, san = doc_cap(a.nganh), doc_cap(a.quy, True), a.chi_phi, a.san_da_khau_tru
    if a.json:
        d = json.load(open(a.json, encoding="utf-8"))
        for k, v in d.get("doanh_thu", {}).items():
            (quy if isinstance(v, list) else dt)[k] = v
        chi_phi = d.get("chi_phi", chi_phi)
        san = d.get("san_da_khau_tru", san)
    for k, v in quy.items():
        dt[k] = dt.get(k, 0) + sum(v)
    if not dt:
        ap.error("cần --nganh, --quy hoặc --json")

    kq = tinh_nam(dt, chi_phi)
    print(f"Tổng doanh thu năm: {dong(kq['tong_dt'])} đồng")
    if kq["dien"] == "A":
        print("→ Từ 1 tỷ trở xuống: KHÔNG nộp GTGT, TNCN (NĐ 68/2026 Đ.3 k.1, Đ.4 k.1). "
              "Chỉ thông báo doanh thu chậm nhất 31/01 năm sau.")
        if san:
            print(f"→ Sàn đã khấu trừ {dong(san)} đồng: được bù trừ/hoàn (NĐ 68/2026 Đ.12 k.1).")
        return
    print("\nCách 1 – TNCN theo tỷ lệ trên doanh thu vượt 1 tỷ (Luật 109/2025 Đ.7 k.3):")
    print(f"{'Ngành':58} {'Doanh thu':>16} {'GTGT':>12} {'Mức trừ':>15} {'TNCN':>12}")
    for ten, v, rg, g, tru, rt, t in kq["dong"]:
        print(f"{ten[:58]:58} {dong(v):>16} {dong(g):>9} {rg:>3.0%} {dong(tru):>15} {dong(t):>9} {rt:.1%}")
    tong_a = kq["gtgt"] + kq["tncn_a"]
    print(f"  GTGT {dong(kq['gtgt'])} + TNCN {dong(kq['tncn_a'])} = {dong(tong_a)} đồng")

    if "tncn_b" in kq:
        tong_b = kq["gtgt"] + kq["tncn_b"]
        print(f"\nCách 2 – TNCN theo thu nhập × {kq['ts_b']:.0%} (Luật 109/2025 Đ.7 k.2):")
        print(f"  Thu nhập = {dong(kq['tong_dt'])} − {dong(chi_phi)} = {dong(kq['thu_nhap'])}")
        print(f"  GTGT {dong(kq['gtgt'])} + TNCN {dong(kq['tncn_b'])} = {dong(tong_b)} đồng")
        if kq["dien"] == "B":
            re_hon = "Cách 2" if tong_b < tong_a else "Cách 1"
            print(f"\n→ {re_hon} thấp hơn {dong(abs(tong_a - tong_b))} đồng. "
                  f"Chi phí hòa vốn (2 cách bằng nhau): {dong(kq['chi_phi_hoa'])} đồng.")
            print("  Lưu ý: chọn Cách 2 phải giữ ổn định 2 năm liên tục, khai tạm nộp quý và quyết toán năm "
                  "(NĐ 68/2026 Đ.4 k.5 điểm d, Đ.10 k.2); chi phí phải có hóa đơn, chứng từ (Đ.6).")
    if kq["dien"] == "C":
        print("\n→ Trên 3 tỷ: BẮT BUỘC tính TNCN theo thu nhập (Cách 2), quyết toán năm (NĐ 68/2026 Đ.4 k.5 điểm b)."
              + ("" if chi_phi is not None else " Cần --chi-phi để tính."))
    if san:
        print(f"\nThuế sàn đã khấu trừ, nộp thay: {dong(san)} đồng – không phải nộp lại "
              "(Luật 108/2025 Đ.12 k.3 điểm c; NĐ 68/2026 Đ.11 k.3).")
    for k in dt:
        if k in CAN_KIEM_TRA:
            print("[cần kiểm tra] " + CAN_KIEM_TRA[k])

    if quy:
        ra, vuot = tinh_quy(quy)
        print("\nTheo quý (Cách 1, mức trừ 1 tỷ trừ dần theo lũy kế):")
        print(f"{'Quý':>4} {'Doanh thu quý':>16} {'Lũy kế':>16} {'GTGT':>12} {'TNCN':>12}")
        for q, d, lk, g, t in ra:
            print(f"{q:>4} {dong(d):>16} {dong(lk):>16} {dong(g):>12} {dong(t):>12}")
        if vuot:
            print(f"→ Vượt 1 tỷ từ quý {vuot}: khai 01/CNKD từ quý này (NĐ 68/2026 Đ.8 k.1 điểm a); "
                  "đăng ký hóa đơn điện tử trong 30 ngày kể từ cuối quý (Đ.8 k.5 điểm c).")
            if vuot > 1:
                print("[cần kiểm tra] Cách tính GTGT cho doanh thu các quý trước khi vượt mốc: bảng trên chỉ tính "
                      "GTGT từ quý vượt mốc; đối chiếu số eTax tự tính và hỏi cơ quan thuế.")
    print("\nĐã kiểm tra phép tính. Đây là ước tính; số chính thức theo tờ khai trên eTax.")


if __name__ == "__main__":
    main()
