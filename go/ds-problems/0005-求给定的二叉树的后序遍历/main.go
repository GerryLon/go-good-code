/**
https://www.nowcoder.com/practice/32af374b322342b68460e6fd2641dd1b?tpId=46&tags=&title=&diffculty=0&judgeStatus=0&rp=1
求给定的二叉树的后序遍历。
例如：
给定的二叉树为{1,#,2,3},
   1
     \
     2
    /
   3

返回[3,2,1].
备注；用递归来解这道题太没有新意了，可以给出迭代的解法么？
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
// 思路: 后序应该是： 左->右->根, 用栈， 依次push 根， 右， 左 然后再一直pop就可以了
func postorderTraversal(root *TreeNode) []int {
	// write code here
	var stack []*TreeNode
	var ret []int
	if root != nil {
		// 入栈
		stack = append(stack, root)
	} else {
		return ret
	}

	for len(stack) > 0 {
		top := stack[len(stack)-1] // 栈顶元素
		// 叶子节点， 可以访问了， 放到结果中
		if top.Left == nil && top.Right == nil {
			ret = append(ret, top.Val)
			stack = stack[:len(stack)-1] // 出栈
			continue
		}

		// 先右子树入栈（因为后序是左右根， 用栈的话应该是根， 右， 左
		if top.Right != nil {
			stack = append(stack, top.Right)
			top.Right = nil // 标记已经访问过了
		}
		if top.Left != nil {
			stack = append(stack, top.Left)
			top.Left = nil // 标记已经访问过了
		}
	}
	return ret
}

func main() {

}
