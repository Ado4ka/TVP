def recursive_method(x):
    if x == 0:
        return 0
    else:
        return recursive_method(x - 1) + 3

def iterative_method(x):
    result = 0
    for _ in range(x):
        result += 3
    return result

print("Multiplication by 3")
x = int(input("Choose x: "))
result = recursive_method(x)
print("Recursive method: ", result)


result = iterative_method(x)
print("Iterative method: ", result)


