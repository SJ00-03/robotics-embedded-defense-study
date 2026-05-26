#ifndef MONITOR_H
#define MONITOR_H
#include <stdbool.h>
#include <stdint.h>
#define RX_CAP 128
#define EV_CAP 32

typedef enum {BOOT=0,SELF_TEST,NORMAL,DEGRADED,FAIL_SAFE} mon_state_t;
typedef enum {EV_PKT_OK=0,EV_PKT_BAD,EV_WDOG} mon_event_t;
typedef struct{uint8_t b[RX_CAP];uint16_t h,t,c;} rx_ring_t;
typedef struct{mon_event_t q[EV_CAP];uint8_t h,t,c;} evq_t;
typedef union{uint32_t raw;struct{uint32_t bad_checksum:1;uint32_t timeout:1;uint32_t abnormal:1;}bits;} fault_u;
typedef struct{volatile uint32_t tick;mon_state_t st;fault_u fault;rx_ring_t rx;evq_t ev;} mon_ctx_t;
void mon_init(mon_ctx_t*);void mon_tick(mon_ctx_t*);void mon_feed(mon_ctx_t*,const uint8_t*,uint16_t);void mon_step(mon_ctx_t*);
#endif
