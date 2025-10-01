#!/usr/bin/env python3
"""最终功能测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, parse_function_calls, global_registry

# 测试基本功能
@function_call(prompt="测试函数", function_str="test_func(arg1, arg2)")
def test_func(arg1, arg2):
    return f"收到参数: {arg1}, {arg2}"

def test_basic_parsing():
    """测试基本解析功能"""
    print("=== 基本解析测试 ===")
    
    test_cases = [
        '<function-call>test_func("hello", "world");</function-call>',
        '<function-call>test_func(arg1="value1", arg2="value2");</function-call>',
        '<function-call>test_func("hello", arg2="world");</function-call>'
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case}")
        calls = parse_function_calls(test_case)
        for call in calls:
            print(f"  解析结果: {call}")
            try:
                result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
                print(f"  执行结果: {result}")
            except Exception as e:
                print(f"  错误: {e}")
        print()

if __name__ == "__main__":
    test_basic_parsing()
    print("✅ 所有测试完成！")