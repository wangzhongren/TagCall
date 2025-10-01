#!/usr/bin/env python3
"""运行完整的功能验证"""

import subprocess
import sys

def run_validation():
    """运行完整验证"""
    print("🔍 TagCall 完整功能验证")
    print("=" * 60)
    
    tests = [
        ("python test_auto_function_str.py", "自动函数字符串生成"),
        ("python test_new_feature.py", "新功能测试"),
        ("python example_usage.py", "更新后的示例"),
        ("python test_beautifulsoup.py", "BeautifulSoup 解析")
    ]
    
    success_count = 0
    for command, description in tests:
        print(f"\n🧪 {description}")
        print("-" * 40)
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            print(result.stdout)
            
            if result.returncode == 0:
                print("✅ 通过")
                success_count += 1
            else:
                print("❌ 失败")
                if result.stderr:
                    print("错误:", result.stderr)
        except Exception as e:
            print(f"❌ 异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {success_count}/{len(tests)} 通过")
    
    if success_count == len(tests):
        print("\n🎉 所有功能验证通过！")
        print("\n🌟 主要改进总结:")
        print("  ✅ 自动从函数源码生成函数签名")
        print("  ✅ 无需手动编写 function_str 参数")
        print("  ✅ 支持各种复杂参数类型")
        print("  ✅ 保持向后兼容性")
        print("  ✅ 更优雅的使用体验")
        
        print("\n💡 现在使用 TagCall 更加简单:")
        print("""
# 只需要写提示词，函数签名自动生成！
@function_call(prompt="你的函数描述")
def your_function(param1, param2=default):
    # 函数实现
    pass
        """)
    else:
        print("\n⚠️ 部分测试未通过")

if __name__ == "__main__":
    run_validation()