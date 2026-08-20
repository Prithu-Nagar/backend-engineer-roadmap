"""
Day 19 - Python OOP Review

Topics:
- Composition vs inheritance
- Encapsulation
- Abstraction
- Polymorphism
- SOLID-oriented design
- Dependency inversion
"""


# ============================================================
# 1. COMPOSITION
# ============================================================

class EmailSender:
    """Responsible only for sending email messages."""

    def send(self, recipient: str, message: str) -> None:
        print(f"Sending email to {recipient}: {message}")


class NotificationService:
    """
    NotificationService uses EmailSender instead of inheriting
    from it.

    This is composition:
        NotificationService HAS-A EmailSender
    """

    def __init__(self, sender: EmailSender) -> None:
        self.sender = sender

    def notify(self, recipient: str, message: str) -> None:
        self.sender.send(recipient, message)


# ============================================================
# 2. INHERITANCE
# ============================================================

class PaymentProcessor:
    """Base abstraction for payment processors."""

    def process(self, amount: float) -> str:
        raise NotImplementedError


class CardPaymentProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"Processed card payment of {amount:.2f}"


class UpiPaymentProcessor(PaymentProcessor):
    def process(self, amount: float) -> str:
        return f"Processed UPI payment of {amount:.2f}"


# ============================================================
# 3. POLYMORPHISM
# ============================================================

def complete_payment(
    processor: PaymentProcessor,
    amount: float,
) -> str:
    """
    The caller depends on the abstraction rather than a
    concrete payment implementation.
    """
    return processor.process(amount)


# ============================================================
# 4. SOLID - SINGLE RESPONSIBILITY PRINCIPLE
# ============================================================

class TaskRepository:
    """Responsible only for task persistence."""

    def save(self, task: dict) -> None:
        print(f"Saving task: {task}")


class TaskValidator:
    """Responsible only for task validation."""

    def validate(self, task: dict) -> bool:
        return bool(task.get("title"))


class TaskService:
    """
    Responsible for task-related business orchestration.

    Persistence and validation responsibilities are delegated
    to separate classes.
    """

    def __init__(
        self,
        repository: TaskRepository,
        validator: TaskValidator,
    ) -> None:
        self.repository = repository
        self.validator = validator

    def create_task(self, task: dict) -> None:
        if not self.validator.validate(task):
            raise ValueError("Task title is required.")

        self.repository.save(task)


# ============================================================
# 5. OPEN/CLOSED PRINCIPLE
# ============================================================

class Discount:
    def calculate(self, amount: float) -> float:
        raise NotImplementedError


class RegularDiscount(Discount):
    def calculate(self, amount: float) -> float:
        return amount * 0.05


class PremiumDiscount(Discount):
    def calculate(self, amount: float) -> float:
        return amount * 0.15


def apply_discount(
    amount: float,
    discount: Discount,
) -> float:
    return amount - discount.calculate(amount)


# ============================================================
# 6. LISKOV SUBSTITUTION PRINCIPLE
# ============================================================

class Bird:
    def move(self) -> str:
        return "Moving"


class FlyingBird(Bird):
    def move(self) -> str:
        return "Flying"


class Penguin(Bird):
    def move(self) -> str:
        return "Walking"


def move_bird(bird: Bird) -> str:
    return bird.move()


# ============================================================
# 7. INTERFACE SEGREGATION PRINCIPLE
# ============================================================

class Printable:
    def print_document(self, document: str) -> None:
        raise NotImplementedError


class Scannable:
    def scan_document(self) -> str:
        raise NotImplementedError


class Printer(Printable):
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")


class MultiFunctionPrinter(Printable, Scannable):
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")

    def scan_document(self) -> str:
        return "Scanned document"


# ============================================================
# 8. DEPENDENCY INVERSION PRINCIPLE
# ============================================================

class MessageSender:
    """Abstraction used by the high-level service."""

    def send(self, recipient: str, message: str) -> None:
        raise NotImplementedError


class EmailMessageSender(MessageSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"Email -> {recipient}: {message}")


class SmsMessageSender(MessageSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"SMS -> {recipient}: {message}")


class AlertService:
    """
    High-level module depends on the MessageSender abstraction.

    It does not directly depend on EmailMessageSender or
    SmsMessageSender.
    """

    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender

    def send_alert(
        self,
        recipient: str,
        message: str,
    ) -> None:
        self.sender.send(recipient, message)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    # Composition
    email_sender = EmailSender()
    notification_service = NotificationService(email_sender)
    notification_service.notify(
        "user@example.com",
        "Task completed.",
    )

    # Inheritance + polymorphism
    processors = [
        CardPaymentProcessor(),
        UpiPaymentProcessor(),
    ]

    for processor in processors:
        print(complete_payment(processor, 1000))

    # Single Responsibility
    task_service = TaskService(
        repository=TaskRepository(),
        validator=TaskValidator(),
    )

    task_service.create_task(
        {"title": "Study OOP design"},
    )

    # Open/Closed
    print(
        apply_discount(
            1000,
            PremiumDiscount(),
        )
    )

    # Liskov Substitution
    print(move_bird(FlyingBird()))
    print(move_bird(Penguin()))

    # Dependency Inversion
    alert_service = AlertService(
        EmailMessageSender()
    )

    alert_service.send_alert(
        "admin@example.com",
        "Server health check completed.",
    )