"""config.py — Configuration loading."""
import os
from pathlib import Path
def load_config(env_path=".env"):
    path = Path(env_path)
    if path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=path, override=False)
        except ImportError:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"'))
