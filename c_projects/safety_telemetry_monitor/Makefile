CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -Iinclude
SRC=$(wildcard src/*.c)
all: safety_monitor
safety_monitor: $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $@
clean:
	rm -f safety_monitor
