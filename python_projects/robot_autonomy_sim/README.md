# Robot Autonomy Simulation (Python)

교육용 2D 이동 로봇 자율주행 시뮬레이션 프로젝트입니다.

- ROS 비의존, 순수 Python 표준 라이브러리 기반
- mock LiDAR 유사 센서 + wheel odometry + BFS 경로계획 + PID + FSM
- 실제 무기 목적 로직 없음 (학습용 시뮬레이션 전용)

## 실행

```bash
python main.py
```

## 테스트

```bash
python -m pytest tests -q
```
