package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"os"
)

func mainChatClient() {
	c, err := net.Dial("tcp", "localhost:8000")
	if err != nil {
		log.Fatal(err)
	}
	defer c.Close()
	go func() {
		_, err = io.Copy(c, os.Stdin)
		if err != nil {
			log.Println(err.Error())
			return
		}
	}()
	_, err = io.Copy(os.Stdout, c)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
}
