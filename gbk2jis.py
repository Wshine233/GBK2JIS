# ------ 配置项 ------
# 原文件名编码方式
input_name_encoding = "gbk"

# 输出文件名编码方式
output_name_encoding = "shift-jis"

# 是否递归处理子文件夹
recursion = True

# END OF CONFIGURATION

# ------ import ------
import sys
from pathlib import Path
import os


# ------ functions ------
has_error = False


def log_error(error_message: str):
    global has_error
    has_error = True
    print(f"[ERROR] {error_message}")
    print()


def log_error_with_path(error_message: str, path: Path):
    log_error(f"在处理文件时发生错误: {path}\n{error_message}")


def encoding_convert(text: str, input_encoding: str, output_encoding: str) -> str:
    decoded_text = text.encode(input_encoding).decode(output_encoding)
    return decoded_text


def rename_file(input_file_path: Path, output_file_path: Path):
    os.rename(input_file_path, output_file_path)


# ------ Main ------
def main(input_file_path: Path) -> Path:
    try:
        output_file_path = input_file_path.with_name(
            encoding_convert(input_file_path.name, input_name_encoding, output_name_encoding))
        rename_file(input_file_path, output_file_path)
        return output_file_path
    except Exception as e:
        log_error_with_path(str(e), input_file_path)
        return input_file_path


def main_recursive(input_file_path: Path):
    out_path = main(input_file_path)
    if not out_path.exists():
        log_error(f"找不到文件: {out_path}")
    if not out_path.is_dir():
        return
    for path in out_path.iterdir():
        main_recursive(path)


def check(input_file_path: Path):
    try:
        print(f"----------------------")
        print(f"原文件名：{input_file_path.name}")
        print(f"将被改为：{encoding_convert(input_file_path.name, input_name_encoding, output_name_encoding)}")
        print()
    except Exception as e:
        log_error_with_path(str(e), input_file_path)


def check_recursive(input_file_path: Path):
    check(input_file_path)
    if not input_file_path.is_dir():
        return
    for path in input_file_path.iterdir():
        check_recursive(path)


def start():
    paths = list(map(lambda x: Path(x), sys.argv[1:]))

    print("输入文件名的编码：" + input_name_encoding)
    print("输出文件名的编码：" + output_name_encoding)
    print("是否修改子文件夹：" + str(recursion))
    print()

    for p in paths:
        if recursion:
            check_recursive(p)
        else:
            check(p)

    if has_error:
        print("出现了一些错误，具体请查看上方信息")
        print("这些出错的文件会被跳过，不会被重命名（但你后续可能依然看到该文件的报错）")

    if input(f"你确定开始转换吗？请记得做好文件备份！！！输入y继续 (y/n)：").lower() != "y":
        print("操作已取消")
        input("Press Enter to exit")
        exit(0)

    print()
    for p in paths:
        if recursion:
            main_recursive(p)
        else:
            main(p)

    print()
    print("完成！")
    input("Press Enter to exit")


if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        log_error(str(e))
        input("Press Enter to exit")



