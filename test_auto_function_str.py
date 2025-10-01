#!/usr/bin/env python3
"""测试自动生成函数字符串功能"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, global_registry

def test_auto_function_string_generation():
    """测试自动生成函数字符串"""
    print("=== 测试自动生成函数字符串 ===")
    
    # 测试各种函数定义
    
    @function_call(prompt="简单函数")
    def simple_func(a, b):
        """简单的位置参数"""
        return a + b
    
    @function_call(prompt="带默认值")
    def func_with_defaults(a, b=10, c="hello"):
        """带默认值的参数"""
        return f"{a}, {b}, {c}"
    
    @function_call(prompt="可变参数")
    def func_with_args(a, *args, **kwargs):
        """可变参数"""
        return f"{a}, {args}, {kwargs}"
    
    @function_call(prompt="关键字参数")
    def func_with_kwonly(a, b, *, key1="default1", key2=20):
        """关键字参数"""
        return f"{a}, {b}, {key1}, {key2}"
    
    @function_call(prompt="复杂参数")
    def complex_func(a, b=5, *args, c=10, d=None, **kwargs):
        """复杂参数组合"""
        return f"{a}, {b}, {args}, {c}, {d}, {kwargs}"
    
    # 查看生成的函数字符串
    functions = global_registry.get_all_functions()
    
    print("自动生成的函数字符串:")
    for name, info in functions.items():
        print(f"  {name}: {info['function_str']}")
    
    # 测试提示词生成
    print("\n生成的提示词:")
    prompt_text = global_registry.get_prompt_descriptions()
    print(prompt_text)

def test_function_execution():
    """测试函数执行"""
    print("\n=== 测试函数执行 ===")
    
    @function_call(prompt="测试执行")
    def test_exec(a, b=5, c="world"):
        return f"a={a}, b={b}, c={c}"
    
    # 测试各种调用方式
    test_cases = [
        ('test_exec("hello")', ["hello"]),
        ('test_exec("hello", 10)', ["hello", 10]),
        ('test_exec("hello", c="python")', ["hello"], {"c": "python"}),
        ('test_exec("hello", 20, "ai")', ["hello", 20, "ai"])
    ]
    
    for call_desc, args in test_cases:
        print(f"执行: {call_desc}")
        try:
            result = global_registry.execute_function("test_exec", *args[0], **args[1] if len(args) > 1 else {})
            print(f"  结果: {result}")
        except Exception as e:
            print(f"  错误: {e}")

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 测试没有源码的情况（比如内置函数）
    try:
        # 尝试注册一个内置函数
        @function_call(prompt="内置函数")
        def builtin_like():
            pass
        
        # 修改函数对象，模拟没有源码的情况
        import types
        builtin_like.__code__ = types.CodeType(0, 0, 0, 0, 0, b'', (), (), (), '', '', 0, b'')
        
        functions = global_registry.get_all_functions()
        print(f"边界情况处理: {functions.get('builtin_like', {}).get('function_str', 'N/A')}")
        
    except Exception as e:
        print(f"边界情况处理正常: {e}")

if __name__ == "__main__":
    test_auto_function_string_generation()
    test_function_execution()
    test_edge_cases()
    print("\n✅ 自动函数字符串生成测试完成！")