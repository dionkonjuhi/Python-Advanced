from typing import Optional, Any
from typing import Union

from lesson3.conditionals import number


def get_name(name: Optional[str] = None) -> str:
    if name:
        return name
    return "Anonymous"

print(get_name())

def process_value(value: Union[int,str]) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"

print(process_value("Probit Academy"))


def process_anything(value: Any) -> str:
    return f"Processed{value}"

print(process_value(1))

def sum_list(numbers: List[int]) -> int:
    return sum(numbers)

number: List[int] = [1,2,3]
result: int = sum_list(numbers)
print(result)
