package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"example.com/hunaidsav/FileTypeAnalyzer/ds"
)

func getAllFileNames(folderPath string) []string {
	filesinfo, err := ioutil.ReadDir(folderPath)
	if err != nil {
		log.Fatal(err)
	}

	filePaths := make([]string, 0)

	for _, fileInfo := range filesinfo {
		absPath := filepath.Join(folderPath, fileInfo.Name())
		filePaths = append(filePaths, absPath)
	}
	return filePaths
}

func readFile(filePath string) []byte {

	file, err := os.Open(filePath)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	data := make([]byte, 1024)
	_, e := file.Read(data)
	if e != nil {
		panic(e)
	}
	return data
}

func getPatterns(filePath string) ds.ByPriority {

	patternStrings := make([]string, 0)
	patternPriority := make([]ds.PatternPriority, 0)
	file, err := os.Open(filePath)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		patternStrings = append(patternStrings, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}

	for _, pattern := range patternStrings {
		patternPieces := strings.Split(pattern, ";")
		i, e := strconv.Atoi(patternPieces[0])
		if e != nil {
			fmt.Println(err)
			os.Exit(2)
		}
		patternPriority = append(patternPriority,
			ds.PatternPriority{Priority: i,
				Pattern:      patternPieces[1][1:(len(patternPieces[1]) - 1)],
				DocumentType: patternPieces[2][1:(len(patternPieces[2]) - 1)]})
	}

	patterns := ds.ByPriority(patternPriority)
	patterns.Sort()
	return patterns
}
