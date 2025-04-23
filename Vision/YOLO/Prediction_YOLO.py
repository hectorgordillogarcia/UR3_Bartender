import cv2
import os
from ultralytics import YOLO
import torch
import copy


def getPrediction(img):
    '''
    Realiza la predicción de YOLO
    '''
    conf_threshold = 0.8
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "best.pt")
    model = YOLO(model_path)
    results = model.predict(source=img, conf=conf_threshold)
    return results


def getCentroid(desiredResults, img_height, img_width):
    '''
    Función para calcular el centroide de las cajas de predicción

    '''
    centroids = []
    boxes = desiredResults.boxes.xywh  # Coordenadas de las cajas (x_min, y_min, x_max, y_max)
    plotted_img = desiredResults.plot()

    # Guardar la imagen en la ruta deseada
    save_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'Vision', 'YOLO', 'resultado.png'))

    for box in boxes:
        centroide_x, centroide_y, w, h = box
        # Normalizamos dividiendo por las dimensiones de la imagen
        centroide_x_norm = centroide_x.item() / img_width
        centroide_y_norm = centroide_y.item() / img_height
        
        centroids.append([centroide_x_norm, centroide_y_norm])
        #Dibujamos el punto del centroide encima de la imagen ya ploteada
        center = (int(centroide_x.item()), int(centroide_y.item()))
        cv2.circle(plotted_img, center, 20, (0, 0, 255), -1)
        cv2.imwrite(save_path, plotted_img)


    return centroids




def filterCanType(img, canType):
    '''    
    Devuelve únicamente los resultados de una de las latas deseadas    
    '''
    results = getPrediction(img)
    pred = results[0]
    class_ids = pred.boxes.cls
    class_names = pred.names

    # Comprueba el ID de la bebida deseada
    target_class_id = None
    for class_id, name in class_names.items():
        if name == canType:
            target_class_id = class_id
            break

    # Si no encuentra la bebida
    if target_class_id is None:
        print(f"There is no stock of '{canType}' cans.")
        return False, None

    # Filtrar solo bebidas deseadas
    indices = torch.where(class_ids == target_class_id)[0]

    #Revisa que al menos hay una bebida deseada
    if len(indices) == 0:
        print(f"There is no '{canType}' can detected in the image.")
        return False, None

    # Cojo solo la primera bebida deseada (si hay dos fanta coge una)
    first_index = indices[0].item()
    predCan = copy.deepcopy(pred)

    # Solo se guarda la caja de la bebida deseada
    predCan.boxes.data = pred.boxes.data[first_index:first_index+1]

    return True, predCan

def getCanCentroid(img, canType):
    '''
    Obtiene el centroide normalizado de la lata deseada
    '''
    bOk, pred = filterCanType(img, canType)
    if not bOk:
        return False    
    img_height, img_width = img.shape[:2]
    centroids=getCentroid(pred,img_height, img_width)
    centroid = centroids[0] #Aseguramos que solo obtenemos el centroide una lata
    return centroid

def main():
    #Test
    # # Define la ruta base relativa a este script
    # base_dir = os.path.dirname(__file__)
    # img = os.path.join(base_dir, "Pruebas.png")
    # centroid=getCanCentroid(img,"nestea")
    # print(f"x: {centroid[0]} y: {centroid[1]}")
    pass


if __name__ == '__main__':
    main()