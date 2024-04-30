CC = g++
CFLAGS = -std=c++17 -Wall -Wextra -Wpedantic -fwrapv -lpqxx

SOURCES = $(wildcard src/*.cpp)
HEADERS = $(wildcard src/*.h)

TARGET = ./coursework

build: $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) $(SOURCES) -o $(TARGET)

run: build
	@$(TARGET)

.PHONY: build run
.IGNORE: run
