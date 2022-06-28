
N = 317

a = 1
init = 5
for i in range(1, N-1):
    a = init * i % N
    
    print('{0:10b}'.format(a))

    
     