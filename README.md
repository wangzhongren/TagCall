# TagCall

一个支持函数调用标记解析和注册的 Python 库，专为大模型函数调用场景设计。使用 BeautifulSoup 提供强大的 HTML/XML 解析能力，并自动从函数源码生成函数签名。

## 特性

- 🎯 简洁的函数注册装饰器
- 📝 自动从函数源码生成函数签名
- 🔍 使用 BeautifulSoup 解析 `<function-call>` 标签内容
- 🚀 支持位置参数和关键字参数
- 🛡️ 健壮的 HTML/XML 解析，支持复杂文档结构
- 🔧 易于扩展和集成

## 安装

```bash
pip install tagcall
```

或者从源码安装：

```bash
git clone <repository-url>
cd TagCall
pip install -e .
```

## 快速开始

### 1. 注册函数（无需手动写函数字符串！）

```python
from tagcall import function_call

@function_call(prompt="获取指定城市的天气信息")
def get_weather(city: str):
    return f"{city}的天气：晴，25°C"

@function_call(prompt="计算两个数字的和")
def add(a: int, b: int):
    return a + b

@function_call(prompt="发送邮件")
def send_email(to: str, subject: str = "无主题", body: str = ""):
    return f"已发送邮件到 {to}"
```

### 2. 获取函数提示词

```python
from tagcall import global_registry

prompt = global_registry.get_prompt_descriptions()
print(prompt)
# 输出:
# get_weather(city) - 获取指定城市的天气信息
# add(a, b) - 计算两个数字的和
# send_email(to, subject='无主题', body='') - 发送邮件
```

### 3. 解析和执行函数调用

```python
from tagcall import parse_function_calls

text = '''
<function-call>
get_weather("北京");
add(1, 3);
send_email("user@example.com", subject="测试邮件");
</function-call>
'''

calls = parse_function_calls(text)
for call in calls:
    result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
    print(f"{call['name']} 结果: {result}")
```

## 自动函数签名生成

TagCall 会自动从函数源码生成函数签名，支持：

- ✅ 位置参数：`func(a, b, c)`
- ✅ 默认值参数：`func(a, b=10, c="hello")`
- ✅ 可变参数：`func(a, *args, **kwargs)`
- ✅ 关键字参数：`func(a, b, *, key="value")`
- ✅ 类型注解：`func(name: str, age: int = 25)`

### 手动指定（可选）

如果需要自定义函数字符串，仍然可以手动指定：

```python
@function_call(
    prompt="自定义函数",
    function_str="custom_name(param1, param2)"  # 可选
)
def actual_function_name(a, b):
    pass
```

## BeautifulSoup 优势

使用 BeautifulSoup 解析提供以下优势：

- ✅ **健壮性**: 处理不完整的 HTML/XML 结构
- ✅ **灵活性**: 支持嵌套在其他标签中的函数调用
- ✅ **容错性**: 忽略注释、无关标签等干扰内容
- ✅ **标准化**: 符合 HTML/XML 解析标准

## API 参考

### 装饰器

`@function_call(prompt: str, function_str: str = None, name: str = None)`

- `prompt`: 函数的功能描述，用于大模型理解
- `function_str`: 函数字符串表示（可选，自动生成）
- `name`: 注册的函数名（可选，默认使用函数名）

### 核心函数

- `parse_function_calls(text: str) -> List[Dict]`: 解析包含函数调用的文本
- `global_registry`: 全局函数注册表实例

### FunctionRegistry 类

- `register(name, prompt, function, function_str)`: 注册函数
- `get_function(name)`: 获取函数信息
- `get_all_functions()`: 获取所有注册函数
- `get_prompt_descriptions()`: 获取提示词描述
- `execute_function(name, *args, **kwargs)`: 执行函数

## 许可证

MIT