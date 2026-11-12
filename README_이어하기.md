# CCEL 홈페이지 강동권 최종안 3종 (261110)

## 보는 법
- `index.html` 을 더블클릭하면 비교 화면이 열린다. 위 막대에서 테마(Awesomic·Intercom·Mercury)와 쪽(Index·Professor·Members·Research·Publications·Contact)을 고르고, "새 창"으로 따로 연다. 키보드 ←/→ 로 테마를 넘긴다.
- 각 테마 폴더(`awesomic\`, `intercom\`, `mercury\`)의 `index.html` 이 그 테마의 메인 화면이다.

## 구성 (세 사람 작업을 나눈 방식)
| 층 | 출처 | 위치 |
|---|---|---|
| 데이터 (논문 403편, 멤버 34명·동문 28명, 표지 48장, 교수 이력, 연락처) | 문진욱 ccel-s1 `_shared/content.js` | `_shared/` (한 벌만) |
| 하위 쪽 5개와 기능 (논문 검색·연도/상태/분야 필터, Selected·Covers 탭, 멤버 보기 전환) | 문진욱 ccel-s1 HTML + `assets/*.js` | 각 테마 폴더, 그대로 복사 |
| 메인 화면 구성 (전면 사진, 숫자, 번호 붙은 연구 목록, 뉴스 + 모집, 대표 논문, 표지, 후원, 소개 + 연구실 영상) | 성기헌 C안 구성을 데이터로 다시 만듦 | `src/home.js`, `build_final.py` 의 `HOME` |
| 디자인 3종 + 스크롤 효과 | 강동권 (261012 토큰, 261026 효과) | `build_final.py` 의 `THEMES`, `src/home.css`, `src/motion.js` |
| 진욱 CSS의 흰색 고정값을 변수로 바꾼 연결층 | 새로 만듦 | `src/bridge.css` |

원본 참고용 클론: `..\_ref_261110\` (ccel-s1, ccel-s3, ccel-preview, qheosldia-preview). `build_final.py` 는 `_ref_261110\ccel-s1` 에서 읽는다.

## 다시 만들기
`python build_final.py` → `_shared\`, 테마 폴더 3개, `index.html` 을 지우고 새로 만든다. 고칠 곳:
- 색·서체·모서리·테마별 배치: `build_final.py` 의 `THEMES` (`vars` 는 토큰, `css` 는 배치 차이)
- 메인 화면 내용·순서: `HOME` 문자열과 `src/home.js`
- 스크롤 효과: `src/motion.js` (등장 대상은 `GROUPS`), `src/home.css` 맨 아래 motion 절
- 진욱 씨가 데이터나 하위 쪽을 고치면 `_ref_261110\ccel-s1` 에서 `git pull` 후 다시 만든다

## 넣은 효과 (모든 쪽)
Lenis 부드러운 스크롤, 맨 위 진행 막대, 내리면 숨고 올리면 나오는 반투명 메뉴, 제목 단어 올라오기, 흐릿하게 떠오르는 등장 효과, 숫자 카운트, 히어로 사진 패럴랙스, 연구 순환 그림 확대, 연구 목록에 마우스를 올리면 그림이 커서를 따라옴, 표지 두 줄 반대 방향 흐름, 후원 로고 흐름. 동작 줄이기 설정을 켠 사람에게는 효과 없이 보인다.

## 검수 (261110)
- PC 1440 폭, 휴대폰 390 폭에서 3종 × 6쪽 = 18쪽 모두 스크립트 오류 0, 가로 넘침 0
- 서버 없이 파일로 열어도 논문 403편, 메인 화면 부품 모두 채워짐

## 남은 일 / 알아둘 것
- 대표 논문 6편(교수님 고정 목록)은 4편이 표지 그림이 없어 분야 번호 카드로 표시한다. 논문별 그림을 받으면 바꿀 수 있다
- 연구실 영상 2개는 지금 서버(http://ccel.snu.ac.kr/pages/vid/)에서 불러온다. https 로 공개하면 막힐 수 있다
- 261112 공개: https://kangdonggwon.github.io/ccel-homepage-final/ (저장소 KangDongGwon/ccel-homepage-final, public, 이 폴더가 곧 저장소). 갱신 = `python build_final.py` 후 이 폴더에서 `git add -A`, `git -c user.name=Mosani13 -c user.email=dkclaude13@gmail.com commit -m ...`, `git push`. 1~2분 뒤 반영. 10/26 링크(ccel-homepage-mockup)는 그대로 둠
- 다음 단계 후보: 진욱·기헌 씨에게 "데이터·하위 쪽은 진욱 것 공통, 디자인은 각자 3종" 구조 제안
