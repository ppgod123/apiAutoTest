import os
import shutil


def copy_move_file(src_file, dst_path):
    if not os.path.isfile(src_file):
        print(f"{src_file}不存在！")
    else:
        fpath, fname = os.path.split(src_file)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        dst_file = os.sep.join([dst_path, fname])
        shutil.copyfile(src_file, dst_file)
        print(f"move {src_file}-> {dst_file}")
