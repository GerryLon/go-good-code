CC = gcc
CFLAGS += -Wall -pthread

RM = rm -f
PHONY =

%.out: %.c
	$(CC) $(CFLAGS) $< -o $@

PHONY += clean
clean:
	$(RM) *.out

.PHONY: $(PHONY)

