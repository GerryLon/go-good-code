#include <stdio.h>
#include <stdlib.h>

#include <pthread.h>

static void *start_fn1(void *arg) {
	printf("thread 1\n");
	pthread_exit((void *)1);
}

static void *start_fn2(void *arg) {
	printf("thread 2\n");
	pthread_exit((void *)2);
}

int main() {
	int err;
	pthread_t tid1, tid2;
	void *thread_retval;

	err = pthread_create(&tid1, NULL, start_fn1, NULL);
	if (err != 0) {
		perror("pthread_create() 1");
		exit(1);
	}
	
	err = pthread_create(&tid2, NULL, start_fn2, NULL);
	if (err != 0) {
		perror("pthread_create() 2");
		exit(1);
	}

	err = pthread_join(tid1, &thread_retval);
	if (err != 0) {
		perror("pthread_join() 1");
		exit(1);
	}
	printf("thread 1 exit code: %d\n", (int)thread_retval);
	
	err = pthread_join(tid2, &thread_retval);
	if (err != 0) {
		perror("pthread_join() 2");
		exit(1);
	}
	printf("thread 2 exit code: %d\n", (int)thread_retval);
	
	exit(0);
}

