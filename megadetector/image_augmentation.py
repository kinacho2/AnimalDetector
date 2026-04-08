import os
import random
from PIL import Image, ImageEnhance, ImageFilter

class AugmentationConfig:
    def __init__(
        self,
        num_random=10,
        contrast_range=(0.8, 1.2),
        brightness_range=(0.8, 1.2),
        saturation_range=(0.8, 1.2),
        zoom_range=(0.8, 1.2),
        blur_range=(0.0, 1.5),
        blur_prob=0.5,
        flip_prob=0.5,
        use_random=True
    ):
        self.num_random = num_random
        self.contrast_range = contrast_range
        self.brightness_range = brightness_range
        self.saturation_range = saturation_range
        self.zoom_range = zoom_range
        self.blur_range = blur_range
        self.blur_prob = blur_prob
        self.use_random = use_random
        self.flip_prob = flip_prob


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

def flip_horizontal(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)

def apply_zoom(img, zoom_factor):
    w, h = img.size
    new_w = int(w * zoom_factor)
    new_h = int(h * zoom_factor)
    resized = img.resize((new_w, new_h), Image.BICUBIC)

    if zoom_factor > 1.0:
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        right = left + w
        bottom = top + h
        return resized.crop((left, top, right, bottom))
    else:
        new_img = Image.new("RGB", (w, h))
        left = (w - new_w) // 2
        top = (h - new_h) // 2
        new_img.paste(resized, (left, top))
        return new_img

def apply_blur(img, radius):
    return img.filter(ImageFilter.GaussianBlur(radius))

def apply_enhancements(img, contrast=1.0, brightness=1.0, saturation=1.0):
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Color(img).enhance(saturation)
    return img

def get_random_factor(value_range):
    return random.uniform(*value_range)

def format_float(value):
    return f"{value:.2f}"

def generate_random_variants(img, base_name, output_dir, config: AugmentationConfig):
    generated_paths = []

    for _ in range(config.num_random):
        if config.use_random:
            contrast = get_random_factor(config.contrast_range)
            brightness = get_random_factor(config.brightness_range)
            saturation = get_random_factor(config.saturation_range)
            zoom = get_random_factor(config.zoom_range)
            blur = get_random_factor(config.blur_range)
        else:
            contrast = sum(config.contrast_range) / 2
            brightness = sum(config.brightness_range) / 2
            saturation = sum(config.saturation_range) / 2
            zoom = sum(config.zoom_range) / 2
            blur = sum(config.blur_range) / 2

        new_img = apply_enhancements(
            img,
            contrast=contrast,
            brightness=brightness,
            saturation=saturation
        )

        new_img = apply_zoom(new_img, zoom)

        blur_tag = ""
        if random.random() < config.blur_prob and blur > 0:
            new_img = apply_blur(new_img, blur)
            blur_tag = f"_BL{format_float(blur)}"

        flip_tag = ""
        if random.random() < config.flip_prob:
            flip_type = random.choice(["H", "V"])
            if flip_type == "H":
                new_img = flip_horizontal(new_img)
            else:
                new_img = flip_vertical(new_img)
            flip_tag = f"_F{flip_type}"

        filename = (
            f"{base_name}_"
            f"C{format_float(contrast)}_"
            f"B{format_float(brightness)}_"
            f"S{format_float(saturation)}_"
            f"Z{format_float(zoom)}"
        )

        if blur_tag:
            filename += blur_tag

        if flip_tag:
            filename += flip_tag

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
        num_random=10,
        contrast_range=(0.3, 1.8),
        brightness_range=(0.3, 1.8),
        saturation_range=(0.3, 1.8),
        zoom_range=(0.7, 1.3),
        blur_range=(0.0, 1.2),
        blur_prob=0.6,
        flip_prob=0.5,
        use_random=True
    )

    process_images(input_folder, output_folder, config)