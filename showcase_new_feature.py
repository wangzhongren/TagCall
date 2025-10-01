#!/usr/bin/env python3
"""展示自动函数字符串生成新功能"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, global_registry

def showcase_auto_generation():
    """展示自动生成功能"""
    print("🎯 TagCall 自动函数字符串生成展示")
    print("=" * 60)
    
    print("现在只需要写提示词，函数签名自动生成！")
    print()
    
    # 展示各种函数定义
    print("1. 📝 简单位置参数")
    @function_call(prompt="计算三个数的和")
    def calculate_sum(a, b, c):
        return a + b + c
    
    print("2. 📝 带默认值的参数")
    @function_call(prompt="创建用户信息")
    def create_user(name, age=25, city="北京"):
        return f"用户: {name}, 年龄: {age}, 城市: {city}"
    
    print("3. 📝 可变参数")
    @function_call(prompt="处理多个数据")
    def process_data(base, *values, **options):
        return f"基础: {base}, 值: {values}, 选项: {options}"
    
    print("4. 📝 关键字参数")
    @function_call(prompt="配置系统参数")
    def configure_system(host, port, *, timeout=30, retries=3):
        return f"主机: {host}, 端口: {port}, 超时: {timeout}, 重试: {retries}"
    
    print("5. 📝 复杂混合参数")
    @function_call(prompt="复杂业务逻辑")
    def complex_business(name, count=1, *items, category="default", **settings):
        return f"名称: {name}, 数量: {count}, 项目: {items}, 分类: {category}, 设置: {settings}"
    
    print("6. 📝 带类型注解")
    @function_call(prompt="类型安全的函数")
    def typed_function(username: str, user_id: int, is_active: bool = True) -> dict:
        return {
            "username": username,
            "user_id": user_id,
            "is_active": is_active
        }
    
    print("\n" + "=" * 60)
    print("🎉 自动生成的函数签名:")
    print("=" * 60)
    
    functions = global_registry.get_all_functions()
    for name, info in functions.items():
        print(f"🔹 {name}: {info['function_str']}")
        print(f"   提示词: {info['prompt']}")
        print()
    
    print("=" * 60)
    print("📋 生成的系统提示词:")
    print("=" * 60)
    
    prompt = global_registry.get_prompt_descriptions()
    print(prompt)

def demonstrate_usage():
    """演示使用方式"""
    print("\n" + "=" * 60)
    print("🚀 实际使用演示")
    print("=" * 60)
    
    # 演示函数执行
    print("执行函数调用:")
    
    # 测试各种调用方式
    test_cases = [
        ("calculate_sum(1, 2, 3)", ["calculate_sum", [1, 2, 3], {}]),
        ("create_user('张三')", ["create_user", ["张三"], {}]),
        ("create_user('李四', 30, '上海')", ["create_user", ["李四", 30, "上海"], {}]),
        ("configure_system('localhost', 8080, timeout=60)", ["configure_system", ["localhost", 8080], {"timeout": 60}]),
        ("complex_business('项目A', 5, 'item1', 'item2', category='重要', priority='高')", 
         ["complex_business", ["项目A", 5, "item1", "item2"], {"category": "重要", "priority": "高"}])
    ]
    
    for call_desc, (func_name, args, kwargs) in test_cases:
        print(f"\n📞 调用: {call_desc}")
        try:
            result = global_registry.execute_function(func_name, *args, **kwargs)
            print(f"✅ 结果: {result}")
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    showcase_auto_generation()
    demonstrate_usage()
    
    print("\n" + "🎊" * 20)
    print("🎊 TagCall 自动生成功能展示完成 🎊")
    print("🎊" * 20)
    print("\n💡 总结:")
    print("  • 无需手动编写 function_str")
    print("  • 自动从函数源码生成准确签名")
    print("  • 支持所有 Python 参数类型")
    print("  • 大大简化开发体验")