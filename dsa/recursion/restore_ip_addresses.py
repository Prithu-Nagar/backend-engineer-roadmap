"""
LeetCode 93
Restore IP Addresses

Day 55 — Backtracking

Generate every valid IPv4 address that can be formed by inserting three
dots into a digit string.

Time Complexity:
O(3^n) in the bounded search formulation, with n <= 12.

Space Complexity:
O(n) auxiliary recursion space, excluding the returned addresses.
"""

def restore_ip_addresses(s: str) -> list[str]:
    """Return all valid IPv4 addresses that can be formed from ``s``."""
    result: list[str] = []
    parts: list[str] = []

    def backtrack(start: int) -> None:
        remaining_chars = len(s) - start
        remaining_parts = 4 - len(parts)

        if remaining_parts == 0:
            if start == len(s):
                result.append(".".join(parts))
            return

        if remaining_chars < remaining_parts or remaining_chars > remaining_parts * 3:
            return

        for end in range(start + 1, min(len(s), start + 3) + 1):
            part = s[start:end]

            if len(part) > 1 and part[0] == "0":
                continue

            value = int(part)
            if value > 255:
                continue

            parts.append(part)
            backtrack(end)
            parts.pop()

    if not s or not s.isdigit() or len(s) > 12:
        return []

    backtrack(0)
    return result


if __name__ == "__main__":
    print(restore_ip_addresses("25525511135"))
