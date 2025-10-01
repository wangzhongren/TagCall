#!/usr/bin/env python3
"""运行最终演示和验证"""

import subprocess
import sys

def run_demo():
    """运行新功能展示"""
    print("🚀 运行 TagCall 自动函数字符串生成展示")
    print("=" * 60)
    
    try:
        # 运行新功能展示
        result = subprocess.run([sys.executable, "showcase_new_feature.py"], 
                              capture_output=True, text=True)
        
        print("展示输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return "展示完成" in result.stdout
        
    except Exception as e:
        print(f"运行展示时出错: {e}")
        return False

def run_validation():
    """运行最终验证"""
    print("\n" + "=" * 60)
    print("🔍 运行最终验证")
    print("=" * 60)
    
    try:
        # 运行最终验证
        result = subprocess.run([sys.executable, "final_validation.py"], 
                              capture_output=True, text=True)
        
        print("验证输出:")
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        return "验证成功" in result.stdout
        
    except Exception as e:
        print(f"运行验证时出错: {e}")
        return False

def main():
    """主运行函数"""
    print("🎯 TagCall 项目最终演示和验证")
    print("=" * 60)
    
    # 运行展示
    demo_success = run_demo()
    
    # 运行验证
    validation_success = run_validation()
    
    print("\n" + "=" * 60)
    print("📊 最终结果:")
    print(f"  功能展示: {'✅ 成功' if demo_success else '❌ 失败'}")
    print(f"  功能验证: {'✅ 成功' if validation_success else '❌ 失败'}")
    
    if demo_success and validation_success:
        print("\n🎉" * 15)
        print("🎉 TAGCall 项目开发圆满完成！ 🎉")
        print("🎉" * 15)
        
        print("\n🌟 项目成就:")
        print("  ✅ 完整的函数调用解析库")
        print("  ✅ BeautifulSoup 驱动的健壮 XML 解析")
        print("  ✅ 自动函数字符串生成（重大改进！）")
        print("  ✅ 完整的大模型集成支持")
        print("  ✅ 全面的测试和文档")
        
        print("\n🚀 核心改进:")
        print("""
之前（繁琐）:
@function_call(
    prompt="获取天气",
    function_str="get_weather(city)"  # 需要手动写
)
def get_weather(city):
    pass

现在（简洁）:
@function_call(prompt="获取天气")  # 只需要写提示词！
def get_weather(city):
    pass
        """)
        
        print("\n💡 立即开始:")
        print("  python example_usage.py      # 基础使用")
        print("  python showcase_new_feature.py # 功能展示")
        print("  python demo.py               # 完整演示")
        print("  pip install -e .            # 安装为包")
        
        print("\n📚 文档指南:")
        print("  README.md                    # 项目说明")
        print("  QUICK_START.md               # 快速开始")
        print("  PROJECT_SUMMARY.md           # 项目总结")
        
    else:
        print("\n⚠️ 部分功能需要进一步检查")

if __name__ == "__main__":
    main()