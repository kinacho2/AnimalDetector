import os
import random
from PIL import Image, ImageEnhance

class AugmentationConfig:
    def __init__(
        self,
        num_random=10,
        contrast_range=(0.8, 1.2),
        brightness_range=(0.8, 1.2),
        saturation_range=(0.8, 1.2),
        rotation_prob=0.0,
        use_random=True
    ):
        self.num_random = num_random
        self.contrast_range = contrast_range
        self.brightness_range = brightness_range
        self.saturation_range = saturation_range
        self.use_random = use_random
        self.rotation_prob = rotation_prob


def load_image(path):
    return Image.open(path).convert("RGB")

def save_image(img, output_path):
    img.save(output_path)

def ensure_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_images_from_folder(folder):
    valid_ext = (".jpg", ".jpeg", ".png")
    return [
        f for f in os.listdir(folder)
        if f.lower().endswith(valid_ext)
    ]

def rotate_image(img, angle):
    return img.rotate(angle, expand=True)

def apply_enhancements(img, contrast=1.0, brightness=1.0, saturation=1.0):
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Color(img).enhance(saturation)
    return img

def get_random_factor(value_range):
    return random.uniform(*value_range)

def format_float(value):
    return f"{value:.2f}"

def build_rotation_name(base_name, angle):
    return f"{base_name}_R{angle}.jpg"

def build_augmentation_name(base_name, contrast, brightness, saturation):
    return (
        f"{base_name}_"
        f"C{format_float(contrast)}_"
        f"B{format_float(brightness)}_"
        f"S{format_float(saturation)}.jpg"
    )

def generate_rotations(img, base_name, output_dir):
    angles = [90, 180, 270]
    generated_paths = []

    for angle in angles:
        rotated = rotate_image(img, angle)
        filename = build_rotation_name(base_name, angle)
        output_path = os.path.join(output_dir, filename)
        save_image(rotated, output_path)
        generated_paths.append(output_path)

    return generated_paths

def generate_random_variants(img, base_name, output_dir, config: AugmentationConfig):
    generated_paths = []
    angles = [0, 90, 180, 270]

    for _ in range(config.num_random):
        if config.use_random:
            contrast = get_random_factor(config.contrast_range)
            brightness = get_random_factor(config.brightness_range)
            saturation = get_random_factor(config.saturation_range)
        else:
            contrast = sum(config.contrast_range) / 2
            brightness = sum(config.brightness_range) / 2
            saturation = sum(config.saturation_range) / 2

        new_img = apply_enhancements(
            img,
            contrast=contrast,
            brightness=brightness,
            saturation=saturation
        )

        angle = 0
        if random.random() < config.rotation_prob:
            angle = random.choice(angles)
            if angle != 0:
                new_img = rotate_image(new_img, angle)

        filename = (
            f"{base_name}_"
            f"C{format_float(contrast)}_"
            f"B{format_float(brightness)}_"
            f"S{format_float(saturation)}"
        )

        if angle != 0:
            filename += f"_R{angle}"

        filename += ".jpg"

        output_path = os.path.join(output_dir, filename)

        save_image(new_img, output_path)
        generated_paths.append(output_path)

    return generated_paths

def process_images(input_dir, output_dir, config: AugmentationConfig):
    ensure_output_dir(output_dir)
    images = get_images_from_folder(input_dir)

    for img_name in images:
        input_path = os.path.join(input_dir, img_name)
        base_name = os.path.splitext(img_name)[0]

        try:
            img = load_image(input_path)
            generate_rotations(img, base_name, output_dir)
            generate_random_variants(img, base_name, output_dir, config)
            print(f"Procesada: {img_name}")
        except Exception as e:
            print(f"Error con {img_name}: {e}")

def clear_output_dir(path):
    if not os.path.exists(path):
        return
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    input_folder = "picsIn"
    output_folder = "picsOut"

    clear_output_dir(output_folder)

    config = AugmentationConfig(
        num_random=20,
        contrast_range = (0.3, 1.8),
        brightness_range = (0.3, 1.8),
        saturation_range = (0.3, 1.8),
        rotation_prob=0.3,
        use_random=True
    )

    process_images(input_folder, output_folder, config)