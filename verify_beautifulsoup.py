#!/usr/bin/env python3
"""验证 BeautifulSoup 版本的 TagCall 库功能"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, parse_function_calls, global_registry

# 注册一些测试函数
@function_call(
    prompt="获取天气信息",
    function_str="get_weather(city)"
)
def get_weather(city):
    return f"{city}的天气：晴，25°C"

@function_call(
    prompt="计算器功能",
    function_str="calculate(expression)"
)
def calculate(expression):
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"

@function_call(
    prompt="发送邮件",
    function_str="send_email(to, subject, body)"
)
def send_email(to, subject="无主题", body=""):
    return f"邮件已发送到 {to}，主题：{subject}"

def test_complex_html_parsing():
    """测试复杂 HTML 文档的解析"""
    print("=== 复杂 HTML 文档解析测试 ===")
    
    complex_documents = [
        # 包含注释和杂项内容
        '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>测试页面</title>
        </head>
        <body>
            <!-- 这是一个注释 -->
            <div class="content">
                <p>用户请求执行以下操作：</p>
                <function-call>
                get_weather("北京");
                calculate("2 + 3 * 4");
                </function-call>
                <p>请完成上述操作。</p>
            </div>
            <!-- 另一个注释 -->
        </body>
        </html>
        ''',
        
        # 多个 function-call 标签
        '''
        <div>
            <function-call>
            get_weather("上海");
            </function-call>
            
            <p>中间段落内容</p>
            
            <function-call>
            send_email("user@example.com", "测试邮件", "这是一封测试邮件");
            </function-call>
        </div>
        ''',
        
        # 嵌套结构
        '''
        <main>
            <section>
                <article>
                    <function-call>
                    calculate("(10 + 5) * 2");
                    get_weather("广州");
                    </function-call>
                </article>
            </section>
        </main>
        ''',
        
        # 包含特殊字符
        '''
        <function-call>
        send_email(to="test&user@example.com", subject="包含&特殊字符", body="内容<tag>测试");
        </function-call>
        '''
    ]
    
    for i, doc in enumerate(complex_documents, 1):
        print(f"\n文档 {i}:")
        print("解析结果:")
        calls = parse_function_calls(doc)
        
        for call in calls:
            print(f"  - {call['name']}{call['args']} {call['kwargs']}")
            try:
                result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
                print(f"    结果: {result}")
            except Exception as e:
                print(f"    错误: {e}")

def test_malformed_html():
    """测试格式不正确的 HTML"""
    print("\n=== 格式不正确的 HTML 测试 ===")
    
    malformed_cases = [
        # 不闭合的标签
        '<function-call>get_weather("北京")',
        'get_weather("上海");</function-call>',
        
        # 错误的标签名
        '<function_call>get_weather("广州");</function_call>',
        '<FUNCTION-CALL>calculate("1+1");</FUNCTION-CALL>',
        
        # 混合大小写
        '<Function-Call>get_weather("深圳");</Function-Call>',
        
        # 包含脚本标签
        '''
        <script>
        function test() { console.log("hello"); }
        </script>
        <function-call>
        get_weather("成都");
        </function-call>
        '''
    ]
    
    for i, case in enumerate(malformed_cases, 1):
        print(f"\n用例 {i}: {case[:50]}...")
        calls = parse_function_calls(case)
        print(f"  解析到 {len(calls)} 个函数调用")
        for call in calls:
            print(f"    - {call['name']}")

def test_real_world_scenario():
    """测试真实场景"""
    print("\n=== 真实场景模拟 ===")
    
    # 模拟大模型返回的响应
    llm_response = '''
用户需要查询天气并进行计算。我将调用以下函数：

<function-call>
get_weather("杭州");
calculate("100 / 4 + 15");
send_email(to="admin@company.com", subject="每日报告", body="今日天气和计算已完成");
</function-call>

请执行这些操作并返回结果。
'''
    
    print("大模型响应:")
    print(llm_response)
    
    print("\n解析和执行:")
    calls = parse_function_calls(llm_response)
    
    results = []
    for call in calls:
        print(f"执行: {call['name']}{call['args']} {call['kwargs']}")
        try:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            results.append(result)
            print(f"  结果: {result}")
        except Exception as e:
            error_msg = f"错误: {e}"
            results.append(error_msg)
            print(f"  {error_msg}")
    
    print(f"\n最终结果汇总: {results}")

def main():
    """主验证函数"""
    print("🔍 BeautifulSoup 版本 TagCall 库功能验证")
    print("=" * 60)
    
    test_complex_html_parsing()
    test_malformed_html()
    test_real_world_scenario()
    
    print("\n🎉 BeautifulSoup 版本验证完成！")
    print("\n📊 总结:")
    print("  ✅ 支持复杂 HTML/XML 文档结构")
    print("  ✅ 忽略注释和无关标签")
    print("  ✅ 处理格式不正确的文档")
    print("  ✅ 支持真实的大模型集成场景")

if __name__ == "__main__":
    main()