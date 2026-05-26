#include "firmware.h"

#include <math.h>
#include <stdio.h>
#include <string.h>

#define FAULT_BAD_PACKET (1u << 0)
#define FAULT_SENSOR_STUCK (1u << 1)

static bool ring_push(ring_buffer_t *rb, float v) {
    if (rb->count >= SENSOR_RING_CAP) {
        return false;
    }
    rb->samples[rb->head] = v;
    rb->head = (uint8_t)((rb->head + 1u) % SENSOR_RING_CAP);
    rb->count++;
    return true;
}

static bool ring_pop(ring_buffer_t *rb, float *out) {
    if (rb->count == 0u) return false;
    *out = rb->samples[rb->tail];
    rb->tail = (uint8_t)((rb->tail + 1u) % SENSOR_RING_CAP);
    rb->count--;
    return true;
}

static bool event_push(event_queue_t *q, event_type_t e) {
    if (q->count >= EVENT_QUEUE_CAP) return false;
    q->queue[q->head] = e;
    q->head = (uint8_t)((q->head + 1u) % EVENT_QUEUE_CAP);
    q->count++;
    return true;
}

static bool event_pop(event_queue_t *q, event_type_t *e) {
    if (q->count == 0u) return false;
    *e = q->queue[q->tail];
    q->tail = (uint8_t)((q->tail + 1u) % EVENT_QUEUE_CAP);
    q->count--;
    return true;
}

static uint8_t checksum8(const uint8_t *d, uint16_t n) {
    uint8_t s = 0u;
    for (uint16_t i = 0; i < n; i++) s ^= d[i];
    return s;
}

static float pid_update(pid_t *pid, float target, float current) {
    float e = target - current;
    pid->integral += e * 0.02f;
    if (pid->integral > 5.0f) pid->integral = 5.0f;
    if (pid->integral < -5.0f) pid->integral = -5.0f;
    float d = (e - pid->prev_error) / 0.02f;
    pid->prev_error = e;
    return pid->kp * e + pid->ki * pid->integral + pid->kd * d;
}

static float mock_encoder_speed(uint32_t t, int side) {
    float base = 1.0f + 0.2f * sinf((float)t / 1000.0f);
    return side == 0 ? base : base * 0.95f;
}

void fw_init(firmware_ctx_t *ctx) {
    memset(ctx, 0, sizeof(*ctx));
    ctx->state = ST_IDLE;
    ctx->pid.kp = 2.0f; ctx->pid.ki = 0.2f; ctx->pid.kd = 0.08f;
}

void fw_tick_isr(firmware_ctx_t *ctx) {
    ctx->tick_ms += 10u;
    (void)event_push(&ctx->events, EV_TICK);
}

void fw_uart_feed(firmware_ctx_t *ctx, const uint8_t *data, uint16_t len) {
    if (len < 4u) return;
    if (data[0] != 0xAAu) return;
    uint8_t payload_len = data[1];
    if ((uint16_t)(payload_len + 3u) != len) {
        ctx->fault_flags |= FAULT_BAD_PACKET;
        (void)event_push(&ctx->events, EV_FAULT);
        return;
    }
    uint8_t c = checksum8(data, (uint16_t)(len - 1u));
    if (c != data[len - 1u]) {
        ctx->fault_flags |= FAULT_BAD_PACKET;
        (void)event_push(&ctx->events, EV_FAULT);
        return;
    }
    if (payload_len > 0u && data[2] == 0x01u) (void)event_push(&ctx->events, EV_OBSTACLE);
    if (payload_len > 0u && data[2] == 0x02u) (void)event_push(&ctx->events, EV_CLEAR);
    (void)event_push(&ctx->events, EV_UART_PACKET);
}

static void handle_tick(firmware_ctx_t *ctx) {
    float left = mock_encoder_speed(ctx->tick_ms, 0);
    float right = mock_encoder_speed(ctx->tick_ms, 1);
    float avg = (left + right) * 0.5f;
    if (!ring_push(&ctx->sensor_ring, avg)) {
        ctx->fault_flags |= FAULT_SENSOR_STUCK;
        ctx->state = ST_ERROR;
        return;
    }

    if (ctx->state == ST_RUNNING) {
        float cmd = pid_update(&ctx->pid, 1.5f, avg);
        ctx->motor.left_rpm = (int16_t)(100 + cmd * 20);
        ctx->motor.right_rpm = (int16_t)(100 + cmd * 18);
    }
}

void fw_main_step(firmware_ctx_t *ctx) {
    event_type_t e;
    while (event_pop(&ctx->events, &e)) {
        switch (e) {
            case EV_TICK:
                if (ctx->state == ST_IDLE && ctx->tick_ms > 50u) ctx->state = ST_CALIBRATION;
                if (ctx->state == ST_CALIBRATION && ctx->tick_ms > 200u) ctx->state = ST_RUNNING;
                handle_tick(ctx);
                break;
            case EV_OBSTACLE:
                ctx->state = ST_OBSTACLE_DETECTED;
                ctx->motor.left_rpm = 0;
                ctx->motor.right_rpm = 0;
                break;
            case EV_CLEAR:
                if (ctx->state == ST_OBSTACLE_DETECTED) ctx->state = ST_RUNNING;
                break;
            case EV_FAULT:
                ctx->state = ST_ERROR;
                break;
            default:
                break;
        }
    }

    float tmp;
    if (ring_pop(&ctx->sensor_ring, &tmp)) {
        (void)tmp;
    }
}
