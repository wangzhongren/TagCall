#!/usr/bin/env python3
"""
TagCall 库完整演示
展示如何在大模型场景中使用函数调用功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, parse_function_calls, global_registry

# 1. 注册各种实用函数
@function_call(
    prompt="获取城市天气信息",
    function_str="get_weather(city)"
)
def get_weather(city):
    """模拟天气查询"""
    weather_data = {
        "北京": "晴，25°C",
        "上海": "多云，23°C", 
        "广州": "雨，28°C",
        "深圳": "晴，30°C"
    }
    return weather_data.get(city, f"未找到{city}的天气信息")

@function_call(
    prompt="计算数学表达式",
    function_str="calculate(expression)"
)
def calculate(expression):
    """安全计算数学表达式"""
    try:
        # 在实际应用中应该使用更安全的表达式求值
        allowed_chars = set('0123456789+-*/.() ')
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"{expression} = {result}"
        else:
            return "表达式包含不安全字符"
    except Exception as e:
        return f"计算错误: {e}"

@function_call(
    prompt="查询股票价格",
    function_str="get_stock_price(symbol)"
)
def get_stock_price(symbol):
    """模拟股票查询"""
    stock_prices = {
        "AAPL": 185.25,
        "GOOGL": 138.75,
        "TSLA": 245.60,
        "MSFT": 378.85
    }
    price = stock_prices.get(symbol.upper())
    if price:
        return f"{symbol} 当前价格: ${price}"
    else:
        return f"未找到股票 {symbol} 的信息"

@function_call(
    prompt="翻译文本",
    function_str="translate(text, target_language='英文')"
)
def translate(text, target_language="英文"):
    """模拟翻译功能"""
    translations = {
        "英文": f"Translation: {text}",
        "中文": f"翻译：{text}",
        "日文": f"翻訳：{text}"
    }
    return translations.get(target_language, f"不支持{target_language}翻译")

class AIAssistant:
    """AI助手类，模拟大模型集成"""
    
    def __init__(self):
        self.available_functions = global_registry.get_prompt_descriptions()
    
    def build_system_prompt(self):
        """构建系统提示词"""
        return f"""你是一个智能AI助手，可以调用以下工具函数来帮助用户：

可用的工具函数：
{self.available_functions}

当用户请求需要调用函数时，请使用以下格式响应：
<function-call>
function_name(argument1, argument2, ...);
another_function(param1=value1, param2=value2);
</function-call>

请根据用户需求选择合适的函数进行调用。"""
    
    def simulate_ai_response(self, user_input):
        """模拟AI响应（在实际应用中这里会调用大模型API）"""
        print(f"🤖 系统提示词预览:")
        print(self.build_system_prompt()[:300] + "...")
        print(f"\n👤 用户输入: {user_input}")
        
        # 基于用户输入的简单规则模拟AI响应
        if "天气" in user_input:
            city = user_input.replace("天气", "").strip() or "北京"
            return f'''
根据您的查询，我将获取{city}的天气信息：
<function-call>
get_weather("{city}");
</function-call>
'''
        elif "计算" in user_input or "等于" in user_input:
            expr = user_input.replace("计算", "").replace("等于", "").strip()
            return f'''
我将为您计算表达式：
<function-call>
calculate("{expr}");
</function-call>
'''
        elif "股票" in user_input or "股价" in user_input:
            symbol = "".join([c for c in user_input if c.isalpha()]).upper() or "AAPL"
            return f'''
查询股票价格：
<function-call>
get_stock_price("{symbol}");
</function-call>
'''
        elif "翻译" in user_input:
            text = user_input.replace("翻译", "").strip()
            return f'''
翻译文本：
<function-call>
translate("{text}");
</function-call>
'''
        else:
            return "我暂时无法处理这个请求，请尝试询问天气、计算、股票或翻译相关的问题。"
    
    def process_response(self, response):
        """处理AI响应，执行函数调用"""
        print(f"\n🤖 AI响应:\n{response}")
        
        if "<function-call>" in response:
            print("\n🔧 执行函数调用:")
            calls = parse_function_calls(response)
            
            results = []
            for call in calls:
                print(f"  调用: {call['name']}{call['args']} {call['kwargs']}")
                try:
                    result = global_registry.execute_function(
                        call['name'], 
                        *call['args'], 
                        **call['kwargs']
                    )
                    print(f"  ✅ 结果: {result}")
                    results.append(result)
                except Exception as e:
                    error_msg = f"  ❌ 错误: {e}"
                    print(error_msg)
                    results.append(error_msg)
            
            return results
        return []

def main():
    """主演示函数"""
    print("🚀 TagCall 库演示")
    print("=" * 50)
    
    # 初始化AI助手
    assistant = AIAssistant()
    
    # 演示用例
    demo_cases = [
        "北京天气怎么样？",
        "计算 125 * 8 + 300",
        "苹果公司股价",
        "翻译'你好世界'成英文",
        "今天深圳的天气",
        "计算 (15 + 25) * 3 / 2"
    ]
    
    for i, user_input in enumerate(demo_cases, 1):
        print(f"\n{'='*60}")
        print(f"案例 {i}: {user_input}")
        print('-'*60)
        
        # 模拟AI响应
        ai_response = assistant.simulate_ai_response(user_input)
        
        # 执行函数调用
        results = assistant.process_response(ai_response)
        
        if results:
            print(f"\n📊 最终答案: {results[0] if len(results) == 1 else results}")
    
    print(f"\n{'='*60}")
    print("🎉 演示完成！")
    print(f"📚 当前注册的函数: {list(global_registry.get_all_functions().keys())}")

if __name__ == "__main__":
    main()