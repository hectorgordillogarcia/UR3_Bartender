from cam_utils import buscar_espacio_vacío

if __name__ == "__main__":

    frame = cv2.imread("prueba.jpeg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("a",gray)
    booleano, resultado = hueco_libre(gray)
    cv2.imshow("Resultado", resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(booleano)