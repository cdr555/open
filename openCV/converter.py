import re
import sys
import os

def convert_nodejs_to_emscripten(input_code):
    # 提取函数名
    function_name_match = re.search(r'NAN_METHOD\((\w+)\)', input_code)
    if not function_name_match:
        print("警告：无法识别NAN_METHOD函数名，尝试其他方式识别...")
        # 尝试其他方式识别函数名
        alternative_match = re.search(r'void\s+(\w+)\(', input_code)
        if alternative_match:
            function_name = alternative_match.group(1)
        else:
            return "错误：无法识别函数名"
    else:
        function_name = function_name_match.group(1)
    
    print(f"识别到函数名: {function_name}")
    
    # 提取所有参数
    string_params = re.findall(r'std::string\s+(\w+)\s*=\s*GetOption\(context,\s*options,\s*"(\w+)"\);', input_code)
    float_params = re.findall(r'float\s+(\w+)\s*=\s*GetOptionFloat\(context,\s*options,\s*"(\w+)"\);', input_code)
    int_params = re.findall(r'int\s+(\w+)\s*=\s*GetOptionInt\(context,\s*options,\s*"(\w+)"\);', input_code)
    bool_params = re.findall(r'bool\s+(\w+)\s*=\s*GetOptionBool\(context,\s*options,\s*"(\w+)"\);', input_code)
    
    # 汇总所有参数信息
    params = {}
    
    for var_name, param_name in string_params:
        params[param_name] = {"var": var_name, "type": "std::string"}
        print(f"找到字符串参数: {param_name} => {var_name}")
    
    for var_name, param_name in float_params:
        params[param_name] = {"var": var_name, "type": "float"}
        print(f"找到浮点数参数: {param_name} => {var_name}")
    
    for var_name, param_name in int_params:
        params[param_name] = {"var": var_name, "type": "int"}
        print(f"找到整数参数: {param_name} => {var_name}")
    
    for var_name, param_name in bool_params:
        params[param_name] = {"var": var_name, "type": "bool"}
        print(f"找到布尔参数: {param_name} => {var_name}")
    
    # 查找默认值设置
    default_values = re.findall(r'if\s*\((\w+)\.empty\(\)\)\s*(\w+)\s*=\s*([^;]+);', input_code)
    
    for var_name, var_name2, default_value in default_values:
        for param_name, info in params.items():
            if info["var"] == var_name or info["var"] == var_name2:
                params[param_name]["default"] = default_value.strip()
                print(f"找到参数默认值: {param_name} => {default_value.strip()}")
    
    # 查找核心函数调用 - 这是我们需要封装的主要部分
    # 先查找主要的函数调用格式：返回类型 变量名 = 命名空间::函数名(参数列表)
    core_function_calls = re.findall(r'(\w+)\s+(\w+)\s*=\s*([\w:]+)::(\w+)\(([^)]*)\);', input_code)
    
    # 还要查找直接的函数调用：命名空间::函数名(参数列表)
    direct_function_calls = re.findall(r'([\w:]+)::(\w+)\(([^)]*)\);', input_code)
    
    # 还要查找类对象的方法调用：返回类型 变量名 = 对象.方法(参数列表)
    method_calls = re.findall(r'(\w+)\s+(\w+)\s*=\s*(\w+)\.(\w+)\(([^)]*)\);', input_code)
    
    # 最后，查找直接的方法调用：对象.方法(参数列表)
    direct_method_calls = re.findall(r'(\w+)\.(\w+)\(([^)]*)\);', input_code)
    
    # 识别返回值设置
    result_sets = []
    result_set_matches = re.findall(r'SetObjectProperty\(context,\s*result,\s*"([^"]+)",\s*([^)]+)\)', input_code)
    
    for prop_name, prop_value in result_set_matches:
        if "Nan::New<Number>" in prop_value:
            value = re.search(r'Nan::New<Number>\(([^)]+)\)', prop_value)
            if value:
                result_sets.append((prop_name, value.group(1)))
        elif "Nan::New<v8::String>" in prop_value:
            value = re.search(r'Nan::New<v8::String>\("([^"]*)"\)', prop_value)
            if value:
                result_sets.append((prop_name, f'"{value.group(1)}"'))
            else:
                var_value = re.search(r'Nan::New<v8::String>\(([^)]+)\)', prop_value)
                if var_value:
                    result_sets.append((prop_name, var_value.group(1)))
        else:
            value = re.search(r'Nan::New\(([^)]+)\)', prop_value)
            if value:
                result_sets.append((prop_name, value.group(1)))
            else:
                result_sets.append((prop_name, prop_value))
    
    # 识别主要的核心函数
    core_function = None
    core_function_params = None
    core_function_var = None
    
    # 优先检查具有返回值赋值的核心函数调用
    if core_function_calls:
        for ret_type, ret_var, namespace, func_name, func_params in core_function_calls:
            # 跳过标准库函数
            if namespace not in ["std", "v8"]:
                core_function = f"{namespace}::{func_name}"
                core_function_params = func_params
                core_function_var = ret_var
                print(f"找到核心函数调用: {core_function}({core_function_params})")
                break
    
    # 如果没找到，检查直接的函数调用
    if not core_function and direct_function_calls:
        for namespace, func_name, func_params in direct_function_calls:
            if namespace not in ["std", "v8"]:
                core_function = f"{namespace}::{func_name}"
                core_function_params = func_params
                print(f"找到直接核心函数调用: {core_function}({core_function_params})")
                break
    
    # 如果还没找到，检查方法调用
    if not core_function and method_calls:
        for ret_type, ret_var, obj_name, method_name, method_params in method_calls:
            core_function = f"{obj_name}.{method_name}"
            core_function_params = method_params
            core_function_var = ret_var
            print(f"找到核心方法调用: {core_function}({core_function_params})")
            break
    
    # 如果还没找到，检查直接的方法调用
    if not core_function and direct_method_calls:
        for obj_name, method_name, method_params in direct_method_calls:
            core_function = f"{obj_name}.{method_name}"
            core_function_params = method_params
            print(f"找到直接核心方法调用: {core_function}({core_function_params})")
            break
    
    # 开始构建新函数
    emscripten_code = f"val {function_name}(val params)\n{{\n"
    emscripten_code += "    val ret = val::object();\n"
    
    # 添加参数检查
    if params:
        # 过滤掉有默认值的参数
        required_params = [p for p, info in params.items() if "default" not in info]
        if required_params:
            condition = " && ".join([f'params.hasOwnProperty("{param}")' for param in required_params])
            emscripten_code += f"    if({condition})\n    {{\n"
        else:
            emscripten_code += "    {\n"
    else:
        emscripten_code += "    {\n"
    
    # 添加参数提取
    for param_name, info in params.items():
        var_name = info["var"]
        param_type = info["type"]
        
        if "default" in info:
            emscripten_code += f'        {param_type} {var_name} = params.hasOwnProperty("{param_name}") ? params["{param_name}"].as<{param_type}>() : {info["default"]};\n'
        else:
            emscripten_code += f'        {param_type} {var_name} = params["{param_name}"].as<{param_type}>();\n'
    
    # 添加核心函数调用
    if core_function:
        if core_function_var:  # 如果有返回值
            emscripten_code += f"\n        bool {core_function_var} = {core_function}({core_function_params});\n"
        else:
            emscripten_code += f"\n        {core_function}({core_function_params});\n"
        
        # 如果有返回值检查，添加条件分支
        if core_function_var and "if (!ret)" in input_code:
            emscripten_code += f"\n        if (!{core_function_var})\n        {{\n"
            # 添加失败情况下的返回值
            fail_code = None
            fail_msg = None
            for prop_name, prop_value in result_sets:
                if "if (!ret)" in input_code and prop_name == "code":
                    fail_code = prop_value
                if "if (!ret)" in input_code and prop_name == "msg":
                    fail_msg = prop_value
            
            if fail_code:
                emscripten_code += f'            ret.set("code", {fail_code});\n'
            else:
                emscripten_code += '            ret.set("code", -1);\n'
            
            if fail_msg:
                emscripten_code += f'            ret.set("msg", {fail_msg});\n'
            else:
                emscripten_code += '            ret.set("msg", "failure");\n'
            
            emscripten_code += "            return ret;\n        }\n"
    
    # 添加成功情况下的结果设置
    # 找出在if (!ret)之后的结果设置
    success_results = []
    in_success_block = False
    for line in input_code.splitlines():
        if "if (!ret)" in line:
            in_success_block = False
        elif "return;" in line and in_success_block is False:
            in_success_block = True
        elif in_success_block and "SetObjectProperty" in line:
            match = re.search(r'SetObjectProperty\(context,\s*result,\s*"([^"]+)",\s*([^)]+)\)', line)
            if match:
                prop_name, prop_value = match.groups()
                if "Nan::New<Number>" in prop_value:
                    value = re.search(r'Nan::New<Number>\(([^)]+)\)', prop_value)
                    if value:
                        success_results.append((prop_name, value.group(1)))
                elif "Nan::New<v8::String>" in prop_value:
                    value = re.search(r'Nan::New<v8::String>\("([^"]*)"\)', prop_value)
                    if value:
                        success_results.append((prop_name, f'"{value.group(1)}"'))
                    else:
                        var_value = re.search(r'Nan::New<v8::String>\(([^)]+)\)', prop_value)
                        if var_value:
                            success_results.append((prop_name, var_value.group(1)))
                else:
                    success_results.append((prop_name, prop_value))
    
    # 如果没有找到成功情况的结果设置，使用所有结果设置
    if not success_results:
        success_results = result_sets
    
    # 添加结果设置
    for prop_name, prop_value in success_results:
        if "ToLocalChecked()" in prop_value:
            prop_value = prop_value.replace(".ToLocalChecked()", "")
        emscripten_code += f'        ret.set("{prop_name}", {prop_value});\n'
    
    # 如果没有设置code和msg，添加默认值
    if not any(prop_name == "code" for prop_name, _ in success_results):
        emscripten_code += '        ret.set("code", 0);\n'
    
    if not any(prop_name == "msg" for prop_name, _ in success_results):
        emscripten_code += '        ret.set("msg", "success");\n'
    
    # 关闭if块
    emscripten_code += "    }\n"
    emscripten_code += "    else\n    {\n"
    emscripten_code += '        ret.set("code", -1);\n'
    
    # 创建丢失参数列表
    if params:
        required_params = [p for p, info in params.items() if "default" not in info]
        if required_params:
            emscripten_code += f'        ret.set("msg", "lost params {{{", ".join(required_params)}}}");\n'
        else:
            emscripten_code += '        ret.set("msg", "invalid parameters");\n'
    else:
        emscripten_code += '        ret.set("msg", "no parameters provided");\n'
    
    emscripten_code += "    }\n"
    emscripten_code += "    return ret;\n"
    emscripten_code += "}"
    
    # 添加EMSCRIPTEN_BINDINGS入口
    binding_code = f'\n\n// 添加到EMSCRIPTEN_BINDINGS部分:\n// emscripten::function("{function_name}", &{function_name});'
    
    return emscripten_code + binding_code

def process_file(input_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        input_code = f.read()
    
    output_code = convert_nodejs_to_emscripten(input_code)
    
    output_file = os.path.splitext(input_file)[0] + "_emscripten.cpp"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_code)
    
    print(f"转换完成，输出文件: {output_file}")
    return output_code

def main():
    if len(sys.argv) < 2:
        print("用法: python converter.py <输入文件路径1> [输入文件路径2 ...]")
        return
    
    for input_file in sys.argv[1:]:
        if not os.path.exists(input_file):
            print(f"文件不存在: {input_file}")
            continue
        
        print(f"处理文件: {input_file}")
        try:
            output_code = process_file(input_file)
            print("\n转换后代码:\n")
            print(output_code)
        except Exception as e:
            print(f"处理文件时出错: {str(e)}")
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()