# This file contants the implementation of some modular arithmetic operations

def exp_modular(N: int, a: int, exp: int) -> int:
    '''
    This function calculates the value: a^exp % N in O(log2(N)) time and O(log2(N)) space complexity
    '''
    
    initial_number = a % N

    if exp == 0:
        return 1
    elif exp == 1:
        return initial_number
    
    binary = bin(exp)[2:]
    size = len(binary) + binary.count('1') - 1

    # Create a dynamic programming table...
    dp = [0] * (size)
    dp[0] = initial_number

    for i in range(1, len(binary)):
        dp[i] = (dp[i-1] * dp[i-1]) % N

    position = len(binary) - 2
    index = len(binary)
    
    for i in range(1, len(binary)):
        if binary[i] == '1':
            dp[index] = (dp[index-1] * dp[position]) % N
            index += 1
        
        position -= 1

    # Return the last element of the dp table
    return dp[-1]

def order(N: int, a: int) -> int:
    ''' 
    This function calculates the order (mod N) of a number a.
    '''
    pass
    
