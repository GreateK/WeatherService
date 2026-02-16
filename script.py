import os
import subprocess
import venv
from pathlib import Path

ROOT = Path(__file__).parent
VENV_DIR = ROOT / ".venv"


def run(cmd, env=None):
    subprocess.check_call(cmd, shell=True, env=env)


def python_bin():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def uvicorn_bin():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "uvicorn.exe"
    return VENV_DIR / "bin" / "uvicorn"


def create_venv():
    if not VENV_DIR.exists():
        print("📦 Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)


def install_requirements():
    print("⬇ Installing dependencies...")
    run(f'"{python_bin()}" -m pip install --upgrade pip')
    run(f'"{python_bin()}" -m pip install -r requirements.txt')


def start_server():
    print("\n🚀 Starting server...")
    print("👉 http://127.0.0.1:8000")
    print("👉 http://127.0.0.1:8000/docs\n")

    python = python_bin()

    cmd = [
        str(python),
        "-m",
        "uvicorn",
        "src.main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]

    try:
        subprocess.call(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")


if __name__ == "__main__":
    create_venv()
    install_requirements()
    start_server()
