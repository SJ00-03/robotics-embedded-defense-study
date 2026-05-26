#include "fw.h"
#include <stdio.h>
int main(void){fw_t f; SystemClock_Config(); GPIO_Init(); UART_Init(); Timer_Init(); FW_Init(&f);
for(int i=0;i<70;i++){FW_TickISR(&f); if(i==12){uint8_t p[4]={0xA1,0x00,0x55,(uint8_t)(0xA1^0x00^0x55)}; for(int k=0;k<4;k++)UART_RxCpltCallback(&f,p[k]);}
if(i==40){uint8_t b[4]={0xE0,0x01,0x00,0x00}; for(int k=0;k<4;k++)UART_RxCpltCallback(&f,b[k]);}
FW_MainLoopStep(&f); printf("tick=%u st=%d led=0x%02X fault=%u\n",f.tick,f.st,f.led,f.fault);} return 0;}
