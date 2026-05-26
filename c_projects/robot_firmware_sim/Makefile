CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -Iinclude
SRC=$(wildcard src/*.c)

all: robot_fw_sim

robot_fw_sim: $(SRC)
	$(CC) $(CFLAGS) $(SRC) -lm -o $@

clean:
	rm -f robot_fw_sim
