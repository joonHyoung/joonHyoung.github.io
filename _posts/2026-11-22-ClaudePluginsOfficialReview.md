---
title: "claude-plugins-official 리뷰: 공식 마켓플레이스 플러그인 317개는 어떻게 관리될까"
series: "AI Skills 리뷰"
strapline: "AI Skills"
description: "Claude Code 공식 플러그인 마켓플레이스 anthropics/claude-plugins-official을 직접 받아, 등록된 317개 플러그인의 구성, Anthropic 자체 플러그인, 외부 플러그인을 검증하는 방식과 설치 전 주의할 점을 정리했습니다."
permalink: /ai-skills/claude-plugins-official-review/
categories:
  - "AI Skills"
tag:
  - "AI Skills"
  - "Claude Code"
  - "Anthropic"
  - "플러그인"
  - "마켓플레이스"
  - "보안"
toc: true
toc_sticky: true
last_modified_at: 2026-11-22
comments: true
mathjax: false
---

Claude Code에서 `/plugin`을 열면 기본으로 보이는 마켓플레이스가 `claude-plugins-official`입니다. 그 원본이 [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) 저장소입니다. 2026년 11월 22일 기준 스타 약 4.8만 개, 마지막 커밋은 11월 21일(한국 시간)입니다. 저장소를 직접 받아 등록된 플러그인을 집계하고, 외부 플러그인을 어떻게 검증하는지 워크플로까지 살펴봤습니다.

[AI Skills 리뷰](/categories/#ai-skills)의 네 번째 글입니다. [지난 글](/ai-skills/claude-code-repo-review/)에서 본 anthropics/claude-code의 공식 플러그인 12개도 실제 코드는 모두 이 저장소에 있습니다.

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 등록된 플러그인 | 317개 |
| 이 저장소 안에 코드가 있는 것 | 55개 (Anthropic 플러그인 41개 + `external_plugins/` 14개) |
| 다른 저장소에서 받아 오는 것 | 262개 |
| 라이선스 | 저장소는 Apache 2.0. 외부 플러그인은 각자의 라이선스 |
| 설치 | `/plugin install <이름>@claude-plugins-official` 또는 `/plugin` → Discover |

분류별로는 개발 123개, 생산성 70개, 데이터베이스 39개, 모니터링 22개, 보안 18개 순입니다. 외부 플러그인은 GitHub, GitLab, Linear, Asana, Firebase, Terraform, Playwright 같은 서비스 연동이 대부분입니다. Adobe, Airtable, Salesforce처럼 회사가 직접 만든 플러그인도 많습니다. Apple의 Xcode 플러그인도 등록돼 있습니다.

## 바뀌고 있는 것: 제출은 claude.ai로

README 맨 위에 운영 방식이 바뀌었다는 안내가 있습니다.

- 외부 플러그인 제출은 이제 [claude.ai/directory/manage](https://claude.ai/directory/manage)에서 받습니다. 여기서 승인된 플러그인은 Claude Code뿐 아니라 다른 Claude 제품에도 제공됩니다.
- 이 저장소로 보내는 PR은 확인하지 않고, 자동으로 닫는 워크플로도 있습니다.
- `marketplace.json`의 외부 플러그인 목록은 점점 줄여서, 결국 Anthropic 자체 플러그인만 남길 예정입니다.

즉 이 저장소는 "공식 마켓플레이스 목록"에서 "Anthropic 플러그인의 소스 저장소"로 바뀌는 중입니다. 지금 보이는 외부 플러그인 262개도 앞으로 이 목록에서는 빠질 수 있습니다.

## Anthropic이 직접 만든 플러그인

`plugins/` 폴더에 있는 43개 중 41개가 목록에 올라 있습니다. 성격별로 묶으면 이렇습니다.

| 분류 | 플러그인 | 하는 일 |
|---|---|---|
| 코드 품질 | **code-review**, **pr-review-toolkit**, **code-simplifier** | PR 리뷰, 분야별 리뷰 에이전트, 코드 단순화 |
| 보안 | **claude-security** | 내 코드의 취약점을 깊게 스캔하고, 결과를 다시 검증한 뒤 패치까지 제안 |
| 보안 | **security-guidance** | 수정할 때 위험 패턴 경고, 끝날 때 diff 보안 리뷰 |
| 개발 흐름 | **feature-dev**, **code-modernization**, **commit-commands** | 기능 개발, 레거시 코드 현대화, 커밋·PR |
| 언어 서버 | **swift-lsp**, **typescript-lsp**, **pyright-lsp** 등 12개 | 정의 이동, 타입 오류 같은 코드 인텔리전스 |
| Claude Code 설정 | **claude-code-setup**, **claude-md-management**, **hookify** | 프로젝트에 맞는 자동화 추천, CLAUDE.md 관리, 훅 만들기 |
| 만들기 도구 | **plugin-dev**, **skill-creator**, **mcp-server-dev**, **agent-sdk-dev** | 플러그인, 스킬, MCP 서버, 에이전트 개발 |
| 사용량 보고 | **session-report**, **receipts** | 토큰·캐시 사용량 보고서, 내가 한 일과 프로젝트별 사용량 정리 |
| 기타 | **playground**, **project-artifact**, **mcp-tunnels**, **math-olympiad**, **math-proof**, **theme-examples** 등 | HTML 플레이그라운드, 프로젝트 현황 페이지, 사설 MCP 연결, 수학 문제 풀이 |

몇 가지는 따로 짚을 만합니다.

- **언어 서버 플러그인 12개**는 이름만 보면 가볍지만 효과가 큽니다. Claude가 텍스트 검색 대신 실제 정의와 참조를 따라가게 됩니다. 다만 언어 서버는 따로 설치해야 합니다. 예를 들어 swift-lsp는 Xcode나 Swift 툴체인에 들어 있는 SourceKit-LSP를 씁니다. iOS 개발자라면 swift-lsp와 Apple의 Xcode 플러그인을 함께 써 볼 만합니다.
- **claude-security**는 security-guidance보다 무겁습니다. 스캔 강도를 고르면, 찾은 문제를 보고하기 전에 다시 반박해 보고, 남은 것만 패치로 만들어 여러 에이전트가 검증합니다.
- **receipts**는 `~/.claude/projects`의 대화 기록과 로컬 git을 읽어 보고서를 만듭니다. 설명에 따르면 외부로는 개수와 프로젝트 이름만 나갑니다. 회사 프로젝트 이름도 민감할 수 있으니 확인하고 쓰는 게 좋습니다.

## 외부 플러그인은 어떻게 검증하나

이 저장소에서 가장 배울 게 많은 부분입니다. 외부 플러그인 262개를 다음 방식으로 관리합니다.

**1. 커밋 SHA로 고정합니다.** 262개 중 261개가 특정 커밋(`sha`)을 가리킵니다. 외부 저장소의 `main`이 바뀌어도 사용자에게 바로 전달되지 않습니다. 남은 하나는 Apple의 Xcode 플러그인입니다. 이 플러그인은 저장소에서 받지 않고, 로컬에 설치된 Xcode에서 `xcrun` 명령으로 플러그인 경로를 가져옵니다.

**2. 매일 밤 SHA를 올리고, 올릴 때마다 Claude가 심사합니다.** 매일 07:23 UTC에 워크플로가 각 외부 저장소의 새 커밋을 찾아 SHA를 올리는 PR을 만듭니다. 이 PR은 Claude가 심사를 통과해야만 병합됩니다. 심사 기준(`.github/policy/prompt.md`)은 꽤 엄격합니다.

- 기준은 "악성이 아니다"가 아니라 "사용자 데이터를 책임 있게 다룬다"입니다. 목적에 비해 너무 많은 것을 관찰하거나, 설명에 없는 동작을 하면 떨어집니다.
- 실제로 로드되는 파일뿐 아니라 저장소 전체를 읽습니다. `.claude/`, `scripts/`, `tests/` 같은 숨은 폴더도 포함됩니다. 플러그인을 설치하면 저장소 전체가 내려받아지기 때문입니다.
- 키체인, `~/.aws/credentials`, SSH 키, 브라우저 쿠키 같은 인증 정보를 읽어 **다른 서비스로 보내는** 코드를 특히 잡아냅니다.
- "다른 지시를 무시하라" 같은 프롬프트 인젝션이 스킬이나 README에 숨어 있는지도 봅니다.

**3. 떨어진 업데이트는 빼고 나머지는 진행합니다.** 심사에 떨어진 플러그인만 업데이트 PR에서 되돌리는 워크플로가 따로 있습니다. 한 플러그인 때문에 나머지 업데이트가 막히지 않습니다. 같은 플러그인의 같은 커밋은 한 번만 심사하고 결과를 저장해 둡니다.

**4. MCP 서버 주소가 살아 있는지 확인합니다.** 플러그인이 선언한 HTTP MCP 서버 주소가 404이거나 DNS·TLS 오류가 나면 실패 처리합니다. 오타나 사라진 서버를 잡기 위한 것입니다.

정리하면 "사람이 한 번 승인하고 끝"이 아니라, 업데이트가 올 때마다 Claude가 전체 코드를 다시 읽는 구조입니다. 자기 회사용 사설 마켓플레이스를 운영한다면 그대로 참고할 만합니다.

## 그래도 주의할 점

**README의 경고를 그대로 받아들이세요.** "플러그인을 설치하거나 쓰기 전에 믿을 수 있는지 확인하라. Anthropic은 플러그인에 포함된 MCP 서버, 파일, 소프트웨어를 통제하지 않으며 의도대로 동작하거나 바뀌지 않는다고 보장할 수 없다"고 적혀 있습니다. 위의 심사는 위험을 줄여 줄 뿐 보증은 아닙니다.

특히 신경 쓸 부분은 이렇습니다.

- **MCP 서버는 심사 범위 밖에서 바뀔 수 있습니다.** SHA 고정은 저장소 코드에만 적용됩니다. 플러그인이 원격 MCP 서버에 연결하면, 그 서버의 동작은 언제든 바뀔 수 있습니다.
- **메시지 연동 플러그인은 권한이 큽니다.** Discord, Telegram, iMessage 플러그인은 Claude를 메신저와 연결합니다. 특히 iMessage 플러그인은 `chat.db`를 직접 읽고 AppleScript로 메시지를 보냅니다. 접근 제어 기능이 들어 있지만, 허용 목록을 꼭 설정하고 써야 합니다.
- **외부 목록은 줄어들 예정입니다.** 지금 이 마켓플레이스로 설치한 외부 플러그인이 나중에 목록에서 빠질 수 있습니다. 오래 쓸 플러그인은 제공사의 마켓플레이스나 claude.ai 디렉터리에서 받을 수 있는지 확인해 두면 좋습니다.

## 총평

**좋은 점**

- Anthropic 자체 플러그인 41개의 소스가 Apache 2.0으로 공개돼 있어, 플러그인 만드는 법을 배우기에 가장 좋은 견본입니다. 처음이라면 `plugins/example-plugin`부터 보면 됩니다.
- 외부 플러그인을 SHA로 고정하고, 업데이트마다 Claude가 전체 코드를 심사하는 구조가 잘 짜여 있습니다.
- 언어 서버, 코드 리뷰, 보안 스캔처럼 바로 효과를 보는 플러그인이 많습니다.

**아쉬운 점**

- 운영 방식이 바뀌는 중이라, 외부 플러그인이 앞으로 어떻게 될지 이 저장소만으로는 알기 어렵습니다.
- 317개를 고르는 기준은 설명과 분류뿐이라, 무엇이 좋은지는 직접 써 봐야 압니다.
- 심사는 Claude가 자동으로 하는 것이고, 원격 MCP 서버의 동작까지 보장하지는 못합니다.

**이렇게 시작하길 권합니다**

1. 쓰는 언어의 LSP 플러그인을 설치합니다 (예: `/plugin install swift-lsp@claude-plugins-official`).
2. `code-review`와 `security-guidance`를 설치해 평소 작업에 붙여 봅니다.
3. 외부 서비스 플러그인은 꼭 필요한 것만, 제공사가 직접 만든 것인지 확인하고 설치합니다.
