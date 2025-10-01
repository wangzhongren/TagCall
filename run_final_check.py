#!/usr/bin/env python3
"""运行最终项目检查"""

import subprocess
import sys

def run_final_check():
    """运行最终检查"""
    print("🔍 TagCall 项目最终检查")
    print("=" * 60)
    
    try:
        # 运行最终检查
        result = subprocess.run([sys.executable, "final_check.py"], 
                              capture_output=True, text=True)
        
        print("检查结果:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        print("=" * 60)
        if result.returncode == 0:
            print("🎊" * 20)
            print("🎊 TAGCall 项目开发圆满完成！ 🎊")
            print("🎊" * 20)
            
            print("\n📦 项目交付物:")
            print("  ✅ 核心库代码 (tagcall/)")
            print("  ✅ 完整示例和演示 (5个文件)")
            print("  ✅ 全面测试套件 (6个文件)") 
            print("  ✅ 详细文档 (5个文件)")
            print("  ✅ 运行脚本 (5个文件)")
            print("  ✅ 打包配置 (setup.py)")
            
            print("\n💡 核心特性:")
            print("  • BeautifulSoup 驱动的 XML 解析")
            print("  • 装饰器模式的函数注册")
            print("  • 大模型函数调用集成")
            print("  • 工业级的错误处理")
            print("  • 完整的向后兼容")
            
            print("\n🚀 开始使用:")
            print("  python example_usage.py  # 基础示例")
            print("  python demo.py           # 完整演示")
            print("  pip install -e .        # 安装为包")
            
        else:
            print("❌ 项目检查未通过")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行检查时出错: {e}")
        return False

if __name__ == "__main__":
    success = run_final_check()
    
    if success:
        print("\n🎯 项目目标达成:")
        print("  ✓ 支持 TagCall 函数调用解析")
        print("  ✓ 使用 BeautifulSoup 提供健壮解析")
        print("  ✓ 实现函数注册和装饰器系统")
        print("  ✓ 提供大模型集成方案")
        print("  ✓ 创建完整测试和文档")
        
        print("\n🌟 TagCall 现已准备好为您的 AI 项目服务！")
    else:
        print("\n⚠️ 需要进一步检查和修复")