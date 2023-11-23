def recursive_method(x):
    if x == 0:
        return 0
    else:
        return recursive_method(x - 1) + 3

result = recursive_method(2)
print("Recursive method: ", result)

def iterative_method(x):
    result = 0
    for _ in range(x):
        result += 3
    return result

result = iterative_method(2)
print("Iterative method: ", result)
