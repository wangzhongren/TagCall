# BeautifulSoup 版本升级说明

## 🎯 升级概述

已将 TagCall 库从基于正则表达式的解析升级为基于 BeautifulSoup 的 HTML/XML 解析，提供更强大和健壮的标签解析能力。

## 🔄 主要变更

### 1. 核心解析逻辑
**之前（正则表达式）:**
```python
# 使用正则表达式匹配
pattern = r'<function-call>(.*?)</function-call>'
matches = re.findall(pattern, text, re.DOTALL)
```

**现在（BeautifulSoup）:**
```python
# 使用 BeautifulSoup 解析
soup = BeautifulSoup(text, 'html.parser')
function_call_tags = soup.find_all('function-call')
```

### 2. 依赖更新
- 添加 `beautifulsoup4>=4.9.0` 依赖
- 更新 `setup.py` 安装配置

## 🚀 新特性

### 1. 健壮的 HTML/XML 解析
```python
# 现在可以处理这些复杂情况：
complex_html = '''
<html>
<!-- 注释 -->
<div>
    <function-call>get_weather("北京");</function-call>
</div>
<script>干扰内容</script>
</html>
'''
# 仍然能正确解析出函数调用
```

### 2. 忽略无关内容
- 自动忽略 HTML 注释 (`<!-- 注释 -->`)
- 忽略脚本标签 (`<script>...</script>`)
- 忽略样式标签 (`<style>...</style>`)
- 忽略其他无关标签

### 3. 支持嵌套结构
```python
# 支持深度嵌套
nested_html = '''
<main>
    <section>
        <article>
            <function-call>
            calculate("1+1");
            </function-call>
        </article>
    </section>
</main>
'''
```

### 4. 容错处理
- 处理不完整的标签
- 忽略大小写差异
- 处理特殊字符转义

## 📊 性能对比

| 特性 | 正则表达式版本 | BeautifulSoup 版本 |
|------|----------------|-------------------|
| 简单标签解析 | ✅ | ✅ |
| 复杂 HTML 文档 | ❌ | ✅ |
| 嵌套标签支持 | ❌ | ✅ |
| 注释忽略 | ❌ | ✅ |
| 容错能力 | 有限 | 优秀 |
| 标准化程度 | 低 | 高 |

## 🔧 迁移指南

### 无需更改的代码
- 函数注册装饰器 `@function_call`
- 函数执行 `global_registry.execute_function()`
- 提示词生成 `global_registry.get_prompt_descriptions()`

### 向后兼容
新版本完全兼容原有的 API 接口，现有代码无需修改即可使用。

## 🧪 测试验证

运行以下测试验证新版本功能：

```bash
# 基础功能测试
python test_beautifulsoup.py

# 完整功能验证
python verify_beautifulsoup.py

# 原有示例（仍然工作）
python example_usage.py
python demo.py
```

## 🎉 总结

BeautifulSoup 版本的 TagCall 库提供了：
- ✅ **工业级解析能力** - 基于成熟的 BeautifulSoup 库
- ✅ **更好的兼容性** - 支持各种 HTML/XML 文档格式
- ✅ **更强的健壮性** - 处理格式问题和干扰内容
- ✅ **完整的向后兼容** - 现有代码无需修改

新版本特别适合处理从大模型返回的可能包含复杂 HTML 结构的响应内容。