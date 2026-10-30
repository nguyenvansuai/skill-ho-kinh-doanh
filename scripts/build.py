#!/usr/bin/env python3
"""Đồng bộ tài liệu dùng chung, sinh bản ChatGPT và đóng gói zip.

Chạy từ thư mục gốc repo:  python3 scripts/build.py

1. Chép shared/*.md vào skills/<skill>/references/ (mỗi skill tự đủ, cài riêng lẻ được)
2. (dành sẵn)
3. Sinh chatgpt/<skill>.md: hướng dẫn dán vào Custom GPT / Project
4. Đóng gói dist/<skill>.zip (upload lên claude.ai) và dist/tat-ca-skill.zip
5. Sinh .claude-plugin/marketplace.json (cài bằng /plugin trong Claude Code)
"""
import re
import shutil
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SKILLS = GOC / "skills"
SHARED = GOC / "shared"

SHARED_MD = ["nguyen-tac-chung.md", "quy-dinh-thue-hkd-2026.md"]  # chép vào mọi skill
GIOI_HAN_GPT = 8000  # ký tự tối đa ô Instructions của Custom GPT


def dong_bo():
    for sk in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        ref = sk / "references"
        ref.mkdir(exist_ok=True)
        for f in SHARED_MD:
            shutil.copy(SHARED / f, ref)


def tach_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    return meta, m.group(2).strip()


def sinh_chatgpt():
    out = GOC / "chatgpt"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    bao_cao = []
    for sk in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        meta, body = tach_frontmatter((sk / "SKILL.md").read_text(encoding="utf-8"))
        # Trong ChatGPT, file references được tải lên mục Knowledge
        body = body.replace("references/", "file Knowledge ").replace("scripts/", "")
        huong_dan = (
            "Bạn là trợ lý cho chủ hộ kinh doanh Việt Nam. Luôn trả lời bằng tiếng Việt có dấu.\n"
            "Các file nhắc tới (nguyen-tac-chung.md, quy-dinh-thue-hkd-2026.md, ...) đã được tải lên mục Knowledge; hãy đọc chúng khi cần.\n\n"
            + body
        )
        files = sorted(f.name for f in (sk / "references").glob("*.md"))
        scripts = sorted(f.name for f in (sk / "scripts").glob("*")) if (sk / "scripts").exists() else []
        noi_dung = [
            f"# {sk.name} – bản dùng cho ChatGPT",
            "",
            f"**Mô tả:** {meta.get('description', '')}",
            "",
            "## Cách cài",
            "1. ChatGPT bản miễn phí: tạo Project mới và mở phần hướng dẫn (instructions) của Project. Bản trả phí: có thể tạo Custom GPT (Explore GPTs → Create → Configure).",
            f"2. Name: `{sk.name}`. Description: copy dòng Mô tả ở trên.",
            "3. Dán toàn bộ khối **Instructions** bên dưới vào ô hướng dẫn.",
            "4. Tải lên (Project files hoặc Knowledge) các file " + ", ".join(f"`skills/{sk.name}/references/{f}`" for f in files) + ".",
        ]
        if scripts:
            noi_dung.append("5. Bật **Code Interpreter & Data Analysis** và tải thêm " +
                            ", ".join(f"`skills/{sk.name}/scripts/{s}`" for s in scripts) + " vào Knowledge.")
        noi_dung += ["", "## Instructions", "", "````markdown", huong_dan, "````", ""]
        (out / f"{sk.name}.md").write_text("\n".join(noi_dung), encoding="utf-8")
        if len(huong_dan) > GIOI_HAN_GPT:
            bao_cao.append(f"  ! {sk.name}: Instructions {len(huong_dan)} ký tự > {GIOI_HAN_GPT}")
    return bao_cao


def dong_goi():
    dist = GOC / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    with zipfile.ZipFile(dist / "tat-ca-skill.zip", "w", zipfile.ZIP_DEFLATED) as tat_ca:
        for sk in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
            with zipfile.ZipFile(dist / f"{sk.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
                for f in sorted(sk.rglob("*")):
                    if f.is_file() and "__pycache__" not in f.parts:
                        z.write(f, f.relative_to(SKILLS))
                        tat_ca.write(f, f.relative_to(SKILLS))


def sinh_marketplace():
    """Sinh .claude-plugin/marketplace.json: mỗi skill là 1 plugin + 1 gói cài cả bộ."""
    import json
    plugins = []
    for sk in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        meta, _ = tach_frontmatter((sk / "SKILL.md").read_text(encoding="utf-8"))
        plugins.append({
            "name": sk.name,
            "source": f"./skills/{sk.name}",
            "description": meta["description"],
            "category": "ho-kinh-doanh",
        })
    plugins.append({
        "name": "tron-bo-skill-hkd",
        "source": "./",
        "description": "Cài cả bộ 12 skill hộ kinh doanh (ghi sổ, đối soát, hỏi đáp, hóa đơn, khai báo, tính thuế, lịch thuế, đăng ký hộ, cho thuê nhà, chậm nộp – phạt, nhân viên) trong một lần.",
        "category": "ho-kinh-doanh",
    })
    data = {
        "name": "skill-ho-kinh-doanh",
        "description": "Bộ 12 skill AI cho hộ kinh doanh, cá nhân kinh doanh Việt Nam 2026: sổ sách, đối soát, tính thuế, "
                       "khai báo eTax, lịch thuế, hóa đơn điện tử, đăng ký hộ, cho thuê nhà, chậm nộp – phạt, nhân viên.",
        "owner": {"name": "nguyenvansuai", "url": "https://github.com/nguyenvansuai"},
        "plugins": plugins,
    }
    out = GOC / ".claude-plugin"
    out.mkdir(exist_ok=True)
    (out / "marketplace.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def kiem_tra():
    loi = []
    for sk in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        meta, body = tach_frontmatter((sk / "SKILL.md").read_text(encoding="utf-8"))
        if meta.get("name") != sk.name:
            loi.append(f"{sk.name}: name trong frontmatter không khớp tên thư mục")
        if not 50 < len(meta.get("description", "")) <= 1024:
            loi.append(f"{sk.name}: description dài {len(meta.get('description', ''))} ký tự (cần ≤ 1024)")
        for ref in re.findall(r"`(references/[\w./-]+|scripts/[\w./-]+)`", body):
            if not (sk / ref).exists():
                loi.append(f"{sk.name}: thiếu file {ref}")
    return loi


if __name__ == "__main__":
    dong_bo()
    canh_bao = sinh_chatgpt()
    sinh_marketplace()
    loi = kiem_tra()
    dong_goi()
    n = len([p for p in SKILLS.iterdir() if p.is_dir()])
    print(f"Đã build {n} skill.")
    for c in canh_bao:
        print(c)
    if loi:
        print("LỖI:")
        print("\n".join("  - " + l for l in loi))
        raise SystemExit(1)
