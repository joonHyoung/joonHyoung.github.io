---
title: "anthropics/skills 리뷰: Anthropic 공식 Claude 스킬 19개 뜯어보기"
series: "AI Skills 리뷰"
strapline: "AI Skills"
description: "Anthropic 공식 스킬 저장소 anthropics/skills를 직접 받아 스킬 19개의 구성, 설치 방법, 번들 스크립트의 보안 포인트, 쓸 만한 스킬과 아쉬운 점을 정리했습니다."
permalink: /ai-skills/anthropic-skills-review/
categories:
  - "AI Skills"
tag:
  - "AI Skills"
  - "Claude"
  - "Claude Code"
  - "Anthropic"
  - "Agent Skills"
  - "SKILL.md"
toc: true
toc_sticky: true
last_modified_at: 2026-11-20
comments: true
mathjax: false
---

Claude에 "스킬"을 붙이면 특정 작업을 정해진 방식대로 반복해서 해낼 수 있습니다. 그 스킬의 공식 예제이자, claude.ai의 Word·Excel·PowerPoint·PDF 기능이 실제로 쓰는 구현이 담긴 곳이 [anthropics/skills](https://github.com/anthropics/skills)입니다. 2026년 11월 20일 기준 스타 약 19.8만 개, 마지막 커밋은 11월 16일입니다. 저장소를 직접 받아 스킬 19개의 내용과 함께 들어 있는 스크립트까지 살펴봤습니다.

## 스킬이란

스킬은 `SKILL.md` 파일 하나가 들어 있는 폴더입니다. 맨 위 YAML 머리말에는 `name`과 `description` 두 필드만 있으면 되고, 그 아래에 Claude가 따를 지시문을 씁니다. 필요하면 스크립트, 템플릿, 참고 문서를 같은 폴더에 둡니다.

```markdown
---
name: my-skill-name
description: 무엇을 하는 스킬이며 언제 써야 하는지
---

# My Skill Name

[스킬이 켜졌을 때 Claude가 따를 지시문]
```

핵심은 `description`입니다. Claude는 평소 모든 스킬의 이름과 설명만 알고 있다가, 요청이 설명과 맞을 때 본문을 읽습니다. 그래서 스킬을 수십 개 깔아도 컨텍스트가 크게 늘지 않습니다. 반대로 설명을 모호하게 쓰면 스킬이 필요한 순간에 불리지 않습니다. 이 저장소의 스킬들이 설명에 "이럴 때 써라, 이럴 땐 쓰지 마라"를 길게 적어 두는 이유입니다.

스킬 형식은 Anthropic 전용이 아니라 [Agent Skills 표준](https://agentskills.io/specification)으로 공개돼 있습니다. 저장소의 `spec/` 폴더에는 이제 그 주소로 가는 링크만 남아 있습니다.

## 저장소 구성과 설치

| 폴더 | 내용 |
|---|---|
| `skills/` | 스킬 19개 |
| `template/` | 새 스킬을 만들 때 복사할 `SKILL.md` 템플릿 |
| `spec/` | Agent Skills 명세 링크 |
| `.claude-plugin/` | Claude Code 플러그인 마켓플레이스 정의 |

Claude Code에서는 이 저장소를 플러그인 마켓플레이스로 등록해 설치합니다.

```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

마켓플레이스에는 플러그인 5개가 있습니다. 스킬을 하나씩 고를 수는 없고 플러그인 단위로 설치합니다.

- **document-skills**: docx, xlsx, pptx, pdf
- **example-skills**: 나머지 예제 스킬 12개
- **claude-api**, **academy-guide**, **discernment-nudge**: 각각 단독 플러그인

claude.ai 유료 플랜에는 이 예제 스킬들이 이미 들어 있고, Claude API에서도 Skills API로 같은 스킬을 쓰거나 직접 만든 스킬을 올릴 수 있습니다.

## 스킬 19개 한눈에 보기

| 분류 | 스킬 | 하는 일 | 스크립트 |
|---|---|---|---|
| 문서 | **docx** | Word 문서 생성·편집, 변경 추적, 댓글 | 있음 |
| 문서 | **xlsx** | 스프레드시트 생성·편집, 수식 재계산 | 있음 |
| 문서 | **pptx** | 프레젠테이션 생성·편집, 썸네일 | 있음 |
| 문서 | **pdf** | 텍스트·표 추출, 병합·분할, 양식 채우기 | 있음 |
| 개발 | **claude-api** | Claude API·SDK 레퍼런스 (8개 언어) | 일부 |
| 개발 | **mcp-builder** | MCP 서버 설계·구현 가이드 (Python, TypeScript) | 평가용 |
| 개발 | **webapp-testing** | Playwright로 로컬 웹앱 테스트 | 있음 |
| 개발 | **web-artifacts-builder** | React + Tailwind + shadcn/ui로 HTML 아티팩트 제작 | 있음 |
| 개발 | **skill-creator** | 스킬 작성, 평가 실행, 설명 최적화 | 있음 |
| 디자인 | **frontend-design** | 뻔한 기본값을 피하는 UI 디자인 방향 | 없음 |
| 디자인 | **canvas-design** | 포스터·아트를 PNG/PDF로 (폰트 동봉) | 없음 |
| 디자인 | **algorithmic-art** | p5.js 생성 예술 | 템플릿 |
| 디자인 | **theme-factory** | 테마 10종을 문서·슬라이드에 적용 | 없음 |
| 디자인 | **brand-guidelines** | Anthropic 브랜드 색·서체 적용 | 없음 |
| 디자인 | **slack-gif-creator** | Slack용 애니메이션 GIF | 있음 |
| 업무 | **internal-comms** | 사내 공지, 상태 보고, 장애 보고서 양식 | 없음 |
| 업무 | **doc-coauthoring** | 문서 공동 작성 워크플로 | 없음 |
| 대화 | **discernment-nudge** | 답변 뒤에 검증용 후속 질문 2~3개 덧붙이기 | 없음 |
| 대화 | **academy-guide** | 사용법 질문에 Claude Academy 강좌 추천 | 없음 |

절반 정도는 지시문만 있는 스킬이고, 문서 스킬과 개발 스킬은 파이썬·셸 스크립트를 함께 씁니다.

## 눈여겨볼 스킬

### 문서 스킬 4종: 가장 실전적인 부분

docx, xlsx, pptx, pdf는 "예제"라기보다 실제 제품 코드에 가깝습니다. claude.ai에서 Word나 Excel 파일을 만들 때 쓰는 구현이 바로 이것입니다. 스크립트 수만 봐도 docx 15개, pptx 17개, xlsx 12개입니다.

지시문을 읽어 보면 어디서 실수가 나는지 잘 정리돼 있습니다. 예를 들어 docx는 기존 문서를 고칠 때 XML을 풀어서 제자리에서만 수정하고 다시 정렬하지 말라고 합니다. 변경 추적이 필요하면 작성자를 지정해 모든 수정이 추적되는지 검증하라고 합니다. xlsx는 LibreOffice로 수식을 다시 계산해 오류 셀이 남았는지 확인합니다. 최근 커밋도 이쪽에 몰려 있습니다. 11월 14일과 16일에 압축 해제, 검증, LibreOffice 실행 부분이 연달아 고쳐졌고, 11월 6일에는 Office 스킬 라이선스가 Apache 2.0으로 바뀌었습니다. 이제 상업적으로 가져다 고쳐 써도 됩니다.

### skill-creator: 스킬을 만드는 스킬

스킬을 직접 만들 생각이라면 가장 먼저 볼 스킬입니다. 의도 파악, 인터뷰, `SKILL.md` 작성까지 안내하고, 평가 단계까지 들어 있습니다. `run_eval.py`가 `claude -p`를 하위 프로세스로 띄워 테스트 질문마다 스킬이 실제로 불리는지 확인합니다. `improve_description.py`는 그 결과를 보고 `description`을 고쳐 줍니다. 앞에서 말한 "설명이 곧 트리거"라는 점을 도구로 해결한 셈입니다.

### claude-api: 가장 자주 갱신되는 스킬

커밋 기록을 보면 9~10월 업데이트의 대부분이 이 스킬입니다. 모델 ID, 가격, 사라진 파라미터 같은 정보를 담아 두고, 학습 데이터에 남은 옛 API를 그대로 쓰지 말라고 경고합니다. 예를 들어 최신 모델에서 `budget_tokens`를 쓰면 400 오류가 난다는 식입니다. Python, TypeScript, Go, Java, C#, PHP, Ruby, curl별 문서가 따로 있습니다.

다만 바로 그 이유로 금방 낡습니다. 모델 표에 "2026-10-06 기준"이라고 적혀 있고, 11월 9일에 나온 Claude Fable 5.2는 아직 반영되지 않았습니다. 모델 정보는 공식 문서와 한 번 더 대조하는 편이 안전합니다.

### discernment-nudge: 답을 의심하게 만드는 스킬

조언, 계획, 추정, 데이터 해석처럼 사용자가 그대로 믿고 행동할 만한 답을 준 뒤에 "이 숫자의 출처를 확인했나요?" 같은 짧은 후속 질문을 2~3개 붙이는 스킬입니다. 대화당 한 번만, 간단한 질문이나 코드 작업이나 창작에는 쓰지 않도록 조건이 꼼꼼합니다. 기능보다 AI 답변을 비판적으로 읽는 습관을 들이게 하려는 시도라는 점이 흥미롭습니다.

## 보안 관점에서 확인한 것

스킬은 지시문뿐 아니라 스크립트도 실행하게 하므로, 공식 저장소라도 무엇을 실행하는지는 알고 쓰는 게 좋습니다. 번들 스크립트에서 하위 프로세스 실행, 네트워크 접근, 패키지 설치 코드를 찾아봤습니다. 악성으로 볼 만한 코드는 없었고, 아래처럼 알고 써야 할 동작은 있었습니다.

| 스킬 | 동작 | 참고 |
|---|---|---|
| docx · pptx · xlsx | LibreOffice(`soffice`)를 하위 프로세스로 실행 | 샌드박스에서 소켓이 막혀 있으면 임시 폴더에 C 소스를 쓰고 `gcc`로 컴파일해 `LD_PRELOAD`로 끼워 넣음 |
| webapp-testing | `with_server.py`가 서버 실행 명령을 `shell=True`로 실행 | 넘겨준 명령이 셸에서 그대로 실행되므로 입력을 신뢰할 수 있을 때만 사용 |
| web-artifacts-builder | `init-artifact.sh`가 `npm install -g pnpm`과 다수의 npm 패키지 설치 | 전역 설치가 포함됨. 프로젝트 폴더나 컨테이너에서 실행 권장 |
| skill-creator | `claude -p`를 하위 프로세스로 실행 | 내 Claude 계정 사용량이 소모됨 |
| claude-api | 진단 스크립트가 `ANTHROPIC_BASE_URL`(기본 api.anthropic.com)로 요청 | API 키는 환경 변수에서 읽음 |

라이선스는 18개 폴더에 Apache 2.0 `LICENSE.txt`가 들어 있습니다. `doc-coauthoring`에만 라이선스 파일이 없습니다. 의존성 고지는 루트의 `THIRD_PARTY_NOTICES.md`에 모여 있습니다.

README에도 "시연과 교육 목적"이라는 면책 문구가 있습니다. claude.ai 안에서 실제로 동작하는 방식이 이 구현과 다를 수 있으니, 중요한 작업에 쓰기 전에 직접 시험해 보라는 뜻입니다.

## 총평

**좋은 점**

- 문서 스킬 4종은 실제 서비스에 쓰이는 수준이고, 이제 Apache 2.0이라 마음껏 참고하고 고칠 수 있습니다.
- `description`을 어떻게 쓰는지, 스크립트와 참고 문서를 어떻게 나누는지 등 스킬 작성의 모범 사례를 한곳에서 볼 수 있습니다.
- skill-creator로 만들기부터 평가까지 한 번에 해 볼 수 있습니다.

**아쉬운 점**

- claude-api처럼 정보성 스킬은 모델 출시 속도를 따라가지 못하는 시차가 생깁니다.
- 플러그인 단위로만 설치되므로 example-skills를 깔면 스킬 12개가 한꺼번에 들어옵니다. 쓰지 않는 스킬이 엉뚱한 요청에 불릴 수 있습니다.
- brand-guidelines와 internal-comms는 Anthropic 사내 양식 그대로라 그대로 쓰기보다는 자기 회사 양식으로 바꿔 쓰는 견본에 가깝습니다.

**추천 순서**

1. 문서 작업이 많다면 `document-skills`부터 설치합니다.
2. 스킬을 만들어 보고 싶다면 `template/`와 `skill-creator`를 함께 봅니다.
3. Claude API로 개발한다면 `claude-api`를 설치하되, 모델 정보는 공식 문서와 대조합니다.

외부 커뮤니티 스킬을 고르기 전에 기준점으로 삼기에 가장 좋은 저장소입니다. 다른 스킬 저장소를 볼 때도 여기서 정한 형식과 견줘 보면 품질을 가늠하기 쉽습니다.
