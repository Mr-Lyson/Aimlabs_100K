from PIL import Image
import pytesseract
import os
import json
import pyautogui

# ======================
# 配置常量
# ======================
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR\tessdata"
BASE_RESOLUTION = (1920, 1080)  # 基准分辨率 (1080p)
THRESHOLD = 150  # 二值化阈值
PSM_MODE = 7  # Tesseract 页面分割模式
OEM_MODE = 1  # Tesseract OCR引擎模式

# ======================
# 区域定义（基于1080p）
# ======================
REGIONS_1080P = {
    "PTS": (630, 20, 140, 50),
    "Time": (920, 20, 100, 50),
    "Accuracy": (1180, 20, 70, 50)
}


# ======================
# 核心函数
# ======================
def get_scaled_regions(base_regions, screen_res):
    """根据屏幕分辨率缩放区域坐标"""
    scaled_regions = {}
    screen_w, screen_h = screen_res
    scale_x = screen_w / BASE_RESOLUTION[0]
    scale_y = screen_h / BASE_RESOLUTION[1]

    for name, (left, top, w, h) in base_regions.items():
        scaled_regions[name] = (
            int(left * scale_x),
            int(top * scale_y),
            int(w * scale_x),
            int(h * scale_y)
        )
    return scaled_regions


def process_region(image, region_coords, threshold):
    """处理单个区域图像"""
    left, top, width, height = region_coords
    region = image.crop((left, top, left + width, top + height))

    # 图像预处理
    region = region.convert("L")
    return region.point(lambda p: p > threshold and 255)


def ocr_recognize(image, config):
    """执行OCR识别"""
    return pytesseract.image_to_string(image, config=config).strip()


def process_single_image(image_path, regions, output_dir):
    """处理单张图片"""
    # 创建输出目录
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, image_name)
    os.makedirs(output_path, exist_ok=True)

    # 处理图片
    results = {}
    img = Image.open(image_path)

    for region_name, coords in regions.items():
        # 图像处理
        processed_img = process_region(img, coords, THRESHOLD)

        # 保存处理后的图像
        img_save_path = os.path.join(output_path, f"{region_name}_processed.png")
        processed_img.save(img_save_path)

        # OCR识别
        text = ocr_recognize(processed_img, f'--psm {PSM_MODE} --oem {OEM_MODE}')
        results[region_name] = text

        print(f"[{region_name}] 识别结果: {text}")

    # 保存JSON结果
    json_path = os.path.join(output_path, "results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"√ 处理完成: {image_path} -> {output_path}\n")
    return json_path


# ======================
# 主程序
# ======================
def main(input_dir, output_dir):
    """主处理函数"""
    # 初始化Tesseract
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX

    # 获取缩放后的区域坐标
    screen_res = pyautogui.size()
    regions = get_scaled_regions(REGIONS_1080P, screen_res)
    print(f"屏幕分辨率: {screen_res[0]}x{screen_res[1]}")
    print("调整后的区域坐标:", regions)

    # 处理所有图片
    processed_files = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            try:
                result_path = process_single_image(image_path, regions, output_dir)
                processed_files.append(result_path)
            except Exception as e:
                print(f"× 处理失败: {filename} - {str(e)}")

    print(f"处理完成，共处理 {len(processed_files)} 张图片")
    return processed_files


if __name__ == "__main__":
    # 配置输入输出路径
    INPUT_DIR = "../input"
    OUTPUT_DIR = "./result"

    # 运行主程序
    main(INPUT_DIR, OUTPUT_DIR)