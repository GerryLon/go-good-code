#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>

pthread_t thread;

static void printids(const char *prefix) {
	pid_t pid = getpid();
	pthread_t tid = pthread_self();
	
	printf("%s pid: %u, tid: %u, (0x%x)\n",
			prefix,	
			(unsigned int)pid,
			(unsigned int)tid,
			(unsigned int)tid);
}

static void *start_fn(void *arg) {
	printids("new  thread: ");	
	return ((void *)0);
}

int main() {
	int err;
	err = pthread_create(&thread, NULL, start_fn, NULL);
	if (err != 0) {
		perror("pthread_create()");
		exit(1);
	}
	printids("main thread: ");
	sleep(1);

	return 0;
}
