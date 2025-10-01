#!/usr/bin/env python3
"""
TagCall 库使用示例 - 自动生成函数字符串版本
"""

from tagcall import function_call, parse_function_calls, global_registry

# 注册函数示例 - 不再需要手动写 function_str!
@function_call(prompt="获取指定城市的天气信息")
def get_weather(city: str):
    """模拟获取天气的函数"""
    return f"{city}的天气：晴，25°C"

@function_call(prompt="计算两个数字的和")
def add(a: int, b: int):
    """加法函数"""
    return a + b

@function_call(prompt="发送邮件到指定地址")
def send_email(to: str, subject: str = "无主题", body: str = ""):
    """模拟发送邮件"""
    return f"已发送邮件到 {to}，主题：{subject}"

@function_call(prompt="复杂参数示例")
def complex_function(name, age=25, *args, city="北京", **kwargs):
    """复杂参数函数"""
    return f"姓名: {name}, 年龄: {age}, 城市: {city}, 其他: {args}, {kwargs}"

def main():
    print("=== 注册的函数列表 ===")
    functions = global_registry.get_all_functions()
    for name, info in functions.items():
        print(f"{name}:")
        print(f"  提示词: {info['prompt']}")
        print(f"  函数签名: {info['function_str']}")  # 自动生成！
        print(f"  函数对象: {info['function']}")
    
    print("\n=== 自动生成的提示词描述 ===")
    prompt_desc = global_registry.get_prompt_descriptions()
    print(prompt_desc)
    
    print("\n=== 解析函数调用示例 ===")
    
    # 示例1：简单的函数调用
    text1 = '''
<function-call>
get_weather("北京");
add(1, 3);
send_email("user@example.com", subject="测试邮件");
complex_function("张三", 30, "额外参数", city="上海", custom="自定义");
</function-call>
'''
    print("示例1:")
    calls1 = parse_function_calls(text1)
    for call in calls1:
        print(f"解析到调用: {call}")
        try:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            print(f"执行结果: {result}")
        except Exception as e:
            print(f"执行错误: {e}")
    
    # 示例2：带关键字参数的调用
    text2 = '''
<function-call>
send_email(to="admin@company.com", subject="重要通知", body="请查收");
add(5, 7);
</function-call>
'''
    print("\n示例2:")
    calls2 = parse_function_calls(text2)
    for call in calls2:
        print(f"解析到调用: {call}")
        try:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            print(f"执行结果: {result}")
        except Exception as e:
            print(f"执行错误: {e}")

if __name__ == "__main__":
    main()