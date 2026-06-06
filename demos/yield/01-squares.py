"""
Lazy Values - From Lists to Generators

Problem Statement:
    Given a sequence of numbers, produce their squares.

We'll solve the same problem severa times, gradually moving from a list-based
approach to a generator-based approach.

The goal is not to change the result, but to change *when* results are produced
and *how much* memory is required to produce them
"""

# ------------------------------------------------------------------
# Step 1: Traditional approach
# ------------------------------------------------------------------
# Build every result in memory before returning

# Input:
#   [1, 2, 3, 4, 5]
# Output:
#   [1, 4, 9, 16, 25]
# This is simple and perfectly find for small datasets
#
# The downside that the entire result list must exists in
# memory before the caller can use even the first value

# def square_numbers(numbers):
#     result = []

#     for number in numbers:
#         result.append(number**2)
#     return result

# ------------------------------------------------------------------
# Step 2: Return `return` with yield
# ------------------------------------------------------------------

# By introducing `yield`, the function becomes a generator.
#
# Instead of producing the complete list immediately, it
# produces values one at a time as they are requested.
#


# def square_numbers(numbers):
#     for number in numbers:
#         yield number**2

# ------------------------------------------------------------------
# Step 3: Calling a generator#
# ------------------------------------------------------------------

# Calling a generator function does NOT execute its body.
#
# Python creates a generator object that remembers:
#   - where execution starts
#   - local variables
#   - current position in the function

# if __name__ == "__main__":
#     squares = square_numbers([1, 2, 3, 4, 5])
#     print(squares)
# Output: <generator object square_numbers at 0xxxxxxx>
# ------------------------------------------------------------------
# Step 4: Request for values manually
# ------------------------------------------------------------------

# `next()` resumes execution until the generator
# reaches the next `yield` statement.

# if __name__ == "__main__":
#     squares = square_numbers([1, 2, 3, 4, 5])

#     print(next(squares))  # 1
#     print(next(squares))  # 4
#     print(next(squares))  # 9
#     print(next(squares))  # 16
#     print(next(squares))  # 25 -
#     # Here the generator has now exhausted all available values.
#     print(next(squares))  # StopIteration -
#     # This exception signals that the generator has finished.

# ------------------------------------------------------------------
# Step 5: Let a for-loop drive the generator
# ------------------------------------------------------------------

# if __name__ == "__main__":
#     for square in square_numbers([1, 2, 3, 4, 5]):
#         print(square)

# ------------------------------------------------------------------
# Step 6: List comprehension equivalent
# ------------------------------------------------------------------

# The original list-based solution can be writen more compactly:
squares = [number**2 for number in [1, 2, 3, 4, 5]]

# This is still a list; all values are calculated and stored in memory immediately

# ------------------------------------------------------------------
# Step 7: Generator expression
# ------------------------------------------------------------------

# A generator expression looks almost identical to a list comprehension
#
# The only difference is:
# [] -> builds a list
# () -> Creates a generator
#
# This gives us lazy evaluation without writing
# a separate generator function.
#
if __name__ == "__main__":
    squares = (number**2 for number in [1, 2, 3, 4, 5])

    for number in squares:
        print(number)
