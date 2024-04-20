"""
한글 주석이 포함된 C/C++ 샘플코드가 일본어 환경에서 빌드가 불가능한 문제를 utf-8로 변환하여 해결
"""

import sys
from pathlib import Path
from os import walk


def is_utf8sig(filepath: str):
    """바이트오더마크가 있는지 확인"""
    with open(filepath, "rb") as f:
        return f.read(3) == b"\xef\xbb\xbf"


def convert(dirname: str):
    """폴더 안에 있는 파일을 유니코드로 변환"""
    for root, _, files in walk(Path.cwd() / dirname):
        for file in files:
            target_file = Path(root) / file
            if target_file.suffix in (".cpp", ".h", ".c") and not is_utf8sig(
                target_file
            ):
                print(f"Converting {target_file}")

                with open(target_file, "r", encoding="euc-kr") as f:
                    content = f.read()

                with open(target_file, "w", encoding="utf-8-sig") as f:
                    f.write(content)
            else:
                print(f"Skipping {target_file}")


if __name__ == "__main__":
    # 도움말 출력
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "-?", "-help", "--help"):
        print("Usage: python convert.py <folder_path>")
        sys.exit(0)

    # 인자가 부족한 경우 예외 처리
    if len(sys.argv) < 2:
        print("Usage: python convert.py <folder_path>")
        sys.exit(1)

    # 폴더가 존재하지 않는 경우 예외 처리
    folder_path = Path(sys.argv[1])
    if not folder_path.exists():
        print(f"Folder '{folder_path}' not found")
        sys.exit(1)

    folder_path = sys.argv[1]
    convert(folder_path)
