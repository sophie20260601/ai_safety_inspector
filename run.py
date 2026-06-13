"""AI Safety Inspector —— 一键运行脚本。"""

import os
import sys

# 确保项目根目录在 path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# 先尝试项目目录的 .env，再尝试上级目录
env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(env_path):
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

if not os.getenv("DEEPSEEK_API_KEY"):
    print("=" * 60)
    print("  [错误] 未找到 DEEPSEEK_API_KEY")
    print("=" * 60)
    print()
    print("  请在项目目录创建 .env 文件并配置:")
    print("  DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here")
    print()
    print("  或复制 .env.example 后填写:")
    print("  cp .env.example .env")
    sys.exit(1)

from main import main

if __name__ == "__main__":
    main()
