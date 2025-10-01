#!/usr/bin/env python3
"""运行 TagCall 库测试"""

import subprocess
import sys

def run_test():
    """运行测试脚本"""
    try:
        result = subprocess.run([sys.executable, "test_library.py"], 
                              capture_output=True, text=True)
        
        print("测试输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ 测试运行成功！")
        else:
            print("❌ 测试运行失败！")
            
    except Exception as e:
        print(f"运行测试时出错: {e}")

if __name__ == "__main__":
    run_test()