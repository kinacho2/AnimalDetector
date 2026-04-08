import tkinter as tk
from tkinter import filedialog
import shutil
import os
from pathlib import Path

def create_temp_folder(folder_name, path):
    base_path = Path(path)
    new_folder = base_path / folder_name

    new_folder.mkdir(parents=True, exist_ok=True)

    return new_folder
    
def copy_file(path, to_dir):
    if not os.path.isfile(path):
        raise ValueError(f"No existe el archivo: {path}")

    if not os.path.isdir(to_dir):
        raise ValueError(f"No existe el directorio destino: {to_dir}")

    shutil.copy(path, to_dir)

def open_folder():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    folder_path = filedialog.askdirectory(
        title="Seleccionar carpeta"
    )

    return folder_path


def clean_temp_folder(folder_name, path):
    base_path = Path(path)
    new_folder = base_path / folder_name
    folder = Path(new_folder)

    if folder.exists():
        shutil.rmtree(folder)

    new_folder.mkdir(parents=True, exist_ok=True)

    return new_folder


