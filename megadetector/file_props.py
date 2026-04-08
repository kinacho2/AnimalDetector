
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

def animal_detected(file, conf):
    for det in file.detections:
        if det["conf"] < conf:
            continue

        category = int(det["category"])
        if category > 1: #1 = "animal", see also at megadetector/detection/run_detector.DEFAULT_DETECTOR_LABEL_MAP
            continue

        return True

    return False
