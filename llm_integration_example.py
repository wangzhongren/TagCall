#!/usr/bin/env python3
"""
大模型集成示例 - 展示如何将 TagCall 用于大模型函数调用场景
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from tagcall import function_call, parse_function_calls, global_registry

# 注册一些实用的函数
@function_call(
    prompt="搜索网络信息",
    function_str='web_search(query)'
)
def web_search(query):
    """模拟网络搜索"""
    return f"关于 '{query}' 的搜索结果：相关文章1，相关文章2，相关文章3"

@function_call(
    prompt="计算器功能",
    function_str='calculator(expression)'
)
def calculator(expression):
    """简单计算器（注意：实际使用中应该安全地执行）"""
    try:
        # 注意：实际生产环境中应该使用更安全的表达式求值方式
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"

@function_call(
    prompt="获取当前时间",
    function_str='get_current_time()'
)
def get_current_time():
    """获取当前时间"""
    from datetime import datetime
    return f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@function_call(
    prompt="文件操作 - 读取文件",
    function_str='read_file(filename)'
)
def read_file(filename):
    """读取文件内容（模拟）"""
    return f"文件 '{filename}' 的内容：[模拟的文件内容]"

class LLMAssistant:
    """模拟大模型助手"""
    
    def __init__(self):
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """构建系统提示词，包含可用的函数"""
        base_prompt = """你是一个智能助手，可以调用以下函数来帮助用户：

可用函数：
{functions}

当需要调用函数时，请使用以下格式：
<function-call>
function_name(arg1, arg2, ...);
another_function(param1, param2);
</function-call>

请根据用户需求选择合适的函数进行调用。"""
        
        functions_desc = global_registry.get_prompt_descriptions()
        return base_prompt.format(functions=functions_desc)
    
    def process_user_query(self, user_input):
        """处理用户查询"""
        print(f"用户输入: {user_input}")
        print(f"系统提示词: {self.system_prompt[:200]}...")
        print()
        
        # 模拟大模型响应（在实际应用中，这里会调用大模型API）
        # 这里我们模拟大模型识别需要函数调用的场景
        if "搜索" in user_input or "查找" in user_input:
            query = user_input.replace("搜索", "").replace("查找", "").strip()
            model_response = f'''
根据您的需求，我将搜索相关信息：
<function-call>
web_search("{query}");
</function-call>
'''
        elif "计算" in user_input:
            # 提取计算表达式
            expression = user_input.replace("计算", "").strip()
            model_response = f'''
我将为您计算：
<function-call>
calculator("{expression}");
</function-call>
'''
        elif "时间" in user_input:
            model_response = f'''
我将获取当前时间：
<function-call>
get_current_time();
</function-call>
'''
        else:
            model_response = "我暂时无法处理这个请求。"
        
        return model_response
    
    def execute_function_calls(self, response_text):
        """执行响应中的函数调用"""
        calls = parse_function_calls(response_text)
        results = []
        
        for call in calls:
            print(f"执行函数调用: {call}")
            try:
                result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
                results.append(result)
                print(f"执行结果: {result}")
            except Exception as e:
                error_msg = f"执行 {call['name']} 时出错: {e}"
                results.append(error_msg)
                print(error_msg)
        
        return results

def main():
    """主函数"""
    assistant = LLMAssistant()
    
    # 测试用例
    test_queries = [
        "搜索人工智能的最新发展",
        "计算 123 * 456 + 789",
        "现在是什么时间？",
        "请帮我查找Python编程教程"
    ]
    
    for query in test_queries:
        print("=" * 60)
        print(f"处理查询: {query}")
        print("-" * 40)
        
        # 模拟大模型响应
        model_response = assistant.process_user_query(query)
        print(f"模型响应:\n{model_response}")
        
        # 执行函数调用
        if "<function-call>" in model_response:
            print("\n执行函数调用:")
            results = assistant.execute_function_calls(model_response)
            print(f"\n最终结果: {results}")
        
        print()

if __name__ == "__main__":
    main()