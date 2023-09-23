package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

/*
func makeTempDir(fileContents, fileTypes, fileNames []string) error {

	i := 0
	dir, err := ioutil.TempDir("/home/brian/golearningstudio/testingFTA", "testingData")
	if err != nil {
		return err
	}
	fmt.Println(dir)
	defer os.RemoveAll(dir) // clean up

	for i < len(fileTypes); i++ {

		if e := makeTempFile(dir, fileContents[i], fileTypes[i], n[i]); e != nil {
			panic(e)
		}
		i++
	}
}
*/

const tempDir = ""

func makeTempFile(dirName string, fileContent, fileName string) error {
	content := []byte(fileContent)
	tmpfn := filepath.Join(dirName, fileName)
	err := ioutil.WriteFile(tmpfn, content, 0666)
	return err
}

func TestFileTypeAnalyzer(t *testing.T) {
	tt := []struct {
		expected   []string
		errMessage string
		out        func() (string, error)
	}{
		{
			expected:   []string{"doc.pdf : PDF document", "text.pdf : Unknown File Type"},
			errMessage: "Wrong answer for the files with PDF documents",
			out: func() (string, error) {

				fileContents := []string{"PFDF%PDF-PDF", "PFPDF-PDFABC"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				fmt.Print(dir)
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "doc.pdf"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "text.pdf"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"doc.zip : Unknown File Type", "doc1.zip : Zip archive"},
			errMessage: "Wrong answer for the files with Zip archives",
			out: func() (string, error) {
				fileContents := []string{"PCK", "PKC"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "doc.zip"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "doc1.zip"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"main : PCP pmview config", "main.config : Unknown File Type"},
			errMessage: "Wrong answer for PCP pmview config files",
			out: func() (string, error) {
				fileContents := []string{"pmview", "pmconfigview"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "main"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "main.config"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"slides1.odp : OpenDocument presentation", "slides2.odp : Unknown File Type"},
			errMessage: "Wrong answer for Document presentationfiles files",
			out: func() (string, error) {
				fileContents := []string{"vnd.oasis.opendocument.presentation", "vnd.oasis.microsoft.presentation"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "slides1.odp"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "slides2.odp"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},

		{
			expected:   []string{"doc.txt : Unknown File Type", "txt.doc : MS Office Word 2003"},
			errMessage: "Wrong answer for Word 2003 files",
			out: func() (string, error) {
				fileContents := []string{"W.o.r.kwwwwwwww", "wwwwwwwwW.o.r.d"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "doc.txt"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "txt.doc"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"slides1.ptp : MS Office PowerPoint 2003", "slides2.ptp : Unknown File Type"},
			errMessage: "Wrong answer for MS Office PowerPoint 2003 files",
			out: func() (string, error) {
				fileContents := []string{"P.o.w.e.r.P.o.i", "P.o.w.e.r.\\Sh.o.i"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "slides1.ptp"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "slides2.ptp"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"doc.txt : Unknown File Type", "txt.doc : MS Office Word 2007+"},
			errMessage: "Wrong answer for MS Office Excel 2007+ files",
			out: func() (string, error) {
				fileContents := []string{"word/\\_rels", "\\word/_rels"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "doc.txt"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "txt.doc"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"sheet1.xls : MS Office Excel 2007+", "sheet2.xls : Unknown File Type"},
			errMessage: "Wrong answer for MS Office Excel 2007+ files",
			out: func() (string, error) {
				fileContents := []string{"asdaxl/_rels", "x2/_reasdadls"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "sheet1.xls"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "sheet2.xls"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"pres1.pptx : MS Office PowerPoint 2007+", "pres2.pptx : Unknown File Type"},
			errMessage: "Wrong answer for MS Office Excel 2007+ files",
			out: func() (string, error) {
				fileContents := []string{"afeefa%ppt/_relsasdad", "ppasfsfafdaet/_rels"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "pres1.pptx"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "pres2.pptx"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"1.jpg : ISO Media JPEG 2000", "2.jpg : Unknown File Type"},
			errMessage: "Wrong answer for ISO Media JPEG 2000 files",
			out: func() (string, error) {
				fileContents := []string{"ftypjp2ddddddaa", "ftypdddjp2dadad"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "1.jpg"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "2.jpg"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"cert.pem : PEM certificate", "cert_core.pem : Unknown File Type"},
			errMessage: "Wrong answer for PEM certificates",
			out: func() (string, error) {
				fileContents := []string{"\\\\\\\\\\aasdw-----BEGIN\\ CERTIFICATE-----", "\\\\\\\\\\adww-----BEGIN\\CERTIFICATE-----"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "cert.pem"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "cert_core.pem"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"tape.jpg : ISO Media MP4 Base Media v2", "tape.mp4 : Unknown File Type"},
			errMessage: "Wrong answer for ISO Media MP4 Base Media v2 files",
			out: func() (string, error) {
				fileContents := []string{"ftypiso2mp4", "mp4ffttypiso2"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "tape.jpg"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "tape.mp4"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},

		{
			expected:   []string{"tape2.jpg : MS Office Word 2003", "tape2.mp4 : ISO Media MP4 Base Media v2"},
			errMessage: "Wrong answer while testing priority 1",
			out: func() (string, error) {
				fileContents := []string{"PK W.o.r.d", "%PDF-mp4fftypiso2"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "tape2.jpg"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "tape2.mp4"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
		{
			expected:   []string{"tape3.jpg : PEM certificate", "tape3.mp4 : MS Office Word 2003"},
			errMessage: "Wrong answer while testing priority 2",
			out: func() (string, error) {
				fileContents := []string{"-----BEGIN\\ CERTIFICATE-----pmview", "%PDF-ftypppfW.o.r.dftypiso"}

				dir, err := ioutil.TempDir(tempDir, "testingData")
				if err != nil {
					return "", err
				}

				if e := makeTempFile(dir, fileContents[0], "tape3.jpg"); e != nil {
					return "", e
				}
				if e := makeTempFile(dir, fileContents[1], "tape3.mp4"); e != nil {
					return "", e
				}

				return dir, nil
			},
		},
	}

	for _, tc := range tt {
		t.Run("", func(t *testing.T) {

			dir, err := tc.out()
			if err != nil {
				t.Fatalf("%s", err)
			}
			defer os.RemoveAll(dir)

			old := os.Stdout
			r, w, _ := os.Pipe()
			os.Stdout = w

			Analyzer(dir, "patterns.db")

			outC := make(chan string)
			// copy the output in a separate goroutine so printing can't block indefinitely
			go func() {
				var buf bytes.Buffer
				io.Copy(&buf, r)
				outC <- buf.String()
			}()

			// restoring the real stdout
			w.Close()
			os.Stdout = old
			out := <-outC

			//reading our temp stdout
			fmt.Println("previous output:")
			fmt.Print(out)

			for _, em := range tc.expected {
				exp := strings.Join([]string{dir, em}, "/")
				if strings.Contains(out, exp) {
				} else {
					t.Errorf(tc.errMessage)
				}
			}
		})
	}

}
