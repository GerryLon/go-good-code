/**
https://www.nowcoder.com/practice/09fbfb16140b40499951f55113f2166c?tpId=190&tags=&title=&diffculty=0&judgeStatus=0&rp=1

题目描述
实现函数 int sqrt(int x).
计算并返回x的平方根
示例1
输入
2

输出
1
*/
package main

import "fmt"

/**
 *
 * @param x int整型
 * @return int整型
 */
func sqrt(x int) int {
	// write code here

	return solution1(x)
}

// 利用二分法
func solution1(x int) int {
	if x < 1 {
		return 0
	}
	lo, hi := 1, x/2+1
	var mid int
	var tmp int
	for lo <= hi {
		mid = lo + (hi-lo)/2
		tmp = x / mid
		if tmp == mid {
			return mid
		} else if tmp < mid { // mid太大了， 导致tmp太小
			hi = mid - 1
		} else {
			lo = mid + 1
		}
	}
	return hi // 较小的那个值
}

// 1^2 = 1
// 2^2 = 1 + 3
// 3^1 = 1 + 3 + 5
// ...
// n^2 = 1 + 3 + ... + 2n-1
// 记奇数的和
func solution2(x int) int {
	if x < 1 {
		return 0
	}
	sum := 0

	t := x/2 + 1 // x的平方根最大值
	var i int
	for i = 1; i <= t; i++ {
		sum += 2*i - 1
		if sum >= x {
			break
		}
	}
	if sum == x {
		return i
	}
	// 如果找不到直接相等的， 就找最接近的（floor)
	for sum > x {
		sum = sum - (2*i - 1)
		i--
	}
	return i
}

func solution3(x int) int {
	if x < 1 {
		return 0
	}
	i := 1
	for i*i <= x {
		i++
	}
	if i*i == x {
		return i
	}
	return i - 1
}

func main() {
	for i := 1; i < 20; i++ {
		fmt.Printf("sqrt(%d)=%d\n", i, solution3(i))
	}
}
