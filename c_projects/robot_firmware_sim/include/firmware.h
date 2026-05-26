#ifndef FIRMWARE_H
#define FIRMWARE_H

#include <stdbool.h>
#include <stdint.h>

#define SENSOR_RING_CAP 32
#define EVENT_QUEUE_CAP 32

typedef enum {
    ST_IDLE = 0,
    ST_CALIBRATION,
    ST_RUNNING,
    ST_OBSTACLE_DETECTED,
    ST_ERROR
} robot_state_t;

typedef enum {
    EV_NONE = 0,
    EV_TICK,
    EV_UART_PACKET,
    EV_OBSTACLE,
    EV_CLEAR,
    EV_FAULT
} event_type_t;

typedef struct {
    float kp, ki, kd;
    float integral;
    float prev_error;
} pid_t;

typedef struct {
    int16_t left_rpm;
    int16_t right_rpm;
} motor_controller_t;

typedef struct {
    float samples[SENSOR_RING_CAP];
    uint8_t head;
    uint8_t tail;
    uint8_t count;
} ring_buffer_t;

typedef struct {
    event_type_t queue[EVENT_QUEUE_CAP];
    uint8_t head;
    uint8_t tail;
    uint8_t count;
} event_queue_t;

typedef struct {
    volatile uint32_t tick_ms; /* volatile: ISR-like tick writer, main loop reader */
    robot_state_t state;
    motor_controller_t motor;
    pid_t pid;
    ring_buffer_t sensor_ring;
    event_queue_t events;
    uint8_t fault_flags;
} firmware_ctx_t;

void fw_init(firmware_ctx_t *ctx);
void fw_tick_isr(firmware_ctx_t *ctx);
void fw_uart_feed(firmware_ctx_t *ctx, const uint8_t *data, uint16_t len);
void fw_main_step(firmware_ctx_t *ctx);

#endif
