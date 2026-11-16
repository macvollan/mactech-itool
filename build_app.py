"""
PyInstaller Compilation Script for MacTech iTool
MacTech Solutions Lab
"""

import os
import sys
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    print("=" * 60)
    print("  MacTech iTool - Standalone Executable Builder")
    print("  MacTech Solutions Lab")
    print("=" * 60)

    # 1. Clean previous build artifacts
    for folder in ["build", "dist"]:
        fpath = os.path.join(BASE_DIR, folder)
        if os.path.exists(fpath):
            shutil.rmtree(fpath, ignore_errors=True)

    # 2. Locate customtkinter package directory for data bundling
    import customtkinter
    ctk_path = os.path.dirname(customtkinter.__file__)

    # 3. Construct PyInstaller command
    icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
    assets_path = os.path.join(BASE_DIR, "assets")
    sep = ";" if sys.platform == "win32" else ":"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=MacTech_iTool",
        "--windowed",
        "--onedir",
        f"--add-data={ctk_path}{sep}customtkinter",
        f"--add-data={assets_path}{sep}assets",
    ]

    if os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")

    cmd.append(os.path.join(BASE_DIR, "main.py"))

    print(f"[BUILD] Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=BASE_DIR)
    if res.returncode == 0:
        print("\n✔ PyInstaller build succeeded!")
        dist_dir = os.path.join(BASE_DIR, "dist", "MacTech_iTool")
        print(f"Artifacts ready in: {dist_dir}")
    else:
        print(f"\n[!] Build failed with exit code: {res.returncode}")

if __name__ == "__main__":
    build()
