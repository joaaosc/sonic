from fitz import *
from typing import List
from PIL import Image
import numpy as np

pdf_path = r"8200-DWG-BS-103-00.pdf"
class Pdfutils:
    def __init__(self, pdfPath: str):
        self.pdfPath = pdfPath

    def _open_document(self):
        try:
            document = fitz.open(self.pdfPath)
            print("SUCCESS: sucessfully opened~~")
            return document

        except FileNotFoundError:
            print("FATAL: no pdf file found~~")

    def get_possible_drwaings(self):
        document = self._open_document()
        pix_list = []
        for page in document:
            if int(page.bound().width) > int(page.bound().height):
                pix = page.get_pixmap()  # render page to an image
                pix_list.append(pix)
                print("probably drawing found")
            else:
                print("probably not drawing")
        return pix_list

    @staticmethod
    def create_combined_image(pix_list: List[fitz.Pixmap]) -> Image:
        """ Combina múltiplas imagens verticalmente numa única imagem. """
        images = []
        for pix in pix_list:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            arr = np.array(img)
            images.append(arr)
        return Image.fromarray(np.concatenate(images, axis=0), 'RGB')

# ----------------------------------------EOF--------------------------------------------------#
