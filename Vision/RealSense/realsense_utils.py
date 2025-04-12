# realsense_utils.py

import pyrealsense2 as rs
import numpy as np

def capture_single_frame():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    pipeline.start(config)

    #Descartar primeros frames para evitar imagenes malas
    for _ in range(20):
        pipeline.wait_for_frames()

    # Captura frame bueno
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
    color_image = np.asanyarray(color_frame.get_data())

    pipeline.stop()
    return color_image, depth_frame, intrinsics


def getCanCoordinates(x, y, width, height,intrinsics,depth_frame):
    """
    Devuelve las coordenadas 3D del punto más cercano a la cámara dentro de una ventana centrada
    en (x, y) con dimensiones (width, height) normalizadas en el rango [0, 1].
    
    Args:
    - x: Coordenada normalizada en el eje X (entre 0 y 1), centro de la ventana.
    - y: Coordenada normalizada en el eje Y (entre 0 y 1), centro de la ventana.
    - width: Ancho de la ventana normalizado (entre 0 y 1).
    - height: Altura de la ventana normalizada (entre 0 y 1).
    
    Returns:
    - Las coordenadas 3D del punto más cercano dentro de la ventana [x', y', z'] en el sistema de referencia de la cámara.
    """
    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
        raise ValueError("Las coordenadas y las dimensiones deben estar entre 0 y 1")

    # Convertir las coordenadas normalizadas (x, y) y las dimensiones (width, height) a píxeles
    img_width = intrinsics.width
    img_height = intrinsics.height

    # Coordenadas del píxel central
    center_x = int(x * img_width)
    center_y = int(y * img_height)

    # Dimensiones de la ventana en píxeles
    half_width = int(width * img_width / 2)
    half_height = int(height * img_height / 2)

    # Inicializar variables para almacenar la coordenada 3D más cercana
    closest_point = None
    min_distance = float('inf')  # Inicialmente, la distancia mínima es infinita

    # Recorrer la ventana centrada en (x, y) con el tamaño dado
    for dx in range(-half_width, half_width + 1):
        for dy in range(-half_height, half_height + 1):
            pixel_x = center_x + dx
            pixel_y = center_y + dy
            
            # Asegurarse de que el píxel esté dentro de los límites de la imagen
            if 0 <= pixel_x < img_width and 0 <= pixel_y < img_height:
                # Obtener la distancia de profundidad en ese píxel
                depth = depth_frame.get_distance(pixel_x, pixel_y)
                
                if depth > 0 and depth < min_distance: # Asegurarse de que la distancia no sea 0 (es decir, que no esté en un área sin datos) y comprobar si es el nuevo punto más cercano

                    min_distance = depth
                    closest_point = rs.rs2_deproject_pixel_to_point(intrinsics, [pixel_x, pixel_y], depth)  # Usar la matriz intrínseca para obtener las coordenadas 3D del punto
                    can_radio = 0.0325
                    alpha = np.arctan2(closest_point[0], closest_point[2])
                    can_center = closest_point + np.array([can_radio * np.sin(alpha), 0, can_radio * np.cos(alpha)])

    print(f"punto más cercano: x'={closest_point[0]}, y'={closest_point[1]}, z'={closest_point[2]}")

    return can_center

import numpy as np

def convertCoordinates(vector, translation, euler_angles):
    """
    Convierte las coordenadas conocidas de un punto 3D, expresadas en el sistema de referencia A, a un sistema de referencia
    de referencia B relacionado con A mediante un vector de traslación y una rotación definida por 3 ángulos de Euler.
    
    Args:
    - vector: Coordenada del vector a convertir en el sistema de referencia A.
    - translation: Vector de traslación entre los orígenes de los sistemas de referencia A y B.
    - euler_angles: Ángulos de Euler (con respecto a X,Y,Z) que relacionan la orientación de los sistemas de referencia A y B.
    
    Returns:
    - Las coordenada del vector en el sistema de referencia B.
    """

    alpha, beta, gamma = euler_angles
    
    # Matriz de rotación sobre X
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])
    
    # Matriz de rotación sobre Y
    R_y = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    
    # Matriz de rotación sobre Z
    R_z = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])
    
    # Matriz de rotación total (Z * Y * X)
    R = R_z @ R_y @ R_x
    
    # Transformación: (vector - traslación) * rotación
    transformed_vector = R @ (vector - translation)
    
    return transformed_vector
