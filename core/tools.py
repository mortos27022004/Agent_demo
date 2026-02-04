"""
Tool functions module cho Agno Agent.

Module này chứa các tool functions mà agent có thể sử dụng:
- sum_1_to_n: Tính tổng từ 1 đến n
- calculator: Máy tính đơn giản với 4 phép toán cơ bản
"""


def sum_1_to_n(n: int) -> int:

    if n < 1:
        return 0
    return sum(range(1, n + 1))


def calculator(a: float, b: float, operation: str) -> float:

    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float('inf')
    }
    return operations.get(operation, 0)

def get_area_of_circle(radius: float) -> float:
    """
    Get area of circle.
    
    Args:
        radius: Radius of circle
        
    Returns:
        Area of circle
    """
    return 3.14159 * radius * radius

def get_area_of_rectangle(length: float, width: float) -> float:
    """
    Get area of rectangle.
    
    Args:
        length: Length of rectangle
        width: Width of rectangle
        
    Returns:
        Area of rectangle
    """
    return length * width