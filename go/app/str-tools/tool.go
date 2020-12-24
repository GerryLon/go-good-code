package main

type ITool interface {
	GetName() string
	GetUsage() string

	Do() (o Output)
}

type Output struct {
	Str string // output的string形式

	// 其他字段以后需要再说
}

func (o Output) String() string {
	return o.Str
}


