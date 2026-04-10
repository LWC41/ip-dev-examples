# 广西龙眼IP - 3D模型生成脚本
# 使用Meshy AI API生成角色3D模型

import os
import requests
import time
import json

class LonganLong3DGenerator:
    def __init__(self):
        self.api_key = os.getenv('MESHY_API_KEY')
        if not self.api_key:
            raise ValueError("请先设置 MESHY_API_KEY 环境变量")
        self.base_url = "https://api.meshy.ai/v1"

    def create_character_prompt(self, character_name, description):
        """
        构建角色3D生成提示词
        """
        prompt = f"""
A 3D character of {character_name}, {description}.

Appearance:
- Round and cute shape, 2.5 head proportion (Q-style)
- Main color: Golden brown (#8B6914) for body
- Bright yellow (#D4A017) highlights
- Dark brown (#654321) shadows
- Big round eyes, black pupils with white highlights
- Small smiley mouth, can show teeth
- Small green leaf on top of head
- Cheeks with light blush
- Body with delicate fruit texture
- Small red scarf around neck
- Slightly protruding round belly

Style:
- Cute cartoon style, healing and child-friendly
- Soft diffuse lighting from top-left
- Round smooth textures
- High quality 8k render
- Suitable for animation and merchandise

View:
- Default standing pose, hands at sides
- Small smile expression
- Bright cheerful atmosphere

Tags: cute, healing, child-friendly, high quality, 8k, cartoon, Q-style, fruit character, longan, guangxi
"""
        return prompt

    def create_scene_prompt(self, scene_name, description):
        """
        构建场景3D生成提示词
        """
        prompt = f"""
A 3D scene of {scene_name}, {description}.

Environment:
- Location: Sweet Fruit Town, near Nanning Guangxi
- Main elements: {description}
- Time: Morning, soft warm sunlight
- Weather: Clear and sunny

Style:
- Cartoon scene style, warm and healing
- Soft diffuse lighting
- Rich but not overwhelming details
- Dreamy fairytale atmosphere

Composition:
- Camera angle: Eye-level or slight bird's eye view
- Background: Blue sky with white clouds
- Foreground: Detailed scene elements

Tags: high quality, 3D render, cartoon scene, warm atmosphere, fruit town, guangxi style, cute, healing
"""
        return prompt

    def create_text_to_3d(self, prompt, model_type="figure"):
        """
        创建文本到3D的生成任务
        """
        url = f"{self.base_url}/text-to-3d"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "model_type": model_type,
            "quality": "standard"
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        task_id = response.json()["task_id"]
        print(f"✓ 3D生成任务已创建，Task ID: {task_id}")
        return task_id

    def check_task_status(self, task_id):
        """检查任务状态"""
        url = f"{self.base_url}/tasks/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def wait_for_completion(self, task_id, timeout=600, interval=30):
        """
        等待任务完成
        """
        elapsed = 0
        while elapsed < timeout:
            status = self.check_task_status(task_id)
            state = status.get("status", "unknown")

            if state == "succeeded":
                print(f"✓ 3D生成完成！")
                return status
            elif state == "failed":
                raise Exception(f"3D生成失败: {status.get('error', 'Unknown error')}")
            elif state == "processing":
                progress = status.get("progress", 0)
                print(f"⏳ 3D生成中... 进度: {progress}%")

            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"任务超时（{timeout}秒）")

    def download_model(self, model_url, output_path):
        """下载3D模型文件"""
        print(f"📥 正在下载模型到: {output_path}")
        response = requests.get(model_url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✓ 模型下载完成！")
        return output_path

    def generate_character_family(self, characters, output_dir):
        """
        批量生成角色家族的3D模型
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        results = []

        for character in characters:
            name = character["name"]
            description = character["description"]

            print(f"\n{'='*50}")
            print(f"开始生成角色: {name}")
            print(f"{'='*50}")

            try:
                # 创建生成任务
                prompt = self.create_character_prompt(name, description)
                task_id = self.create_text_to_3d(prompt, model_type="figure")

                # 等待完成
                result = self.wait_for_completion(task_id)

                # 下载模型
                model_url = result["model_urls"].get("glb") or result["model_urls"].get("obj")
                if model_url:
                    output_path = os.path.join(output_dir, f"{name}.glb")
                    self.download_model(model_url, output_path)

                    results.append({
                        "name": name,
                        "status": "success",
                        "path": output_path,
                        "task_id": task_id
                    })
                else:
                    raise Exception("未找到模型下载链接")

            except Exception as e:
                print(f"✗ 生成 {name} 失败: {e}")
                results.append({
                    "name": name,
                    "status": "failed",
                    "error": str(e)
                })

        return results

    def generate_scenes(self, scenes, output_dir):
        """
        批量生成场景的3D模型
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        results = []

        for scene in scenes:
            name = scene["name"]
            description = scene["description"]

            print(f"\n{'='*50}")
            print(f"开始生成场景: {name}")
            print(f"{'='*50}")

            try:
                # 创建生成任务
                prompt = self.create_scene_prompt(name, description)
                task_id = self.create_text_to_3d(prompt, model_type="scene")

                # 等待完成
                result = self.wait_for_completion(task_id)

                # 下载模型
                model_url = result["model_urls"].get("glb") or result["model_urls"].get("obj")
                if model_url:
                    output_path = os.path.join(output_dir, f"{name}.glb")
                    self.download_model(model_url, output_path)

                    results.append({
                        "name": name,
                        "status": "success",
                        "path": output_path,
                        "task_id": task_id
                    })
                else:
                    raise Exception("未找到模型下载链接")

            except Exception as e:
                print(f"✗ 生成 {name} 失败: {e}")
                results.append({
                    "name": name,
                    "status": "failed",
                    "error": str(e)
                })

        return results


# 使用示例
if __name__ == "__main__":
    # 初始化生成器
    generator = LonganLong3DGenerator()

    # 角色配置
    characters = [
        {
            "name": "Longan-Long",
            "description": "A cute anthropomorphic Guangxi longan character, round shape, golden brown skin, big eyes, small green leaf on top, wearing red scarf, cartoon style"
        },
        {
            "name": "Litchi-Lily",
            "description": "A cute anthropomorphic litchi character, round shape, red textured skin with bumps, big eyes, two small green leaves on top, wearing pink dress, cartoon style"
        },
        {
            "name": "Mango-Max",
            "description": "A cute anthropomorphic mango character, oval shape, golden yellow skin, smooth texture, big eyes, small green stem on top, wearing blue baseball cap, cartoon style"
        }
    ]

    # 场景配置
    scenes = [
        {
            "name": "Longan-Orchard",
            "description": "Ancient longan orchard with hundred-year-old trees, grandfather's small wooden house, sunny morning with light filtering through leaves, warm and peaceful atmosphere"
        },
        {
            "name": "Creek-Bank",
            "description": "Clear creek flowing through the orchard, small stones and wildflowers, summer setting, water with small fish, playful and refreshing"
        },
        {
            "name": "Town-Square",
            "description": "Central square of Sweet Fruit Town, huge banyan tree for gathering, small shops selling fruits and desserts, festive atmosphere"
        }
    ]

    # 批量生成角色
    print("\n" + "="*60)
    print("开始生成角色3D模型")
    print("="*60)
    character_results = generator.generate_character_family(
        characters,
        output_dir="3d-models/characters"
    )

    # 批量生成场景
    print("\n" + "="*60)
    print("开始生成场景3D模型")
    print("="*60)
    scene_results = generator.generate_scenes(
        scenes,
        output_dir="3d-models/scenes"
    )

    # 保存生成报告
    report = {
        "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "characters": character_results,
        "scenes": scene_results
    }

    with open("3d-generation-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("✓ 所有3D模型生成完成！")
    print("="*60)
    print(f"报告已保存到: 3d-generation-report.json")
