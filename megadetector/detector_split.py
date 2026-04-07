from megadetector.detection.run_detector_batch import \
    load_and_run_detector_batch, write_results_to_file
import json
from so_explorer import open_folder
from so_explorer import create_temp_folder
from image_tools import create_crop_box
from file_props import process_result
from image_tools import crop_and_save


def main():
    # Choose a folder to run MD on recursively, and an output file
    folder = open_folder()
    temp_folder = create_temp_folder(".megadetector", folder)
    output_folder = create_temp_folder("output", folder)
    output_file = './output/file.json'

    # The package will automatically download whichever model you request; you 
    # can also specify a filename.
    model_name = 'MDV5A'

    # Run the model on all images in the folder
    results = load_and_run_detector_batch(model_name, folder)

    results_json = json.dumps(results[0]);

    for result in results:

        file = process_result(result)
        crop_and_save(result, file, temp_folder)

    write_results_to_file(results,
                          output_file,
                          relative_path_base=folder,
                          detector_file=model_name)

if __name__ == "__main__":
    main()

