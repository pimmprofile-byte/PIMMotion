# assets/ — 이미지 파이프라인

핌아트웍스 리뉴얼 시안(`../pimmartworks.html`)이 참조하는 실이미지 폴더.

## 파일명 규칙 (핸드오프 §5)

`프로젝트이름_용도.확장자`

| 용도 | 예시 | 설명 |
|---|---|---|
| `_hero` | `toemarok_hero.jpg` | 카드/상세 대표 이미지 (16:9 권장, ≤300KB) |
| `_g1`, `_g2` … | `bestpen_g1.jpg` | 상세 모달 갤러리 (정방형 크롭) |

이 외 사이트 공통 이미지:

| 파일 | 용도 |
|---|---|
| `hero_main.jpg` | 히어로 풀스크린 배경 (교체 지점) |
| `og_cover.jpg` | Open Graph 공유 카드 (1200×630) |

## 현재 상태

시안 단계라 실이미지가 없습니다. `hero` 경로가 없거나 로드 실패하면
자동으로 **빗금 플레이스홀더 + "공간 사진 준비중"** 으로 폴백합니다(§5 엣지케이스).
실이미지를 이 폴더에 규칙대로 넣으면 코드 수정 없이 반영됩니다.

## 프로젝트 추가

`pimmartworks.html`의 `PROJECTS` 배열에 객체 하나만 추가하면 그리드·필터·상세가
자동 렌더링됩니다. `id`와 `WORK` 번호는 자동 생성됩니다.

```js
{
  cat: "IMMERSIVE EXHIBITION",   // CATEGORY_ORDER 중 하나
  title: "프로젝트명",
  client: "클라이언트",
  place: "지역",
  date: "2024",
  hero: "assets/project_hero.jpg",  // 없으면 null → 플레이스홀더
  desc: ["문단1", "문단2"],
  gallery: ["assets/project_g1.jpg"], // 선택
  filmSoon: true,                     // 선택: "영상 준비중" 타일
  link: "https://…", linkText: "자세히 보기" // 선택
}
```
