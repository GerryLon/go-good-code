/**
https://www.nowcoder.com/practice/54275ddae22f475981afa2244dd448c6?tpId=190&tags=&title=&diffculty=0&judgeStatus=0&rp=1

用两个栈来实现一个队列，完成队列的Push和Pop操作。 队列中的元素为int类型。
*/
package main

var stack1 []int // in
var stack2 []int // out

func Push(node int) {
	stack1 = append(stack1, node)
}

func Pop() int {
	var ret = -1
	var tmp int

	// 如果out有值， 就弹出
	if len(stack2) > 0 {
		ret = stack2[len(stack2)-1]
		stack2 = stack2[:len(stack2)-1]
		return ret
	}

	for len(stack1) > 0 {
		tmp = stack1[len(stack1)-1]
		stack1 = stack1[:len(stack1)-1]
		stack2 = append(stack2, tmp)
	}

	if len(stack2) > 0 {
		ret = stack2[len(stack2)-1]
		stack2 = stack2[:len(stack2)-1]
		return ret
	}

	return ret
}
