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
    
    #output_file = './output/file.json'
    output_classified_file = output_folder + '/classified.json'
    animals_05 = []
    animals_03 = []
    detections_discarded = []
    # The package will automatically download whichever model you request; you 
    # can also specify a filename.
    model_name = 'MDV5A'

    # Run the model on all images in the folder in order to clasify them
    results = load_and_run_detector_batch(model_name, folder)

    for result in results:
        file = process_result(result)
        #crop_and_save(result, file, temp_folder)

        filtered05, filtered03, discarded = animal_detected(file, 0.5, 0.3) 
        if(len(filtered05) > 0):
            animals_05.append({"file": result["file"], "detections": filtered05, "max_detection_conf": result["max_detection_conf"]})
        if(len(filtered03) > 0):
            animals_03.append({"file": result["file"], "detections": filtered03, "max_detection_conf": result["max_detection_conf"]})
        if(len(discarded) > 0):
            detections_discarded.append({"file": result["file"], "detections": discarded, "max_detection_conf": result["max_detection_conf"]})

    #Clasify confidency //TODO

    image_paths = [
        {
            "filepath": str(img_path["file"])
        }
        for img_path in animals_05
    ]
    #system("python -m speciesnet.scripts.run_model --folders \"F:/Code/Phyton/Animals/fotos2\" --predictions_json \"output/file2.json\"")

    FLAGS = flags.FLAGS
    folders_param = "--folders=\"" + folder + "\""
    classify_file = output_folder + "/predictions.json\""
    FLAGS(["program_name", folders_param])
    FLAGS(["program_name", "--classifier_only"])

    classified = run_model.classify(image_paths, animals_05)

    classified_dict = dict()
    
    for elem in classified:
        filepath = elem["filepath"]
        bbox = elem["bbox"]
        conf = elem["det_conf"]
        classifications = elem["classifications"]
        classifications_result = []
        classes = classifications["classes"]
        scores = classifications["scores"]
        for i in range(0, len(classes)):
            classifications_result.append({"class": classes[i], "score": scores[i]})

        if not filepath in classified_dict:
            classified_dict[filepath] = []

        aux = {"bbox": bbox, "det_conf": conf, "classifications": classifications_result}
        classified_dict[filepath].append(aux)
    
    #ct_utils.write_json(output_classified_file, classified_dict, force_str=True)

    with open(output_classified_file, "w", encoding="utf-8") as f:
        json.dump(classified_dict, f, indent=4, ensure_ascii=False)




if __name__ == "__main__":
    main()

