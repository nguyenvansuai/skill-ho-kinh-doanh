#!/usr/bin/env python3
"""Tính lương thực nhận, bảo hiểm, thuế TNCN của nhân viên và chi phí của hộ kinh doanh (theo tháng, năm 2026).

TNCN tiền lương: Luật 109/2025/QH15 Đ.8, Đ.9 (biểu lũy tiến tháng), Đ.10 (giảm trừ 15,5 triệu; 6,2 triệu/người phụ thuộc);
áp dụng từ kỳ tính thuế 2026 (Đ.29 k.2).
Tỷ lệ bảo hiểm mặc định (cần kiểm tra với cơ quan BHXH):
  người lao động  BHXH 8% · BHYT 1,5% · BHTN 1%
  hộ kinh doanh   BHXH 17% (ốm đau-thai sản 3%, hưu trí-tử tuất 14%) · TNLĐ-BNN 0,5% · BHYT 3% · BHTN 1%
Lương tối thiểu vùng từ 01/01/2026 (NĐ 293/2025/NĐ-CP): I 5.310.000 · II 4.730.000 · III 4.140.000 · IV 3.700.000.

  python3 tinh_luong.py --luong 9000000 --npt 1 --vung I
  python3 tinh_luong.py --luong 12000000 --luong-dong-bh 6000000 --vung II
  python3 tinh_luong.py --luong 4000000 --thoi-vu       # hợp đồng dưới 1 tháng: không BHXH bắt buộc
"""
import argparse

BIEU = [(10e6, 0.05), (30e6, 0.10), (60e6, 0.20), (100e6, 0.30), (float("inf"), 0.35)]
GIAM_TRU, NPT = 15_500_000, 6_200_000
TOI_THIEU = {"I": 5_310_000, "II": 4_730_000, "III": 4_140_000, "IV": 3_700_000}
NLD = {"BHXH": 0.08, "BHYT": 0.015, "BHTN": 0.01}
HKD = {"BHXH": 0.17, "TNLĐ-BNN": 0.005, "BHYT": 0.03, "BHTN": 0.01}


def dong(x):
    return f"{round(x):,}".replace(",", ".")


def thue_luy_tien(tntt):
    thue, duoi = 0.0, 0.0
    for tren, ts in BIEU:
        if tntt > duoi:
            thue += (min(tntt, tren) - duoi) * ts
        duoi = tren
    return thue


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--luong", type=float, required=True, help="tổng thu nhập chịu thuế tháng (lương + phụ cấp chịu thuế)")
    ap.add_argument("--luong-dong-bh", type=float, help="tiền lương làm căn cứ đóng bảo hiểm (mặc định = --luong)")
    ap.add_argument("--npt", type=int, default=0, help="số người phụ thuộc đã đăng ký")
    ap.add_argument("--vung", choices=TOI_THIEU, help="vùng lương tối thiểu để kiểm tra")
    ap.add_argument("--thoi-vu", action="store_true", help="hợp đồng dưới 1 tháng: không thuộc diện BHXH bắt buộc")
    a = ap.parse_args()

    bh_cs = 0 if a.thoi_vu else (a.luong_dong_bh if a.luong_dong_bh is not None else a.luong)
    bh_nld = {k: bh_cs * v for k, v in NLD.items()}
    bh_hkd = {k: bh_cs * v for k, v in HKD.items()}
    tntt = max(a.luong - sum(bh_nld.values()) - GIAM_TRU - NPT * a.npt, 0)
    tncn = thue_luy_tien(tntt)
    net = a.luong - sum(bh_nld.values()) - tncn

    print(f"Lương tháng: {dong(a.luong)} · lương đóng bảo hiểm: {dong(bh_cs)} · người phụ thuộc: {a.npt}")
    if a.vung and a.luong < TOI_THIEU[a.vung]:
        print(f"[!] Thấp hơn lương tối thiểu vùng {a.vung} ({dong(TOI_THIEU[a.vung])}) với công việc làm đủ giờ (NĐ 293/2025).")
    if not a.thoi_vu and a.vung and bh_cs and bh_cs < TOI_THIEU[a.vung]:
        print(f"[!] Lương đóng bảo hiểm thấp hơn lương tối thiểu vùng {a.vung} – kiểm tra mức sàn với BHXH.")
    if bh_cs > 46_800_000:
        print("[cần kiểm tra] Lương đóng bảo hiểm có thể vượt mức trần (20 lần mức tham chiếu/lương tối thiểu vùng).")
    print("\nNgười lao động đóng:  " + " · ".join(f"{k} {dong(v)}" for k, v in bh_nld.items()) + f"  = {dong(sum(bh_nld.values()))}")
    print(f"Thu nhập tính thuế = {dong(a.luong)} − bảo hiểm {dong(sum(bh_nld.values()))} − giảm trừ {dong(GIAM_TRU)}"
          + (f" − {a.npt} × {dong(NPT)}" if a.npt else "") + f" = {dong(tntt)}")
    print(f"Thuế TNCN tháng (biểu lũy tiến, Luật 109/2025 Đ.9): {dong(tncn)}")
    print(f"→ THỰC NHẬN: {dong(net)} đồng")
    print("\nHộ kinh doanh đóng thêm: " + " · ".join(f"{k} {dong(v)}" for k, v in bh_hkd.items()) + f"  = {dong(sum(bh_hkd.values()))}")
    print(f"→ TỔNG CHI PHÍ CỦA HỘ cho người này: {dong(a.luong + sum(bh_hkd.values()))} đồng/tháng")
    print("\nHộ khấu trừ, khai và nộp thay phần TNCN này nếu > 0 (Luật 108/2025 Đ.12 k.3 điểm a). "
          "Chi phí lương có đóng bảo hiểm bắt buộc được trừ khi hộ tính TNCN theo thu nhập (NĐ 68/2026 Đ.6 k.1 điểm b).")
    if a.thoi_vu:
        print("[cần kiểm tra] Hợp đồng dưới 3 tháng / không ký HĐLĐ: quy định khấu trừ 10% trên mỗi lần trả từ 2 triệu "
              "trở lên trước đây (TT 111/2013) – kiểm tra văn bản hướng dẫn Luật 109/2025.")
    print("Đã kiểm tra phép tính. Tỷ lệ bảo hiểm mặc định – đối chiếu thông báo của cơ quan BHXH.")


if __name__ == "__main__":
    main()
