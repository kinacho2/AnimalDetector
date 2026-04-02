from megadetector.detection.run_detector_batch import \
    load_and_run_detector_batch, write_results_to_file
import json
from PIL import Image, ImageDraw

# Choose a folder to run MD on recursively, and an output file
image_folder = '../fotos2'
output_file = './output/file.json'

# The package will automatically download whichever model you request; you 
# can also specify a filename.
model_name = 'MDV5A'

# Run the model on all images in the folder
results = load_and_run_detector_batch(model_name, image_folder)

results_json = json.dumps(results[0]);

for result in results:
    image_path = result["file"]
    image_name = image_path.split("/")[-1]
    img_ext = "." + image_name.split(".")[-1]
    img_folder = image_path.replace(image_name, "")
    image_name = image_name.replace(img_ext, "")
    image = Image.open(image_path)
    width = image.width
    height = image.height
    detections = result["detections"]
    img_index = 0
    img_to_draw = image.copy()
    for det in detections:
        conf = det["conf"]
        if conf < 0.5:
            continue

        category = int(det["category"])
        if category > 1:
            continue

        bbox = det["bbox"]
        left = width * bbox[0]
        upper = height * bbox[1]
        right = width * (bbox[0] + bbox[2])
        lower = height * (bbox[1] + bbox[3])
        crop_box = (left, upper, right, lower)
        cropped_image = image.crop(crop_box)
        cropped_image.save(img_folder + "temp/" + image_name + str(img_index) + img_ext)

        # Define the coordinates and drawing properties
        # Coordinates format: [x0, y0, x1, y1] or [(x0, y0), (x1, y1)]
        outline_color = 'red' # Can be a color name or RGB tuple
        draw = ImageDraw.Draw(img_to_draw)
        # Draw the rectangle
        draw.rectangle(crop_box, outline=outline_color, width=3)

        img_index = img_index + 1
    img_to_draw.show()


print(results[0]["detections"][0]["bbox"])#results[0]["detections"][0]["bbox"]


#.images[0].detections[0].bbox[0]

# Write results to a format that Timelapse and other downstream tools like
write_results_to_file(results,
                      output_file,
                      relative_path_base=image_folder,
                      detector_file=model_name)