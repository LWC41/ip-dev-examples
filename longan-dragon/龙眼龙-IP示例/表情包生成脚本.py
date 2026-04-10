# 广西龙眼IP - 表情包生成脚本
# 批量生成表情包素材

import json

# 角色配置
CHARACTER_NAME = "龙眼龙 (Longan Long)"

# 表情包配色方案
COLORS = {
    "bg_yellow": "#FFFACD",  # 柠檬黄背景
    "bg_pink": "#FFB6C1",   # 浅粉色背景
    "bg_blue": "#87CEEB",   # 天蓝色背景
    "bg_white": "#FFFFFF",  # 纯白背景
    "primary": "#8B6914",   # 龙眼金
    "accent": "#FF6347",    # 珊瑚红
    "green": "#32CD32"      # 鲜绿色
}

# 必备表情（8个）
EXPRESSIONS_BASIC = {
    "开心": {
        "description": "大笑表情，眼睛弯成月牙，嘴巴张开呈心形，双手举过头顶欢呼",
        "tags": "happy, laughing, cheerful, excited",
        "bg_color": COLORS["bg_yellow"]
    },
    "难过": {
        "description": "哭泣表情，眼泪滴落，眉头皱起，嘴角下垂，双手捂脸",
        "tags": "sad, crying, upset, tears",
        "bg_color": COLORS["bg_blue"]
    },
    "生气": {
        "description": "小拳头握在腰间，腮帮鼓起，眉毛竖起，可爱但不凶",
        "tags": "angry, pouting, annoyed",
        "bg_color": COLORS["bg_pink"]
    },
    "惊讶": {
        "description": "嘴巴呈O型，眼睛瞪大，双手张开，震惊表情",
        "tags": "surprised, shocked, amazed",
        "bg_color": COLORS["bg_white"]
    },
    "害羞": {
        "description": "脸红通红，双手捂脸，透过手指缝偷看，脚尖对脚尖",
        "tags": "shy, blushing, embarrassed",
        "bg_color": COLORS["bg_pink"]
    },
    "无语": {
        "description": "嘴角下垂，眼睛翻白，一只手扶额，无奈表情",
        "tags": "speechless, facepalm,无奈",
        "bg_color": COLORS["bg_white"]
    },
    "爱你": {
        "description": "比心动作，双手比心形，粉色爱心背景，甜蜜表情",
        "tags": "love, heart, sweet, 爱你",
        "bg_color": COLORS["bg_pink"]
    },
    "加油": {
        "description": "握拳向上，充满力量，眼神坚定，红色背景",
        "tags": "cheer up, fighting, 加油",
        "bg_color": COLORS["accent"]
    }
}

# 特殊表情（5个）
EXPRESSIONS_SPECIAL = {
    "想你了": {
        "description": "抱着心形图案，眼神温柔，粉色背景，治愈系",
        "tags": "miss you, 想你了, longing",
        "bg_color": COLORS["bg_pink"]
    },
    "晚安": {
        "description": "戴睡帽，闭眼睡觉，小绿叶也睡觉，星星背景，温馨",
        "tags": "goodnight, sleep, 晚安",
        "bg_color": "#191970"  # 深蓝色
    },
    "早安": {
        "description": "伸懒腰，阳光照射，充满活力，黄色背景",
        "tags": "good morning, 早安, energetic",
        "bg_color": COLORS["bg_yellow"]
    },
    "好吃": {
        "description": "流口水，眼睛发光，双手抱住龙眼，馋嘴表情",
        "tags": "yummy, delicious, 好吃, drooling",
        "bg_color": COLORS["bg_yellow"]
    },
    "加油鸭": {
        "description": "小鸭子造型，因为'加油鸭'谐音，可爱搞笑",
        "tags": "加油鸭, duck, cute",
        "bg_color": COLORS["bg_yellow"]
    }
}

def generate_sticker_prompts(expressions_dict, output_file="sticker_prompts.json"):
    """
    生成所有表情包的提示词
    """
    all_prompts = {}
    
    # 处理必备表情
    for exp_name, exp_info in expressions_dict.items():
        prompt = f"""
{CHARACTER_NAME} {exp_name}表情包设计

角色描述:
{exp_info['description']}

风格要求:
- 可爱卡通风格，Q版比例
- 圆润柔和的线条
- 色彩符合IP视觉规范
- 主色: {COLORS['primary']}
- 背景色: {exp_info['bg_color']}

规格:
- 尺寸: 512x512px
- 格式: PNG透明背景
- 四周留20px padding
- 适合微信表情包使用

标签: {exp_info['tags']}, cute, healing, fruit character, longan, guangxi, cartoon, sticker
"""
        all_prompts[exp_name] = prompt
    
    # 保存为JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_prompts, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 表情包提示词已保存到: {output_file}")
    return all_prompts

def generate_wechat_pack_info():
    """
    生成微信表情包包信息
    """
    wechat_info = {
        "package_name": "龙眼龙日常",
        "package_intro": "可爱的广西龙眼精灵，陪你度过每一天！",
        "total_count": 16,  # 微信需要16个或更多
        "expressions": list(EXPRESSIONS_BASIC.keys()) + list(EXPRESSIONS_SPECIAL.keys()),
        "cover_design": "封面图需要包含完整IP名称'龙眼龙'和主角色形象",
        "upload_status": "待上传"
    }
    
    with open("wechat_pack_info.json", 'w', encoding='utf-8') as f:
        json.dump(wechat_info, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 微信表情包信息已保存到: wechat_pack_info.json")
    return wechat_info

def print_expression_summary():
    """
    打印表情包清单
    """
    print("\n" + "="*60)
    print("龙眼龙表情包清单")
    print("="*60)
    
    print("\n【必备表情（8个）】")
    for i, (name, info) in enumerate(EXPRESSIONS_BASIC.items(), 1):
        print(f"{i}. {name}: {info['description'][:30]}...")
    
    print("\n【特殊表情（5个）】")
    for i, (name, info) in enumerate(EXPRESSIONS_SPECIAL.items(), 1):
        print(f"{i}. {name}: {info['description'][:30]}...")
    
    print(f"\n总计: {len(EXPRESSIONS_BASIC) + len(EXPRESSIONS_SPECIAL)} 个表情包")
    print("="*60)

# 使用示例
if __name__ == "__main__":
    # 打印表情包清单
    print_expression_summary()
    
    # 生成所有表情包提示词
    print("\n" + "="*60)
    print("生成表情包提示词")
    print("="*60)
    
    # 合并所有表情
    all_expressions = {**EXPRESSIONS_BASIC, **EXPRESSIONS_SPECIAL}
    prompts = generate_sticker_prompts(all_expressions)
    
    # 生成微信表情包信息
    print("\n" + "="*60)
    print("生成微信表情包包信息")
    print("="*60)
    wechat_info = generate_wechat_pack_info()
    
    print("\n" + "="*60)
    print("✓ 表情包配置生成完成！")
    print("="*60)
    print("\n下一步：")
    print("1. 使用生成的提示词调用AI绘图API生成表情包")
    print("2. 将生成的图片整理成微信表情包格式")
    print("3. 上传到微信表情开放平台")
