#ifndef FW_H
#define FW_H
#include <stdint.h>
#include <stdbool.h>
#define RB_CAP 64
#define LED_OK (1u<<0)
#define LED_ERR (1u<<1)
typedef enum{S_INIT=0,S_SELF_TEST,S_RUN,S_COMM_LOSS,S_ERROR} fw_state_t;
typedef struct{uint8_t b[RB_CAP];uint8_t h,t,c;} rb_t;
typedef struct{volatile uint32_t tick; volatile uint8_t rx_irq_flag; rb_t rb; fw_state_t st; uint8_t led; uint8_t fault;} fw_t;
void SystemClock_Config(void); void GPIO_Init(void); void UART_Init(void); void Timer_Init(void);
void FW_Init(fw_t*); void UART_RxCpltCallback(fw_t*,uint8_t); void FW_TickISR(fw_t*); void FW_MainLoopStep(fw_t*);
#endif
