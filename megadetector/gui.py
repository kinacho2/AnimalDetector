import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import sys
import traceback

import detector_split


class ConsoleRedirector:

    def __init__(self, textbox):
        self.textbox = textbox
        self.buffer = ""

    def write(self, text):

        self.buffer += text

        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)

            self.textbox.after(
                0,
                self._append_text,
                line + "\n"
            )

    def flush(self):

        if self.buffer:
            self.textbox.after(
                0,
                self._append_text,
                self.buffer
            )

            self.buffer = ""

    def _append_text(self, text):

        self.textbox.insert(tk.END, text)
        self.textbox.see(tk.END)

        # MUY IMPORTANTE
        self.textbox.update_idletasks()

class App:

    def __init__(self, root):

        self.root = root

        root.title("Detector de animales")
        root.geometry("900x600")
        root.minsize(700, 400)

        root.resizable(False, False)

        # CONFIGURAR GRID PRINCIPAL
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # FRAME SUPERIOR
        top_frame = tk.Frame(root)
        top_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        top_frame.grid_columnconfigure(0, weight=1)

        self.start_button = tk.Button(
            top_frame,
            text="Seleccionar carpeta",
            command=self.start_process,
            height=2,
            width=20
        )

        self.start_button.grid(row=0, column=0)

        # AREA DE LOGS
        self.log_area = ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )

        self.log_area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        # REDIRECCIONAR PRINTS
        sys.stdout = ConsoleRedirector(self.log_area)
        sys.stderr = ConsoleRedirector(self.log_area)

        print("Aplicación iniciada.\n")

    def start_process(self):

        self.start_button.config(state=tk.DISABLED)

        thread = threading.Thread(
            target=self.run_detector,
            daemon=True
        )

        thread.start()

    def run_detector(self):

        try:
            print("===================================")
            print("Iniciando procesamiento...")
            print("===================================\n")

            detector_split.main()

            print("\n===================================")
            print("Proceso finalizado correctamente.")
            print("===================================\n")

        except Exception:
            print("\nERROR DURANTE LA EJECUCIÓN:\n")
            traceback.print_exc()

        finally:
            self.root.after(
                0,
                lambda: self.start_button.config(state=tk.NORMAL)
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = App(root)

    root.mainloop()