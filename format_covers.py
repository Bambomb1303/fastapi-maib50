import os
import re
from pathlib import Path

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        # 检查是否是5位数字的文件名（不含扩展名）
        name, ext = os.path.splitext(filename)
        if re.fullmatch(r'\d{5}', name):
            new_name = name[1:] + ext  # 去掉第一位
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)

            if os.path.exists(new_path):
                print(f"跳过：{new_path} 已存在")
            else:
                os.rename(old_path, new_path)
                print(f"已重命名：{filename} -> {new_name}")

if __name__ == '__main__':
    directory = str(Path(__file__).resolve().parent / "static" / "img" / "covers")
    rename_files_in_directory(directory)
