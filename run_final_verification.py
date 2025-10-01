#!/usr/bin/env python3
"""运行最终验证"""

import subprocess
import sys

def run_final_verification():
    """运行最终验证"""
    print("🔍 运行 TagCall 库最终验证")
    print("=" * 60)
    
    try:
        # 运行最终验证
        result = subprocess.run([sys.executable, "final_verification.py"], 
                              capture_output=True, text=True)
        
        print("验证输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        print("=" * 60)
        if result.returncode == 0:
            print("🎉 最终验证成功！TagCall 库完全就绪！")
            print("\n📁 项目文件结构:")
            print("  tagcall/           - 核心库")
            print("  *.py              - 各种示例和测试")
            print("  *.md              - 完整文档")
            print("\n🚀 快速开始:")
            print("  python example_usage.py  - 基础使用")
            print("  python demo.py           - 完整演示")
            print("  python test_beautifulsoup.py - 功能测试")
        else:
            print("❌ 最终验证失败！")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行验证时出错: {e}")
        return False

if __name__ == "__main__":
    success = run_final_verification()
    
    if success:
        print("\n💡 下一步:")
        print("  1. 查看 README.md 了解完整功能")
        print("  2. 查看 BEAUTIFULSOUP_UPGRADE.md 了解升级详情")
        print("  3. 运行示例代码体验功能")
        print("  4. 集成到您的大模型项目中！")
    else:
        print("\n⚠️ 请检查错误信息并修复问题")