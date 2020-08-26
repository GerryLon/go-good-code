/**
https://www.nowcoder.com/practice/650474f313294468a4ded3ce0f7898b9?tpId=188&tags=&title=&diffculty=0&judgeStatus=0&rp=1
题目描述
判断给定的链表中是否有环
扩展：
你能给出空间复杂度O(1)的解法么？
*/
package main

/*
 * type ListNode struct{
 *   Val int
 *   Next *ListNode
 * }
 */

type ListNode struct {
	Val  int
	Next *ListNode
}

/**
 *
 * @param head ListNode类
 * @return bool布尔型
 */
func hasCycle(head *ListNode) bool {
	// write code here
	// 快慢指针能够相遇就说明有环
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
		if slow == fast {
			return true
		}
	}
	return false
}

func hasCycle2(head *ListNode) bool {
	if head == nil || head.Next == nil {
		return false
	}
	// 如果map中有重复key， 则说明访问过
	m := make(map[*ListNode]*struct{}, 0)
	cur := head
	for cur != nil {
		if m[cur] == nil {
			m[cur] = &struct{}{}
		} else {
			return true
		}
		cur = cur.Next
	}
	return false
}
