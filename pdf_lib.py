from fitz import *
from typing import List
from PIL import Image
import numpy as np



class PdfUtils:

    def __init__(self, pdfPath):
        self.text = ''
        self.pdfPath = pdfPath
        self.finalDwgImage = None

    def _open_document(self):
        if os.path.exists(self.pdfPath):
            try:
                document = fitz.open(self.pdfPath)  # type: ignore
                print("[SUCCESS]: successfully opened~~")
                return document
            except FileNotFoundError:
                print("[FATAL]: no pdf file found~~")
                return None
        else:
            print("[ERROR]: File does not exist~~")
            return None

    def get_text(self):
        document = self._open_document()
        for page_number in range(len(document)):
            page = document.load_page(page_number)
            self.text = page.get_text().lower()
            print(self.text)
            if "reference drawing" in self.text or "tooling sketch" in self.text:
                print("\033[92m[SUCCESS]: Found 'Reference Drawing' or 'Tooling Sketch'~~\033[0m")
                return True
        print("\033[93m[WARN]: Didn't find 'Reference Drawing' or 'Tooling Sketch'~~\033[0m")
        return None

    def crop_pdf(self):
        pass  # todo

    def get_possible_drwaings(self) -> list:
        document = self._open_document()
        pix_list = []
        for page in document:
            page_text = page.get_text().lower()

            if (int(page.bound().width) > int(page.bound().height) and
                    ("reference drawing" in page_text or "tooling sketch" in page_text)):
                zoom = 3.0  # Increase the resolution by a factor of 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)  # Render page to an image with increased resolution
                pix_list.append(pix)
                print("[INFO]: probably drawing found~~")
            else:
                print("[INFO:] probably not drawing~~")
        return pix_list




    @staticmethod
    def create_combined_image(pix_list: List[fitz.Pixmap], save=True) -> Image:
        """ Combina múltiplas imagens verticalmente numa única imagem. """
        images = []
        for pix in pix_list:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # type: ignore
            arr = np.array(img)
            images.append(arr)
        if save:
            try:
                # Get the current directory
                curr_dir = os.getcwd()
                print(curr_dir)
                # Define the full output path
                full_path = os.path.join(curr_dir, 'combined.png')
                Image.fromarray(np.concatenate(images, axis=0), 'RGB').save(full_path)
                print(f"[SUCCESS]: Image successfully combined and saved to {full_path}~~")

                return Image.fromarray(np.concatenate(images, axis=0), 'RGB')

            except Exception as e:
                print(f"[FATAL]: error occurred when trying to save image {e}")
        else:
            print(f"[SUCCESS]: Image successfully combined~~")
            return Image.fromarray(np.concatenate(images, axis=0), 'RGB')

    def construct_DWG_image(self, image: Image):
        self.finalDwgImage = image
        print(f"[SUCCESS]: final DWG image created and added to instance field~~")






