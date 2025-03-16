import re

import requests
from prompter import unified_interface

# 定义function calling的工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "unified_interface",
            "description": "优化用户提示，使其更清晰、具体、结构化",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_prompt": {
                        "type": "string",
                        "description": "用户输入的原始提示"
                    },
                    "deep_think": {
                        "type": "boolean",
                        "description": "是否需要深度思考，默认False"
                    }
                },
                "required": ["user_prompt"]
            }
        }
    }
]

def should_enhance(prompt):
    """
    通过API调用大模型判断是否需要强化提示
    :param prompt: 用户输入的原始提示
    :return: 返回布尔值，表示是否需要强化
    """
    print("开始分析提示是否需要强化...")
    system_prompt = """你是一个提示词分析专家，请根据用户输入的提示判断是否需要强化。
    强化标准：
    1. 提示过于笼统或模糊
    2. 缺少具体背景或要求
    3. 输出格式不明确
    4. 缺少限制条件
    如果符合以上任一标准，返回True，否则返回False。"""
    
    print("正在准备API请求...")
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "tools": tools,
        "temperature": 0.3,
        "max_tokens": 128,
        "top_p": 0.9
    }
    
    print("正在发送API请求...")
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
    print("原始响应内容：", response.text)
    decision = response.json()['choices'][0]['message']
    print("解析后的数据结构：", decision)
    if decision.tool_calls:
        tool_call = decision.tool_calls[0]
        if tool_call.function.name == "unified_interface":
            print("检测到需要强化提示，正在调用unified_interface...")
            return unified_interface(prompt)
    print("提示无需强化，返回原始提示")
    return prompt

def analyze_prompt(user_input):
    """
    分析用户输入，判断是否需要调用unified_interface进行提示优化
    :param user_input: 用户输入的原始提示
    :return: 返回处理后的提示
    """
    print("开始分析用户提示...")
    try:
        if should_enhance(user_input):
            print("提示需要优化，正在处理...")
            return unified_interface(user_input)
        print("提示无需优化，返回原始提示")
        return user_input
    except Exception as e:
        print(f"分析出错: {str(e)}")
        return user_input

if __name__ == "__main__":
    # 获取用户输入
    user_prompt = input("请输入您的原始提示：").encode('utf-8').decode('utf-8')
    
    # 分析并处理提示
    processed_prompt = analyze_prompt(user_prompt)
    
    # 输出结果
    print("\n处理后的提示：")
    print(processed_prompt)