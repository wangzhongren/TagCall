#!/usr/bin/env python3
"""运行 BeautifulSoup 版本测试"""

import subprocess
import sys

def run_test():
    """运行测试脚本"""
    print("🚀 启动 BeautifulSoup 版本测试")
    print("=" * 60)
    
    try:
        # 运行 BeautifulSoup 测试
        result = subprocess.run([sys.executable, "test_beautifulsoup.py"], 
                              capture_output=True, text=True)
        
        print("测试输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ BeautifulSoup 版本测试成功！")
        else:
            print("❌ BeautifulSoup 版本测试失败！")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    
    if success:
        print("\n🎉 BeautifulSoup 版本 TagCall 库已就绪！")
        print("\n📋 主要改进：")
        print("  ✅ 使用 BeautifulSoup 替换正则表达式解析")
        print("  ✅ 支持复杂的 HTML/XML 文档结构")
        print("  ✅ 更好的错误处理和容错性")
        print("  ✅ 忽略注释和无关标签内容")
        print("\n💡 运行 'python test_beautifulsoup.py' 查看详细测试结果")
    else:
        print("\n⚠️ 测试未通过，请检查错误信息")