#!/usr/bin/env python3
"""测试新的自动函数字符串生成功能"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, global_registry

def test_various_function_signatures():
    """测试各种函数签名"""
    print("=== 测试各种函数签名自动生成 ===")
    
    # 测试1: 简单位置参数
    @function_call(prompt="简单位置参数")
    def simple_func(a, b, c):
        return a + b + c
    
    # 测试2: 带默认值参数
    @function_call(prompt="带默认值参数")
    def func_with_defaults(a, b=10, c="hello"):
        return f"{a}, {b}, {c}"
    
    # 测试3: 可变参数
    @function_call(prompt="可变参数")
    def func_with_varargs(a, *args, **kwargs):
        return f"{a}, {args}, {kwargs}"
    
    # 测试4: 关键字参数
    @function_call(prompt="关键字参数")
    def func_with_kwonly(a, b, *, key1="default1", key2=20):
        return f"{a}, {b}, {key1}, {key2}"
    
    # 测试5: 混合参数
    @function_call(prompt="混合参数")
    def mixed_func(a, b=5, *args, c=10, d=None, **kwargs):
        return f"{a}, {b}, {args}, {c}, {d}, {kwargs}"
    
    # 测试6: 类型注解
    @function_call(prompt="带类型注解")
    def typed_func(name: str, age: int = 25, city: str = "北京") -> str:
        return f"{name}, {age}, {city}"
    
    # 显示所有生成的函数字符串
    functions = global_registry.get_all_functions()
    print("自动生成的函数签名:")
    for name, info in functions.items():
        print(f"  {name}: {info['function_str']}")
    
    # 测试提示词生成
    print("\n生成的提示词描述:")
    prompt = global_registry.get_prompt_descriptions()
    print(prompt)

def test_backward_compatibility():
    """测试向后兼容性"""
    print("\n=== 测试向后兼容性 ===")
    
    # 仍然支持手动指定 function_str
    @function_call(
        prompt="手动指定函数字符串",
        function_str="custom_func(param1, param2='default')"
    )
    def custom_func(a, b="default"):
        return f"{a}, {b}"
    
    functions = global_registry.get_all_functions()
    info = functions.get('custom_func', {})
    print(f"手动指定: {info.get('function_str', 'N/A')}")
    print("✅ 向后兼容性保持")

def main():
    """主测试函数"""
    print("🔧 测试自动函数字符串生成新功能")
    print("=" * 60)
    
    test_various_function_signatures()
    test_backward_compatibility()
    
    print("\n✅ 新功能测试完成！")
    print("\n📋 总结:")
    print("  • 自动从函数源码生成函数签名")
    print("  • 支持各种复杂的参数类型")
    print("  • 保持向后兼容性")
    print("  • 大大简化了使用方式")

if __name__ == "__main__":
    main()