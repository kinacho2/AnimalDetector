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

from image_tools import draw_and_save
from os import system

from speciesnet.scripts import run_model
from pathlib import Path


def main():
    # Choose a folder to run MD on recursively, and an output file
    folder = open_folder()
    output_folder = create_temp_folder(".output", folder)
    
    temp_folder = "img"
    img_temp_folder = create_temp_folder(temp_folder, output_folder)

    #output_file = './output/file.json'
    output_classified_file = output_folder + '/classified.json'
    output_result = output_folder + '/result.json'
    #animals_05 = []
    animals_03 = []
    detections_discarded = []
    # The package will automatically download whichever model you request; you 
    # can also specify a filename.
    model_name = 'MDV5A'

    # Run the model on all images in the folder in order to clasify them
    results = load_and_run_detector_batch(model_name, folder)



    animals_05_dict = dict()

    for result in results:
        file = process_result(result)
        #crop_and_save(result, file, temp_folder)

        filtered05, filtered03, discarded = animal_detected(file, 0.5, 0.3) 
        filepath = result["file"]
        directory = str(Path(filepath).parent)

        if not directory in animals_05_dict:
            animals_05_dict[directory] = []

        if(len(filtered05) > 0):
            animals_05_dict[directory].append({"file": result["file"], "detections": filtered05, "max_detection_conf": result["max_detection_conf"]})
        if(len(filtered03) > 0):
            animals_05_dict[directory].append({"file": result["file"], "detections": filtered03, "max_detection_conf": result["max_detection_conf"]})
        if(len(discarded) > 0):
            detections_discarded.append({"file": result["file"], "detections": discarded, "max_detection_conf": result["max_detection_conf"]})

    #Clasify confidency //TODO

    
    #system("python -m speciesnet.scripts.run_model --folders \"F:/Code/Phyton/Animals/fotos2\" --predictions_json \"output/file2.json\"")

    classified_dict_per_dir = dict()

    for directory in animals_05_dict:

        FLAGS = flags.FLAGS
        prediction_file = str(Path(directory) / "predictions.json")

        FLAGS([
            "program_name",
            f"--folders={folder}",
            f"--predictions_json={prediction_file}",
            "--classifier_only"
        ])

        animals_05 = animals_05_dict[directory]

        image_paths = [
            {
                "filepath": str(img_path["file"])
            }
            for img_path in animals_05
        ]

        classified = run_model.classify(image_paths, animals_05)
        classified_dict_per_dir[directory] = classified

    puma_detections = []

    full_classification = dict()

    for directory in classified_dict_per_dir:
        classified_dict = dict()
        classified = classified_dict_per_dir[directory]
        for elem in classified:
            filepath = elem["filepath"]
            bbox = elem["bbox"]
            conf = elem["det_conf"]
            classifications = elem["classifications"]
            classifications_result = []
            classes = classifications["classes"]
            scores = classifications["scores"]

            if not filepath in classified_dict:
                classified_dict[filepath] = []

            if(not filepath in full_classification):
                full_classification[filepath] = []

            elem_index = len(classified_dict[filepath]) + 1

            for i in range(0, len(classes)):
                current_class = classes[i]
                classifications_result.append({"class": classes[i], "score": scores[i]})
                cc = 0
                if("mammalia;carnivora" in current_class):
                    #ignoring following scores that should be minor
                    if cc < scores[i]:
                        relative_path = "..\\" + str(Path(filepath).relative_to(folder))
                        e = { "path": relative_path, "bbox": bbox, "det_conf": conf, "class": classes[i], "score": scores[i] }
                        cc = scores[i]
                        puma_detections.append(e)
                        draw_and_save(filepath, bbox, scores[i], current_class, relative_path, img_temp_folder, elem_index)
                
            aux = {"bbox": bbox, "det_conf": conf, "classifications": classifications_result}
            classified_dict[filepath].append(aux)
            full_classification[filepath].append(aux)
    
        #ct_utils.write_json(output_classified_file, classified_dict, force_str=True)
        output_classified_file = directory + '/classified.json'

        with open(output_classified_file, "w", encoding="utf-8") as f:
            json.dump(classified_dict, f, indent=4, ensure_ascii=False)

    with open(output_result, "w", encoding="utf-8") as f:
        json.dump(puma_detections, f, indent=4, ensure_ascii=False)

    output_classified_file = output_folder + "\\full_classification.json"
    with open(output_classified_file, "w", encoding="utf-8") as f:
        json.dump(full_classification, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    try:
        main()
        print("\nPrograma finalizado correctamente.")
    except Exception as e:
        import traceback

        print("\nOcurrió un error:")
        traceback.print_exc()

    input("\nPresioná Enter para cerrar...")

