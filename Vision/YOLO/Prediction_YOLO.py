import cv2
import os
from ultralytics import YOLO

# Función para realizar la detección y guardar la imagen
def realizar_deteccion(img_name, model_path):
    # Cargar la imagen
    img = cv2.imread(img_name)

    # Cargar el modelo
    model = YOLO(model_path)

    # Realizar la predicción
    results = model.predict(img)

    # Los resultados se encuentran en 'results' y contienen las predicciones
    pred = results[0]  # Obtener el primer resultado de la predicción

    pred_img = pred.plot()

    # Guardar la imagen con la detección
    cv2.imwrite(f"{img_name}_deteccion.png", pred_img)

    return img, pred  # Retornar la imagen original y la predicción

# # Función para calcular el centroide de las cajas de predicción
def calcular_centroides(pred):
    centroids = []
    
    # Los resultados de la predicción tienen un atributo 'boxes' que es un ndarray
    # Acceder a las coordenadas de las cajas
    boxes = pred.boxes.xyxy  # Coordenadas de las cajas (x_min, y_min, x_max, y_max)

    # Iterar sobre las cajas y calcular el centroide
    for box in boxes:
        x_min, y_min, x_max, y_max = box
        # Calcular las coordenadas del centroide (promedio de las coordenadas x y y)
        centroide_x = (x_min + x_max) / 2
        centroide_y = (y_min + y_max) / 2
        centroids.append((centroide_x, centroide_y))
    return centroids


if __name__ == '__main__':
    # Define la ruta base relativa a este script
    base_dir = os.path.dirname(__file__)  # Directorio del script

    # Rutas relativas para los archivos
    img_name = os.path.join(base_dir, "Aquarius6.png")
    model_path = os.path.join(base_dir, "best.pt")

    # Llamar a la función para realizar la detección y obtener la predicción
    img, pred = realizar_deteccion(img_name, model_path)

    # Llamar a la función para calcular los centroides
    centroides = calcular_centroides(pred)
