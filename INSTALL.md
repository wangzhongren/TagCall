# TagCall 安装和使用指南

## 安装

### 方法1：直接使用源码
```bash
# 克隆或下载项目到本地
git clone <repository-url>
cd TagCall

# 直接使用（确保Python路径包含项目目录）
python demo.py
```

### 方法2：安装为Python包
```bash
# 在项目根目录执行
pip install -e .
```

## 快速开始

### 1. 基本使用

```python
from tagcall import function_call, parse_function_calls, global_registry

# 注册函数
@function_call(
    prompt="获取天气信息",
    function_str="get_weather(city)"
)
def get_weather(city):
    return f"{city}的天气：晴，25°C"

# 获取所有函数的提示词描述
prompt_text = global_registry.get_prompt_descriptions()
print(prompt_text)

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

### 2. 与大模型集成

```python
class AIAssistant:
    def __init__(self):
        self.functions_prompt = global_registry.get_prompt_descriptions()
    
    def build_system_prompt(self):
        return f"""你可以调用以下函数：
{self.functions_prompt}

使用格式：
<function-call>
function_name(args);
</function-call>"""
    
    def process_ai_response(self, response):
        calls = parse_function_calls(response)
        results = []
        for call in calls:
            result = global_registry.execute_function(call['name'], *call['args'], **call['kwargs'])
            results.append(result)
        return results
```

## 功能特性

✅ **函数注册**: 使用装饰器轻松注册函数  
✅ **自动提示词生成**: 自动生成函数描述供大模型使用  
✅ **函数调用解析**: 解析 `<function-call>` 标签内容  
✅ **参数支持**: 支持位置参数和关键字参数  
✅ **错误处理**: 完善的错误处理和异常管理  
✅ **易于扩展**: 模块化设计，易于扩展新功能  

## 文件结构

```
TagCall/
├── tagcall/           # 核心库
│   ├── __init__.py
│   ├── core.py       # 核心功能
│   └── decorator.py  # 装饰器
├── example_usage.py  # 基础示例
├── demo.py          # 完整演示
├── test_library.py  # 功能测试
└── README.md        # 文档
```

## 运行示例

```bash
# 运行基础示例
python example_usage.py

# 运行完整演示
python demo.py

# 运行功能测试
python test_library.py
```

## 注意事项

1. **安全性**: 在实际生产环境中，请确保函数执行的安全性
2. **参数解析**: 当前参数解析支持基本类型，复杂类型需要扩展
3. **错误处理**: 建议在实际使用中添加适当的错误处理逻辑
4. **大模型集成**: 需要根据具体的大模型API调整集成方式

## 扩展开发

要扩展 TagCall 库的功能，可以：

1. 修改 `core.py` 中的参数解析逻辑
2. 添加新的函数注册选项
3. 扩展错误处理机制
4. 添加日志记录功能

欢迎贡献代码和改进建议！