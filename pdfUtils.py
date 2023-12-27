from fitz import *
from typing import List
from PIL import Image
import numpy as np



class Pdfutils:

    def __init__(self, pdfPath):  # add pdfPath parameter to the init
        self.text = ''
        self.pdfPath = pdfPath  # path must be passed to the class when it is created

    def _open_document(self):
        if os.path.exists(self.pdfPath):
            try:
                document = fitz.open(self.pdfPath)
                print("SUCCESS: successfully opened~~")
                return document
            except FileNotFoundError:
                print("FATAL: no pdf file found~~")
                return None
        else:
            print("ERROR: File does not exist")
            return None

    def get_text(self):
        document = self._open_document()
        for page_number in range(len(document)):
            page = document.load_page(page_number)
            self.text = page.get_text().lower()
            print(self.text)
            if "reference drawing" in self.text or "tooling sketch" in self.text:
                self.crop_pdf()
                print("\033[92m[SUCCESS]: Found 'Reference Drawing' or 'Tooling Sketch'\033[0m")
                return True
        print("\033[93m[WARN]: Didn't find 'Reference Drawing' or 'Tooling Sketch'.\033[0m")
        return None

    def crop_pdf(self):
        document = self._open_document()
        new_document = fitz.open()

        for page_number in range(len(document)):
            page = document[page_number]
            words = page.get_text("words")
            words.sort(key=lambda w: (w[3], w[0]))
            found = False
            min_x = 0
            max_x = 0

            # Get the position of "reference drawing" or "tooling sketch"
            for word in words:
                if 'reference drawing' in word[4].lower() or 'tooling sketch' in word[4].lower():
                    if not found:  # check if this if the first occurrence
                        min_x = word[0]
                        found = True
                    if word[2] > max_x:  # search for maximum x to cut the right part of the page too
                        max_x = word[2]

            # If the text is found
            if found:
                left_rect = fitz.Rect(0, 0, min_x, page.rect.height)  # rectangle for left side
                right_rect = fitz.Rect(max_x, 0, page.rect.width, page.rect.height)  # rectangle for right side

                # Add left and right part of the page to new document
                new_page_left = new_document.new_page(width=left_rect.width, height=page.rect.height)
                new_page_left.show_pdf_page(left_rect, page.pixmap())
                new_page_right = new_document.new_page(width=right_rect.width, height=page.rect.height)
                new_page_right.show_pdf_page(right_rect, page.pixmap())

        document.close()
        if new_document.page_count > 0:
            new_document.save('/home/joaop/PycharmProjects/sonic/output.pdf')
        else:
            print("Warning: The new document has zero pages.")

    def get_possible_drwaings(self):
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
                print("probably drawing found")
            else:
                print("probably not drawing")
        return pix_list




    @staticmethod
    def create_combined_image(pix_list: List[fitz.Pixmap], save=True) -> bool:
        """ Combina múltiplas imagens verticalmente numa única imagem. """
        images = []
        for pix in pix_list:
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            arr = np.array(img)
            images.append(arr)




        if save:
            try:
                # Get the current directory
                curr_dir = os.getcwd()
                print(curr_dir)
                # Define the full output path
                full_path = os.path.join(curr_dir, 'combined.png')
#               Image.fromarray(np.concatenate(images, axis=0), 'RGB').save(full_path)
#               print(f"Image saved to {full_path}")

                #return True
                return Image.fromarray(np.concatenate(images, axis=0), 'RGB')

            except Exception as e:
                print(f"[FATAL]: error occurred when trying to save image {e}")



