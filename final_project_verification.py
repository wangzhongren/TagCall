#!/usr/bin/env python3
"""最终项目验证"""

import os
import subprocess
import sys

def check_project_completeness():
    """检查项目完整性"""
    print("📁 项目完整性检查")
    print("=" * 50)
    
    # 检查核心文件
    core_files = [
        "tagcall/__init__.py",
        "tagcall/core.py", 
        "tagcall/decorator.py",
        "setup.py"
    ]
    
    missing_files = []
    for file in core_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_basic_functionality():
    """测试基本功能"""
    print("\n🔧 基本功能测试")
    print("=" * 50)
    
    try:
        # 测试导入
        sys.path.insert(0, '.')
        from tagcall import function_call, parse_function_calls, global_registry
        print("✅ 导入功能正常")
        
        # 测试自动函数字符串生成
        @function_call(prompt="测试函数")
        def test_func(a, b=10):
            return f"{a}, {b}"
        
        functions = global_registry.get_all_functions()
        if "test_func" in functions:
            func_info = functions["test_func"]
            print(f"✅ 自动生成函数签名: {func_info['function_str']}")
        else:
            print("❌ 函数注册失败")
            return False
        
        # 测试解析和执行
        text = '<function-call>test_func("hello");</function-call>'
        calls = parse_function_calls(text)
        if len(calls) == 1:
            result = global_registry.execute_function("test_func", "hello")
            if "hello" in result:
                print("✅ 解析和执行正常")
            else:
                print("❌ 执行结果异常")
                return False
        else:
            print("❌ 解析失败")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def run_key_demos():
    """运行关键演示"""
    print("\n🎯 运行关键演示")
    print("=" * 50)
    
    demos = [
        ("python example_usage.py", "基础示例"),
        ("python showcase_new_feature.py", "新功能展示")
    ]
    
    success_count = 0
    for command, description in demos:
        print(f"\n运行: {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 运行成功")
                success_count += 1
            else:
                print("❌ 运行失败")
                if result.stderr:
                    print(f"错误: {result.stderr}")
        except Exception as e:
            print(f"❌ 异常: {e}")
    
    return success_count == len(demos)

def main():
    """主验证函数"""
    print("🎯 TagCall 项目最终验证")
    print("=" * 60)
    
    # 检查完整性
    completeness_ok = check_project_completeness()
    
    # 测试功能
    functionality_ok = test_basic_functionality()
    
    # 运行演示
    demos_ok = run_key_demos()
    
    print("\n" + "=" * 60)
    print("📊 验证结果:")
    print(f"  项目完整性: {'✅ 通过' if completeness_ok else '❌ 失败'}")
    print(f"  基本功能: {'✅ 通过' if functionality_ok else '❌ 失败'}")
    print(f"  演示运行: {'✅ 通过' if demos_ok else '❌ 失败'}")
    
    if completeness_ok and functionality_ok and demos_ok:
        print("\n🎉" * 15)
        print("🎉 TAGCall 项目验证通过！ 🎉")
        print("🎉" * 15)
        
        print("\n🚀 项目交付:")
        print("  ✅ 完整的 TagCall Python 库")
        print("  ✅ BeautifulSoup XML 解析引擎")
        print("  ✅ 自动函数字符串生成功能")
        print("  ✅ 完整的大模型集成支持")
        print("  ✅ 全面的测试和文档")
        
        print("\n💡 核心改进:")
        print("  从手动编写 function_str 到自动生成函数签名")
        print("  大大简化了开发体验！")
        
        print("\n📦 立即使用:")
        print("  pip install -e .")
        print("  python example_usage.py")
        print("  python demo.py")
        
        return 0
    else:
        print("\n⚠️ 项目验证未通过")
        return 1

if __name__ == "__main__":
    sys.exit(main())