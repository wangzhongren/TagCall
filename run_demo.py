#!/usr/bin/env python3
"""运行 TagCall 演示"""

import subprocess
import sys

def run_demo():
    """运行演示脚本"""
    print("🚀 启动 TagCall 库演示")
    print("=" * 60)
    
    try:
        # 运行完整演示
        result = subprocess.run([sys.executable, "demo.py"], 
                              capture_output=True, text=True)
        
        print("演示输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ 演示运行成功！")
        else:
            print("❌ 演示运行失败！")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行演示时出错: {e}")
        return False

def run_basic_example():
    """运行基础示例"""
    print("\n" + "=" * 60)
    print("运行基础示例")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, "example_usage.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行基础示例时出错: {e}")
        return False

if __name__ == "__main__":
    success1 = run_demo()
    success2 = run_basic_example()
    
    if success1 and success2:
        print("\n🎉 所有测试和演示都成功完成！")
        print("\n📋 您可以：")
        print("  1. 查看 example_usage.py - 基础使用示例")
        print("  2. 查看 demo.py - 完整功能演示") 
        print("  3. 查看 test_library.py - 功能测试")
        print("  4. 查看 llm_integration_example.py - 大模型集成示例")
        print("  5. 阅读 README.md 和 INSTALL.md - 详细文档")
    else:
        print("\n⚠️ 部分测试未通过，请检查错误信息")