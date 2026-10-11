# Python OOP Interview Questions

Use these prompts to practice concise explanations, small examples, and design
trade-offs. Prefer examples grounded in backend services and testability.

## Core Questions

### 1. What are the four pillars of OOP?

- **Encapsulation:** keep state and the operations that protect its invariants
  together; expose a clear public interface.
- **Abstraction:** expose essential behavior while hiding implementation detail.
- **Inheritance:** derive a specialized type from a base type when the subtype
  truly satisfies the base contract.
- **Polymorphism:** allow callers to use a shared interface with different
  implementations.

Python supports these ideas through classes, conventions, properties, abstract
base classes, protocols, and dynamic dispatch; it does not enforce private
instance attributes in the same way as some statically typed languages.

### 2. What is the difference between a class and an instance?

A class defines behavior and the structure expected of its objects. An
instance is a concrete object with its own instance state. Class attributes are
shared through the class lookup rules, while instance attributes normally
store per-object values. Avoid mutable class attributes for state intended to
be independent for each instance.

### 3. Explain instance, class, and static methods.

- An instance method receives `self` and operates on an instance.
- A `@classmethod` receives `cls` and is useful for alternative constructors
  or behavior tied to the class.
- A `@staticmethod` receives no implicit first argument and groups a helper
  with a class when it has no need for instance or class state.

Choose the method type based on the data and contract it needs, not stylistic
preference alone.

### 4. What is the difference between inheritance and composition?

Inheritance models a subtype relationship and reuses behavior through a base
class. Composition builds an object from collaborators and delegates work to
them. Composition is often easier to change and test when a service needs
replaceable storage, notification, or payment behavior. Use inheritance when
the subtype can safely honor the base contract.

### 5. What is polymorphism in Python?

Callers depend on a common behavior while concrete objects provide the
implementation. Python often uses duck typing: an object is suitable when it
supports the operations the caller requires. `abc.ABC` and `typing.Protocol`
can make contracts more explicit when useful.

### 6. What are `__init__` and `__new__`?

`__new__` creates and returns an instance; `__init__` initializes an instance
that has already been created. Most application classes only need `__init__`.
`__new__` is relevant for specialized immutable types, metaclass-related
behavior, or controlled instance creation.

### 7. How do properties help encapsulation?

A property exposes attribute-like access while allowing validation or computed
behavior. Use it when it protects a meaningful invariant or provides a stable
interface; avoid turning every simple attribute into unnecessary boilerplate.

### 8. What is method overriding, and does Python support overloading?

A subclass overrides a method by providing its own implementation. Python does
not select ordinary methods by argument signature in the traditional
compile-time overloading sense; default arguments, `*args`, dispatch helpers,
or `functools.singledispatch` may address different needs.

### 9. Explain the SOLID principles briefly.

- **Single Responsibility:** a module has one coherent reason to change.
- **Open/Closed:** extend behavior without repeatedly editing stable code.
- **Liskov Substitution:** subtypes preserve the promises of their base type.
- **Interface Segregation:** clients should not depend on methods they do not use.
- **Dependency Inversion:** high-level policy depends on abstractions, not
  low-level implementation details.

SOLID is a design aid, not a reason to create abstractions before they are
needed.

### 10. How does dependency injection improve testing?

A service receives collaborators such as repositories or message senders rather
than constructing concrete dependencies internally. Tests can inject fakes or
mocks, isolate business logic, and exercise failure paths without requiring a
real database or external service.

## Practical Interview Exercise

Design a task-creation service with a validator and repository interface.
Explain which behavior belongs in the service, how dependencies are supplied,
how invalid input is represented, and how a unit test can substitute an
in-memory repository.

## Common Mistakes

- Using inheritance only to reuse a few lines of code.
- Putting mutable state on the class when each instance needs its own state.
- Treating a leading underscore as a security boundary; it is a convention.
- Overusing getters, setters, abstract classes, or design patterns for trivial
  behavior.
- Making a subclass violate assumptions made by code using its base type.
- Claiming dependency injection requires a framework; constructor injection is
  often sufficient.

## Quick Revision

Explain encapsulation, abstraction, inheritance, and polymorphism with one
example each. Compare inheritance with composition, describe method types, and
show how dependency injection improves testability.
