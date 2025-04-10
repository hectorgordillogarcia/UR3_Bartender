import cv2
import os
from ultralytics import YOLO

def getImage():
    #Aqui saco la foto con la camara
    #return imagen
    pass

# Función para realizar la detección y guardar la imagen
def getPrediction(img_name, model_path):
    conf_threshold = 0.8
    img = cv2.imread(img_name)
    model = YOLO(model_path)
    results = model.predict(source=img, conf=conf_threshold)
    return results

# # Función para calcular el centroide de las cajas de predicción
def getCentroid(results):
    pred=results[0]
    centroids = []
    boxes = pred.boxes.xyxy  # Coordenadas de las cajas (x_min, y_min, x_max, y_max)

    for box in boxes:
        x_min, y_min, x_max, y_max = box
        centroide_x = (x_min + x_max) / 2
        centroide_y = (y_min + y_max) / 2
        centroids.append((centroide_x, centroide_y))
    return centroids

def getCanCentroid(Selection):

    results=getPrediction(img,model)
    centroids=getCentroid(results)
    return centroids

def main():
    # Define la ruta base relativa a este script
    base_dir = os.path.dirname(__file__)  # Directorio del script

    # Rutas relativas para los archivos
    img_name = os.path.join(base_dir, "Test Images", "Aquarius1.png")
    model_path = os.path.join(base_dir, "best_model.pt")

    # Llamar a la función para realizar la detección y obtener la predicción
    img, pred = getPrediction(img_name, model_path)

    # Llamar a la función para calcular los centroides
    centroides = getCentroid(pred)



if __name__ == '__main__':
    main()