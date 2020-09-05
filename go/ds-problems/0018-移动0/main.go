/*
https://leetcode-cn.com/leetbook/read/all-about-array/x9rh8e/

移动零
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

示例:

输入: [0,1,0,3,12]
输出: [1,3,12,0,0]
说明:

必须在原数组上操作，不能拷贝额外的数组。
尽量减少操作次数。

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/all-about-array/x9rh8e/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
*/
package main

import (
	"fmt"
)

func moveZeroes(nums []int) {
	startIndex := 0
	n := len(nums)
	var i int
	for ; i < n; i++ {
		if nums[i] != 0 {
			nums[startIndex] = nums[i]
			startIndex++
		}
	}

	for i = startIndex; i < n; i++ {
		nums[i] = 0
	}
}

func main() {
	arr := []int{0, 1, 0, 3, 12}
	moveZeroes(arr)
	fmt.Println(arr)

	arr = []int{0, 0, 1}
	moveZeroes(arr)
	fmt.Println(arr)
}
