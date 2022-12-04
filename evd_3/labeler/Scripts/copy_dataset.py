import os
import shutil

dataset_src_path = os.path.join("evd_3", "original_dataset")
dataset_dst_path = os.path.join("evd_3", "labeler", "dataset")

shutil.copytree(dataset_src_path, dataset_dst_path)
