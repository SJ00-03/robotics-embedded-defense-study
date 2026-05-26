# Embedded Systems Study Checklist

## Fundamentals
- [ ] UART/SPI/I2C/CAN 동작 개념 비교 설명 가능
- [ ] polling vs interrupt 차이와 trade-off 설명 가능
- [ ] timer tick 기반 scheduler 개념 설명 가능
- [ ] DMA 개념 및 CPU offloading 의미 이해

## Firmware Architecture
- [ ] HAL/driver/app 계층 분리 이유 설명 가능
- [ ] ISR와 main loop 간 데이터 공유 위험(race condition) 설명 가능
- [ ] watchdog 역할과 fail-safe 전략 설명 가능
- [ ] 상태머신 기반 운용 로직 독해 가능

## Data Handling
- [ ] ring buffer 기반 RX/TX 처리 독해 가능
- [ ] packet framing/header/payload/checksum 흐름 설명 가능
- [ ] endian 처리 이슈 식별 가능

## Reliability
- [ ] fault detection(timeout/range/checksum) 조건 설계 가능
- [ ] health monitoring 지표 정의 가능
- [ ] 로그/진단 코드 체계화 가능
