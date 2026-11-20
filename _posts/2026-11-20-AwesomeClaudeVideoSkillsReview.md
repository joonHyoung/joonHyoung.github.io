---
title: "awesome-claude-video-skills 리뷰: Claude로 영상 만드는 스킬 526개, 믿고 골라도 될까"
series: "AI Skills 리뷰"
strapline: "AI Skills"
description: "Claude Code로 영상을 만드는 스킬 526개를 모은 awesome-claude-video-skills를 직접 받아, 무엇이 들어 있는지, 추천 스킬과 실측 결과, 보안 등급을 얼마나 믿어도 되는지 정리했습니다."
permalink: /ai-skills/awesome-claude-video-skills-review/
categories:
  - "AI Skills"
tag:
  - "AI Skills"
  - "Claude Code"
  - "Agent Skills"
  - "영상 제작"
  - "Remotion"
  - "HyperFrames"
toc: true
toc_sticky: true
last_modified_at: 2026-11-20
comments: true
mathjax: false
---

Claude Code에게 영상을 만들게 하는 스킬이 빠르게 늘고 있습니다. [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills)는 그런 스킬과 툴킷 526개를 한곳에 모은 목록입니다. 2026년 11월 20일 기준 스타 약 2,400개, 마지막 갱신은 11월 19일입니다. 저장소를 직접 받아 목록 데이터를 집계하고, 보안 등급을 어떻게 매겼는지까지 살펴봤습니다.

[지난 글](/ai-skills/anthropic-skills-review/)에서 다룬 Anthropic 공식 스킬 저장소와 달리, 이 저장소에는 스킬이 하나도 들어 있지 않습니다. 다른 사람들이 만든 스킬로 가는 링크 모음입니다.

## 저장소에 들어 있는 것

| 파일 | 내용 |
|---|---|
| `README.md`, `README.zh-CN.md` | 분류별 표: 저장소, 스타 수, 설명, 보안 등급 |
| `data/skills.json` | 526개 항목의 이름, 스타, 분류, 보안 등급, 언어, 라이선스 |
| `assets/previews/` | 각 프로젝트 README에서 가져와 줄인 미리보기 이미지·GIF 약 350개 |
| `.github/ISSUE_TEMPLATE/` | 저장소 추천용 이슈 양식 |

설치 스크립트나 실행 코드, GitHub Actions 워크플로는 없습니다. 저장소를 받거나 읽는 것만으로 무언가 실행될 일은 없습니다. 목록 자체는 CC0(퍼블릭 도메인)이고, 미리보기 이미지는 원 프로젝트의 라이선스를 따릅니다.

## 무엇을 만드는 스킬들인가

| 분류 | 개수 | 예 |
|---|---:|---|
| 홍보·데모 영상 | 94 | onetake, claude-motion-design |
| 프레임워크·툴킷 | 93 | heygen-com/hyperframes, OpenMontage, remotion-dev/skills |
| 설명 영상 | 93 | explainroo, remotion-video-skill |
| 쇼츠·SNS | 70 | 세로 영상, 릴스·틱톡용 |
| 편집 (컷, 자막, B-roll) | 63 | FireRed-OpenStoryline, OpenChatCut |
| 모션그래픽 | 40 | lottie, 로고·타이틀 애니메이션 |
| 스토리·애니메이션 | 35 | lemo-opuscar, ClaudeAnimationBase |
| 뮤직비디오 | 19 | |
| 대본·학습 | 10 | 대본, 장면 분석 |
| 아바타 | 9 | 디지털 휴먼, 립싱크 |

기술적으로는 대부분 비슷한 방식을 씁니다. Claude가 Remotion(React)이나 HyperFrames(HTML + GSAP) 코드로 장면을 짜고, Playwright와 ffmpeg로 렌더링합니다. 언어는 Python 198개, JavaScript 138개, TypeScript 104개 순입니다.

## 추천과 실측 결과

이 목록에서 가장 쓸모 있는 부분은 직접 돌려 본 비교 테스트입니다. 2026년 10월 11일에 스킬 16개로 같은 영상을 만들었습니다. 조건은 가상 앱의 15초 홍보 영상, 화면 문구 5줄, 1920×1080 30fps, 영상·이미지·음성 생성 API 키 없음이었습니다. 스킬 없이 Claude Code만으로도 한 번 만들어 비교했습니다.

결과는 이렇습니다.

- 16개 모두 4가지 점검을 통과했습니다: 재생되는지, 길이와 해상도가 맞는지, 문구 5줄이 모두 읽히는지, 화면이 움직이는지.
- **스킬 없이 만든 영상도 4.4분 만에 통과했습니다.**
- 걸린 시간은 2.0분에서 23.5분까지 차이가 컸습니다. 소리를 넣은 스킬은 9개였습니다.
- 6개는 스킬 없이 만든 영상과 비슷한 모습(짙은 청록 배경, 물결, 가운데 흰 글씨)이었고, 10개는 나름의 스타일이 있었습니다.

목록이 추천하는 스킬은 세 가지입니다.

| 용도 | 스킬 | 이유 |
|---|---|---|
| 완성본을 빨리 | [explainroo](https://github.com/vincentsch/explainroo) | 2.0분으로 가장 빠르고, 소리가 있고, 기본값 같지 않은 결과 |
| 한 가지 아이디어로 이어지는 영상 | [onetake](https://github.com/feitangyuan/onetake) | 컷 없이 물방울 하나로 문구 5줄을 이어감 (8.5분) |
| Remotion으로 직접 디자인 | [remotion-dev/skills](https://github.com/remotion-dev/skills) | Remotion 공식, 4.5분에 안정적인 렌더링. 결과물은 기본값에 가까움 |

반대로 스타가 가장 많은 hyperframes는 15초 영상에 23.5분이 걸렸습니다.

목록이 직접 적은 결론이 가장 현실적입니다. 간단한 홍보 영상이라면 스킬이 필요 없을 수 있고, 스킬은 고유한 스타일이나 작업 흐름, 기존 영상 편집 같은 이유가 있을 때 쓸 만하다는 것입니다. 다만 테스트는 결과물이 "나오는지"만 점검했고, 얼마나 보기 좋은지는 점수로 매기지 않았습니다. 생김새는 운영자가 눈으로 판단한 것이니 영상을 직접 보고 고르는 게 좋습니다.

## 보안 등급, 얼마나 믿어도 될까

README 표의 모든 항목에 SAFE 또는 CAUTION 등급이 붙어 있습니다. 집계해 보니 SAFE 508개, CAUTION 18개입니다. 등급만 보면 거의 다 안전해 보이지만, 몇 가지를 알고 봐야 합니다.

**1. README만 읽고 매긴 등급입니다.** 목록 설명에 따르면 각 저장소의 README를 AI 모델이 읽고 판단합니다. 코드를 분석한 결과가 아닙니다. README에 위험한 내용이 없다고 해서 스크립트도 안전하다는 보장은 없습니다. SAFE는 "README상 문제 없어 보임" 정도로 읽어야 합니다.

**2. 등급을 매긴 곳이 목록 운영자의 사이트입니다.** 등급, 비교 테스트, 상세 페이지가 모두 운영자의 사이트(agentskillshub.top)로 연결되고, 테스트 스크립트도 같은 운영자의 다른 저장소에 있습니다. 운영 방식이 투명하게 공개돼 있다는 장점은 있지만, 제3자의 독립 검증은 아닙니다.

**3. CAUTION에 유명한 저장소도 있습니다.** OpenMontage(스타 약 8.2만), howseen-ai/claude-motion-design(857), wshuyi/remotion-video-skill(479) 등 18개입니다. 왜 CAUTION인지는 운영자 사이트에만 있고 저장소에는 없습니다. 비교 테스트에서는 이 중 몇 개가 문제없이 영상을 만들었으니, 등급만 보고 버리기보다 코드를 직접 확인해 볼 대상으로 보면 됩니다.

**4. 별이 적은 저장소가 많습니다.** 526개 중 330개가 스타 50개 미만입니다. 50개 미만이면 README 품질 기준을 넘고 별이 5개 이상이어야 하지만, README에 Claude Opus 5.5를 언급하면 별 조건이 면제됩니다. 이름이 같은 저장소도 여럿 있습니다(`video-shotcraft`, `motion-graphics-skills`, `paper2video` 등). 일부는 포크나 복제본이니 원본인지 확인하는 게 좋습니다.

**5. 라이선스가 불분명한 저장소가 있습니다.** 라이선스가 없는 저장소 55개, GitHub가 판별하지 못한 저장소 71개, AGPL-3.0이 11개입니다. 회사 업무나 상업 영상에 쓰려면 미리 확인이 필요합니다.

참고로 OpenMontage는 목록에 `calesthio/OpenMontage`와 `OpenMontageInc/OpenMontage` 두 주소로 나옵니다. GitHub API로 확인하니 앞의 주소가 뒤로 옮겨진 같은 저장소였습니다.

## 영상 스킬을 설치하기 전에

영상 스킬은 문서 스킬보다 권한을 많이 씁니다. 대부분 `npm install`로 패키지를 받고, Playwright 브라우저와 ffmpeg를 실행하고, 셸 명령을 돌립니다. TTS나 영상 생성 API 키를 요구하는 것도 있습니다. 설치 전에 이것만은 확인하길 권합니다.

1. `SKILL.md`를 읽고 Claude에게 무엇을 실행하라고 시키는지 봅니다.
2. `scripts/` 폴더와 `package.json`의 `postinstall` 같은 자동 실행 스크립트를 봅니다.
3. API 키를 어디로 보내는지 확인합니다.
4. 처음에는 별도 폴더나 컨테이너처럼 격리된 곳에서 돌려 봅니다.

## 총평

**좋은 점**

- 영상 스킬을 분류별로 한 번에 훑어볼 수 있는 가장 큰 목록입니다. 미리보기 이미지가 있어 결과물의 분위기를 바로 볼 수 있습니다.
- 같은 조건으로 16개를 직접 돌린 비교 테스트와 근거 자료가 공개돼 있고, "스킬 없이도 된다"는 결과까지 솔직하게 보여 줍니다.
- 선정 기준이 문서로 공개돼 있고, 필터가 있는 운영자 사이트 페이지는 8시간마다 갱신됩니다.

**아쉬운 점**

- 보안 등급이 README 기반이라, 실제 위험을 판단하는 근거로 쓰기엔 약합니다.
- 등급의 이유가 저장소가 아닌 외부 사이트에만 있습니다.
- 별 적은 저장소와 이름이 겹치는 복제본이 많아, 결국 직접 골라내야 합니다.

**이렇게 쓰길 권합니다**

목록은 "어떤 스킬이 있는지" 찾는 지도로 쓰고, 설치할지는 직접 판단하는 게 좋습니다. 빨리 결과물이 필요하면 explainroo, Remotion으로 직접 만들 거라면 remotion-dev/skills부터 시작하세요. 그 밖의 스킬은 위의 네 가지를 확인한 뒤 격리된 환경에서 시험해 보는 편이 안전합니다.
