# Terminal Log 스킨 — joonHyoung/joonHyoung.github.io 적용 가이드

실제 저장소(main, remote_theme: mmistakes/minimal-mistakes)의 파일 구조를 읽고 맞춘 버전입니다.
아래 파일을 저장소의 같은 경로에 넣으면 됩니다. 덮어쓰는 파일은 먼저 백업하세요.

| 이 폴더의 파일 | 저장소 경로 | 상태 |
|---|---|---|
| `_sass/minimal-mistakes/skins/_terminal.scss` | 동일 | **새 파일** |
| `assets/css/main.scss` | 동일 | **덮어씀** — Inconsolata 오버라이드 제거(변수는 스킨에서 지정) |
| `_includes/head/custom.html` | 동일 | **새 파일** — JetBrains Mono + Pretendard |
| `_includes/head.html` | 동일 | **덮어씀** — 마지막에 `{% include head/custom.html %}` 한 줄 추가 |
| `_layouts/home.html` | 동일 | **덮어씀** — 로그 리스트 래퍼 + 헤더 행 |
| `_includes/archive-single.html` | 동일 | **덮어씀** — DATE/CAT/TITLE/READ 4열 행 |
| `_includes/masthead.html` | 동일 | **덮어씀** — 터미널 프롬프트 한 줄 추가 |
| `_includes/series-progress.html` | 동일 | 새 파일 (선택) |
| `index.html` | 동일 | **덮어씀** — `entries_layout: grid` 제거, `author_profile: true` |
| `_config-snippet.yml` | — | `_config.yml`에 2군데 반영 |

## 왜 이렇게 나뉘나
- 현재 `assets/css/main.scss`는 폰트 변수를 **import 뒤**에 선언해 실제로 적용되지 않습니다.
  Minimal Mistakes 변수는 partials import 전에 정해져야 하므로 스킨 파일에서 지정하도록 옮겼습니다.
- 저장소의 `_includes/head.html`에는 `head/custom.html` include가 없어서, 새 폰트를 넣으려면 head.html도 함께 교체해야 합니다.
- 홈은 지금 `entries_layout: grid`라 카드형입니다. 시안은 로그 리스트라서 grid 지정을 뺐습니다.

## 순서
1. 위 파일들을 복사
2. `_config.yml`에서 `minimal_mistakes_skin: "dark"` → `"terminal"`, posts defaults에 toc 3줄 추가
3. `bundle exec jekyll serve --livereload`로 확인
4. 문제 없으면 커밋 → GitHub Pages 자동 빌드

## 확인 포인트
- 홈 목록이 4열(날짜 / 카테고리 / 제목+요약+태그 / 읽는 시간)로 보이는지
- 포스트 상세 우측에 ON THIS PAGE 목차가 붙는지 (`toc: true`)
- 코드 블록 배경이 `#0d1014`, 액센트가 민트(`#34d399`)인지
- 모바일(≤600px)에서 로그 행이 2행 레이아웃으로 접히는지

## 연재(시리즈) 진행도 — 선택
포스트 front matter에 `series: "오늘의 AI 뉴스"` 추가하고,
`_layouts/single.html` 사이드바 영역에 `{% include series-progress.html %}`를 넣으면
시안의 진행도 바(03/12)가 나옵니다. `_layouts/single.html`은 저장소에 이미 로컬 복사본이 있습니다.

## 아직 남은 것
- 시안 03(카테고리 아카이브 3열 격자)은 `_layouts/categories.html` 오버라이드가 추가로 필요합니다.
- 다크 전용입니다.
