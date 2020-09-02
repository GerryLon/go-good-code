/**
https://www.nowcoder.com/practice/65cfde9e5b9b4cf2b6bafa5f3ef33fa6?tpId=188&tags=&title=&diffculty=0&judgeStatus=0&rp=1

合并\ k k 个已排序的链表并将其作为一个已排序的链表返回。分析并描述其复杂度。
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
 * @param lists ListNode类一维数组
 * @return ListNode类
 */
func mergeKLists(lists []*ListNode) *ListNode {
	if len(lists) == 0 {
		return nil
	}
	if len(lists) == 1 {
		return lists[0]
	}

	for i := 1; i < len(lists); i++ {
		lists[i] = mergeTwoList(lists[i-1], lists[i])
	}
	return lists[len(lists)-1]
}

func mergeTwoList(l1 *ListNode, l2 *ListNode) *ListNode {
	sentinel := &ListNode{}
	cur := sentinel

	for l1 != nil && l2 != nil {
		if l1.Val < l2.Val {
			cur.Next = l1
			l1 = l1.Next
			cur = cur.Next
		} else {
			cur.Next = l2
			l2 = l2.Next
			cur = cur.Next
		}
	}
	if l1 != nil {
		cur.Next = l1
	}
	if l2 != nil {
		cur.Next = l2
	}

	return sentinel.Next
}
