package algorithms


func ContainsBruteForce(text, pattern string) bool {

	contains := false
	
	i := 0
	j := 0
	textRunes := []rune(text)
	patternRunes := []rune(pattern)
	for i < len(textRunes) {
		
		if textRunes[i] == patternRunes[j] {
			i++ 
			j++
		} else {
			i = i - j + 1 
			j = 0
		}

		if j == len(patternRunes) {
			contains = true
			break
		}
	}
	return contains

}
