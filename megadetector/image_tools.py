from PIL import Image, ImageDraw
from file_props import FileData
from so_explorer import create_temp_folder

def create_crop_box(detection, width, height):
    bbox = detection["bbox"]
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