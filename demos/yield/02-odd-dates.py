"""
Large Sequences - Demonstration of Python's `yield` keyword.

From: https://amitamola.medium.com/understanding-yield-in-python-b11e7e23d674

Problem statement:
    The date 01-03-2005 (March 1 2005) contains three consecutive odd numbers:
        day = 1,
        month = 3,
        year = 5
    It is the first date in the 21st century with this property.
    How many such dates exist in total?
"""

from datetime import date, timedelta


def date_range(start: date, end: date):
    """
    Generator that yields every date between `start` and `end` (inclusive).

    Because this function uses `yield`, calling it does not immediately
    execute the body. Instead, Python returns a generator object.

    Each time the caller requests another value:
        1. Execution resumes where it previously paused
        2. The next date is yielded
        3. Execution pauses again
    """
    delta: timedelta = end - start

    for offset in range(delta.days + 1):
        yield start + timedelta(days=offset)


def has_consecutive_odd_numbers(d: date) -> bool:
    """
    check whether day, month, and two-digit year form three consecutive odd numbers.
    Example:
        01-03-05 -> True
        03-05-07 -> True
        01-05-07 -> False
    """
    year = d.year % 100
    month = d.month
    day = d.day

    odd_values = (day, month, year)
    return (
        all(value % 2 == 1 for value in odd_values)
        and day + 2 == month
        and month + 2 == year
    )


if __name__ == "__main__":
    start_date = date(2000, 1, 1)
    end_date = date(2100, 12, 31)

    # the for-loop drives the generator
    for current_date in date_range(start_date, end_date):
        if has_consecutive_odd_numbers(current_date):
            print(current_date)
