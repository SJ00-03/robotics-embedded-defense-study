CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -Iinclude
SRC=$(wildcard src/*.c)
all: stm32_fw_sim
stm32_fw_sim: $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $@
clean:
	rm -f stm32_fw_sim
