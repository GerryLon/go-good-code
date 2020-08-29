/**
https://www.nowcoder.com/practice/f95dcdafbde44b22a6d741baf71653f6?tpId=190&&tqId=35195&rp=1&ru=/ta/job-code-high-rd&qru=/ta/job-code-high-rd/question-ranking
题目描述
给定一个链表，删除链表的倒数第n个节点并返回链表的头指针
例如，
 给出的链表为:1->2->3->4->5, n= 2.
 删除了链表的倒数第n个节点之后,链表变为1->2->3->5.
备注：
题目保证n一定是有效的
请给出请给出时间复杂度为\ O(n) O(n)的算法

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
 * @param n int整型
 * @return ListNode类
 */
func removeNthFromEnd(head *ListNode, n int) *ListNode {
	if head == nil {
		return head
	}
	sentinel := &ListNode{Next: head} // 用哨兵节点， 删除操作可以统一起来
	head = sentinel
	fast := head
	slow := head
	// 先让fast走到第n个节点
	for i := 0; i < n && fast != nil; i++ {
		fast = fast.Next
	}
	if fast == nil { // 说明n太大
		return head.Next
	}

	// 当fast为最后一个时， slow就是我们要删除的节点的前一个节点
	// 因为：
	// fast和slow相差n个节点（当fast在第n位时， slow还在哨兵的位置（相当于0）)
	// 或者可以这样想： fast比slow多走了n步
	// 那么当fast在length位置时， slow就在length - n的位置
	// 我们要删除的节点正着数 位于： length - n + 1的位置
	for fast.Next != nil {
		fast = fast.Next
		slow = slow.Next
	}

	slow.Next = slow.Next.Next

	return sentinel.Next
}
func main() {

}
