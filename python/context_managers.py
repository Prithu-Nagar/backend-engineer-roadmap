"""
Context Manager Examples

Demonstrates:
- Using the with statement
- Custom context managers
- contextlib.contextmanager
"""

from contextlib import contextmanager


# ---------------------------------------
# Using a Context Manager
# ---------------------------------------

with open("sample.txt", "w") as file:
    file.write("Hello from a context manager.")

print("File written successfully.")


# ---------------------------------------
# Custom Context Manager
# ---------------------------------------

class ManagedResource:
    def __enter__(self):
        print("Resource opened.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Resource closed.")
        return False


with ManagedResource():
    print("Using the resource.")


# ---------------------------------------
# contextlib.contextmanager
# ---------------------------------------

@contextmanager
def managed_resource():
    print("Resource opened.")

    try:
        yield
    finally:
        print("Resource closed.")


with managed_resource():
    print("Using contextlib context manager.")
