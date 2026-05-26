#include "monitor.h"
#include <string.h>
#include <stdio.h>
static bool rpush(rx_ring_t*r,uint8_t v){if(r->c>=RX_CAP)return false;r->b[r->h]=v;r->h=(r->h+1)%RX_CAP;r->c++;return true;}
static bool rpop(rx_ring_t*r,uint8_t*v){if(!r->c)return false;*v=r->b[r->t];r->t=(r->t+1)%RX_CAP;r->c--;return true;}
static bool qpush(evq_t*q,mon_event_t e){if(q->c>=EV_CAP)return false;q->q[q->h]=e;q->h=(q->h+1)%EV_CAP;q->c++;return true;}
static bool qpop(evq_t*q,mon_event_t*e){if(!q->c)return false;*e=q->q[q->t];q->t=(q->t+1)%EV_CAP;q->c--;return true;}
static uint8_t csum(const uint8_t*d,uint16_t n){uint8_t s=0;for(uint16_t i=0;i<n;i++)s+=d[i];return s;}
void mon_init(mon_ctx_t*c){memset(c,0,sizeof(*c));c->st=BOOT;}
void mon_tick(mon_ctx_t*c){c->tick+=10; if(c->tick%200==0)qpush(&c->ev,EV_WDOG);} 
void mon_feed(mon_ctx_t*c,const uint8_t*d,uint16_t n){for(uint16_t i=0;i<n;i++)rpush(&c->rx,d[i]);}
static void parse(mon_ctx_t*c){uint8_t hdr[2]; if(c->rx.c<4)return; rpop(&c->rx,&hdr[0]); rpop(&c->rx,&hdr[1]); if(hdr[0]!=0x55){qpush(&c->ev,EV_PKT_BAD);return;} uint8_t payload=hdr[1]; if(c->rx.c<payload+1)return; uint8_t buf[64]; for(uint8_t i=0;i<payload+1;i++)rpop(&c->rx,&buf[i]); if(csum(hdr,2)+csum(buf,payload)!=buf[payload]) qpush(&c->ev,EV_PKT_BAD); else qpush(&c->ev,EV_PKT_OK);} 
void mon_step(mon_ctx_t*c){parse(c); mon_event_t e; while(qpop(&c->ev,&e)){if(c->st==BOOT)c->st=SELF_TEST; else if(c->st==SELF_TEST)c->st=NORMAL; if(e==EV_PKT_BAD){c->fault.bits.bad_checksum=1;c->st=DEGRADED;} if(e==EV_WDOG && c->fault.raw)c->st=FAIL_SAFE;}}
