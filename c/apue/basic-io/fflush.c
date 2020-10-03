#include <stdio.h>
#include <stdlib.h>

int main() {
	printf("Before");
	fflush(NULL);
	// printf("Before\n");

	while (1);

	printf("After");
}
