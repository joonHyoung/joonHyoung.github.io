---
title: "anthropics/claude-code 리뷰: 소스는 없지만 꼭 볼 만한 공식 저장소"
series: "AI Skills 리뷰"
strapline: "AI Skills"
description: "Claude Code 공식 GitHub 저장소 anthropics/claude-code를 직접 받아, 무엇이 들어 있는지(플러그인 마켓플레이스, mods 소스, 조직용 설정 예제, 변경 로그)와 보안 관점에서 참고할 점을 정리했습니다."
permalink: /ai-skills/claude-code-repo-review/
categories:
  - "AI Skills"
tag:
  - "AI Skills"
  - "Claude Code"
  - "Anthropic"
  - "플러그인"
  - "Hooks"
  - "보안"
toc: true
toc_sticky: true
last_modified_at: 2026-11-20
comments: true
mathjax: false
---

[anthropics/claude-code](https://github.com/anthropics/claude-code)는 Claude Code의 공식 GitHub 저장소입니다. 2026년 11월 20일 기준 스타 약 15.6만 개, 포크 2.5만 개이고, 열린 이슈와 PR이 1.7만 개가 넘습니다. 이름만 보면 Claude Code 소스 코드가 있을 것 같지만 그렇지 않습니다. 그래도 Claude Code를 제대로 쓰려면 한 번은 둘러볼 가치가 있는 저장소입니다. 직접 받아서 무엇이 들어 있는지 살펴봤습니다.

[AI Skills 리뷰](/categories/#ai-skills)의 세 번째 글입니다. 앞의 [anthropics/skills 리뷰](/ai-skills/anthropic-skills-review/)가 Claude가 쓰는 스킬을 다뤘다면, 이번에는 스킬과 플러그인이 돌아가는 도구 쪽입니다.

## 먼저 알아 둘 점: 오픈소스가 아닙니다

`LICENSE.md`는 한 줄입니다. "© Anthropic PBC. All rights reserved." 사용은 Anthropic 상업 이용 약관을 따릅니다. 이 저장소는 Claude Code 본체를 개발하는 곳이 아니라, 다음 용도로 쓰입니다.

- 버그 신고와 기능 요청을 받는 **이슈 트래커**
- 버전마다 무엇이 바뀌었는지 적은 **변경 로그**
- 공식 **플러그인 마켓플레이스** 목록
- Claude Code에 내장된 **mods의 소스**
- 조직 배포용 **설정·훅·게이트웨이 예제**

## 설치 방법이 바뀌었습니다

README 맨 위에 npm 설치는 더 이상 권장하지 않는다는 안내가 있습니다. 지금 권장하는 방법은 다음과 같습니다.

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew
brew install --cask claude-code

# Windows
irm https://claude.ai/install.ps1 | iex
winget install Anthropic.ClaudeCode
```

`npm install -g @anthropic-ai/claude-code`도 아직 동작하지만 "Deprecated"로 표시돼 있습니다. 다만 `plugins/README.md`에는 여전히 npm 설치법이 남아 있는 등, 문서 사이에 맞지 않는 부분이 조금 있습니다.

## 저장소 구성

| 위치 | 내용 |
|---|---|
| `CHANGELOG.md` | 버전별 변경 사항. 445개 버전, 1.3MB |
| `.claude-plugin/marketplace.json` | 공식 플러그인 12개 목록 |
| `mods/` | Claude Code에 내장된 mod 7개의 TypeScript 소스와 테스트 |
| `examples/settings/` | 조직용 권한·샌드박스 설정 예제 (lax, strict, bash-sandbox, HIPAA) |
| `examples/mdm/` | Jamf, Intune 등으로 설정을 배포하는 템플릿 |
| `examples/hooks/` | Bash 명령을 검사하는 훅 예제 |
| `examples/gateway/` | AWS·GCP에 Claude apps gateway를 띄우는 Terraform 예제 |
| `.devcontainer/` | 방화벽을 건 개발 컨테이너 |
| `.github/workflows/` | Claude가 이슈를 분류하고 중복을 찾는 워크플로 14개 |

## 공식 플러그인 12개

이 저장소를 마켓플레이스로 등록하면 Anthropic 플러그인을 설치할 수 있습니다. 플러그인의 실제 코드는 [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) 저장소에 있고, 여기에는 목록만 있습니다.

| 분류 | 플러그인 | 하는 일 |
|---|---|---|
| 개발 | **feature-dev** | 코드 탐색, 설계, 품질 검토 에이전트로 기능 개발 |
| 개발 | **plugin-dev** | 플러그인 개발 도구. 훅, MCP 연동 등 스킬 7개 |
| 개발 | **agent-sdk-dev** | Claude Agent SDK 개발 도구 |
| 개발 | **frontend-design** | 완성도 높은 프론트엔드 화면 디자인 |
| 개발 | **ralph-loop** | 같은 작업을 반복하며 스스로 결과를 개선하는 루프 |
| 생산성 | **code-review** | 여러 에이전트로 PR을 리뷰하고 신뢰도 점수로 오탐을 거름 |
| 생산성 | **pr-review-toolkit** | 주석, 테스트, 오류 처리, 타입 설계를 나눠 리뷰 |
| 생산성 | **commit-commands** | 커밋, 푸시, PR 생성 명령 |
| 생산성 | **hookify** | 대화 패턴을 보고 원치 않는 동작을 막는 훅을 만들어 줌 |
| 보안 | **security-guidance** | 수정할 때 패턴 기반 경고, 작업이 끝날 때 diff 보안 리뷰 |
| 학습 | **explanatory-output-style** | 구현 선택의 이유를 설명해 주는 출력 스타일 |
| 학습 | **learning-output-style** | 중요한 지점에서 사용자가 직접 코드를 쓰게 하는 학습 모드 |

플러그인은 슬래시 명령, 에이전트, 스킬, 훅, MCP 서버를 하나로 묶은 패키지입니다. 스킬은 그 구성 요소 중 하나입니다.

## mods: 내장 기능의 소스

이 저장소에서 가장 새로운 부분입니다. mod는 훅 모듈 하나로 Claude Code의 동작을 바꾸는 플러그인이고, 아래 7개는 Claude Code에 이미 내장돼 있습니다. 여기 있는 건 바이너리에 들어간 소스 그대로입니다.

| mod | 하는 일 |
|---|---|
| **diff** | `/diff`로 이번 세션의 변경 사항을 파일별로 옆 창에 보여 줌 |
| **easel** | 대화 안에 차트를 그림. 시간에 따른 MCP 지표는 자동으로 차트화 |
| **agents-md** | 프로젝트에 `CLAUDE.md`가 없으면 `AGENTS.md`를 대신 읽음 |
| **privacy** | 로그인한 계정의 이메일이 외부 요청의 신원 정보로 나가는 것을 막음 |
| **sec-default** | 조직이 정한 훅·설정·권한 규칙을 개인이 설치한 플러그인이 건드리지 못하게 함 |
| **hipaa-default** | HIPAA 조직에서 관리자가 막은 도구 호출을 거부 |
| **telemetry** | 내장 플러그인의 사용 통계. 분석을 끄면 아무것도 보내지 않음 |

내장 기능이 어떻게 동작하는지 소스로 확인할 수 있다는 점이 좋습니다. 예를 들어 `agents-md`를 보면, 다른 에이전트용으로 써 둔 `AGENTS.md`가 언제 읽히는지 정확히 알 수 있습니다. 직접 mod를 만들 때도 좋은 견본입니다. `claude --plugin-dir mods/diff`로 소스에서 바로 띄워 볼 수 있고, `claude plugin test mods/diff`로 테스트를 돌릴 수 있습니다.

## 보안 관점에서 참고할 것

개인 사용자보다 팀이나 회사에서 Claude Code를 도입할 때 특히 쓸모 있는 부분입니다.

### 조직용 설정 예제

`examples/settings/`에는 세 단계 예제가 있습니다.

| 설정 | lax | strict | bash-sandbox |
|---|:---:|:---:|:---:|
| `--dangerously-skip-permissions` 금지 | ✅ | ✅ | |
| 플러그인 마켓플레이스 차단 | ✅ | ✅ | |
| 사용자·프로젝트가 정한 권한 규칙 무시 | | ✅ | ✅ |
| 사용자·프로젝트가 정한 훅 무시 | | ✅ | |
| 웹 검색·가져오기 금지 | | ✅ | |
| Bash 실행마다 승인 | | ✅ | |
| Bash는 샌드박스 안에서만 | | | ✅ |

가장 느슨한 lax도 권한 확인을 건너뛰는 옵션과 외부 마켓플레이스는 막아 둔다는 점이 눈에 띕니다. 예제 README에는 샌드박스가 Bash에만 적용되고 파일 읽기·쓰기, 웹 요청, MCP, 훅에는 적용되지 않는다는 주의 사항도 있습니다. 샌드박스만 켜면 안전하다고 오해하기 쉬운 부분입니다. 예제는 "커뮤니티가 관리하는 것이라 틀릴 수 있다"고 적혀 있으니 그대로 배포하기 전에 먼저 시험해 봐야 합니다.

### 방화벽을 건 개발 컨테이너

`.devcontainer/init-firewall.sh`는 기본으로 모든 네트워크를 막고(`iptables -P OUTPUT DROP`), GitHub와 `api.anthropic.com` 등 필요한 곳만 허용합니다. 권한 확인 없이 Claude Code를 돌려야 한다면 이런 격리 환경에서 하는 것이 안전합니다.

### 저장소 자체의 자동화

이슈 분류와 중복 찾기를 Claude가 GitHub Actions에서 합니다. 저장소의 `CLAUDE.md`를 보면, Claude를 부르는 작업에는 세 가지 보호 장치를 반드시 걸도록 정해 두었습니다.

1. 외부 네트워크를 걸러내는 방화벽 러너에서만 실행
2. 접속 가능한 호스트를 허용 목록으로 제한
3. `--permission-mode auto`로 허용 목록 밖의 도구 호출은 안전 검토를 통과해야 실행

그리고 이 규칙을 어긴 워크플로가 있으면 실패시키는 검사 워크플로도 따로 있습니다. 공개 이슈처럼 누구나 글을 쓸 수 있는 입력을 AI 에이전트가 처리할 때 어떻게 막아야 하는지 보여 주는 좋은 예입니다. 자기 저장소에 Claude 자동화를 붙이려는 사람에게 가장 참고가 될 부분입니다.

## 변경 로그 읽는 법

`CHANGELOG.md`는 1.3MB, 445개 버전이 쌓여 있고 최신은 2.1.329입니다. 한 버전에도 수십 줄씩 적혀 있어서 처음부터 읽기는 어렵습니다. 이렇게 읽으면 편합니다.

- 쓰고 있는 기능 이름(`/code-review`, `hooks`, `MCP`, `sandbox`)으로 검색해 최근 바뀐 점을 확인합니다.
- "Fixed" 항목에서 지금 겪는 문제가 이미 고쳐졌는지 봅니다. 예를 들어 2.1.329에는 macOS 키체인에서 인증 정보를 읽기만 하고 저장하지 못할 때 로그아웃이 반복되던 문제가 고쳐졌다고 적혀 있습니다.
- 버그를 신고하기 전에 확인합니다. 이미 고쳐진 문제라면 업데이트만 하면 됩니다.

## 총평

**좋은 점**

- 공식 플러그인 12개를 명령 한 줄로 받을 수 있습니다.
- 내장 mods의 소스와 테스트가 공개돼 있어 동작 방식을 직접 확인하고, 자기 mod를 만들 때 견본으로 쓸 수 있습니다.
- 조직용 설정, MDM, 게이트웨이, 방화벽 컨테이너 예제가 한곳에 있어 회사 도입 준비에 유용합니다.
- 저장소의 Actions 보안 규칙은 AI 자동화를 안전하게 붙이는 방법의 좋은 실례입니다.

**아쉬운 점**

- Claude Code 본체 소스는 없고 라이선스도 오픈소스가 아닙니다.
- 열린 이슈와 PR이 1.7만 개가 넘어 원하는 이슈를 찾기 어렵습니다. 버그 신고는 Claude Code 안에서 `/bug`로 하는 편이 빠릅니다.
- 변경 로그가 너무 길고, 일부 문서는 설치법처럼 최신 내용과 어긋납니다.
- 설정 예제는 공식 지원 대상이 아니라고 명시돼 있습니다.

**이렇게 쓰길 권합니다**

1. 개인 사용자라면 `/plugin marketplace add anthropics/claude-code`로 공식 플러그인을 받아 `code-review`나 `security-guidance`부터 써 봅니다.
2. 팀에 도입한다면 `examples/settings/`의 strict 예제에서 시작해 필요한 만큼 풀어 줍니다.
3. GitHub Actions에 Claude를 붙인다면 이 저장소의 `CLAUDE.md`와 워크플로를 그대로 참고합니다.
