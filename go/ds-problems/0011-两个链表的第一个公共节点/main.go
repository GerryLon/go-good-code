/**
https://www.nowcoder.com/practice/6ab1d9a29e88450685099d45c9e31e46?tpId=190&tags=&title=&diffculty=0&judgeStatus=0&rp=1
输入两个链表，找出它们的第一个公共结点。（注意因为传入数据是链表，所以错误测试数据的提示是用其他方式显示的，保证传入数据是正确的）
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
 * @param pHead1 ListNode类
 * @param pHead2 ListNode类
 * @return ListNode类
 */
func FindFirstCommonNode(pHead1 *ListNode, pHead2 *ListNode) *ListNode {
	// write code here
	return solution1(pHead1, pHead2)
}

// 最简单的想法， 用map
func solution1(pHead1 *ListNode, pHead2 *ListNode) *ListNode {
	if pHead1 == nil || pHead2 == nil {
		return nil
	}
	m := make(map[*ListNode]*struct{})
	cur := pHead1
	for cur != nil {
		m[cur] = &struct{}{}
		cur = cur.Next
	}

	cur = pHead2
	var ok bool
	for cur != nil {
		if _, ok = m[cur]; ok {
			return cur
		}
		cur = cur.Next
	}

	return nil
}

//
func solution2(pHead1 *ListNode, pHead2 *ListNode) *ListNode {
	if pHead1 == nil || pHead2 == nil {
		return nil
	}

	p1, p2 := pHead1, pHead2
	// 根据题目， 一定有p1==p2， 所以这里不会死循环
	for p1 != p2 {
		p1 = p1.Next
		p2 = p2.Next

		if p1 != p2 {
			if p1 == nil {
				p1 = pHead2
			}
			if p2 == nil {
				p2 = pHead1
			}
		}
	}
	return p1
}
func main() {

}
