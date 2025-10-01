"""TagCall - 一个支持函数调用标记解析和注册的 Python 库"""
from .core import FunctionRegistry, parse_function_calls
from .decorator import function_call

__version__ = "0.1.0"
__all__ = ['FunctionRegistry', 'parse_function_calls', 'function_call']