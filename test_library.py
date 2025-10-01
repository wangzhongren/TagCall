#!/usr/bin/env python3
"""
测试 TagCall 库的完整功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, parse_function_calls, global_registry

# 测试函数注册
@function_call(
    prompt="获取城市天气信息",
    function_str='get_weather(city)'
)
def get_weather(city):
    """模拟天气查询"""
    return f"{city}的天气：晴，25°C，湿度60%"

@function_call(
    prompt="计算两个数字的加法",
    function_str='add(a, b)'
)
def add(a, b):
    """加法计算"""
    return a + b

@function_call(
    prompt="发送电子邮件",
    function_str='send_email(to, subject, body)'
)
def send_email(to, subject="无主题", body=""):
    """邮件发送函数"""
    return f"邮件已发送到 {to}，主题：{subject}"

def test_function_registration():
    """测试函数注册功能"""
    print("=== 测试函数注册 ===")
    functions = global_registry.get_all_functions()
    print(f"注册的函数数量: {len(functions)}")
    
    for name, info in functions.items():
        print(f"函数名: {name}")
        print(f"  提示词: {info['prompt']}")
        print(f"  函数字符串: {info['function_str']}")
        print(f"  函数对象: {info['function']}")
    print()

def test_prompt_generation():
    """测试提示词生成"""
    print("=== 测试提示词生成 ===")
    prompt_text = global_registry.get_prompt_descriptions()
    print("生成的提示词:")
    print(prompt_text)
    print()

def test_function_parsing():
    """测试函数调用解析"""
    print("=== 测试函数调用解析 ===")
    
    # 测试用例1：标准函数调用
    test_text1 = '''
用户需要执行以下操作：
<function-call>
get_weather("上海");
add(5, 10);
send_email("test@example.com", "Hello", "This is a test email");
</function-call>
请完成这些操作。
'''
    
    print("测试文本1:")
    print(test_text1)
    
    calls1 = parse_function_calls(test_text1)
    print(f"解析出的函数调用: {len(calls1)} 个")
    
    for i, call in enumerate(calls1, 1):
        print(f"调用 {i}: {call}")
        try:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            print(f"  执行结果: {result}")
        except Exception as e:
            print(f"  执行错误: {e}")
    print()
    
    # 测试用例2：带关键字参数的调用
    test_text2 = '''
<function-call>
send_email(to="user@test.com", subject="重要通知", body="请查收重要文件");
add(3 + 7);
</function-call>
'''
    
    print("测试文本2:")
    print(test_text2)
    
    calls2 = parse_function_calls(test_text2)
    for i, call in enumerate(calls2, 1):
        print(f"调用 {i}: {call}")
        try:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            print(f"  执行结果: {result}")
        except Exception as e:
            print(f"  执行错误: {e}")
    print()

def test_error_handling():
    """测试错误处理"""
    print("=== 测试错误处理 ===")
    
    # 测试未注册的函数
    test_text = '''
<function-call>
unknown_function("test");
</function-call>
'''
    
    calls = parse_function_calls(test_text)
    for call in calls:
        print(f"尝试调用未注册函数: {call}")
        try:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            print(f"  执行结果: {result}")
        except Exception as e:
            print(f"  预期错误: {e}")
    print()

def main():
    """主测试函数"""
    print("TagCall 库功能测试")
    print("=" * 50)
    
    test_function_registration()
    test_prompt_generation()
    test_function_parsing()
    test_error_handling()
    
    print("测试完成！")

if __name__ == "__main__":
    main()