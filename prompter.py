import requests

# 添加文件写入函数
def write_to_file(content, filename='output.md'):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def enhance_prompt(original_prompt):
    """第一次API调用：优化用户原始提示"""
    system_prompt = """你是一个提示词优化专家，请将用户的原始提示转化为更清晰、具体、结构化的专业版本。
优化后的提示应包含：
1. 明确的背景设定
2. 具体的分析维度/要求
3. 期望的输出格式
4. 相关限制条件
请保持专业性和逻辑性，同时确保核心诉求得到完整保留。"""
    
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": original_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
        "top_p": 0.9
    }
    
    response = requests.post(
        url="https://api.siliconflow.cn/v1/chat/completions",
        json=payload,
        headers={
            "Authorization": "Bearer sk-ilaucaqhgfrxaorawljnehpgwmrlkyepdzaaoiczbamsvzyv",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code != 200:
        error_msg = f"API请求失败，状态码：{response.status_code}"
        write_to_file(error_msg)
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    enhanced = response.json()['choices'][0]['message']['content']
    return enhanced.strip('"')

def get_final_response(enhanced_prompt, model="deepseek-ai/DeepSeek-V3"):
    """第二次API调用：获取最终回答"""
    print("开始生成最终回答...")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": enhanced_prompt}],
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9
    }
    
    print("正在准备API请求...")
    response = requests.post(
        url="https://api.siliconflow.cn/v1/chat/completions",
        json=payload,
        headers={
            "Authorization": "Bearer sk-ilaucaqhgfrxaorawljnehpgwmrlkyepdzaaoiczbamsvzyv",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code != 200:
        print(f"API请求失败，状态码：{response.status_code}")
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    print("正在解析API响应...")
    return response.json()['choices'][0]['message']['content']

def unified_interface(user_prompt, deep_think=False):
    """
    统一功能接口
    :param user_prompt: 用户原始提示
    :param deep_think: 是否需要深度思考，默认False
    :return: 返回最终回答
    """
    try:
        enhanced = enhance_prompt(user_prompt)
        model = "deepseek-ai/DeepSeek-R1" if deep_think else "deepseek-ai/DeepSeek-V3"
        final_response = get_final_response(enhanced, model)
        return final_response
    except Exception as e:
        print(f"处理出错：{str(e)}")
        raise Exception(f"接口调用失败: {str(e)}")

if __name__ == "__main__":
    # 获取用户输入
    user_prompt = input("请输入您的原始提示：").encode('utf-8').decode('utf-8')
    
    # 询问是否需要深度思考
    deep_think = input("是否需要深度思考？(是-1，否-0)：")
    
    try:
        # 第一步：优化提示
        write_to_file("正在优化提示...")
        enhanced = enhance_prompt(user_prompt)
        write_to_file("优化完成！")
        write_to_file("\n优化后的专业提示：")
        write_to_file(enhanced)
        
        # 根据深度思考选项设置模型
        model = "deepseek-ai/DeepSeek-R1" if deep_think == "1" else "deepseek-ai/DeepSeek-V3"
        
        write_to_file("正在生成回答...")
        final_response = get_final_response(enhanced, model)
        write_to_file("回答生成完成！")
        write_to_file("\n最终回答：")
        write_to_file(final_response)
        
    except Exception as e:
        error_msg = f"运行出错：{str(e)}"
        write_to_file(error_msg)
