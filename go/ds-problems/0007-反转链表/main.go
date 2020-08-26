/**
https://www.nowcoder.com/practice/75e878df47f24fdc9dc3e400ec6058ca?tpId=188&&tqId=35160&rp=1&ru=/activity/oj&qru=/ta/job-code-high-week/question-ranking
题目描述
输入一个链表，反转链表后，输出新链表的表头。
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
 * @param pHead ListNode类
 * @return ListNode类
 */
func ReverseList(pHead *ListNode) *ListNode {
	// write code here
	// 链表为空， 或者只有一个节点
	if pHead == nil || pHead.Next == nil {
		return pHead
	}

	// 新链表哨兵
	sentinel := &ListNode{}
	cur := pHead
	for cur != nil {
		// 原链表 删除头节点
		tmp := cur
		cur = cur.Next

		// 新链表 头插入法
		tmp.Next = sentinel.Next
		sentinel.Next = tmp
	}

	return sentinel.Next
}
