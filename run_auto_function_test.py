#!/usr/bin/env python3
"""运行自动函数字符串生成测试"""

import subprocess
import sys

def run_test():
    """运行测试"""
    print("🚀 测试自动函数字符串生成功能")
    print("=" * 60)
    
    try:
        # 运行自动生成测试
        result = subprocess.run([sys.executable, "test_auto_function_str.py"], 
                              capture_output=True, text=True)
        
        print("测试输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        print("=" * 60)
        if result.returncode == 0:
            print("✅ 自动函数字符串生成测试成功！")
            print("\n🌟 主要改进:")
            print("  ✅ 自动从函数源码生成函数字符串")
            print("  ✅ 支持各种参数类型（位置、默认值、可变参数等）")
            print("  ✅ 无需手动编写 function_str")
            print("  ✅ 更好的错误恢复机制")
        else:
            print("❌ 测试失败！")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    
    if success:
        print("\n🎉 现在可以这样使用:")
        print("""
# 之前（需要手动写 function_str）
@function_call(
    prompt="获取天气",
    function_str="get_weather(city)"  # 需要手动写
)
def get_weather(city):
    pass

# 现在（自动生成）
@function_call(prompt="获取天气")  # 只需要写提示词！
def get_weather(city):
    pass
        """)
        
        print("\n💡 运行更新后的示例:")
        print("  python example_usage.py")
    else:
        print("\n⚠️ 需要进一步检查和修复")