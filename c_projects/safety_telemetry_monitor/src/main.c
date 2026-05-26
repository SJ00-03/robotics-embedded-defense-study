#include "monitor.h"
#include <stdio.h>
int main(void){mon_ctx_t c; mon_init(&c); uint8_t good[]={0x55,0x01,0x10,(uint8_t)(0x55+0x01+0x10)}; uint8_t bad[]={0x55,0x01,0x20,0x00};
for(int i=0;i<40;i++){mon_tick(&c); if(i==5)mon_feed(&c,good,sizeof(good)); if(i==10)mon_feed(&c,bad,sizeof(bad)); mon_step(&c); printf("t=%u st=%d fault=0x%X\n",c.tick,c.st,c.fault.raw);} return 0;}
