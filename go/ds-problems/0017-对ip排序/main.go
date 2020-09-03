package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"sort"
	"strconv"
	"strings"
)

type IPs []string

func (ips IPs) Len() int {
	return len(ips)
}
func (ips IPs) Swap(i, j int) {
	ips[i], ips[j] = ips[j], ips[i]
}
func (ips IPs) Less(i, j int) bool {
	return ip2int(ips[i]) < ip2int(ips[j])
}

func ip2int(ip string) int {
	seg := strings.Split(ip, ".")
	var ret int
	n1, _ := strconv.Atoi(seg[0])
	n2, _ := strconv.Atoi(seg[1])
	n3, _ := strconv.Atoi(seg[2])
	n4, _ := strconv.Atoi(seg[3])

	ret += n1 << 24
	ret += n2 << 16
	ret += n3 << 8
	ret += n4

	return ret
}

func readIP(filename string) (ips IPs, err error) {
	f, err := os.Open(filename)
	if err != nil {
		return
	}
	r := bufio.NewReader(f)
	var line []byte
	ips = make(IPs, 0)
	for {
		line, _, err = r.ReadLine()
		if err != nil {
			if err == io.EOF {
				err = nil
				break
			} else {
				return
			}
		}
		ips = append(ips, string(line))
	}
	return
}

func main() {
	ips, err := readIP("ip.txt")
	if err != nil {
		panic(err)
	}
	sort.Sort(ips)
	fmt.Println(ips)
}
