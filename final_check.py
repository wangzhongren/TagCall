#!/usr/bin/env python3
"""最终项目检查"""

import os
import subprocess
import sys

def check_all_files():
    """检查所有必要文件是否存在"""
    print("📁 项目文件完整性检查")
    print("=" * 50)
    
    required_files = [
        # 核心库
        "tagcall/__init__.py",
        "tagcall/core.py", 
        "tagcall/decorator.py",
        
        # 示例和演示
        "example_usage.py",
        "demo.py",
        "llm_integration_example.py",
        
        # 测试文件
        "test_library.py",
        "test_beautifulsoup.py",
        "verify_beautifulsoup.py",
        "final_verification.py",
        
        # 文档
        "README.md",
        "INSTALL.md",
        "QUICK_START.md", 
        "BEAUTIFULSOUP_UPGRADE.md",
        "PROJECT_SUMMARY.md",
        
        # 配置
        "setup.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def run_quick_test():
    """运行快速功能测试"""
    print("\n🔧 快速功能测试")
    print("=" * 50)
    
    try:
        # 测试基本导入
        sys.path.insert(0, '.')
        from tagcall import function_call, parse_function_calls, global_registry
        print("✅ 导入测试通过")
        
        # 测试函数注册
        @function_call(prompt="测试", function_str="test_func(param)")
        def test_func(param):
            return f"收到: {param}"
        
        # 测试解析
        text = '<function-call>test_func("hello");</function-call>'
        calls = parse_function_calls(text)
        if len(calls) == 1:
            print("✅ 解析测试通过")
        else:
            print("❌ 解析测试失败")
            return False
            
        # 测试执行
        result = global_registry.execute_function("test_func", "world")
        if "world" in result:
            print("✅ 执行测试通过")
        else:
            print("❌ 执行测试失败")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def main():
    """主检查函数"""
    print("🎯 TagCall 项目最终检查")
    print("=" * 50)
    
    # 检查文件完整性
    files_ok, missing = check_all_files()
    
    # 运行功能测试
    function_ok = run_quick_test()
    
    print("\n" + "=" * 50)
    print("📊 检查结果:")
    print(f"  文件完整性: {'✅ 通过' if files_ok else '❌ 失败'}")
    print(f"  功能测试: {'✅ 通过' if function_ok else '❌ 失败'}")
    
    if files_ok and function_ok:
        print("\n🎉 TagCall 项目开发完成！")
        print("\n🌟 项目特色:")
        print("  • 基于 BeautifulSoup 的健壮 XML 解析")
        print("  • 简洁的函数注册装饰器")
        print("  • 完整的大模型集成支持")
        print("  • 全面的测试和文档")
        
        print("\n🚀 下一步行动:")
        print("  1. 运行 'python demo.py' 查看完整演示")
        print("  2. 阅读 'QUICK_START.md' 快速上手")
        print("  3. 集成到您的 AI 项目中")
        print("  4. 分享和贡献代码！")
        
        return 0
    else:
        print("\n⚠️ 项目检查未通过")
        if not files_ok:
            print(f"  缺失文件: {missing}")
        return 1

if __name__ == "__main__":
    sys.exit(main())