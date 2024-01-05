package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
)

type chatUser struct {
	id string
	c  net.Conn
}

type chatMessage struct {
	userId string
	msg    string
}

var (
	messages chan chatMessage
	joinings chan chatUser
	leavings chan chatUser
)

// reads the chat messages from the connection and sends the messages to the broadcaster
func handleConnectionChatServer(ctx context.Context, cu chatUser) {
	defer func() {
		cu.c.Close()
		leavings <- cu
	}()

	go func() {
		<-ctx.Done()
		cu.c.Close()
	}()

	joinings <- cu
	scanner := bufio.NewScanner(cu.c)
	for scanner.Scan() {
		messages <- chatMessage{
			userId: cu.id,
			msg:    fmt.Sprintf("%s", scanner.Text()),
		}
	}

}

// receives chat messages, joining or leaving messages from the channels messages, joinings, leavings and broadcast the events to all the current users
func broadCaster(ctx context.Context) {
	userConnections := make(map[string]net.Conn)
	broadcast := func(userId, msg string) {
		for _, val := range userConnections {
			_, err := io.WriteString(val, fmt.Sprintf("%s: %s\n", userId, msg))
			if err != nil {
				log.Printf("unable to send message to the connection %v", val)
				log.Println(err)
			}
		}
	}

	for {
		select {
		case chMsg := <-messages:
			broadcast(chMsg.userId, chMsg.msg)
		case cu := <-joinings:
			userConnections[cu.id] = cu.c
			broadcast(cu.id, "joined the room")
		case cu := <-leavings:
			delete(userConnections, cu.id)
			broadcast(cu.id, "left the room")
		case <-ctx.Done():
			return
		}
	}

}

func mainChatServer() {
	messages = make(chan chatMessage, 1024)
	joinings = make(chan chatUser, 1024)
	leavings = make(chan chatUser, 1024)

	currentId := 0
	listener, err := net.Listen("tcp", "localhost:8000")
	if err != nil {
		log.Fatal(err)
	}

	ctx, cancelFunc := context.WithCancel(context.Background())
	go broadCaster(ctx)

	// for graceful shutdown, closing the channels
	go func() {
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
		<-quit
		cancelFunc()
		close(messages)
		close(joinings)
		close(leavings)
		os.Exit(0)
	}()

	for {
		c, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleConnectionChatServer(ctx, chatUser{
			id: fmt.Sprintf("user-%d", currentId),
			c:  c,
		})
		currentId++
	}

}
