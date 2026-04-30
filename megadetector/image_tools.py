from PIL import Image, ImageDraw, ImageFont
from file_props import FileData, from_filepath
from so_explorer import create_temp_folder
from pathlib import Path

def create_crop_box(detection, width, height):
    bbox = detection["bbox"]
    left = width * bbox[0]
    upper = height * bbox[1]
    right = width * (bbox[0] + bbox[2])
    lower = height * (bbox[1] + bbox[3])
    box = (left, upper, right, lower)
    return box

def create_crop_box_bbox(bbox, width, height):
    left = width * bbox[0]
    upper = height * bbox[1]
    right = width * (bbox[0] + bbox[2])
    lower = height * (bbox[1] + bbox[3])
    box = (left, upper, right, lower)
    return box

def crop_and_save(result, file, temp_path):
    image = Image.open(file.path)
    width = image.width
    height = image.height
    img_index = 0
    img_to_draw = image.copy()

    temp_folder = "temp"
    create_temp_folder(temp_folder, temp_path)

    detections = result["detections"]
    for det in detections:
        conf = det["conf"]
        if conf < 0.5:
            continue

        category = int(det["category"])
        if category > 1:
            continue

        crop_box = create_crop_box(det, width, height)
        cropped_image = image.crop(crop_box)
        new_file_name = file.name + str(img_index) + file.ext
        cropped_image.save(temp_path / temp_folder / new_file_name)

        # Define the coordinates and drawing properties
        # Coordinates format: [x0, y0, x1, y1] or [(x0, y0), (x1, y1)]
        outline_color = 'red' # Can be a color name or RGB tuple
        draw = ImageDraw.Draw(img_to_draw)
        # Draw the rectangle
        draw.rectangle(crop_box, outline=outline_color, width=3)

        img_index = img_index + 1
    img_to_draw.show()


def draw_and_save(filepath, bbox, score, class_desc, relative_path, output_folder, det_index):
    image = Image.open(filepath)
    width = image.width
    height = image.height
    img_to_draw = image.copy()

    crop_box = create_crop_box_bbox(bbox, width, height)

    # Define the coordinates and drawing properties
    # Coordinates format: [x0, y0, x1, y1] or [(x0, y0), (x1, y1)]
    outline_color = 'red' # Can be a color name or RGB tuple
    value = score * 100
    value = f"{value:.2f}"
    score_label = "score: "+value
    class_label = "class: "+ class_desc[37:len(class_desc)]

    draw = ImageDraw.Draw(img_to_draw)
    draw_text = ImageDraw.Draw(img_to_draw)
    # Draw the rectangle
    factor = width / 1024
    font_size = 24 * factor
    sep_size = 30 * factor

    font = ImageFont.truetype("arial.ttf", font_size)

    relative_path = relative_path[3:len(relative_path)]
    relative_path = relative_path.replace("\\", "/")

    draw_text.text((20, 20), relative_path, fill=outline_color, font=font)
    draw_text.text((20, 20 + sep_size), score_label, fill=outline_color, font=font)
    draw_text.text((20, 20 + sep_size * 2), class_label, fill=outline_color, font=font)
    draw.rectangle(crop_box, outline=outline_color, width=3)

    relative_path = relative_path.replace("/", "_")
    
    file = from_filepath(output_folder + "/" + relative_path)

    output_file = output_folder + "/" + file.name + "_" + str(det_index) + file.ext

    img_to_draw.save(output_file)