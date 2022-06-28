from math import gcd



from sympy import prime

# Generate 100 prime numbers

num = 3
total_primes = 0

def isPrime(n: int) -> bool:
    for i in range(2, n-1):
        if n % i == 0:
            return False
    return True

primes = []

while True:
    if isPrime(num):
        primes.append(num)
        total_primes += 1
    if total_primes == 20:
        break
    num += 1

a = 4
init = 4

for i in range(total_primes-1):
    for j in range(i+1, total_primes):
        N = primes[i] * primes[j]

        a = 4
        r = 1

        while True:
            a = (a * init) % N
            r += 1
            if a == 1:
                break

        original_r = r

        even = False
        if r % 2 == 1:
            r += 1
        else:
            even = True
        
        if even:
            p1 = 4**(r >> 1) - 1
            p2 = 4**(r >> 1) + 1
        else:
            p1 = 4**(r >> 1) - 2
            p2 = 4**(r >> 1) + 2

        f1 = gcd(p1, N)
        f2 = gcd(p2, N)

        print(f1, f2)

        if (f1 == primes[i] and f2 == primes[j]) or (f1 == primes[j] and f2 == primes[i]):
            print('OK:', f1, f2)
        else:
            print('ERROR', '##############', even, 'r=', original_r)
            print(primes[i], primes[j])
            print('-------------------')

        