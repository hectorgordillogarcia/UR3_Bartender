import cv2
import os
from ultralytics import YOLO
import torch
import copy

def getImage():
    #Aqui saco la foto con la camara
    #return imagen
    pass

# Función para realizar la detección y guardar la imagen
def getPrediction(img):
    conf_threshold = 0.8
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "best.pt")
    model = YOLO(model_path)
    results = model.predict(source=img, conf=conf_threshold)
    return results


# # Función para calcular el centroide de las cajas de predicción
def getCentroid(desiredResults):
    centroids = []
    boxes = desiredResults.boxes.xyxy  # Coordenadas de las cajas (x_min, y_min, x_max, y_max)

    for box in boxes:
        x_min, y_min, x_max, y_max = box
        centroide_x = (x_min + x_max) / 2
        centroide_y = (y_min + y_max) / 2
        centroids.append([centroide_x.item(), centroide_y.item()])

    return centroids



def filterCanType(img,canType):

    results=getPrediction(img)
    pred=results[0]
    class_ids = pred.boxes.cls
    class_names = pred.names

    # Comprueba el ID de la bebida deseada
    target_class_id = None
    for class_id, name in class_names.items():
        if name == canType:
            target_class_id = class_id
            break

    #Si no encuentra la bebida
    if target_class_id is None:
        print(f"There is no stock of'{canType}' cans.")
        return
    
    # Filtrar solo bebidas deseadas
    indices = torch.where(class_ids == target_class_id)[0]

    #Cojo solo la primera bebida deseada (si hay dos fanta coge una)
    first_index = indices[0].item()

    predCan = copy.deepcopy(pred) 

    # Solo se guarda la caja de la bebida deseada
    predCan.boxes.data = pred.boxes.data[first_index:first_index+1]

    return predCan

def getCanCentroid(img,canType):
    pred=filterCanType(img,canType) #Hago yolo y saco los resultados de una sola lata
    centroids=getCentroid(pred)
    centroid=centroids[0]
    return centroid


def main():
    #Test
    # # Define la ruta base relativa a este script
    # base_dir = os.path.dirname(__file__)
    # img = os.path.join(base_dir, "Pruebas.png")
    # centroid=getCanCentroid(img,"nestea")
    # print(f"x: {centroid[0]} y: {centroid[1]}")
    


if __name__ == '__main__':
    main()