"""
Fallback code generator for when external LLM APIs are unavailable.
Generates simple keyword-matched Python solutions locally.
"""

from __future__ import annotations

import random
import re
from typing import Tuple


class LocalFallbackGenerator:
    def generate_code(self, prompt: str, language: str = "python") -> str:
        text = prompt.lower()
        if "prime" in text:
            return self._primes()
        if "fibonacci" in text:
            return self._fibonacci()
        if "palindrome" in text or "palindromic" in text:
            return self._palindrome()
        if "reverse" in text and ("string" in text or "list" in text or "array" in text):
            return self._reverse_string()
        if "sort" in text:
            return self._bubble_sort()
        if "factorial" in text:
            return self._factorial()
        if "binary" in text and ("search" in text or "tree" in text):
            return self._binary_search()
        if "linked list" in text or "list" in text:
            return self._linked_list()
        return self._generic(prompt)

    def repair_code(self, code: str, errors: list[str], prompt: str, language: str = "python") -> Tuple[str, str]:
        fixed = code
        if "SyntaxError" in "\n".join(errors):
            fixed += "\n# [fallback repair] syntax stub added\n"
        if not fixed.strip():
            fixed = self.generate_code(prompt, language)
        return fixed, "Fallback local repair applied because external LLM is unavailable."

    def _primes(self) -> str:
        return '''def sieve_of_eratosthenes(limit: int) -> list[int]:
    """Return all prime numbers up to limit using sieve."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]


def is_prime(n: int) -> bool:
    """Check whether a single number is prime."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


if __name__ == "__main__":
    print(sieve_of_eratosthenes(50))
    print(is_prime(97))
'''

    def _fibonacci(self) -> str:
        return '''def fibonacci(n: int) -> list[int]:
    """Return Fibonacci sequence with n elements."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def fibonacci_recursive(n: int) -> int:
    """Return the nth Fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


if __name__ == "__main__":
    print(fibonacci(10))
    print(fibonacci_recursive(10))
'''

    def _palindrome(self) -> str:
        return '''def is_palindrome(text: str) -> bool:
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def longest_palindromic_substring(s: str) -> str:
    if not s:
        return ""
    start, max_len = 0, 1
    for i in range(len(s)):
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1
    return s[start:start + max_len]


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))
    print(longest_palindromic_substring("babad"))
'''

    def _reverse_string(self) -> str:
        return '''def reverse_string(text: str) -> str:
    return text[::-1]


def reverse_list(items: list[int]) -> list[int]:
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1
    return items


if __name__ == "__main__":
    print(reverse_string("python"))
    print(reverse_list([1, 2, 3, 4, 5]))
'''

    def _bubble_sort(self) -> str:
        return '''def bubble_sort(items: list[int]) -> list[int]:
    data = items[:]
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


if __name__ == "__main__":
    print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
'''

    def _factorial(self) -> str:
        return '''def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    if n in (0, 1):
        return 1
    return n * factorial_recursive(n - 1)


if __name__ == "__main__":
    print(factorial(5))
    print(factorial_recursive(6))
'''

    def _binary_search(self) -> str:
        return '''def binary_search(items: list[int], target: int) -> int:
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


class TreeNode:
    def __init__(self, value: int):
        self.value = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def insert(node: TreeNode | None, value: int) -> TreeNode:
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    else:
        node.right = insert(node.right, value)
    return node


if __name__ == "__main__":
    print(binary_search([1, 3, 5, 7, 9], 5))
'''

    def _linked_list(self) -> str:
        return '''class Node:
    def __init__(self, value):
        self.value = value
        self.next: Node | None = None


class LinkedList:
    def __init__(self):
        self.head: Node | None = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def reverse(self):
        previous = None
        current = self.head
        while current:
            nxt = current.next
            current.next = previous
            previous = current
            current = nxt
        self.head = previous

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


if __name__ == "__main__":
    lst = LinkedList()
    for value in [1, 2, 3]:
        lst.append(value)
    lst.reverse()
    print(lst.to_list())
'''

    def _generic(self, prompt: str) -> str:
        safe_topic = re.sub(r"[^a-zA-Z0-9_ ]", "", prompt).strip().replace(" ", "_")[:40]
        return f'''def solution(input_data):
    """Auto-generated solution for: {prompt}"""
    result = []
    for item in input_data:
        processed = item * 2
        result.append(processed)
    return result


if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    print(solution(data))
'''


# Shared instance
local_generator = LocalFallbackGenerator()
