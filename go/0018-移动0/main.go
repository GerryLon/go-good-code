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
	// 当数组从后往前数， 一直是0时， 索引最小的0的索引
	minIndex := len(nums)

	// 从左到右扫描， 遇到一个0, 记此位置为i
	// 将 i+1到 minIndex之间的数字前移([i+1, minIndex-1])， 然后将此0放到minIndex-1的位置
	// 更新minIndex = minIndex - 1
	for i := 0; i < len(nums); i++ {
		if nums[i] == 0 {
			// 所有的0都移动完了，就退出
			if i >= minIndex {
				break
			}
			for j := i; j < minIndex-1; j++ {
				nums[j] = nums[j+1]
			}
			nums[minIndex-1] = 0
			minIndex--
		}
	}
}

func main() {
	arr := []int{0, 1, 0, 3, 12}
	moveZeroes(arr)
	fmt.Println(arr)
}
