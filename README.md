# TagCall —— 基于 `<function-call>` 标签的轻量级大模型工具调用框架

**TagCall** 是一个简单、灵活、无依赖的大模型函数调用（Function Calling）解决方案。它通过在模型输出中插入标准 XML 风格标签（如 `<function-call>add(a=1, b=2)</function-call>`），实现本地函数的安全调用，适用于任何支持文本生成的大模型（OpenAI、Ollama、Llama.cpp、vLLM 等）。

无需复杂 Schema 定义，无需 JSON 模式约束，只需装饰器注册 + 标准提示词，即可让任意大模型“调用你的代码”。

---

## ✨ 方案对比与核心优势

| 特性 | TagCall | OpenAI Function Calling | LangChain Tools | 自定义正则方案 |
|------|--------|------------------------|----------------|--------------|
| **依赖复杂度** | 极简（可选 `bs4`） | 强依赖 OpenAI SDK | 重型框架（数十个依赖） | 无依赖 |
| **模型兼容性** | ✅ 所有文本生成模型 | ❌ 仅限 OpenAI 及兼容 API | ⚠️ 需适配器 | ✅ 所有模型 |
| **函数注册方式** | 装饰器自动提取签名 | 手动编写 JSON Schema | 子类化 `BaseTool` | 手动维护映射表 |
| **参数解析安全性** | 严格类型限制（基础类型） | 由 OpenAI 解析 | 依赖 Pydantic | 易出错（需自行处理引号/嵌套） |
| **提示词灵活性** | 纯文本片段，任意拼接 | 固定格式 | 框架内嵌 | 需自行设计 |
| **流式支持** | ✅ 先输出后解析 | ✅ | ⚠️ 复杂 | ✅ |
| **学习成本** | <5 分钟 | 中等 | 高 | 低但易错 |

### 🌟 TagCall 的独特优势：

1. **真正的模型无关性**  
   不绑定任何厂商 API，无论是 OpenAI、Ollama、Llama.cpp 还是私有部署的 vLLM，只要能生成文本，就能使用 TagCall。

2. **零心智负担的函数注册**  
   使用 `@function_call(prompt="...")` 装饰器，自动提取函数签名（如 `add(a, b)`），无需手动维护参数列表或 JSON Schema。

3. **安全且健壮的解析机制**  
   基于 `BeautifulSoup` 的标签解析天然免疫注入攻击；参数解析严格限定为字符串、数字、布尔值、None，杜绝 `eval()` 风险。

4. **无缝集成现有系统**  
   `get_system_prompt()` 返回纯文本描述，可轻松拼接到任何角色设定中，不强制改变你的对话流程。

5. **极简架构，易于审计和修改**  
   核心代码不足 300 行，无黑盒逻辑，适合对安全性要求高的场景（如金融、医疗）。

---

## 📦 安装

将 `tagcall/` 目录放入你的 Python 项目中，确保可导入：

```bash
your_project/
├── tagcall/
│   ├── __init__.py
│   ├── core.py
│   ├── decorator.py
│   └── prompt.py
└── your_agent.py
```

依赖（仅解析 HTML 标签时需要）：
```bash
pip install beautifulsoup4
```

> 💡 若你希望完全移除 `bs4` 依赖，可自行替换 `parse_function_calls` 中的解析逻辑（例如用正则）。

---

## 🚀 快速开始

### 1. 注册工具函数

```python
from tagcall import function_call

@function_call(prompt="获取当前时间")
def get_time():
    import time
    return time.strftime("%H:%M:%S")

@function_call(prompt="计算两个数的和")
def add(a: int, b: int):
    return a + b
```

### 2. 获取系统提示词（用于注入模型）

```python
from tagcall import get_system_prompt

system_prompt = get_system_prompt()
# 输出示例：
# 可用工具函数：
# get_time() - 获取当前时间
# add(a, b) - 计算两个数的和
#
# 调用规则：
# - 若需调用，请在回答中插入 <function-call> 标签...
```

### 3. 调用大模型（以 OpenAI SDK 为例）

```python
from openai import OpenAI
from tagcall import parse_function_calls, global_registry

client = OpenAI()  # 或配置 Ollama base_url

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "现在几点？"}
    ]
)

llm_output = response.choices[0].message.content
```

### 4. 解析并执行函数调用

```python
calls = parse_function_calls(llm_output)
for call in calls:
    result = global_registry.execute_function(
        call['name'],
        *call['args'],
        **call['kwargs']
    )
    print(f"{call['name']} → {result}")
```

---

## 🧪 示例项目

查看完整示例：
- [`test_tagcall_agent_with_openai.py`](../test_tagcall_agent_with_openai.py)：支持 OpenAI / Ollama（兼容 API）+ 流式输出
- [`test_tagcall_agent.py`](../test_tagcall_agent.py)：纯本地模拟测试

---

## 📝 提示词设计说明

`get_system_prompt()` 返回的内容**不含角色定义**，仅为工具描述片段，便于拼接：

```python
my_role = "你是公司内部效率助手，语气简洁。"
full_prompt = f"{my_role}\n\n{get_system_prompt()}"
```

模型将被引导输出如下格式：
```text
<function-call>get_time()</function-call>
```
或
```text
<function-call>add(a=3, b=5)</function-call>
```

---

## 🔒 安全性

- 函数必须显式注册才能被调用，防止任意代码执行；
- 参数解析严格限制为基本类型，不支持表达式求值；
- 标签解析基于 HTML/XML 安全解析器，避免注入风险。

---

## 🤝 贡献与扩展

- 替换 `parse_function_calls` 实现（如使用正则）以移除 `bs4` 依赖；
- 扩展 `_parse_value` 支持更多类型（如列表、字典）；
- 添加异步执行支持（当前为同步）。

---

## 📜 License

MIT License — 自由用于个人及商业项目。