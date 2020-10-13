#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#include <string.h>


int main() {
	int fd[2];
	int err;
	pid_t pid;

	// 创建管道, pipefd[0]为读端, pipefd[1]为写端
	err = pipe(fd);
	if (err) {
		perror("pipe()");
		exit(1);
	}

	// 创建子进程
	pid = fork();
	if (pid < 0) {
		perror("fork()");
		exit(1);
	}

	// child
	if (pid == 0) {
		close(fd[0]); // 关闭读端

		int i;
		char msg[100];


		for (i = 0; i < 5; i++) {
			memset(msg, 0, sizeof(msg));
			sprintf(msg, "child msg %d", i);

			if ((write(fd[1], msg, strlen(msg))) < 0) {
				perror("write()");
				exit(1);
			}
			sleep(1);
		}
		exit(0);

	} else { // parent
		close(fd[1]); // 关闭写端
		// int i;
		char buf[100] = {'\0'};
		ssize_t n;

		for (;;) {
			memset(buf, 0, sizeof(buf)); // 每次读之前清空一下缓冲
			if ((n = read(fd[0], buf, sizeof(buf))) < 0) {
				perror("read()");
				exit(1);
			}
			if (n == 0) {
				printf("read end\n");
				exit(0);
			}
			printf("%s\n", buf);
		}

		pid = wait(NULL);
		printf("wait pid: %d\n", pid);
	}

	exit(0);
}
