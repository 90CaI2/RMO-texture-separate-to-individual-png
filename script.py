import os
import argparse
from PIL import Image
import numpy as np


def process_texture_channels(input_folder, output_folder, invert_channels=None, create_subfolders=False):
    """
    Batch process textures containing '_rmo' in the filename, separate RGBA channels,
    and save as individual grayscale images with corresponding suffixes.

    批量处理文件名中包含'_rmo'的贴图，分离RGBA通道，并保存为带有对应后缀的单独灰度图。

    Args:
        input_folder (str): Path to the folder containing input images / 输入图片所在文件夹路径
        output_folder (str): Path to the folder where processed images will be saved / 处理后的图片保存文件夹路径
        invert_channels (list, optional): List of channels to invert (e.g., ['r', 'g']) / 需要反相的通道列表(例如: ['r', 'g'])
        create_subfolders (bool, optional): Whether to create subfolders for each image / 是否为每张图片创建单独文件夹
    """

    # Ensure output folder exists / 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define channel suffixes and their corresponding indices / 定义通道后缀及其对应的索引
    channel_info = {
        '_r': 0,  # Red channel / 红色通道
        '_g': 1,  # Green channel / 绿色通道
        '_b': 2,  # Blue channel / 蓝色通道
        '_a': 3  # Alpha channel / 透明度通道
    }

    # Supported image formats / 支持的图片格式
    supported_formats = ('.png', '.jpg', '.jpeg', '.tga', '.tif', '.tiff', '.bmp', '.exr')

    # Process each file in the input folder / 处理输入文件夹中的每个文件
    for filename in os.listdir(input_folder):
        # Check if file contains '_rmo' and is a supported image format / 检查文件是否包含'_rmo'且是支持的图片格式
        if '_rmo' in filename.lower() and filename.lower().endswith(supported_formats):
            try:
                # Open the image / 打开图片
                img_path = os.path.join(input_folder, filename)
                img = Image.open(img_path)

                # Convert to RGBA if necessary / 如果需要则转换为RGBA模式
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Split into channels / 分离通道
                channels = img.split()

                # Get base filename without extension / 获取不含扩展名的基本文件名
                base_name = os.path.splitext(filename)[0]

                # Determine output directory / 确定输出目录
                if create_subfolders:
                    # Create subfolder with base name / 使用基本文件名创建子文件夹
                    subfolder_path = os.path.join(output_folder, base_name)
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)
                    output_dir = subfolder_path
                else:
                    output_dir = output_folder

                # Process each channel / 处理每个通道
                for suffix, channel_index in channel_info.items():
                    # Check if channel exists (some images might not have alpha) / 检查通道是否存在(有些图片可能没有alpha通道)
                    if channel_index < len(channels):
                        channel = channels[channel_index]

                        # Invert channel if specified / 如果指定则反相通道
                        if invert_channels and suffix[1] in invert_channels:  # suffix[1] gets 'r', 'g', 'b', or 'a'
                            channel = Image.fromarray(255 - np.array(channel))

                        # Create output filename / 创建输出文件名
                        output_filename = f"{base_name}{suffix}.png"
                        output_path = os.path.join(output_dir, output_filename)

                        # Save as grayscale image / 保存为灰度图
                        channel.save(output_path)
                        print(f"Saved: {output_path}")

                print(f"Processed: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


# 直接调用函数处理特定文件夹
if __name__ == "__main__":
    # 定义输入和输出文件夹路径
    input_dir = r""
    output_dir = input_dir  # 输出文件夹与输入相同

    # 调用处理函数
    process_texture_channels(
        input_folder=input_dir,
        output_folder=output_dir,
        invert_channels=['r'],  # 反相红色通道
        create_subfolders=True  # 为每个图片创建单独文件夹
    )