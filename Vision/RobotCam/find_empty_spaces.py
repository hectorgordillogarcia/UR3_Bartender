import cv2
import numpy as np

# Parámetros
delta_x = 50  # ancho de cada casilla (píxeles)
delta_y = 50  # alto de cada casilla (píxeles)
gradient_threshold = 30  # umbral para detectar "cambios fuertes" de intensidad

# Captura desde la webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if not ret:
    print("Error al capturar la imagen")
    exit()

# Convertimos a escala de grises
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Calculamos el gradiente con Sobel
grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
gradient_magnitude = cv2.magnitude(grad_x, grad_y)

# Región central
h, w = gray.shape
center_x, center_y = w // 2, h // 2
grid_width = delta_x * 5
grid_height = delta_y * 5
top_left_x = 50
top_left_y = 50

# Recorremos la cuadrícula
for j in range(grid_height // delta_y):
    for i in range(grid_width // delta_x):
        x = top_left_x + i * delta_x
        y = top_left_y + j * delta_y
        roi = gradient_magnitude[y:y + delta_y, x:x + delta_x]

        max_grad = np.max(roi)
        if max_grad < gradient_threshold:
            print(f"Casilla vacía (sin gradientes fuertes) en fila {j}, columna {i}")
            # Dibujamos un rectángulo verde sobre la casilla detectada
            cv2.rectangle(frame, (x, y), (x + delta_x, y + delta_y), (0, 255, 0), 2)
            break
    else:
        continue
    break

# Mostrar imagen con casilla resaltada
cv2.imshow("Resultado", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
