"""
Tool functions module cho Agno Agent.

Module này chứa các tool functions mà agent có thể sử dụng:
- sum_1_to_n: Tính tổng từ 1 đến n
- calculator: Máy tính đơn giản với 4 phép toán cơ bản
"""


def sum_1_to_n(n: int) -> int:
    """
    Tính tổng từ 1 đến n.
    
    Args:
        n: Số nguyên dương
        
    Returns:
        Tổng từ 1 đến n, hoặc 0 nếu n < 1
        
    Examples:
        >>> sum_1_to_n(5)
        15
        >>> sum_1_to_n(0)
        0
    """
    if n < 1:
        return 0
    return sum(range(1, n + 1))


def calculator(a: float, b: float, operation: str) -> float:
    """
    Thực hiện phép tính đơn giản.
    
    Args:
        a: Số thứ nhất
        b: Số thứ hai
        operation: Phép tính ("add", "subtract", "multiply", "divide")
        
    Returns:
        Kết quả phép tính, hoặc 0 nếu operation không hợp lệ
        
    Examples:
        >>> calculator(5, 3, "add")
        8.0
        >>> calculator(10, 2, "divide")
        5.0
    """
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float('inf')
    }
    return operations.get(operation, 0)
