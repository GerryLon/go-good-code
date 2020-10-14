/**
https://www.nowcoder.com/practice/d75c232a0405427098a8d1627930bea6?tpId=46&tags=&title=&diffculty=0&judgeStatus=0&rp=1

题目描述
在O(n log n)的时间内使用常数级空间复杂度对链表进行排序。
Sort a linked list in O(n log n) time using constant space complexity.
*/
package main

/*
 * type ListNode struct{
 *   Val int
 *   Next *ListNode
 * }
 */

/**
 *
 * @param head ListNode类
 * @return ListNode类
 */
type ListNode struct {
	Val  int
	Next *ListNode
}

func sortList(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}

	middle := head // 最终会指向链表的中间
	fast := head.Next
	for fast != nil && fast.Next != nil {
		middle = middle.Next
		fast = fast.Next.Next
	}

	right := sortList(middle.Next) // 右半边排序
	middle.Next = nil              // 划分左半边
	left := sortList(head)         // 左半边排序

	// 合并两个有序链表
	return mergeTwoList(left, right)
}

func mergeTwoList(l1 *ListNode, l2 *ListNode) *ListNode {
	dummyHead := &ListNode{}
	cur := dummyHead

	for l1 != nil && l2 != nil {
		if l1.Val < l2.Val {
			cur.Next = l1
			cur = cur.Next
			l1 = l1.Next
		} else {
			cur.Next = l2
			cur = cur.Next
			l2 = l2.Next
		}
	}

	if l1 != nil {
		cur.Next = l1
	}
	if l2 != nil {
		cur.Next = l2
	}

	return dummyHead.Next
}

func main() {

}
