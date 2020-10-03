CFLAGS = -Wall

RM = rm -f
PHONY = 

%.out: %.c
	gcc $(CFLAGS) $< -o $@ 

PHONY += clean
clean:
	$(RM) *.out

.PHONY: $(PHONY)

