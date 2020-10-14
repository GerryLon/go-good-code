package semaphore

import (
	"time"
)

type Semaphore struct {
	max     int           // 最大数量
	channel chan struct{} // 通道
}

// 创建信号量
func NewSemaphore(max int) *Semaphore {
	return &Semaphore{channel: make(chan struct{}, max), max: max}
}

func (s *Semaphore) Acquire() {
	if s.max > 0 { // max <= 0直接跳过
		s.channel <- struct{}{}
	}
}

func (s *Semaphore) Release() {
	if s.max > 0 {
		<-s.channel
	}
}

// 尝试获取许可
func (s *Semaphore) TryAcquire() bool {
	if s.max > 0 {
		select {
		case s.channel <- struct{}{}:
			return true
		default:
			return false
		}
	}
	return true
}

// 尝试指定时间内获取
func (s *Semaphore) TryAcquireOnTime(timeout time.Duration) bool {
	if s.max > 0 {
		for {
			select {
			case s.channel <- struct{}{}:
				return true
			case <-time.After(timeout):
				return false
			}
		}
	}
	return true
}

// 当前可用的许可数
func (s *Semaphore) Available() int {
	return s.max - len(s.channel)
}
