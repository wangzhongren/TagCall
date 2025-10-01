# TagCall 快速开始指南

## 🚀 5分钟上手

### 1. 安装依赖
```bash
pip install beautifulsoup4
```

### 2. 基础使用
```python
from tagcall import function_call, parse_function_calls, global_registry

# 注册函数
@function_call(
    prompt="获取天气信息",
    function_str="get_weather(city)"
)
def get_weather(city):
    return f"{city}的天气：晴，25°C"

# 解析和执行函数调用
text = '''
<function-call>
get_weather("北京");
</function-call>
'''

calls = parse_function_calls(text)
for call in calls:
    result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
    print(result)
```

### 3. 大模型集成
```python
# 生成系统提示词
system_prompt = f"""
你可以调用以下函数：
{global_registry.get_prompt_descriptions()}

当需要调用函数时，请使用：
<function-call>
function_name(arguments);
</function-call>
"""
```

## 📚 示例文件

| 文件 | 描述 | 运行命令 |
|------|------|----------|
| `example_usage.py` | 基础使用示例 | `python example_usage.py` |
| `demo.py` | 完整功能演示 | `python demo.py` |
| `final_verification.py` | 最终验证测试 | `python final_verification.py` |

## 🔧 核心 API

### 函数注册
```python
@function_call(prompt="描述", function_str="func(arg)", name="可选名称")
def your_function(arg):
    pass
```

### 解析调用
```python
calls = parse_function_calls(text)
# 返回: [{'name': 'func', 'args': [], 'kwargs': {}}]
```

### 执行函数
```python
result = global_registry.execute_function(name, *args, **kwargs)
```

## 💡 使用技巧

### 1. 处理复杂响应
```python
# BeautifulSoup 可以处理复杂的 HTML 响应
complex_response = '''
<div>
    <function-call>
    func1("param");
    func2(key="value");
    </function-call>
</div>
'''
calls = parse_function_calls(complex_response)  # 正常工作
```

### 2. 错误处理
```python
try:
    result = global_registry.execute_function(name, *args, **kwargs)
except ValueError as e:
    print(f"函数未注册: {e}")
except Exception as e:
    print(f"执行错误: {e}")
```

### 3. 自定义函数字符串
```python
@function_call(
    prompt="描述",
    function_str="custom_name(param: type) -> return_type"
)
def actual_function_name(param):
    pass
```

## 🎯 最佳实践

1. **明确的提示词**: 为每个函数提供清晰的描述
2. **合理的参数**: 使用有意义的参数名称
3. **错误处理**: 在函数内部处理可能的异常
4. **文档完整**: 为函数添加 docstring

## 🆘 故障排除

**问题**: 解析不到函数调用
**解决**: 检查标签是否正确闭合，使用 `print(parse_function_calls(text))` 调试

**问题**: 函数执行错误
**解决**: 检查参数类型和数量，使用 try-except 捕获异常

**问题**: 依赖安装失败
**解决**: 确保使用 `pip install beautifulsoup4`

---

现在就开始使用 TagCall 构建您的大模型函数调用系统吧！ 🎉