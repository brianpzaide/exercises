package ds

import("sort")

type PatternPriority struct {
	Priority 	      int
	Pattern, DocumentType string
}

type ByPriority []PatternPriority

func (p ByPriority) Len() int {
	return len(p)
}

func (p ByPriority) Less(i, j int) bool {
	return -p[i].Priority < -p[j].Priority	
}

func (p ByPriority) Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}

func (p ByPriority) Sort() {
	sort.Sort(p)
}

