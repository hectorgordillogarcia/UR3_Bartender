import cv2
import numpy as np

def buscar_espacio_vacío():
    """
    Busca un hueco vacío en la zona de trabajo del robot para dejar una lata.

    Devuelve:
        (x_free, y_free): Coordenadas del centro de la casilla vacía, o None si no se encuentra.
    """

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error al capturar la imagen")
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    resultado, img_out = buscar_casilla_vacia(gray)

    if resultado is None:
        print("No se encontró ninguna casilla vacía")
        return None

    i, j = resultado

    cv2.imshow("Resultado", img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    x_0 = 0  # Coordenada x de la primera cuadrícula
    y_0 = 0  # Coordenada y de la primera cuadrícula
    dx = 0.15  # Anchura aprox de la cuadrícula (m)
    dy = 0.15  # Altura aprox de la cuadrícula (m)

    return (x_0 + j * dx, y_0 + i * dy)

    


def buscar_casilla_vacia(gray_img):
    """
    Busca la primera casilla sin gradientes fuertes en una cuadrícula centrada en la imagen.
    Los parámetros están fijados dentro de la función.

    Parámetro:
        gray_img (np.ndarray): Imagen en escala de grises.

    Devuelve:
        (i, j): Índices de la primera casilla vacía encontrada (columna, fila). None si no se encuentra.
        annotated_img (np.ndarray): Imagen con la cuadrícula y la casilla vacía dibujadas.
    """

    # Parámetros fijos
    delta_x = 50  # ancho de casilla
    delta_y = 50  # alto de casilla
    grid_cols = 8
    grid_rows = 8
    gradient_threshold = 30

    # Tamaño de la cuadrícula
    grid_width = delta_x * grid_cols
    grid_height = delta_y * grid_rows

    # Punto superior izquierdo (centrado)
    h, w = gray_img.shape
    top_left_x = w // 2 - grid_width // 2
    top_left_y = h // 2 - grid_height // 2

    # Calcular gradiente
    grad_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = cv2.magnitude(grad_x, grad_y)

    # Imagen anotada
    annotated_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    for j in range(grid_rows):
        for i in range(grid_cols):
            x = top_left_x + i * delta_x
            y = top_left_y + j * delta_y
            roi = grad_mag[y:y + delta_y, x:x + delta_x]

            if roi.shape[0] == 0 or roi.shape[1] == 0:
                continue

            max_grad = np.max(roi)
            color = (255, 0, 0)  # azul por defecto

            if max_grad < gradient_threshold:
                color = (0, 255, 0)  # verde si es vacía
                cv2.rectangle(annotated_img, (x, y), (x + delta_x, y + delta_y), color, 2)
                return (i, j), annotated_img

            cv2.rectangle(annotated_img, (x, y), (x + delta_x, y + delta_y), color, 1)

    return None, annotated_img