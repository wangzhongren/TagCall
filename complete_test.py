#!/usr/bin/env python3
"""完整项目测试"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔧 {description}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    """运行完整测试套件"""
    print("🧪 TagCall 完整项目测试")
    print("=" * 60)
    
    tests = [
        ("python example_usage.py", "基础使用示例"),
        ("python demo.py", "完整功能演示"), 
        ("python final_verification.py", "最终验证"),
        ("python test_beautifulsoup.py", "BeautifulSoup 测试"),
        ("python verify_beautifulsoup.py", "BeautifulSoup 验证")
    ]
    
    success_count = 0
    for command, description in tests:
        if run_command(command, description):
            success_count += 1
            print("✅ 通过")
        else:
            print("❌ 失败")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {success_count}/{len(tests)} 通过")
    
    if success_count == len(tests):
        print("\n🎉 所有测试通过！TagCall 项目完全就绪！")
        print("\n📁 项目结构:")
        for root, dirs, files in os.walk("."):
            level = root.replace(".", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files:
                if file.endswith(('.py', '.md')) and not file.startswith('.'):
                    print(f"{subindent}{file}")
    else:
        print("\n⚠️ 部分测试失败，请检查相关问题")

if __name__ == "__main__":
    main()