#include "firmware.h"

#include <stdio.h>

int main(void) {
    firmware_ctx_t ctx;
    fw_init(&ctx);

    for (int i = 0; i < 80; i++) {
        fw_tick_isr(&ctx);
        if (i == 30) {
            uint8_t pkt[] = {0xAA, 0x01, 0x01, 0xAA ^ 0x01 ^ 0x01};
            fw_uart_feed(&ctx, pkt, sizeof(pkt));
        }
        if (i == 45) {
            uint8_t pkt[] = {0xAA, 0x01, 0x02, 0xAA ^ 0x01 ^ 0x02};
            fw_uart_feed(&ctx, pkt, sizeof(pkt));
        }
        fw_main_step(&ctx);
        printf("t=%u state=%d motor=(%d,%d) faults=0x%02X\n", ctx.tick_ms, ctx.state,
               ctx.motor.left_rpm, ctx.motor.right_rpm, ctx.fault_flags);
    }
    return 0;
}
