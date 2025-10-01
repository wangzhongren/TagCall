from typing import Callable, Optional
from .core import global_registry

def function_call(prompt: str, function_str: str = None, name: str = None):
    """函数调用装饰器
    
    Args:
        prompt: 方法提示词说明
        function_str: 方法字符串表示，如果为None则自动从源码生成
        name: 注册的函数名，如果为None则使用函数名
    """
    def decorator(func: Callable):
        func_name = name or func.__name__
        global_registry.register(func_name, prompt, func, function_str)
        return func
    return decorator