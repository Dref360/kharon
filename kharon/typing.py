from typing import Optional, TypeVar

T = TypeVar("T")


def assert_not_none(val: Optional[T]) -> T:
    """
    This function makes sure that the variable is not None and has a fixed type for mypy purposes.
    Args:
        val: any value which is Optional.
    Returns:
        val [T]: The same value with a defined type.
    Raises:
        Assertion error if val is None.
    """
    if val is None:
        raise AssertionError(f"value of {val} is None, expected not None")
    return val
