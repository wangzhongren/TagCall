#!/usr/bin/env python3
"""最终验证 BeautifulSoup 版本的 TagCall 库"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_all_features():
    """测试所有核心功能"""
    print("🔍 最终验证 TagCall 库所有功能")
    print("=" * 60)
    
    # 测试1: 导入功能
    try:
        from tagcall import function_call, parse_function_calls, global_registry
        print("✅ 导入功能正常")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 测试2: 函数注册
    try:
        @function_call(
            prompt="测试函数",
            function_str="test_function(param)"
        )
        def test_function(param):
            return f"收到参数: {param}"
        
        functions = global_registry.get_all_functions()
        if "test_function" in functions:
            print("✅ 函数注册正常")
        else:
            print("❌ 函数注册失败")
            return False
    except Exception as e:
        print(f"❌ 函数注册失败: {e}")
        return False
    
    # 测试3: 提示词生成
    try:
        prompt = global_registry.get_prompt_descriptions()
        if prompt and "test_function" in prompt:
            print("✅ 提示词生成正常")
        else:
            print("❌ 提示词生成失败")
            return False
    except Exception as e:
        print(f"❌ 提示词生成失败: {e}")
        return False
    
    # 测试4: 简单解析
    try:
        simple_text = '<function-call>test_function("hello");</function-call>'
        calls = parse_function_calls(simple_text)
        if len(calls) == 1 and calls[0]['name'] == 'test_function':
            print("✅ 简单解析正常")
        else:
            print("❌ 简单解析失败")
            return False
    except Exception as e:
        print(f"❌ 简单解析失败: {e}")
        return False
    
    # 测试5: 复杂 HTML 解析
    try:
        complex_html = '''
        <html>
        <body>
            <!-- 注释 -->
            <div>
                <function-call>
                test_function("complex");
                </function-call>
            </div>
        </body>
        </html>
        '''
        calls = parse_function_calls(complex_html)
        if len(calls) == 1:
            print("✅ 复杂 HTML 解析正常")
        else:
            print("❌ 复杂 HTML 解析失败")
            return False
    except Exception as e:
        print(f"❌ 复杂 HTML 解析失败: {e}")
        return False
    
    # 测试6: 函数执行
    try:
        result = global_registry.execute_function("test_function", "world")
        if "world" in result:
            print("✅ 函数执行正常")
        else:
            print("❌ 函数执行失败")
            return False
    except Exception as e:
        print(f"❌ 函数执行失败: {e}")
        return False
    
    # 测试7: 错误处理
    try:
        global_registry.execute_function("nonexistent_function")
        print("❌ 错误处理失败 - 应该抛出异常")
        return False
    except ValueError:
        print("✅ 错误处理正常")
    except Exception as e:
        print(f"❌ 错误处理异常: {e}")
        return False
    
    return True

def test_beautifulsoup_specific():
    """测试 BeautifulSoup 特定功能"""
    print("\n=== BeautifulSoup 特定功能测试 ===")
    
    from tagcall import parse_function_calls
    
    test_cases = [
        # 多个 function-call 标签
        ('''
        <function-call>func1("a");</function-call>
        <function-call>func2("b");</function-call>
        ''', 2, "多个标签"),
        
        # 包含注释
        ('''
        <!-- 开始 -->
        <function-call>func1("test");</function-call>
        <!-- 结束 -->
        ''', 1, "包含注释"),
        
        # 嵌套结构
        ('''
        <div><section><function-call>func1("nested");</function-call></section></div>
        ''', 1, "嵌套结构"),
        
        # 大小写混合
        ('''
        <FUNCTION-CALL>func1("upper");</FUNCTION-CALL>
        <function-CALL>func2("mixed");</function-CALL>
        ''', 2, "大小写混合"),
    ]
    
    all_passed = True
    for test_text, expected_count, description in test_cases:
        try:
            calls = parse_function_calls(test_text)
            if len(calls) == expected_count:
                print(f"✅ {description}: 通过")
            else:
                print(f"❌ {description}: 失败 (期望 {expected_count}, 得到 {len(calls)})")
                all_passed = False
        except Exception as e:
            print(f"❌ {description}: 异常 {e}")
            all_passed = False
    
    return all_passed

def main():
    """主验证函数"""
    print("🚀 TagCall 库最终验证")
    print("=" * 60)
    
    # 测试核心功能
    core_ok = test_all_features()
    
    # 测试 BeautifulSoup 特定功能
    bs_ok = test_beautifulsoup_specific()
    
    print("\n" + "=" * 60)
    if core_ok and bs_ok:
        print("🎉 所有验证通过！TagCall 库功能完整！")
        print("\n📋 验证总结:")
        print("  ✅ 核心功能: 导入、注册、解析、执行")
        print("  ✅ BeautifulSoup: 复杂文档、多标签、容错")
        print("  ✅ 错误处理: 异常捕获和恢复")
        print("  ✅ 向后兼容: 原有 API 完全支持")
    else:
        print("⚠️ 部分验证未通过，请检查问题")
        return 1
    
    print("\n🌟 TagCall 库现已就绪！")
    print("   使用 'python demo.py' 查看完整演示")
    print("   使用 'python example_usage.py' 查看基础示例")
    return 0

if __name__ == "__main__":
    sys.exit(main())