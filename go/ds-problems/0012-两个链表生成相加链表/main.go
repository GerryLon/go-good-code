/**
https://www.nowcoder.com/practice/c56f6c70fb3f4849bc56e33ff2a50b6b?tpId=190&tags=&title=&diffculty=0&judgeStatus=0&rp=1

假设链表中每一个节点的值都在 0 - 9 之间，那么链表整体就可以代表一个整数。
给定两个这种链表，请生成代表两个整数相加值的结果链表。
例如：链表 1 为 9->3->7，链表 2 为 6->3，最后生成新的结果链表为 1->0->0->0。
*/
package main

import "fmt"

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
 * @param head1 ListNode类
 * @param head2 ListNode类
 * @return ListNode类
 */
func addInList(head1 *ListNode, head2 *ListNode) *ListNode {
	if head1 == nil && head2 == nil {
		return nil
	}

	p1 := reverseList(head1)
	p2 := reverseList(head2)

	resultSentinel := &ListNode{} // 结果链表哨兵
	carry := 0                    // 进位
	var val1, val2 int
	for p1 != nil || p2 != nil || carry > 0 {
		if p1 != nil {
			val1 = p1.Val
			p1 = p1.Next
		} else {
			val1 = 0
		}
		if p2 != nil {
			val2 = p2.Val
			p2 = p2.Next
		} else {
			val2 = 0
		}

		// 计算当前节点要存的数字， 及进位值
		r := val1 + val2 + carry
		if r >= 10 {
			carry = r / 10
			r = r % 10
		} else {
			carry = 0
			//r = r
		}

		// 结果节点， 头插法
		rNode := &ListNode{Val: r}
		rNode.Next = resultSentinel.Next
		resultSentinel.Next = rNode
	}
	return resultSentinel.Next
}

func reverseList(head *ListNode) *ListNode {
	if head == nil || head.Next == nil {
		return head
	}
	sentinel := &ListNode{} // 反转后的链表的哨兵节点
	cur := head
	for cur != nil {
		tmp := cur
		cur = cur.Next

		// 头插法
		tmp.Next = sentinel.Next
		sentinel.Next = tmp
	}

	return sentinel.Next
}

func printList(head *ListNode, name string) {
	fmt.Printf("list: %s: ", name)
	for cur := head; cur != nil; cur = cur.Next {
		if cur.Next == nil { // 最后一个节点
			fmt.Printf("%v -> nil", cur.Val)
		} else {
			fmt.Printf("%v ->", cur.Val)
		}
	}
	fmt.Printf("\n")
}

func main() {
	// 9 -> 3 -> 7 -> nil
	l1 := &ListNode{
		Val: 9,
		Next: &ListNode{
			Val: 3, Next: &ListNode{
				7, nil,
			},
		},
	}
	// 6, 3
	l2 := &ListNode{
		Val: 6,
		Next: &ListNode{
			Val:  3,
			Next: nil,
		},
	}
	printList(l1, "l1")
	printList(l2, "l2")

	l3 := addInList(l1, l2)
	printList(l3, "l3")
}
