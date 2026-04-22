
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileData:
    path: Path
    name_w_ext: str
    ext: str
    folder: Path
    name: str
    detections: list

def process_result(result):
    path = Path(result["file"])

    file = FileData(
        path = path,
        name_w_ext = path.name,
        ext = path.suffix,
        folder = path.parent,
        name = path.stem,
        detections = result["detections"],
    )

    return file

def animal_detected(file, conf, conf2):
    result_conf = list()
    result_conf2 = list()
    discarded = list()
    
    for det in file.detections:
        category = int(det["category"])
        if category > 1: #1 = "animal", see also at megadetector/detection/run_detector.DEFAULT_DETECTOR_LABEL_MAP
            discarded.append(det)
            continue

        if det["conf"] < conf:
            if(det["conf"] >= conf2):
                result_conf2.append(det)
                continue
            discarded.append(det)
            continue

        result_conf.append(det)

    return result_conf, result_conf2, discarded
