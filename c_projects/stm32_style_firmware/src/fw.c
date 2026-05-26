#include "fw.h"
#include <stdio.h>
#include <string.h>
static bool rb_push(rb_t*r,uint8_t v){if(r->c>=RB_CAP)return false;r->b[r->h]=v;r->h=(r->h+1)%RB_CAP;r->c++;return true;}
static bool rb_pop(rb_t*r,uint8_t*v){if(!r->c)return false;*v=r->b[r->t];r->t=(r->t+1)%RB_CAP;r->c--;return true;}
static uint8_t checksum(const uint8_t*d,uint8_t n){uint8_t s=0;for(uint8_t i=0;i<n;i++)s^=d[i];return s;}
void SystemClock_Config(void){puts("SystemClock_Config");}
void GPIO_Init(void){puts("GPIO_Init");}
void UART_Init(void){puts("UART_Init");}
void Timer_Init(void){puts("Timer_Init");}
void FW_Init(fw_t*f){memset(f,0,sizeof(*f));f->st=S_INIT;}
void UART_RxCpltCallback(fw_t*f,uint8_t byte){/* race risk: ISR writes, main reads */ rb_push(&f->rb,byte); f->rx_irq_flag=1;}
void FW_TickISR(fw_t*f){f->tick+=10;}
static void parse_cmd(fw_t*f){uint8_t b[4]; if(f->rb.c<4)return; for(int i=0;i<4;i++)rb_pop(&f->rb,&b[i]); if(checksum(b,3)!=b[3]){f->fault=1;f->st=S_ERROR;return;} if(b[0]==0xA1)f->led^=LED_OK; if(b[0]==0xE0){f->fault=2;f->st=S_COMM_LOSS;}}
void FW_MainLoopStep(fw_t*f){if(f->st==S_INIT && f->tick>20)f->st=S_SELF_TEST; if(f->st==S_SELF_TEST && f->tick>80)f->st=S_RUN; if(f->tick>500 && f->st==S_RUN)f->st=S_COMM_LOSS; if(f->rx_irq_flag){parse_cmd(f);f->rx_irq_flag=0;} if(f->fault)f->led|=LED_ERR;}
