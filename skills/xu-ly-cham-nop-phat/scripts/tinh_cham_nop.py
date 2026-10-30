#!/usr/bin/env python3
"""Ước tính tiền chậm nộp thuế và khung phạt chậm nộp hồ sơ khai thuế của hộ kinh doanh, cá nhân.

Tiền chậm nộp 0,03%/ngày: Luật Quản lý thuế 108/2025/QH15 Đ.16 k.2 điểm a.
Số ngày: từ ngày kế tiếp hạn nộp đến ngày liền trước ngày nộp (cách tính Luật 38/2019 Đ.59 k.2 điểm b;
Luật 108/2025 giao Chính phủ quy định – cần kiểm tra nghị định hướng dẫn).
Khung phạt chậm nộp hồ sơ: NĐ 125/2020/NĐ-CP Đ.13 (mức cho tổ chức); hộ kinh doanh, cá nhân = 1/2
(Luật 108/2025 Đ.44 k.4). Kiểm tra nghị định xử phạt hiện hành trước khi dùng.

  python3 tinh_cham_nop.py tien --so-thue 15000000 --han 2026-07-31 --ngay-nop 2026-10-30
  python3 tinh_cham_nop.py ho-so --han 2026-07-31 --ngay-nop 2026-10-30 --co-thue --da-nop-du
"""
import argparse
import datetime as dt

# (từ ngày, đến ngày, phạt tối thiểu, tối đa) – mức cho TỔ CHỨC theo NĐ 125/2020 Đ.13 k.2–k.4 (k.5: trên 90 ngày có thuế)
KHUNG = [
    (1, 30, 2_000_000, 5_000_000, "Đ.13 k.2"),
    (31, 60, 5_000_000, 8_000_000, "Đ.13 k.3"),
    (61, 90, 8_000_000, 15_000_000, "Đ.13 k.4"),
]


def dong(x):
    return f"{round(x):,}".replace(",", ".")


def ngay(s):
    return dt.date.fromisoformat(s)


def tien(a):
    so_ngay = max((ngay(a.ngay_nop) - ngay(a.han)).days - 1, 0)
    t = a.so_thue * 0.0003 * so_ngay
    print(f"Số thuế chậm nộp: {dong(a.so_thue)} đồng · hạn {ngay(a.han):%d/%m/%Y} · nộp {ngay(a.ngay_nop):%d/%m/%Y}")
    print(f"Số ngày chậm: {so_ngay} → tiền chậm nộp ≈ {dong(a.so_thue)} × 0,03% × {so_ngay} = {dong(t)} đồng")
    print("Nộp càng sớm càng ít: mỗi ngày thêm ≈ " + dong(a.so_thue * 0.0003) + " đồng.")
    print("Miễn tiền chậm nộp nếu bất khả kháng (Luật 108/2025 Đ.16 k.5). Cơ quan thuế tự tính nếu sau 30 ngày "
          "kể từ ngày nộp thuế mà người nộp chưa tự tính (Đ.16 k.3).")


def ho_so(a):
    tre = (ngay(a.ngay_nop) - ngay(a.han)).days
    print(f"Hạn nộp hồ sơ {ngay(a.han):%d/%m/%Y} · nộp {ngay(a.ngay_nop):%d/%m/%Y} → trễ {tre} ngày")
    if tre <= 0:
        print("→ Không trễ.")
        return
    if tre <= 5:
        print("→ Trễ 1–5 ngày và có tình tiết giảm nhẹ: phạt CẢNH CÁO (NĐ 125/2020 Đ.13 k.1); không có thì như dòng dưới.")
    for tu, den, lo, hi, cc in KHUNG:
        if tu <= tre <= den or (tre > 90 and not a.co_thue and den == 90):
            ghi = " (trễ trên 90 ngày nhưng không phát sinh thuế phải nộp)" if tre > 90 else ""
            print(f"→ Khung tổ chức {dong(lo)}–{dong(hi)} đồng ({cc}){ghi}")
            print(f"  Hộ kinh doanh, cá nhân (1/2): {dong(lo / 2)}–{dong(hi / 2)} đồng; "
                  f"mức trung bình thường áp dụng ≈ {dong((lo + hi) / 4)} đồng")
            break
    else:
        if a.da_nop_du:
            lo, hi = 15_000_000, 25_000_000
            print(f"→ Trễ trên 90 ngày, có phát sinh thuế, đã nộp đủ thuế và tiền chậm nộp trước khi cơ quan thuế "
                  f"công bố quyết định kiểm tra/lập biên bản: phạt vi phạm thủ tục (Luật 108/2025 Đ.45 k.4 điểm l; "
                  f"NĐ 125/2020 Đ.13 k.5). Khung tổ chức {dong(lo)}–{dong(hi)}; hộ/cá nhân {dong(lo / 2)}–{dong(hi / 2)} đồng.")
        else:
            print("→ Trễ trên 90 ngày, có phát sinh thuế, CHƯA nộp đủ thuế: có thể bị xử lý về hành vi TRỐN THUẾ, "
                  "phạt 1–3 lần số thuế trốn (Luật 108/2025 Đ.45 k.4 điểm a; Đ.44 k.3 điểm c).")
            print("  Việc nên làm ngay: nộp tờ khai và nộp đủ thuế + tiền chậm nộp TRƯỚC khi cơ quan thuế kiểm tra.")
    if a.so_thue_to_khai:
        tran = a.so_thue_to_khai
        san = (8_000_000 + 15_000_000) / 2 / 2
        print(f"Nếu tiền phạt cao hơn số thuế trên tờ khai ({dong(tran)}): phạt tối đa bằng số thuế đó nhưng không thấp "
              f"hơn mức trung bình khung 8–15 triệu (hộ/cá nhân ≈ {dong(san)}) (NĐ 125/2020 Đ.13 k.5 – cần kiểm tra).")
    if a.co_thue:
        print("Còn phải nộp tiền chậm nộp trên số thuế nộp trễ (dùng lệnh 'tien').")
    print("[cần kiểm tra] Mức phạt theo NĐ 125/2020 (đã sửa bởi NĐ 102/2021, 310/2025, 291/2026); Chính phủ có thể đã "
          "ban hành nghị định xử phạt mới theo Luật 108/2025.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    t = sub.add_parser("tien", help="tiền chậm nộp thuế")
    t.add_argument("--so-thue", type=float, required=True)
    t.add_argument("--han", required=True)
    t.add_argument("--ngay-nop", default=dt.date.today().isoformat())
    h = sub.add_parser("ho-so", help="khung phạt chậm nộp hồ sơ khai thuế")
    h.add_argument("--han", required=True)
    h.add_argument("--ngay-nop", default=dt.date.today().isoformat())
    h.add_argument("--co-thue", action="store_true", help="tờ khai có phát sinh số thuế phải nộp")
    h.add_argument("--da-nop-du", action="store_true", help="đã nộp đủ thuế và tiền chậm nộp trước khi bị kiểm tra")
    h.add_argument("--so-thue-to-khai", type=float)
    a = ap.parse_args()
    (tien if a.lenh == "tien" else ho_so)(a)
    print("Ước tính để tham khảo; số chính thức theo quyết định, thông báo của cơ quan thuế. Đã kiểm tra phép tính.")


if __name__ == "__main__":
    main()
