# TagCall 快速开始指南

## 🚀 5分钟上手

### 1. 安装依赖
```bash
pip install beautifulsoup4
```

### 2. 基本使用
```python
from tagcall import function_call, parse_function_calls, global_registry

# 注册函数
@function_call(
    prompt="获取天气信息",
    function_str="get_weather(city)"
)
def get_weather(city):
    return f"{city}天气：晴，25°C"

# 解析和执行函数调用
text = '''
<function-call>
get_weather("北京");
</function-call>
'''

calls = parse_function_calls(text)
for call in calls:
    result = global_registry.execute_function(call['name'], *call['args'])
    print(result)
# 输出: 北京天气：晴，25°C
```

### 3. 大模型集成
```python
# 构建系统提示词
system_prompt = f"""
你可以调用以下函数：
{global_registry.get_prompt_descriptions()}

使用格式：
<function-call>
function_name(parameters);
</function-call>
"""

# 处理大模型响应
def process_ai_response(response):
    calls = parse_function_calls(response)
    results = []
    for call in calls:
        result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
        results.append(result)
    return results
```

## 📚 核心概念

### 函数注册
使用 `@function_call` 装饰器注册函数：
```python
@function_call(
    prompt="函数描述",      # 给大模型的说明
    function_str="函数签名", # 函数调用格式
    name="可选函数名"       # 可选，默认使用函数名
)
def your_function(parameters):
    # 函数实现
    pass
```

### 标签解析
解析 `<function-call>` 标签内容：
```python
# 支持复杂 HTML
text = '''
<div>
    <function-call>
    func1("param");
    func2(key="value");
    </function-call>
</div>
'''
calls = parse_function_calls(text)
```

### 函数执行
执行解析出的函数调用：
```python
for call in calls:
    result = global_registry.execute_function(
        call['name'], 
        *call['args'],      # 位置参数
        **call['kwargs']    # 关键字参数
    )
```

## 🎯 常用模式

### 模式1: 简单工具调用
```python
@function_call(prompt="计算器", function_str="calc(expr)")
def calc(expr):
    return eval(expr)

# 使用: <function-call>calc("2+3*4");</function-call>
```

### 模式2: 数据查询
```python
@function_call(prompt="查询用户信息", function_str="get_user(id)")
def get_user(id):
    # 查询数据库或API
    return user_data
```

### 模式3: 系统操作
```python
@function_call(prompt="发送通知", function_str="notify(message, level)")
def notify(message, level="info"):
    # 发送邮件、短信等
    return "通知已发送"
```

## 🔧 参数类型

支持以下参数类型：
- 字符串: `"hello"`
- 数字: `123`, `45.67`
- 布尔值: `true`, `false`
- 关键字参数: `param=value`

## 🛠️ 故障排除

### 常见问题

**Q: 函数调用未解析**
A: 检查标签格式是否正确：`<function-call>...</function-call>`

**Q: 参数解析错误**
A: 确保参数格式正确，字符串用引号包围

**Q: 函数未找到**
A: 确认函数已使用 `@function_call` 注册

### 调试技巧
```python
# 查看所有注册的函数
print(global_registry.get_all_functions())

# 查看解析结果
calls = parse_function_calls(text)
print("解析结果:", calls)
```

## 📖 下一步

- 查看 `example_usage.py` - 基础示例
- 运行 `demo.py` - 完整演示
- 阅读 `README.md` - 详细文档
- 查看 `BEAUTIFULSOUP_UPGRADE.md` - BeautifulSoup 特性

现在就开始使用 TagCall 构建智能的 AI 应用吧！🎉