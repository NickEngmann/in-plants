CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -I.
LDFLAGS = -lm

TEST_SRC = test/test_runner.c
TEST_BIN = test_runner

.PHONY: all test clean

all: $(TEST_BIN)

$(TEST_BIN): $(TEST_SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

test: $(TEST_BIN)
	./$(TEST_BIN)

clean:
	rm -f $(TEST_BIN)
