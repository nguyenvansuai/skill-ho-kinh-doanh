#!/usr/bin/env python3
"""Tạo lịch hạn nộp thuế hộ kinh doanh cho 1 năm tính thuế; xuất bảng và file .ics (Google Calendar, iPhone, Outlook).

Căn cứ hạn: NĐ 68/2026/NĐ-CP (VBHN 25/2026) Đ.8 k.1, k.3, k.4, k.5; Đ.9 k.1.
Hạn trùng ngày nghỉ → lùi sang ngày làm việc tiếp theo (Bộ luật Dân sự 2015 Đ.148 k.5).

Trường hợp (--truong-hop, chọn được nhiều):
  A            doanh thu năm từ 1 tỷ trở xuống: thông báo doanh thu năm
  moi-6t-dau   mới kinh doanh trong 6 tháng đầu năm, từ 1 tỷ trở xuống
  moi-6t-cuoi  mới kinh doanh trong 6 tháng cuối năm, từ 1 tỷ trở xuống
  B            trên 1 tỷ, khai quý (TNCN theo tỷ lệ %)
  C            trên 3 tỷ hoặc chọn TNCN theo thu nhập: khai quý + quyết toán
  thang        doanh thu trên 50 tỷ: GTGT khai theo tháng
  cho-thue-2   cho thuê bất động sản, khai 2 lần/năm
  cho-thue-1   cho thuê bất động sản, khai 1 lần/năm

Ví dụ:
  python3 tao_lich_thue.py --nam 2026 --truong-hop B --quy-vuot 3 --ra lich_thue_2026.ics
  python3 tao_lich_thue.py --nam 2026 --truong-hop A cho-thue-2 --nghi 2027-02-01
"""
import argparse
import datetime as dt
import uuid

# Mùng 1 Tết Nguyên đán (âm lịch) – để cảnh báo hạn gần Tết
TET = {2026: dt.date(2026, 2, 17), 2027: dt.date(2027, 2, 6), 2028: dt.date(2028, 1, 26),
       2029: dt.date(2029, 2, 13), 2030: dt.date(2030, 2, 3)}


def cuoi_thang(y, m):
    return (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))


def ngay_nghi_co_dinh(y):
    # Ngày lễ dương lịch cố định (Bộ luật Lao động 2019 Đ.112); 2/9 nghỉ thêm 1 ngày liền kề do Thủ tướng quyết định
    return {dt.date(y, 1, 1), dt.date(y, 4, 30), dt.date(y, 5, 1), dt.date(y, 9, 2)}


def lui_ngay(d, them):
    nghi = ngay_nghi_co_dinh(d.year) | them
    goc = d
    while d.weekday() >= 5 or d in nghi:
        d += dt.timedelta(days=1)
    return d, goc


def su_kien(nam, ths, quy_vuot):
    n1 = nam + 1
    ev = []  # (ngày gốc, việc, mẫu, căn cứ)

    def them(d, viec, mau, cc):
        ev.append((d, viec, mau, cc))

    if "A" in ths:
        them(dt.date(n1, 1, 31), f"Thông báo doanh thu năm {nam}", "01/TKN-CNKD", "NĐ 68/2026 Đ.8 k.1 điểm a")
    if "moi-6t-dau" in ths:
        them(dt.date(nam, 7, 31), f"Thông báo doanh thu từ khi bắt đầu đến 30/6/{nam}", "01/TKN-CNKD (kỳ 6 tháng đầu năm)", "NĐ 68/2026 Đ.9 k.1")
        them(dt.date(n1, 1, 31), f"Thông báo doanh thu 6 tháng cuối năm {nam}", "01/TKN-CNKD (kỳ 6 tháng cuối năm)", "NĐ 68/2026 Đ.9 k.1")
    if "moi-6t-cuoi" in ths:
        them(dt.date(n1, 1, 31), f"Thông báo doanh thu năm {nam} (mới kinh doanh 6 tháng cuối)", "01/TKN-CNKD", "NĐ 68/2026 Đ.9 k.1")
    if {"B", "C"} & set(ths):
        tu = quy_vuot or 1
        for q in range(tu, 5):
            m = q * 3 + 1
            d = cuoi_thang(nam if q < 4 else n1, m if q < 4 else 1)
            them(d, f"Khai, nộp thuế GTGT, TNCN quý {q}/{nam}", "01/CNKD", "NĐ 68/2026 Đ.8 k.3 điểm a, điểm e")
        if quy_vuot:
            d = cuoi_thang(nam, quy_vuot * 3) + dt.timedelta(days=30)
            them(d, f"Hạn đăng ký hóa đơn điện tử (30 ngày từ cuối quý {quy_vuot})", "Đăng ký HĐĐT có mã / máy tính tiền", "NĐ 68/2026 Đ.8 k.5 điểm c")
    if "C" in ths:
        them(dt.date(n1, 3, 31), f"Quyết toán thuế TNCN năm {nam}", "02/CNKD-TNCN-QTT", "NĐ 68/2026 Đ.8 k.3 điểm c")
    if "thang" in ths:
        for m in range(1, 13):
            y, mm = (nam, m + 1) if m < 12 else (n1, 1)
            them(dt.date(y, mm, 20), f"Khai, nộp thuế GTGT tháng {m}/{nam}", "01/CNKD (kỳ tháng)", "NĐ 68/2026 Đ.8 k.3 điểm b; Đ.10 k.1 điểm b")
    if "cho-thue-2" in ths:
        them(dt.date(nam, 7, 31), f"Khai thuế cho thuê BĐS lần 1 năm {nam}", "01/BĐS + 01/BK-BĐS", "NĐ 68/2026 Đ.8 k.3 điểm d")
        them(dt.date(n1, 1, 31), f"Khai thuế cho thuê BĐS lần 2 năm {nam}", "01/BĐS + 01/BK-BĐS", "NĐ 68/2026 Đ.8 k.3 điểm d")
    if "cho-thue-1" in ths:
        them(dt.date(n1, 1, 31), f"Khai thuế cho thuê BĐS năm {nam}", "01/BĐS + 01/BK-BĐS", "NĐ 68/2026 Đ.8 k.3 điểm d")
    return sorted(ev)


def ics(events, nhac):
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//skill-ho-kinh-doanh//lich-thue-hkd//VI", "CALSCALE:GREGORIAN"]
    for d, viec, mau, cc, ghi in events:
        out += ["BEGIN:VEVENT", f"UID:{uuid.uuid4()}@skill-ho-kinh-doanh",
                f"DTSTAMP:{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}",
                f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}",
                f"SUMMARY:[Thuế] {viec}",
                "DESCRIPTION:" + f"Mẫu: {mau}\\nCăn cứ: {cc}{ghi}\\nNộp trên eTax Mobile hoặc dichvucong.gdt.gov.vn. "
                "Đối chiếu quy định hiện hành.".replace(",", "\\,")]
        for n in nhac:
            out += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:Còn {n} ngày: {viec}", f"TRIGGER:-P{n}D", "END:VALARM"]
        out.append("END:VEVENT")
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nam", type=int, required=True, help="năm tính thuế")
    ap.add_argument("--truong-hop", nargs="+", required=True)
    ap.add_argument("--quy-vuot", type=int, choices=[1, 2, 3, 4], help="quý doanh thu lũy kế vượt 1 tỷ (B, C)")
    ap.add_argument("--nghi", nargs="*", default=[], help="ngày nghỉ bổ sung YYYY-MM-DD (Tết, nghỉ bù)")
    ap.add_argument("--nhac", nargs="*", type=int, default=[7, 1], help="nhắc trước bao nhiêu ngày")
    ap.add_argument("--ra", help="file .ics")
    a = ap.parse_args()

    them = {dt.date.fromisoformat(x) for x in a.nghi}
    rows = []
    for d, viec, mau, cc in su_kien(a.nam, a.truong_hop, a.quy_vuot):
        han, goc = lui_ngay(d, them)
        ghi = f" (hạn gốc {goc:%d/%m/%Y} trùng ngày nghỉ → lùi)" if han != goc else ""
        tet = TET.get(han.year)
        if tet and abs((han - tet).days) <= 10:
            ghi += " [kiểm tra lịch nghỉ Tết]"
        rows.append((han, viec, mau, cc, ghi))

    print(f"{'Hạn':10}  {'Việc':58}  {'Mẫu':34}  Căn cứ")
    for han, viec, mau, cc, ghi in rows:
        print(f"{han:%d/%m/%Y}  {viec[:58]:58}  {mau[:34]:34}  {cc}{ghi}")
    print("\nHạn nộp tiền thuế = hạn nộp tờ khai (NĐ 68/2026 Đ.8 k.3 điểm e).")
    print("Việc phát sinh, không cố định ngày: thông báo địa điểm kinh doanh mới, thay đổi, tạm ngừng, chấm dứt "
          "trong 10 ngày làm việc (Đ.8 k.4 điểm đ); thông báo tài khoản ngân hàng, ví điện tử mới (01/BK-STK, Đ.13 k.4).")
    if a.ra:
        with open(a.ra, "w", encoding="utf-8", newline="") as f:
            f.write(ics(rows, a.nhac))
        print(f"Đã ghi {a.ra} ({len(rows)} sự kiện, nhắc trước {a.nhac} ngày).")


if __name__ == "__main__":
    main()
