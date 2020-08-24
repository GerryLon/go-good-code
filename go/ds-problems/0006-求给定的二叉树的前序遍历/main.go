/**
https://www.nowcoder.com/practice/501fb3ca49bb4474bf5fa87274e884b4?tpId=46&tags=&title=&diffculty=0&judgeStatus=0&rp=1

题目描述
求给定的二叉树的前序遍历。
例如：
给定的二叉树为{1,#,2,3},

返回：[1,2,3].
备注；用递归来解这道题很简单，你可以给出迭代的解法么？
如果你不明白{1,#,2,3}的含义，点击查看相关信息
*/
package main

/*
 * type TreeNode struct {
 *   Val int
 *   Left *TreeNode
 *   Right *TreeNode
 * }
 */

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

/**
 *
 * @param root TreeNode类
 * @return int整型一维数组
 */
// 前序： 根->左->右, 用栈： 右， 左， 根
// 实际上是先从根开始， 然后再右子树入栈， 再左子树入栈
func preorderTraversal(root *TreeNode) []int {
	// write code here
	var ret []int
	var stack []*TreeNode

	if root == nil {
		return ret
	}

	stack = append(stack, root)
	for len(stack) > 0 {
		top := stack[len(stack)-1]
		stack = stack[:len(stack)-1] // 出栈
		ret = append(ret, top.Val)

		if top.Right != nil {
			stack = append(stack, top.Right)
			top.Right = nil
		}
		if top.Left != nil {
			stack = append(stack, top.Left)
			top.Left = nil
		}
	}
	return ret
}

func main() {

}
