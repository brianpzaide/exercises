package algorithms

const (
	a uint64 = 53
	m uint64 = 1000000009
)

func ContainsRabinKarp(text, pattern string) bool {

	textRunes := []byte(text)
	patternRunes := []byte(pattern)

	textLength := len(text)
	patternLength := len(pattern)
	var patternHash uint64 = 0
	var currSubstrHash uint64 = 0
	var pow uint64 = 1

	for i := 0; i < len(patternRunes); i++ {
		patternHash += getValue(patternRunes[i]) * pow
		patternHash %= m

		currSubstrHash += getValue(textRunes[textLength-patternLength+i]) * pow
		currSubstrHash %= m

		if i != patternLength-1 {
			pow = pow * a % m
		}
	}

	occurrences := make([]int, 0)

	for i := textLength; i >= patternLength; i-- {
		if patternHash == currSubstrHash {
			patternIsFound := true

			for j := 0; j < patternLength; j++ {
				if textRunes[i-patternLength+j] != patternRunes[j] {
					patternIsFound = false
					break
				}
			}
			if patternIsFound {
				occurrences = append(occurrences, i-patternLength)
			}
		}
		if i > patternLength {
			currSubstrHash = (currSubstrHash - getValue(textRunes[i-1])*pow%m + m) * a % m
			currSubstrHash = (currSubstrHash + getValue(textRunes[i-patternLength-1])) % m
		}
	}
	return len(occurrences) != 0
}

func getValue(a byte) uint64 {
	return uint64(a - 'A' + 1)
}
