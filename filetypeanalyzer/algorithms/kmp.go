package algorithms

func ContainsKMP(text, pattern string) bool {
	occurrences := make([]int, 0)
	j := 0
	textRunes := []rune(text)
	patternRunes := []rune(pattern)
	searchHelper := prefixFunction(patternRunes)
	for i := 0; i < len(textRunes); i++ {

		for j > 0 && textRunes[i] != patternRunes[j] {
			j = searchHelper[j-1]
		}
		if textRunes[i] == patternRunes[j] {
			j += 1
		}
		if j == len(patternRunes) {
			occurrences = append(occurrences, i-j+1)
			j = searchHelper[j-1]
		}
	}
	return len(occurrences) != 0
}

func prefixFunction(pattern []rune) []int {
	searchHelper := make([]int, len(pattern))
	i := 1
	j := 0

	for i < len(pattern) {
		if pattern[i] == pattern[j] {
			searchHelper[i] = searchHelper[i-1] + 1
			i++
			j++
		} else {
			if j != 0 {
				j = searchHelper[j-1]
			} else {
				searchHelper[i] = 0
				i++
			}
		}
	}
	return searchHelper
}
