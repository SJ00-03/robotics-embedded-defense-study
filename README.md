# Robotics / Embedded / Safety-Critical Study Portfolio

이 저장소는 **로봇·임베디드·안전중요 시스템 분야 취업 준비생**이 C/Python 코드를 직접 읽고 해석하며 실무 감각을 키우기 위한 학습 포트폴리오입니다.

> ⚠️ 안전 원칙: 본 저장소의 모든 예제는 **교육용 가상 시뮬레이션**입니다. 실제 무기 제어, 유도, 타격, 교전, 살상 목적의 로직은 포함하지 않습니다.

## 프로젝트 목적

- 긴 코드 독해 중심 학습 (단순 따라치기 지양)
- C와 Python을 모두 활용한 시스템적 사고 훈련
- 로봇/임베디드/안전중요 분야 면접 및 포트폴리오 대비
- 자료구조, 상태머신, 통신 파싱, fault detection 등 핵심 개념 체득

## 저장소 구조

```text
.
├── AGENTS.md
├── README.md
├── c_projects/
├── python_projects/
└── study_notes/
    ├── c_language_checklist.md
    ├── embedded_checklist.md
    ├── interview_questions.md
    ├── python_checklist.md
    └── robotics_checklist.md
```

## 실행 방법 (현재 단계)

현재는 학습 구조 및 체크리스트를 먼저 구성한 상태입니다.

1. 저장소 클론
2. `study_notes/`의 체크리스트 기반으로 학습 계획 수립
3. 이후 PR에서 `c_projects/`, `python_projects/`에 실행 가능한 시뮬레이션 프로젝트 추가

## 학습해야 할 핵심 개념

### 자료구조 / 알고리즘
- Queue, Stack, Ring Buffer, Linked List, Heap
- Finite State Machine, Path Planning(BFS/A*)

### C 언어 / 펌웨어
- Pointer, Struct, Enum, Union, Bit Operation
- Memory Layout, Static/Extern, Volatile
- Header/Source 분리, Makefile 기반 빌드
- Function Pointer, Defensive Coding

### Python / 시스템 코드
- Class, Dataclass, Enum, Deque/Queue
- Pathlib, Argparse, Logging, Type Hint
- Exception Handling, Threading/Asyncio

### 도메인 역량
- 로봇: 센서처리, PID, Odometry, Sensor Fusion, FSM
- 안전중요: Telemetry Parsing, Packet Protocol, CRC/Checksum, Health Monitoring, Fault Detection
- 임베디드: UART/SPI/I2C/CAN 개념, Timer/Interrupt 시뮬레이션, HAL 추상화 구조

## 포트폴리오 사용 가이드

- 각 프로젝트는 **학습용 시뮬레이션**임을 명시
- README에 목표·실행법·핵심 개념·확장 아이디어 포함
- 코드 리뷰 관점에서 “왜 이렇게 설계했는지”를 주석/문서로 기록
- 면접 대비용으로 `study_notes/interview_questions.md`를 지속 업데이트
