def join(separator: str, separated: list[str]) -> str:
    """
    Joins a list of strings using a separator
    and returns the result.

    :param separator: Separator to be used
                for joining the strings.
    :param separated: List of strings to be joined.

    :return: Joined string with the specified separator.

    Examples:

    >>> join("", ["a", "b", "c", "d"])
    'abcd'
    >>> join("#", ["a", "b", "c", "d"])
    'a#b#c#d'
    >>> join("#", ["a"])
    'a'
    >>> join(" ", ["You", "are", "amazing!"])
    'You are amazing!'

    This example should raise an
    exception for non-string elements:
    >>> join("#", ["a", "b", "c", 1])
    Traceback (most recent call last):
        ...
    Exception: join() accepts only strings

    Additional test case with a different separator:
    >>> join("-", ["apple", "banana", "cherry"])
    'apple-banana-cherry'
    >>> join(",", ["", "", ""])
    ',,'

    """

    # Check for non-string elements
    for word_or_phrase in separated:
        if not isinstance(word_or_phrase, str):
            raise Exception("join() accepts only strings")

    # Use the built-in join method for cleaner implementation
    return separator.join(separated)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
