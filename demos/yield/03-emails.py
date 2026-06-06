"""
Recursive traversal - Demonstration of recursive generators and `yield from`.

Problem statement:
    Imagine an API response containing deeply nested dictionaries and lists.

    We want to find every ocurrence of a specific key
    (for example, "email"), regardless of how deeply it is buried.

    A tradicional approach might:
        1. Traverse the entire structure.
        2. Collect every match into a list.
        4. Return the complete list.

    A generator takes a different approach:
        - Find one match
        - Yield it immediately
        - Continue searching only when asked

    This allows us to stream results as they are discovered
"""


def extract_values(nested_data: dict | list, target_key: str):
    """
    Recursively search dictionaries/lists for a given key.

    Whenever a matching key is found, its value is yielded.

    The function explores  nested containers by calling itself recursively and forwarding any yielded values with the `yield from` statement.
    """

    if isinstance(nested_data, dict):
        for key, value in nested_data.items():
            # found the key we are looking for
            # yield the value immediately and pause execution
            if key == target_key:
                yield value
            # continue searching inside nested containers
            if isinstance(value, (dict, list)):
                yield from extract_values(value, target_key)
    elif isinstance(nested_data, list):
        for item in nested_data:
            if isinstance(item, (dict, list)):
                yield from extract_values(item, target_key)


if __name__ == "__main__":
    # Mock API response containing nested dictionaries and lists.
    company_data = {
        "name": "Tech Corp",
        "departments": [
            {
                "name": "Engineering",
                "lead": {"name": "Alice", "email": "alice@example.com"},
                "teams": [
                    {
                        "members": [
                            {"email": "bob@example.com"},
                            {"email": "charlie@example.com"},
                        ]
                    }
                ],
            },
            {"name": "HR", "lead": {"name": "Diana", "email": "diana@example.com"}},
        ],
    }

    # The for-loop drives the entire search.
    #
    # The generator:
    #   1. Starts exploring the structure.
    #   2. Finds the first email.
    #   3. Yields it and pauses.
    #   4. Resumes exactly where it stopped when the loop asks again.
    #
    # At no point is a list of all emails created.
    for email in extract_values(company_data, "email"):
        print(email)
