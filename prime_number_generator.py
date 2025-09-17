def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**(0.5)) + 1, 2):
        if n % i == 0:
            return False
    return True

def gen_prime():
    n = 2
    while True:
        while not is_prime(n):
            n += 1
        yield n
        n += 1

if __name__ == '__main__':
    gp = gen_prime()
    for i in range(101):
        print(next(gp))