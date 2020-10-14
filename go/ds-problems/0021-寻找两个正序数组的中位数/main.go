/**
https://leetcode-cn.com/problems/median-of-two-sorted-arrays/


给定两个大小为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。

请你找出这两个正序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。

你可以假设 nums1 和 nums2 不会同时为空。



示例 1:

nums1 = [1, 3]
nums2 = [2]

则中位数是 2.0
示例 2:

nums1 = [1, 2]
nums2 = [3, 4]

则中位数是 (2 + 3)/2 = 2.5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/median-of-two-sorted-arrays
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
*/
package main

import "fmt"

func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	n := len(nums1) + len(nums2)
	merged := make([]int, n)
	i, j, k := 0, 0, 0

	for i < len(nums1) && j < len(nums2) {
		if nums1[i] < nums2[j] {
			merged[k] = nums1[i]
			i++
			k++
		} else {
			merged[k] = nums2[j]
			j++
			k++
		}
	}

	for ; i < len(nums1); i++ {
		merged[k] = nums1[i]
		k++
	}
	for ; j < len(nums2); j++ {
		merged[k] = nums2[j]
		k++
	}

	if n&1 == 1 {
		return float64(merged[n/2])
	} else {
		return float64(merged[n/2-1]+merged[n/2]) / 2
	}
}

func main() {
	r := findMedianSortedArrays([]int{1, 2}, []int{3, 4})
	fmt.Println(r)
}
