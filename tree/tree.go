package main

import (
	"fmt"
	"os"
	"path/filepath"
)

const (
	ELBOW        = "└── "
	TEE          = "├── "
	PIPE_PREFIX  = "│   "
	SPACE_PREFIX = "    "
)

type TreeItem struct {
	root   string
	indent string
	prefix string
}

type MyStack struct {
	arr []TreeItem
}

func NewStack() *MyStack {
	return &MyStack{
		arr: make([]TreeItem, 0),
	}
}

func (ms *MyStack) put(item TreeItem) {
	ms.arr = append(ms.arr, item)
}

func (ms *MyStack) pop() (TreeItem, error) {
	n := len(ms.arr)
	if n == 0 {
		return TreeItem{}, fmt.Errorf("stack is empty")
	}
	item := ms.arr[n-1]
	ms.arr = ms.arr[:n-1]
	return item, nil
}

func tree(root string) error {
	ms := NewStack()
	ms.put(TreeItem{
		root:   root,
		indent: "",
		prefix: "",
	})

	for len(ms.arr) > 0 {
		ti, err := ms.pop()
		if err != nil {
			return err
		}
		fi, err := os.Stat(ti.root)
		if err != nil {
			return fmt.Errorf("could not stat %s: %v", ti.root, err)
		}
		fmt.Printf("%s%s\n", ti.prefix, ti.root)
		if !fi.IsDir() {
			continue
		} else {
			fis, err := os.ReadDir(ti.root)
			if err != nil {
				return fmt.Errorf("could not read dir %s: %v", ti.root, err)
			}
			var names []string
			for _, fi := range fis {
				if fi.Name()[0] != '.' {
					names = append(names, fi.Name())
				}
			}

			childrenTis := make([]TreeItem, 0)
			for i, name := range names {
				add_, prefix_ := PIPE_PREFIX, ""
				if i == len(names)-1 {
					prefix_ = ti.indent + ELBOW
					add_ = SPACE_PREFIX
				} else {
					prefix_ = ti.indent + TEE
				}
				childrenTis = append(childrenTis, TreeItem{
					root:   filepath.Join(ti.root, name),
					indent: ti.indent + add_,
					prefix: prefix_,
				})
			}

			for i := len(childrenTis) - 1; i >= 0; i-- {
				ms.put(childrenTis[i])
			}
		}
	}
	return nil
}

func main() {
	root := "."
	if len(os.Args) > 1 {
		root = os.Args[1]
	}

	tree(root)

}
