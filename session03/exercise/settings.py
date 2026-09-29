"""設定を読む。APIキーをこのファイルに書かない。"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# 各アプリ専用の.envを読む。Codespaces Secretsの環境変数を優先する。
load_dotenv(BASE_DIR / '.env')
DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'
MODEL = os.getenv('OPENAI_MODEL', 'gpt-6-luna')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
DATABASE = BASE_DIR / 'classroom.db'
