"""
Examples of *args and **kwargs
"""


def add(*args):
    return sum(args)


print(add(1, 2))
print(add(1, 2, 3, 4))


def profile(**kwargs):

    for key, value in kwargs.items():
        print(f"{key}: {value}")


profile(
    name="Prithu",
    city="Lucknow",
    role="Python Developer"
)