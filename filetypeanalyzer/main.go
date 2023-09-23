package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path"
	"sync"

	"example.com/FileTypeAnalyzer/algorithms"
	"example.com/FileTypeAnalyzer/ds"
)

func doWork(path string, patterns ds.ByPriority) {
	text := string(readFile(path))
	matched := false
	for _, p := range patterns {
		if algorithms.ContainsKMP(text, p.Pattern) {
			matched = true
			fmt.Println(path, ":", p.DocumentType)
			break
		}
	}
	if !matched {
		fmt.Println(path, ": Unknown File Type")
	}
}

func Analyzer(filesDir, patternsDir string) {

	patterns := getPatterns(patternsDir)

	filePaths := getAllFileNames(filesDir)
	n := len(filePaths)

	var wg sync.WaitGroup
	wg.Add(n)
	for _, path := range filePaths {

		go func(p string) {
			doWork(p, patterns)
			wg.Done()
		}(path)
	}

	wg.Wait()
}

func main() {
	currDir, err := os.Getwd()
	if err != nil {
		log.Fatal("unable to get current directory", err)
	}
	patternsFile := path.Join(currDir, "patterns.db")
	documentsDir := path.Join(currDir, "docs")
	flag.StringVar(&documentsDir, "docdir", documentsDir, "folder containing the files to be analyzed")
	flag.StringVar(&patternsFile, "patternsdb", patternsFile, "file that lists the patterns to be matched against")

	Analyzer(documentsDir, patternsFile)
}
