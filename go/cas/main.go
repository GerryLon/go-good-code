package main

import (
	"fmt"
	"runtime"
	"sync"
	"sync/atomic"
)

func problem(goMaxProcs int, useAtomic bool) uint64 {
	runtime.GOMAXPROCS(goMaxProcs)

	var count uint64 = 0
	wg := &sync.WaitGroup{}

	if !useAtomic {
		for i := 0; i < 10000; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				count++
			}()
		}
	} else {
		for i := 0; i < 10000; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				atomic.AddUint64(&count, 1)
			}()
		}
	}

	wg.Wait()

	return count
}

func main() {
	fmt.Println("NumCPU:", runtime.NumCPU())
	c1 := problem(1, false)
	c2 := problem(1, true)
	c3 := problem(runtime.NumCPU(), false)
	c4 := problem(runtime.NumCPU(), true)

	// 10000 10000 8924 10000
	fmt.Println(c1, c2, c3, c4)

	// 如果是单个CPU, 也就是同时最多只有一个goroutine在跑, 无论用不用atomic.AddUint64, 自增都正确

	// 如果是多个CPU, 不用atomic.AddUint64是不行的
	// 因为count++不是原子操作, 分三步: (read, add, write)
	// 所以会有并发问题
}
