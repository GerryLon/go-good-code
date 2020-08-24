/**
https://www.nowcoder.com/practice/152bc6c5b14149e49bf5d8c46f53152b?tpId=46&tags=&title=&diffculty=0&judgeStatus=0&rp=1

使用插入排序对链表进行排序。
Sort a linked list using insertion sort.
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

func insertionSortList(head *ListNode) *ListNode {
	sentinel := &ListNode{} // 临时链表的哨兵节点

	pre, cur := sentinel, head
	for cur != nil {
		pre = sentinel // 每次都从临时链表头开始找
		for pre.Next != nil && pre.Next.Val <= cur.Val {
			pre = pre.Next
		}

		// cur后移
		tmp := cur
		cur = cur.Next

		// 将tmp节点插入到pre节点后边
		tmp.Next = pre.Next
		pre.Next = tmp
	}

	return sentinel.Next
}

func main() {

}
