# List Comprehension

squares = [x * x for x in range(5)]

print(squares)

# Dictionary Comprehension

square_dict = {x: x * x for x in range(5)}

print(square_dict)

# Set Comprehension

even = {x for x in range(10) if x % 2 == 0}

print(even)

# Generator Expression

generator = (x * x for x in range(5))

print(list(generator))