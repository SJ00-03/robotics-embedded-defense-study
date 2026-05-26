# C Language Study Checklist

## Core Syntax & Memory
- [ ] pointer 기초/이중 포인터/배열과 포인터 차이 설명 가능
- [ ] struct/enum/union을 상황에 따라 선택 가능
- [ ] memory layout(정렬/패딩) 확인 및 설명 가능
- [ ] bit mask/bit operation으로 플래그 관리 가능

## Compilation & Linkage
- [ ] header guard 작성 습관화
- [ ] header/source 분리 원칙 이해
- [ ] static vs extern 차이 및 사용 시점 설명 가능
- [ ] Makefile로 다중 소스 빌드 가능

## Embedded-oriented C
- [ ] volatile 필요성(ISR/shared variable) 설명 가능
- [ ] ring buffer 구현/독해 가능
- [ ] function pointer 콜백 구조 이해
- [ ] defensive coding(경계 검사, null 체크) 적용 가능

## Practice Targets
- [ ] UART packet parser 읽고 checksum 검증 흐름 설명
- [ ] FSM(IDLE/RUN/ERROR 등) 전이 조건 추적
- [ ] fault code 체계 설계 및 로깅 전략 정리
