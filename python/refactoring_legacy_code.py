"""
Day 65 — Refactoring Legacy Code

A small backend-oriented example showing how a legacy function with mixed
responsibilities can be refactored into focused, testable components without
changing the public behavior of the use case.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Order:
    customer_id: int
    subtotal: Decimal
    discount_code: str | None = None


class DiscountPolicy:
    """Encapsulates discount rules instead of mixing them into orchestration."""

    RATES = {
        "SAVE10": Decimal("0.10"),
        "SAVE20": Decimal("0.20"),
    }

    def calculate(self, subtotal: Decimal, code: str | None) -> Decimal:
        rate = self.RATES.get((code or "").upper(), Decimal("0"))
        return (subtotal * rate).quantize(Decimal("0.01"))


class TaxCalculator:
    """Keeps tax calculation independent from order orchestration."""

    def __init__(self, rate: Decimal = Decimal("0.18")) -> None:
        self.rate = rate

    def calculate(self, taxable_amount: Decimal) -> Decimal:
        return (taxable_amount * self.rate).quantize(Decimal("0.01"))


class OrderPricingService:
    """Coordinates pricing steps while delegating individual rules."""

    def __init__(
        self,
        discount_policy: DiscountPolicy,
        tax_calculator: TaxCalculator,
    ) -> None:
        self.discount_policy = discount_policy
        self.tax_calculator = tax_calculator

    def calculate_total(self, order: Order) -> Decimal:
        if order.subtotal < 0:
            raise ValueError("subtotal must not be negative")

        discount = self.discount_policy.calculate(
            order.subtotal,
            order.discount_code,
        )
        taxable_amount = order.subtotal - discount
        tax = self.tax_calculator.calculate(taxable_amount)
        return (taxable_amount + tax).quantize(Decimal("0.01"))


def legacy_pricing(order: Order) -> Decimal:
    """Reference implementation representing the original mixed-responsibility style."""
    if order.subtotal < 0:
        raise ValueError("subtotal must not be negative")

    discount_rate = {
        "SAVE10": Decimal("0.10"),
        "SAVE20": Decimal("0.20"),
    }.get((order.discount_code or "").upper(), Decimal("0"))
    discounted = order.subtotal - (order.subtotal * discount_rate)
    tax = discounted * Decimal("0.18")
    return (discounted + tax).quantize(Decimal("0.01"))


def main() -> None:
    order = Order(101, Decimal("1000.00"), "SAVE10")
    service = OrderPricingService(DiscountPolicy(), TaxCalculator())
    print("legacy:", legacy_pricing(order))
    print("refactored:", service.calculate_total(order))


if __name__ == "__main__":
    main()
