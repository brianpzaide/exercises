package main

import (
	"context"
	"time"
)

const LIMITER_CAPACITY = 1024

type RateLimiter interface {
	Allow(int) bool
	Stop()
}

type requestTokensCh struct {
	tokens int
	resCh  chan bool
}

type RateLimiterBase struct {
	allowCh  chan requestTokensCh
	stopFunc context.CancelFunc
}

func (rlb *RateLimiterBase) Allow(tokens int) bool {
	if tokens <= 0 {
		return false
	}

	reqTokensCh := requestTokensCh{
		tokens: tokens,
		resCh:  make(chan bool),
	}

	rlb.allowCh <- reqTokensCh
	return <-reqTokensCh.resCh
}

func (rlb *RateLimiterBase) Stop() {
	rlb.stopFunc()
	close(rlb.allowCh)
}

type TokenBucket struct {
	capacity        int
	tokensPerSecond int
	tokens          int
	lastTime        time.Time
	*RateLimiterBase
}

func NewTokenBucket(capacity, tokensPerSecond, tokens int) RateLimiter {
	allowCh := make(chan requestTokensCh, LIMITER_CAPACITY)
	ctx, cancelFunc := context.WithCancel(context.Background())
	rlBase := &RateLimiterBase{
		allowCh:  allowCh,
		stopFunc: cancelFunc,
	}
	rl := &TokenBucket{
		RateLimiterBase: rlBase,
		capacity:        capacity,
		tokensPerSecond: tokensPerSecond,
		tokens:          tokens,
		lastTime:        time.Now(),
	}

	go rl.tokenBucketAlgorithm(ctx)

	return rl
}

func (rl *TokenBucket) tokenBucketAlgorithm(ctx context.Context) {
	// runs the token bucket algorithm in a separate goroutine and also checks for event(cancelling the context) to stop this goroutine
	for {
		select {
		case <-ctx.Done():
			return
		case reqTokensCh := <-rl.allowCh:
			currentTime := time.Now()
			timePassed := rl.lastTime.Sub(currentTime).Seconds()
			temp := rl.tokens + int(timePassed)*rl.tokensPerSecond
			if rl.capacity <= temp {
				rl.tokens = rl.capacity
			} else {
				rl.tokens = temp
			}
			rl.lastTime = currentTime
			resp := false

			if reqTokensCh.tokens <= rl.tokens {
				rl.tokens -= reqTokensCh.tokens
				resp = true
			} else {
				resp = false
			}
			reqTokensCh.resCh <- resp
		}
	}
}

type LeakyBucket struct {
	capacity int
	leakRate int
	tokens   int
	lastTime time.Time
	*RateLimiterBase
}

func NewLeakyBucket(capacity, leakRate int) RateLimiter {
	allowCh := make(chan requestTokensCh, LIMITER_CAPACITY)
	ctx, cancelFunc := context.WithCancel(context.Background())
	rlBase := &RateLimiterBase{
		allowCh:  allowCh,
		stopFunc: cancelFunc,
	}
	rl := &LeakyBucket{
		RateLimiterBase: rlBase,
		capacity:        capacity,
		leakRate:        leakRate,
		tokens:          capacity,
		lastTime:        time.Now(),
	}

	go rl.leakyBucketAlgorithm(ctx)

	return rl
}

func (rl *LeakyBucket) leakyBucketAlgorithm(ctx context.Context) {
	// runs the leaky bucket algorithm in a separate goroutine and also checks for event(cancelling the context) to stop this goroutine
	for {
		select {
		case <-ctx.Done():
			return
		case reqTokensCh := <-rl.allowCh:
			currentTime := time.Now()
			timePassed := rl.lastTime.Sub(currentTime).Seconds()

			leakedTokens := int(timePassed) * rl.leakRate

			temp := rl.tokens - leakedTokens
			if temp < 0 {
				temp = 0
			}
			if rl.capacity <= temp {
				rl.tokens = rl.capacity
			} else {
				rl.tokens = temp
			}
			rl.lastTime = currentTime
			resp := false

			if reqTokensCh.tokens <= rl.tokens {
				rl.tokens -= reqTokensCh.tokens
				resp = true
			} else {
				resp = false
			}
			reqTokensCh.resCh <- resp
		}
	}
}

type FixedWindow struct {
	limit      int
	windowSize int
	capacity   int
	lastTime   time.Time
	*RateLimiterBase
}

func NewFixedWindow(limit, windowSize, capacity int) RateLimiter {
	allowCh := make(chan requestTokensCh, LIMITER_CAPACITY)
	ctx, cancelFunc := context.WithCancel(context.Background())
	rlBase := &RateLimiterBase{
		allowCh:  allowCh,
		stopFunc: cancelFunc,
	}
	rl := &FixedWindow{
		RateLimiterBase: rlBase,
		limit:           limit,
		capacity:        capacity,
		windowSize:      windowSize,
		lastTime:        time.Now(),
	}

	go rl.fixedWindowAlgorithm(ctx)

	return rl
}

func (rl *FixedWindow) fixedWindowAlgorithm(ctx context.Context) {
	// runs the fixed window algorithm in a separate goroutine and also checks for event(cancelling the context) to stop this goroutine
	for {
		select {
		case <-ctx.Done():
			return
		case reqTokensCh := <-rl.allowCh:
			currentTime := time.Now()
			timePassed := int(rl.lastTime.Sub(currentTime).Seconds())

			resp := false
			if timePassed >= rl.windowSize {
				rl.lastTime = currentTime
				rl.limit = rl.capacity
				resp = true
			} else {
				if rl.limit > 0 {
					rl.limit -= 1
					resp = true
				} else {
					resp = false
				}
			}
			reqTokensCh.resCh <- resp
		}
	}
}

type SlidingWindow struct {
	limit      int
	windowSize time.Duration
	timeStamps []time.Time
	*RateLimiterBase
}

func NewSlidingWindow(limit int, windowSize time.Duration) RateLimiter {
	allowCh := make(chan requestTokensCh, LIMITER_CAPACITY)
	ctx, cancelFunc := context.WithCancel(context.Background())
	rlBase := &RateLimiterBase{
		allowCh:  allowCh,
		stopFunc: cancelFunc,
	}
	rl := &SlidingWindow{
		RateLimiterBase: rlBase,
		limit:           limit,
		windowSize:      windowSize,
		timeStamps:      make([]time.Time, 0),
	}

	go rl.slidingWindowAlgorithm(ctx)

	return rl
}

func (rl *SlidingWindow) slidingWindowAlgorithm(ctx context.Context) {
	// runs the sliding window algorithm in a separate goroutine and also checks for event(cancelling the context) to stop this goroutine
	for {
		select {
		case <-ctx.Done():
			return
		case reqTokensCh := <-rl.allowCh:
			currentTime := time.Now()
			rl.timeStamps = append(rl.timeStamps, currentTime)

			for len(rl.timeStamps) > 0 && rl.timeStamps[0].Before(currentTime.Add(-rl.windowSize)) {
				rl.timeStamps = rl.timeStamps[1:]
			}

			resp := false
			if len(rl.timeStamps) <= rl.limit {
				resp = true
			}
			reqTokensCh.resCh <- resp
		}
	}
}

func main() {

}
