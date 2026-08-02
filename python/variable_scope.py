"""
LEGB Scope Rule
"""

count = 0


def increment():
    global count
    count += 1


increment()

print(count)


def outer():

    x = 10

    def inner():
        nonlocal x
        x += 5
        print(x)

    inner()


outer()