#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char **argv) {
	FILE *fp = NULL;
	char *line_buffer;
	size_t line_size;

	if (argc < 2) {
		fprintf(stderr, "Usage: %s filename", argv[0]);
		exit(1);
	}	

	fp = fopen(argv[1], "r");
	if (!fp) {
		perror("fopen()");
		exit(1);
	}
	
	// 重要
	line_buffer = NULL;
	line_size = 0;

	while (1) {
		if (getline(&line_buffer, &line_size, fp) < 0) {
			break;
		}
		printf("%ld, line_size=%ld\n", strlen(line_buffer), line_size);
	}

	fclose(fp);
	return 0;
}

