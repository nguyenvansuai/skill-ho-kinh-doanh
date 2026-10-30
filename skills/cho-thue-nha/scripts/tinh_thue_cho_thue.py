#!/usr/bin/env python3
"""Ước tính thuế cho thuê bất động sản của cá nhân năm 2026 theo từng hợp đồng, theo 2 lần khai (6 tháng) và cả năm.

Căn cứ: Luật 109/2025/QH15 Đ.7 k.4 (TNCN 5% phần doanh thu vượt mức); NĐ 68/2026 (VBHN 25/2026) Đ.3, Đ.4 k.1, k.4,
Đ.5 k.2 điểm đ, Đ.8 k.3 điểm d, đ; mức 1 tỷ theo NĐ 141/2026; Luật 48/2024 Đ.12 k.2 (GTGT dịch vụ 5%).

Hợp đồng: --hd "ten:tien_thue_thang:thang_dau-thang_cuoi" (các tháng thuộc năm tính thuế)
  python3 tinh_thue_cho_thue.py --hd "Nha Q1:45000000:1-12" "Mat bang Q3:50000000:4-12"
  python3 tinh_thue_cho_thue.py --hd "Kiot:20000000:1-12" --khai-thay "Kiot"
Trả trước nhiều năm: --tra-truoc "ten:tong_tien:so_nam" (phân bổ đều cho số năm – NĐ 68 Đ.5 k.2 điểm đ)
"""
import argparse
import sys

MUC_TRU = 1_000_000_000
GTGT, TNCN = 0.05, 0.05


def dong(x):
    return f"{round(x):,}".replace(",", ".")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hd", nargs="*", default=[])
    ap.add_argument("--tra-truoc", nargs="*", default=[])
    ap.add_argument("--khai-thay", nargs="*", default=[], help="tên hợp đồng mà bên thuê là tổ chức khai thay, nộp thay")
    ap.add_argument("--thu-tu-tru", nargs="*", help="thứ tự hợp đồng được trừ 1 tỷ (mặc định: tự khai trước)")
    a = ap.parse_args()

    hd = []  # (ten, dt_6t_dau, dt_6t_cuoi)
    for s in a.hd:
        try:
            ten, tien, ky = s.rsplit(":", 2)
            t1, t2 = (int(x) for x in ky.split("-"))
            tien = float(tien)
        except ValueError:
            sys.exit(f"Sai định dạng --hd: {s} (đúng: ten:tien_thang:1-12)")
        dau = sum(tien for m in range(t1, t2 + 1) if m <= 6)
        cuoi = sum(tien for m in range(t1, t2 + 1) if m > 6)
        hd.append([ten, dau, cuoi])
    for s in a.tra_truoc:
        ten, tong, nam = s.rsplit(":", 2)
        moi_nam = float(tong) / int(nam)
        hd.append([ten + " (trả trước, phân bổ)", moi_nam / 2, moi_nam / 2])
    if not hd:
        ap.error("cần ít nhất 1 --hd hoặc --tra-truoc")

    tong = sum(d + c for _, d, c in hd)
    print(f"Tổng doanh thu cho thuê năm: {dong(tong)} đồng")
    if tong <= MUC_TRU:
        print("→ Từ 1 tỷ trở xuống: KHÔNG nộp GTGT, TNCN (NĐ 68/2026 Đ.3 k.1, Đ.4 k.1).")
        print("  [cần kiểm tra] Nghĩa vụ thông báo doanh thu cho thuê khi dưới mức: hỏi cơ quan thuế nơi có bất động sản.")
        return

    ten_list = [h[0] for h in hd]
    thu_tu = a.thu_tu_tru or sorted(ten_list, key=lambda t: any(t.startswith(k) for k in a.khai_thay))
    con = MUC_TRU
    tru = {}
    for t in thu_tu:
        h = next(h for h in hd if h[0] == t)
        tru[t] = min(h[1] + h[2], con)
        con -= tru[t]

    print("\nTheo hợp đồng (GTGT 5% trên toàn bộ doanh thu; TNCN 5% trên phần vượt mức trừ):")
    print(f"{'Hợp đồng':30} {'6 tháng đầu':>14} {'6 tháng cuối':>14} {'Cả năm':>15} {'Mức trừ':>15} {'GTGT':>12} {'TNCN':>12}  Ai khai")
    tg = tt = 0
    for ten, d, c in hd:
        n = d + c
        g, t = n * GTGT, (n - tru.get(ten, 0)) * TNCN
        tg += g
        tt += t
        ai = "Bên thuê khai thay" if any(ten.startswith(k) for k in a.khai_thay) else "Tự khai 01/BĐS"
        print(f"{ten[:30]:30} {dong(d):>14} {dong(c):>14} {dong(n):>15} {dong(tru.get(ten, 0)):>15} {dong(g):>12} {dong(t):>12}  {ai}")
    print(f"{'Cộng':30} {'':>14} {'':>14} {dong(tong):>15} {dong(MUC_TRU):>15} {dong(tg):>12} {dong(tt):>12}")
    print(f"\nTổng thuế ước tính: {dong(tg + tt)} đồng (GTGT {dong(tg)} + TNCN {dong(tt)}).")

    # Khai 2 lần: chỉ các hợp đồng tự khai; mức trừ còn lại sau khi phân cho hợp đồng khai thay
    tu = [h for h in hd if not any(h[0].startswith(k) for k in a.khai_thay)]
    tru_tu = sum(tru.get(h[0], 0) for h in tu)
    dau = sum(h[1] for h in tu)
    nam_tu = sum(h[1] + h[2] for h in tu)
    g_tu, t_tu = nam_tu * GTGT, (nam_tu - tru_tu) * TNCN
    g1, t1 = dau * GTGT, max(dau - tru_tu, 0) * TNCN
    print("\nPhần anh/chị tự khai 01/BĐS nếu chọn khai 2 lần/năm (NĐ 68/2026 Đ.8 k.3 điểm d):")
    print(f"  Lần 1 (hạn 31/07): doanh thu {dong(dau)} → GTGT {dong(g1)}, TNCN {dong(t1)}")
    print(f"  Lần 2 (hạn 31/01 năm sau): doanh thu {dong(nam_tu - dau)} → GTGT {dong(g_tu - g1)}, TNCN {dong(t_tu - t1)}")
    print(f"  Khai 1 lần (hạn 31/01 năm sau): GTGT {dong(g_tu)}, TNCN {dong(t_tu)}")
    print("  [cần kiểm tra] Lần 1 khi doanh thu 6 tháng đầu chưa chắc cả năm vượt 1 tỷ: cách tính GTGT lần 1 "
          "đối chiếu số eTax tự tính.")
    if a.khai_thay:
        print("\nHợp đồng bên thuê khai thay: ghi rõ trong hợp đồng việc khai thay, nộp thay và số tiền được trừ "
              "(NĐ 68/2026 Đ.4 k.4 điểm b). Phần thuế đó bên thuê nộp, anh/chị không nộp lại.")
    print("Tổng thuế không đổi dù chọn trừ 1 tỷ vào hợp đồng nào (cùng thuế suất). Đã kiểm tra phép tính.")


if __name__ == "__main__":
    main()
