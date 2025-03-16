from prompter import unified_interface

# 测试用例1：普通模式
try:
    print("测试普通模式...")
    result = unified_interface("请解释量子计算的基本原理")
    print("测试结果：")
    print(result)
except Exception as e:
    print(f"测试失败：{str(e)}")

# 测试用例2：深度思考模式
try:
    print("\n测试深度思考模式...")
    result = unified_interface("请详细分析人工智能的发展趋势", deep_think=True)
    print("测试结果：")
    print(result)
except Exception as e:
    print(f"测试失败：{str(e)}")