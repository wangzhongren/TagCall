#!/usr/bin/env python3
"""
测试 BeautifulSoup 版本的 TagCall 解析功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, parse_function_calls, global_registry

# 注册测试函数
@function_call(
    prompt="测试函数1",
    function_str="test_func1(arg1, arg2)"
)
def test_func1(arg1, arg2):
    return f"func1: {arg1}, {arg2}"

@function_call(
    prompt="测试函数2",
    function_str="test_func2(name, age=0)"
)
def test_func2(name, age=0):
    return f"func2: {name}, {age}岁"

def test_beautifulsoup_parsing():
    """测试 BeautifulSoup 解析功能"""
    print("=== BeautifulSoup 解析测试 ===")
    
    # 测试用例1：标准格式
    test_cases = [
        # 标准格式
        '''
        <function-call>
        test_func1("hello", "world");
        test_func2("Alice", age=25);
        </function-call>
        ''',
        
        # 包含HTML注释和杂项内容
        '''
        这是一些文本
        <!-- 这是一个注释 -->
        <function-call>
        test_func1("value1", "value2");
        </function-call>
        更多文本内容
        ''',
        
        # 多个function-call标签
        '''
        <function-call>
        test_func1("first", "call");
        </function-call>
        中间内容
        <function-call>
        test_func2("Bob");
        </function-call>
        ''',
        
        # 包含特殊字符
        '''
        <function-call>
        test_func1("hello<world>", "test&value");
        test_func2(name="John&Doe");
        </function-call>
        ''',
        
        # 嵌套在其他HTML中
        '''
        <html>
        <body>
            <div>
                <function-call>
                test_func1("nested", "value");
                </function-call>
            </div>
        </body>
        </html>
        ''',
        
        # 空标签和无效内容
        '''
        <function-call></function-call>
        <function-call>
        invalid_function();
        </function-call>
        '''
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"输入文本: {test_case.strip()[:100]}...")
        
        calls = parse_function_calls(test_case)
        print(f"解析出的调用数量: {len(calls)}")
        
        for j, call in enumerate(calls, 1):
            print(f"  调用 {j}: {call}")
            try:
                result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
                print(f"    执行结果: {result}")
            except Exception as e:
                print(f"    执行错误: {e}")

def test_robustness():
    """测试解析的健壮性"""
    print("\n=== 健壮性测试 ===")
    
    edge_cases = [
        # 不完整的标签
        '<function-call>test_func1("hello")',
        'test_func1("hello")</function-call>',
        
        # 错误的标签
        '<function_call>test_func1("hello");</function_call>',
        '<FUNCTION-CALL>test_func1("hello");</FUNCTION-CALL>',
        
        # 空内容
        '',
        '    ',
        '<function-call>   </function-call>',
        
        # 包含换行和空格
        '''
        <function-call>
        
        
        test_func1("hello", "world");
        
        
        </function-call>
        ''',
        
        # 混合内容
        '''
        开始<function-call>test_func1("mixed", "content");</function-call>结束
        '''
    ]
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"\n边界用例 {i}:")
        calls = parse_function_calls(test_case)
        print(f"  解析结果: {len(calls)} 个调用")
        for call in calls:
            print(f"    {call}")

def main():
    """主测试函数"""
    print("BeautifulSoup 版本 TagCall 测试")
    print("=" * 50)
    
    test_beautifulsoup_parsing()
    test_robustness()
    
    print("\n✅ BeautifulSoup 版本测试完成！")

if __name__ == "__main__":
    main()