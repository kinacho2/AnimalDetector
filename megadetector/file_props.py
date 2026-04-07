
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileData:
    path: Path
    name_w_ext: str
    ext: str
    folder: Path
    name: str

def process_result(result):
    path = Path(result["file"])

    file = FileData(
        path = path,
        name_w_ext = path.name,
        ext = path.suffix,
        folder = path.parent,
        name = path.stem
    )

    return file


    