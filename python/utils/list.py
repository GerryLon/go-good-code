# coding: utf-8
"""
一些工具方法集合
"""


def readfile_to_array(filename, ignore_empty_line=True):
    """
    readfile_to_array
    按行读文件, 转成数组
    """
    array = []
    with open(filename) as my_file:
        for line in my_file:
            line = line.strip()
            if ignore_empty_line and not line:
                continue
            array.append(line)
        return array


if __name__ == "__main__":
    print(readfile_to_array("list.py"))
