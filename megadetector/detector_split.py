from megadetector.detection.run_detector_batch import \
    load_and_run_detector_batch, write_results_to_file
import json
from so_explorer import open_folder
from so_explorer import clean_temp_folder
from so_explorer import create_temp_folder
from so_explorer import copy_file
from absl import flags
from megadetector.utils import ct_utils

from file_props import process_result
from file_props import animal_detected

from image_tools import crop_and_save
from os import system

from speciesnet.scripts import run_model

def main():
    # Choose a folder to run MD on recursively, and an output file
    folder = open_folder()
    output_folder = create_temp_folder("output", folder)
    output_file = './output/file.json'
    output_classified_file = './output/classified.json'
    animals = []
    # The package will automatically download whichever model you request; you 
    # can also specify a filename.
    model_name = 'MDV5A'

    # Run the model on all images in the folder in order to clasify them
    results = load_and_run_detector_batch(model_name, folder)

    for result in results:
        file = process_result(result)
        #crop_and_save(result, file, temp_folder)
        if(animal_detected(file, 0.5)):
            animals.append(result)

    detections = write_results_to_file(animals, output_file, relative_path_base=folder, detector_file=model_name)

    image_paths = [
        {
            "filepath": str(img_path["file"])
        }
        for img_path in animals
    ]
    #system("python -m speciesnet.scripts.run_model --folders \"F:/Code/Phyton/Animals/fotos2\" --predictions_json \"output/file2.json\"")

    FLAGS = flags.FLAGS
    folders_param = "--folders=\"" + folder + "\""
    classify_file = output_folder + "/predictions.json\""
    FLAGS(["program_name", folders_param])
    FLAGS(["program_name", "--classifier_only"])


    classified = run_model.classify(image_paths, detections)

    for item in classified:
        print("cosas")

    ct_utils.write_json(output_classified_file, classified, force_str=True)

if __name__ == "__main__":
    main()

