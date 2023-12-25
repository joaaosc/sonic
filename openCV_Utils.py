import cv2


def preprocess_image(image_path):
    """
    Processa uma imagem convertendo-a em escala de cinza e posteriormente aplicando binarização.
    Args:
        image_path (str): Caminho da imagem
    Returns:
        numpy.ndarray: Imagem binarizadaself.
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    print("~~sucessfully preproccessed")
    return binary_image
