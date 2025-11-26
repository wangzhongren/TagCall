import inspect
import ast
from typing import Dict, List, Callable, Any, Optional
from bs4 import BeautifulSoup

class FunctionRegistry:
    """函数注册表，支持按 agent 隔离注册"""
    
    def __init__(self):
        # 结构: {agent_name: {func_name: func_info}}
        self._functions: Dict[str, Dict[str, Dict]] = {}
    
    def register(self, name: str, prompt: str, function: Callable, function_str: str = None, agent: str = "default"):
        """注册函数
        
        Args:
            name: 函数名称
            prompt: 方法提示词说明
            function: 真实的方法
            function_str: 方法字符串，如果为None则自动从源码生成
            agent: 所属 agent 名称，默认为 "default"
        """
        if function_str is None:
            # 自动从函数源码生成字符串表示
            function_str = self._generate_function_str_from_source(function, name)
        
        if agent not in self._functions:
            self._functions[agent] = {}
        
        self._functions[agent][name] = {
            "prompt": prompt,
            "function_str": function_str,
            "function": function
        }
    
    def _generate_function_str_from_source(self, func: Callable, name: str) -> str:
        """从函数源码自动生成函数字符串表示"""
        try:
            # 获取函数源码
            source = inspect.getsource(func)
            
            # 解析函数定义
            tree = ast.parse(source)
            func_def = tree.body[0]
            
            if not isinstance(func_def, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return f"{name}(...)"
            
            # 提取参数
            args = func_def.args
            params = []
            
            # 位置参数
            for arg in args.args:
                params.append(arg.arg)
            
            # 可变位置参数 (*args)
            if args.vararg:
                params.append(f"*{args.vararg.arg}")
            
            # 关键字参数
            for arg in args.kwonlyargs:
                default = None
                # 查找对应的默认值
                for i, kw_default in enumerate(args.kw_defaults):
                    if i < len(args.kwonlyargs) and args.kwonlyargs[i].arg == arg.arg:
                        if kw_default is not None:
                            default = ast.unparse(kw_default) if hasattr(ast, 'unparse') else self._format_default(kw_default)
                        break
                
                if default is not None:
                    params.append(f"{arg.arg}={default}")
                else:
                    params.append(arg.arg)
            
            # 可变关键字参数 (**kwargs)
            if args.kwarg:
                params.append(f"**{args.kwarg.arg}")
            
            return f"{name}({', '.join(params)})"
            
        except (SyntaxError, IndexError, AttributeError):
            # 如果源码解析失败，回退到签名方式
            return self._generate_function_str_from_signature(func, name)
    
    def _format_default(self, node) -> str:
        """格式化默认值节点"""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Name) and node.id == 'None':
            return 'None'
        elif isinstance(node, ast.Str):
            return repr(node.s)
        elif isinstance(node, ast.Num):
            return repr(node.n)
        elif isinstance(node, ast.NameConstant):
            return repr(node.value)
        else:
            # 对于复杂表达式，返回占位符
            return "..."
    
    def _generate_function_str_from_signature(self, func: Callable, name: str) -> str:
        """使用inspect.signature生成函数字符串（备用方案）"""
        try:
            sig = inspect.signature(func)
            params = []
            for param_name, param in sig.parameters.items():
                if param.default == inspect.Parameter.empty:
                    if param.kind == param.VAR_POSITIONAL:
                        params.append(f"*{param_name}")
                    elif param.kind == param.VAR_KEYWORD:
                        params.append(f"**{param_name}")
                    else:
                        params.append(param_name)
                else:
                    params.append(f"{param_name}={param.default!r}")
            
            return f"{name}({', '.join(params)})"
        except:
            return f"{name}(...)"
    
    def get_function(self, name: str, agent: str = "default") -> Optional[Dict]:
        """获取注册的函数信息"""
        return self._functions.get(agent, {}).get(name)
    
    def get_all_functions(self, agent: str = "default") -> Dict[str, Dict]:
        """获取指定 agent 的所有注册函数"""
        return self._functions.get(agent, {}).copy()
    
    def get_all_agents(self) -> List[str]:
        """获取所有已注册的 agent 名称"""
        return list(self._functions.keys())
    
    def get_prompt_descriptions(self, agent: str = "default") -> str:
        """获取指定 agent 所有函数的提示词描述"""
        descriptions = []
        for name, info in self._functions.get(agent, {}).items():
            descriptions.append(f"{info['function_str']} - {info['prompt']}")
        return "\n".join(descriptions)
    
    def execute_function(self, name: str, *args, agent: str = "default", **kwargs) -> Any:
        """执行注册的函数"""
        func_info = self.get_function(name, agent)
        if not func_info:
            raise ValueError(f"Function '{name}' is not registered for agent '{agent}'")
        
        return func_info['function'](*args, **kwargs)

# 全局注册表实例
global_registry = FunctionRegistry()

def _split_parameters(args_text: str) -> List[str]:
    """分割参数字符串，处理嵌套的引号和括号"""
    parts = []
    current = ""
    quote_char = None
    paren_depth = 0
    
    for char in args_text:
        if char in ['"', "'"] and quote_char is None:
            quote_char = char
            current += char
        elif char == quote_char:
            quote_char = None
            current += char
        elif char == '(' and quote_char is None:
            paren_depth += 1
            current += char
        elif char == ')' and quote_char is None and paren_depth > 0:
            paren_depth -= 1
            current += char
        elif char == ',' and quote_char is None and paren_depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    
    if current.strip():
        parts.append(current.strip())
    
    return parts

def _parse_value(value_str: str) -> Any:
    """解析参数值"""
    value_str = value_str.strip()
    
    # 字符串
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    
    # 数字
    try:
        if '.' in value_str:
            return float(value_str)
        else:
            return int(value_str)
    except ValueError:
        pass
    
    # 布尔值
    if value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False
    
    # None值
    if value_str.lower() == 'none' or value_str.lower() == 'null':
        return None
    
    # 其他情况返回原字符串
    return value_str

def parse_function_calls(text: str) -> List[Dict]:
    """解析函数调用文本
    
    Args:
        text: 包含<function-call>标签的文本
        
    Returns:
        List[Dict]: 解析出的函数调用列表，每个元素包含 'name', 'args', 'kwargs'
    """
    # 使用 BeautifulSoup 解析 XML/HTML 标签
    soup = BeautifulSoup(text, 'html.parser')
    
    # 查找所有的 function-call 标签
    function_call_tags = soup.find_all('function-call')
    
    if not function_call_tags:
        return []
    
    function_calls = []
    
    for tag in function_call_tags:
        call_text = tag.get_text().strip()
        
        # 按行分割并解析每个函数调用
        for line in call_text.split(';'):
            line = line.strip()
            if not line:
                continue
                
            # 解析函数名和参数
            if '(' in line and line.endswith(')'):
                name_part, args_part = line.split('(', 1)
                name = name_part.strip()
                args_text = args_part[:-1].strip()  # 去掉结尾的 ')'
                
                # 解析参数
                args = []
                kwargs = {}
                
                if args_text:
                    param_parts = _split_parameters(args_text)
                    for part in param_parts:
                        part = part.strip()
                        if '=' in part:
                            # 关键字参数
                            key, value = part.split('=', 1)
                            key = key.strip()
                            value = _parse_value(value.strip())
                            kwargs[key] = value
                        else:
                            # 位置参数
                            args.append(_parse_value(part))
                
                function_calls.append({
                    'name': name,
                    'args': args,
                    'kwargs': kwargs
                })
    
    return function_calls