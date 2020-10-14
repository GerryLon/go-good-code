/**
并发求和

https://blog.csdn.net/butterfly5211314/article/details/83341311#comments_13397266
*/

package main

import (
	"fmt"
	"math/rand"
	"sync"
	"sync/atomic"
	"time"
)

func calcTime(f func([]int) int, arr []int, tag string) {
	t1 := time.Now().UnixNano()

	s := f(arr)
	t2 := time.Now().UnixNano() - t1
	fmt.Printf("%15s: time: %d, sum: %d\n", tag, t2, s)
}

func main() {
	const MAX = 1e8 // 1亿
	arr := make([]int, MAX)

	for i := 0; i < MAX; i++ {
		arr[i] = rand.Intn(10)
	}

	/*
					某次跑的结果
		            for: time: 99961094, sum: 450032946
		         worker: time: 80271644, sum: 450032946
		      WaitGroup: time: 338243407, sum: 450032946
		WaitGroup_atomic: time: 1884448700, sum: 450032946
	*/
	calcTime(sum1, arr, "for")
	calcTime(sum2, arr, "worker")
	calcTime(sum3, arr, "WaitGroup")
	calcTime(sum3_atomic, arr, "WaitGroup_atomic")
}

func sum1(data []int) int {
	s := 0
	l := len(data)

	for i := 0; i < l; i++ {
		s += data[i]
	}
	return s
}

func sum2(data []int) int {
	s := 0
	l := len(data)
	const N = 5
	seg := l / N
	var chs [N]<-chan int

	for i := 0; i < N; i++ {
		chs[i] = worker(data[i*seg : (i+1)*seg])
	}

	for i := 0; i < N; i++ {
		s += <-chs[i]
	}

	return s
}

func worker(s []int) <-chan int {
	out := make(chan int)

	go func() {
		length := len(s)
		sum := 0
		for i := 0; i < length; i++ {
			sum += s[i]
		}
		out <- sum
	}()
	return out
}

func sum3(data []int) int {
	s := 0
	l := len(data)
	const N = 5
	seg := l / N

	var mu sync.Mutex
	var wg sync.WaitGroup
	wg.Add(N) // 直接加N个

	for i := 0; i < N; i++ {
		go func(ii int) {
			tmpS := data[ii*seg : (ii+1)*seg]
			ll := len(tmpS)
			mu.Lock()
			for i := 0; i < ll; i++ {
				s += tmpS[i]
			}
			mu.Unlock()
			wg.Done() // 一个goroutine运行完
		}(i)
	}
	wg.Wait() // 等N个goroutine都运行完

	return s
}

func sum3_atomic(data []int) int {
	l := len(data)
	const N = 5
	seg := l / N

	var wg sync.WaitGroup
	wg.Add(N) // 直接加N个

	var s_uint64 uint64

	for i := 0; i < N; i++ {
		go func(ii int) {
			tmpS := data[ii*seg : (ii+1)*seg]
			ll := len(tmpS)
			for i := 0; i < ll; i++ {
				// s += tmpS[i]
				atomic.AddUint64(&s_uint64, uint64(tmpS[i]))
			}
			wg.Done() // 一个goroutine运行完
		}(i)
	}
	wg.Wait() // 等N个goroutine都运行完

	return int(s_uint64)
}
