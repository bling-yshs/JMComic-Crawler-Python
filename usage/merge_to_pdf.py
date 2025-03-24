from PIL import Image
import os
import glob

def find_image_directories(base_dir):
    """
    在基础目录下查找所有包含图片的目录
    
    Args:
        base_dir: 基础目录路径
    
    Returns:
        包含图片的目录列表
    """
    image_dirs = []
    for root, dirs, files in os.walk(base_dir):
        if any(file.lower().endswith(('.jpg', '.webp')) for file in files):
            image_dirs.append(root)
    return image_dirs

def get_manga_name(image_dir, base_dir):
    """
    从图片目录路径中提取漫画名称
    
    Args:
        image_dir: 图片目录的完整路径
        base_dir: 基础目录路径
    
    Returns:
        漫画名称
    """
    # 获取相对路径
    rel_path = os.path.relpath(image_dir, base_dir)
    # 分割路径
    parts = rel_path.split(os.sep)
    # 如果路径中包含数字目录（如 "1"），则使用其父目录作为漫画名
    if parts[-1].isdigit():
        return parts[-2]
    return parts[-1]

def convert_images_to_pdf(image_dir, output_pdf):
    """
    将指定目录下的所有图片按照文件名顺序合并成一个PDF文件
    
    Args:
        image_dir: 包含图片的目录路径
        output_pdf: 输出PDF文件的路径
    """
    # 获取所有图片文件并按名称排序（支持jpg和webp）
    jpg_files = glob.glob(os.path.join(image_dir, "*.[jJ][pP][gG]"))
    webp_files = glob.glob(os.path.join(image_dir, "*.[wW][eE][bB][pP]"))
    image_files = sorted(jpg_files + webp_files)
    
    if not image_files:
        print(f"在 {image_dir} 中没有找到jpg或webp图片文件")
        return False
    
    # 打开第一张图片
    first_image = Image.open(image_files[0]).convert('RGB')
    images = []
    
    print(f"正在处理目录: {image_dir}")
    print(f"找到 {len(image_files)} 张图片")
    
    # 转换其余的图片
    for image_file in image_files[1:]:
        try:
            image = Image.open(image_file).convert('RGB')
            images.append(image)
        except Exception as e:
            print(f"处理图片 {image_file} 时出错: {str(e)}")
            return False
    
    # 保存为PDF
    try:
        first_image.save(output_pdf, save_all=True, append_images=images)
        print(f"PDF文件已成功保存到: {output_pdf}")
        return True
    except Exception as e:
        print(f"保存PDF时出错: {str(e)}")
        return False

def process_all_manga(base_dir):
    """
    处理基础目录下的所有漫画
    
    Args:
        base_dir: 基础目录路径
    """
    # 查找所有包含图片的目录
    image_dirs = find_image_directories(base_dir)
    
    if not image_dirs:
        print(f"在 {base_dir} 中没有找到包含jpg或webp图片的目录")
        return
    
    print(f"找到 {len(image_dirs)} 个包含图片的目录")
    
    success_count = 0
    # 处理每个目录
    for image_dir in image_dirs:
        # 获取漫画名称
        manga_name = get_manga_name(image_dir, base_dir)
        # 创建PDF文件名
        pdf_name = f"{manga_name}.pdf"
        output_pdf = os.path.join(base_dir, pdf_name)
        
        print(f"\n开始处理漫画: {manga_name}")
        if convert_images_to_pdf(image_dir, output_pdf):
            print(f"成功将 {manga_name} 转换为PDF")
            success_count += 1
        else:
            print(f"转换 {manga_name} 失败")
    
    return success_count > 0

if __name__ == "__main__":
    # 设置基础目录
    base_dir = "/home/runner/work/jmcomic/download"
    
    # 处理所有漫画
    process_all_manga(base_dir) 