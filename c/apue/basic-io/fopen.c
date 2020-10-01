#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int main() {
	FILE* fp = fopen("fopen.c", "r");
	if (!fp) {
		// fprintf(stderr, "fopen()");
		perror("fopen()");
		exit(1);
	}
	
	fclose(fp);
	return 0;
}

