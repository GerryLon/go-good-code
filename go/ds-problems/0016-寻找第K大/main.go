/**
https://www.nowcoder.com/practice/e016ad9b7f0b45048c58a9f27ba618bf?tpId=188&tags=&title=&diffculty=0&judgeStatus=0&rp=1

有一个整数数组，请你根据快速排序的思路，找出数组中第K大的数。

给定一个整数数组a,同时给定它的大小n和要找的K(K在1到n之间)，请返回第K大的数，保证答案存在。

测试样例：
[1,3,5,2,2],5,3
返回：2
*/
package main

/**
 *
 * @param a int整型一维数组
 * @param n int整型
 * @param K int整型
 * @return int整型
 */
func findKth(a []int, n int, K int) int {
	return solution1(a, n, K)
}

func solution1(a []int, n int, K int) int {
	var left, right []int
	pivot := a[0]

	for i := 1; i < n; i++ {
		if a[i] < pivot {
			left = append(left, a[i])
		} else {
			right = append(right, a[i])
		}
	}

	if len(right) == K-1 {
		return pivot
	} else if len(right) > K-1 {
		return solution1(right, len(right), K)
	} else {
		return solution1(left, len(left), K-len(right)-1)
	}
}

func main() {

}
