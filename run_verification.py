#!/usr/bin/env python3
"""运行 BeautifulSoup 版本验证"""

import subprocess
import sys

def run_verification():
    """运行验证脚本"""
    print("🔍 验证 BeautifulSoup 版本 TagCall 库")
    print("=" * 60)
    
    try:
        # 运行验证脚本
        result = subprocess.run([sys.executable, "verify_beautifulsoup.py"], 
                              capture_output=True, text=True)
        
        print("验证输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ BeautifulSoup 版本验证成功！")
            return True
        else:
            print("❌ BeautifulSoup 版本验证失败！")
            return False
            
    except Exception as e:
        print(f"运行验证时出错: {e}")
        return False

if __name__ == "__main__":
    success = run_verification()
    
    if success:
        print("\n🎉 BeautifulSoup 版本 TagCall 库完全就绪！")
        print("\n🌟 主要特性:")
        print("  🛡️  使用 BeautifulSoup 提供工业级 HTML/XML 解析")
        print("  🔧 支持复杂文档结构和嵌套标签")
        print("  🎯 忽略注释、脚本等无关内容")
        print("  💪 处理格式不正确的文档")
        print("  🚀 完美适配大模型集成场景")
        print("\n📁 可用文件:")
        print("  - tagcall/core.py - BeautifulSoup 版本核心代码")
        print("  - test_beautifulsoup.py - 基础测试")
        print("  - verify_beautifulsoup.py - 完整功能验证")
        print("  - demo.py - 使用示例")
    else:
        print("\n⚠️ 验证过程中发现问题，请检查错误信息")