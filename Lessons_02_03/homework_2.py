"""Homework #2. Working with data types."""


# Strings:
# Write a function that takes a string and returns its length.
def string_length(string: str) -> int:
    """Return the length of the given string.

    Args:
        string (str): The input string.

    Returns:
        int: The length of the string.
    """
    return len(string)


# Create a function that takes two strings and returns the concatenated string.
def concat_strings(string1: str, string2: str) -> str:
    """Concatenate two strings and returns the result.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.

    Returns:
        str: The concatenated string.
    """
    return string1 + string2


# Numbers(Int/float):
# Implement a function that takes a number and returns its square.
def square_number(number: int) -> int:
    """Return the square of the given number.

    Args:
        number (int): The input number.

    Returns:
        int: The squared number.
    """
    return number ** 2


# Create a function that takes two numbers and returns their sum.
def sum_numbers(number1: int, number2: int) -> int:
    """Return the sum of two numbers.

    Args:
        number1 (int): The first number.
        number2 (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return number1 + number2


# Create a function that takes 2 int numbers, divides them,
# and returns the quotient and remainder.
def divide_numbers(number1: int, number2: int) -> tuple:
    """Divide two numbers and returns the quotient and remainder as a tuple.

    Args:
        number1 (int): The numerator.
        number2 (int): The denominator.

    Returns:
        tuple: A tuple containing the quotient and remainder.
    """
    return number1 // number2, number1 % number2


# Lists:
# Write a function to calculate the average of a list of numbers.
def average(numbers: list) -> float:
    """Calculate and returns the average of a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        float: The average of the numbers.
    """
    return sum(numbers) / len(numbers)


# Implement a function that takes two lists and
# returns a list that contains the common elements of both lists.
def common_elements(list1: list, list2: list) -> list:
    """Return a list containing the common elements of both input lists.

    Args:
        list1 (list): The first list.
        list2 (list): The second list.

    Returns:
        list: A list of common elements.
    """
    return list(set(list1) & set(list2))


# Dictionaries:
# Create a function that takes a dictionary and
# prints all the keys in that dictionary.
def print_keys(dictionary: dict) -> None:
    """Return all the keys in the given dictionary.

    Args:
        dictionary (dict): The input dictionary.

    Returns:
        list: A list of dictionary keys.
    """
    return list(dictionary.keys())


# Implement a function that takes two dictionaries and
# returns a new dictionary that is the union of both dictionaries.
def union_dicts(dict1: dict, dict2: dict) -> dict:
    """Return a new dictionary that is the union of both input dictionaries.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        dict: A merged dictionary containing keys and values.
    """
    return {**dict1, **dict2}


# Sets:
# Write a function that takes two sets and returns their union.
def union_sets(set1: set, set2: set) -> set:
    """Return the union of two sets.

    Args:
        set1 (set): The first set.
        set2 (set): The second set.

    Returns:
        set: The union of the two sets.
    """
    return set1.union(set2)


# Create a function that checks if one set is a subset of another.
def is_subset(set1: set, set2: set) -> bool:
    """Check if the first set is a subset of the second set.

    Args:
        set1 (set): The first set.
        set2 (set): The second set.

    Returns:
        bool: True if set1 is a subset of set2, otherwise False.
    """
    return set1.issubset(set2)


# Conditional expressions and loops:
# Implement a function that takes a number and
# outputs 'Even' if the number is even and 'Odd' if it is odd.
def even_or_odd(number: int) -> str:
    """Return 'Even' if the number is even and 'Odd' if it is odd.

    Args:
        number (int): The input number.

    Returns:
        str: 'Even' if the number is even, 'Odd' otherwise.
    """
    return 'Even' if number % 2 == 0 else 'Odd'


# Create a function that takes a list of numbers and
#  returns a new list containing only even numbers.
def even_numbers(numbers: list) -> list:
    """Return a new list containing only even numbers from the input list.

    Args:
        numbers (list): A list of numbers.

    Returns:
        list: A list containing only even numbers.
    """
    return [number for number in numbers if number % 2 == 0]


if __name__ == '__main__':
    # Testing the functions
    print(string_length('Hello, World!'))  # 13
    print(concat_strings('Hello, ', 'World!'))  # Hello, World!
    print(square_number(5))  # 25
    print(sum_numbers(5, 3))  # 8
    print(divide_numbers(10, 3))  # (3, 1)
    print(average([1, 2, 3, 4, 5]))  # 3.0
    print(common_elements([1, 2, 3], [3, 4, 5]))  # [3]
    print(print_keys({'name': 'Johnny', 'age': 25}))  # ['name', 'age']
    # Dictionary: 'name': 'Johnny', 'age': 25
    print(union_dicts({'name': 'Johnny'}, {'age': 25}))
    print(union_sets({1, 2, 3}, {3, 4, 5}))  # {1, 2, 3, 4, 5}
    print(is_subset({1, 2}, {1, 2, 3}))  # True
    print(is_subset({10, 12}, {1, 2, 3}))  # False
    print(even_or_odd(5))  # Odd
    print(even_or_odd(8))  # Even
    print(even_numbers([1, 2, 3, 4, 5]))  # [2, 4]
