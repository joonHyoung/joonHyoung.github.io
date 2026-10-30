"""글마다 공유용 대표 이미지(og:image, 1200x630)를 만든다.

대상: header.image 가 없거나, 여러 글이 같은 header.image 를 같이 쓰는 글.
('오늘의 AI 뉴스'는 전부 ai-news.png 를 공유해서 검색 결과·SNS 공유 화면에서
글끼리 구분이 안 됐다.) 직접 만든 이미지를 쓰는 글은 건드리지 않는다.

결과는 assets/images/og/<포스트 파일명>.png 로 저장되고, _includes/seo.html 이
파일이 있으면 og:image 와 BlogPosting image 로 쓴다. 생성물은 커밋하지 않는다
(.gitignore). 배포 워크플로가 jekyll build 직전에 매번 만든다.

사용법: python og_images.py [폰트 경로]
  폰트 기본값은 CI(ubuntu, fonts-noto-cjk)의 Noto Sans CJK Bold.
"""
import collections
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
OUT = ROOT / "assets" / "images" / "og"
FONT = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
KO = 1  # .ttc 안의 Korean 서체 인덱스 (Noto Sans CJK: 0=JP, 1=KR)

W, H, PAD = 1200, 630, 80
# _sass/minimal-mistakes/skins/_terminal.scss 와 같은 색
BG, RAISED, LINE = "#08090b", "#101319", "#1d1f24"
ACCENT, TEXT, DIM = "#34d399", "#d7d9dd", "#7b8089"


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""

    def get(key, src=fm):
        m = re.search(rf"^{key}:\s*(.+)$", src, re.M)
        return m.group(1).strip().strip("\"'") if m else ""

    header = re.search(r"^header:\n((?:[ \t]+.+\n?)+)", fm, re.M)
    image = re.search(r"^\s+image:\s*(.+)$", header.group(1), re.M) if header else None
    return {
        "title": get("title"),
        "series": get("series"),
        "strapline": get("strapline"),
        "image": image.group(1).strip().strip("\"'") if image else "",
    }


def font(size):
    try:
        return ImageFont.truetype(FONT, size, index=KO)
    except OSError:
        return ImageFont.truetype(FONT, size)


def wrap(draw, text, fnt, width):
    """공백 기준으로 줄바꿈하고, 한 단어가 너무 길면 글자 단위로 자른다."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
            continue
        if line:
            lines.append(line)
        line = ""
        for ch in word:
            if draw.textlength(line + ch, font=fnt) > width:
                lines.append(line)
                line = ""
            line += ch
    if line:
        lines.append(line)
    return lines


def render(meta, date, dest):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=LINE, width=2)
    d.rectangle([0, 0, 10, H], fill=ACCENT)

    title = meta["title"]
    label = meta["series"] or meta["strapline"] or "POST"
    # "오늘의 AI 뉴스 (2026년 10월 23일): 헤드라인들" → 시리즈명·날짜는 위 라벨이 이미 보여준다
    if meta["series"] and title.startswith(meta["series"]) and ": " in title:
        title = title.split(": ", 1)[1]

    small = font(30)
    d.text((PAD, PAD), label, font=small, fill=ACCENT)
    d.text((W - PAD, PAD), date, font=small, fill=DIM, anchor="ra")

    # 제목: 4줄 안에 들어가는 가장 큰 크기
    box_w, top, bottom = W - PAD * 2, PAD + 80, H - PAD - 60
    for size in (64, 58, 52, 46, 42):
        fnt = font(size)
        lines = wrap(d, title, fnt, box_w)
        step = int(size * 1.4)
        if len(lines) * step <= bottom - top:
            break
    else:
        max_lines = (bottom - top) // step
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" ,") + "…"
    y = top + (bottom - top - len(lines) * step) // 2
    for line in lines:
        d.text((PAD, y), line, font=fnt, fill=TEXT)
        y += step

    d.line([PAD, H - PAD - 30, W - PAD, H - PAD - 30], fill=RAISED, width=2)
    d.text((PAD, H - PAD), "joonhyoung.github.io", font=small, fill=DIM, anchor="ls")
    img.save(dest, optimize=True)


def main():
    posts = sorted(POSTS.glob("*.md"))
    metas = {p: front_matter(p) for p in posts}
    shared = collections.Counter(m["image"] for m in metas.values() if m["image"])

    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    for path, meta in metas.items():
        if meta["image"] and shared[meta["image"]] < 2:
            continue
        date = path.name[:10].replace("-", ".")
        render(meta, date, OUT / f"{path.stem}.png")
        made += 1
    print(f"og images: {made} generated -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
