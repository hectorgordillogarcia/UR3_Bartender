
# Documentación del código

## Funciones

### 1. `connect_robot()`
**Propósito:**  
Establece una conexión con el robot, inicializando las interfaces de control, recepción y E/S.

**Parámetros de entrada:**  
- No tiene parámetros de entrada.

**Retorno:**  
- **bool**: Retorna `True` si la conexión al robot es exitosa, de lo contrario `False`.

---

### 2. `check_timeout(condition, affirmation)`
**Propósito:**  
Espera que se cumpla una condición dentro de un tiempo determinado. Permite comprobar si una condición es verdadera o falsa según el valor de `affirmation`.

**Parámetros de entrada:**  
- **condition**: Función sin parámetros que devuelve un valor booleano.  
- **affirmation** (`bool`): Si es `True`, la función espera que `condition()` sea verdadera. Si es `False`, espera que `condition()` sea falsa.

**Retorno:**  
- **bool**: Retorna `True` si la condición se cumple dentro del tiempo establecido, de lo contrario `False`.

---

### 3. `CloseGrip()`
**Propósito:**  
Cierra la pinza del robot.

**Parámetros de entrada:**  
- No tiene parámetros de entrada.

**Retorno:**  
- **bool**: Retorna `True` si la pinza se cierra correctamente, de lo contrario `False`.

---

### 4. `OpenGrip()`
**Propósito:**  
Abre la pinza del robot.

**Parámetros de entrada:**  
- No tiene parámetros de entrada.

**Retorno:**  
- **bool**: Retorna `True` si la pinza se abre correctamente, de lo contrario `False`.

---

### 5. `moveL(target, speed, acceleration)`
**Propósito:**  
Realiza un movimiento lineal del robot a una posición cartesiana dada, utilizando la cinemática inversa.

**Parámetros de entrada:**  
- **target** (`list` o `np.array`): Coordenadas cartesianas de destino `[x, y, z, rx, ry, rz]`.  
- **speed** (`float`): Velocidad de movimiento.  
- **acceleration** (`float`): Aceleración de movimiento.

**Retorno:**  
- **bool**: Retorna `True` si se alcanza el objetivo dentro del tiempo especificado, de lo contrario `False`.

---

### 6. `moveL_FK(target_q, speed, acceleration)`
**Propósito:**  
Realiza un movimiento lineal del robot a una posición articular dada, utilizando la cinemática inversa.

**Parámetros de entrada:**  
- **target_q** (`list` o `np.array`): Posiciones articulares de destino `[q1, q2, q3, q4, q5, q6]`.  
- **speed** (`float`): Velocidad de movimiento.  
- **acceleration** (`float`): Aceleración de movimiento.

**Retorno:**  
- **bool**: Retorna `True` si se alcanza el objetivo dentro del tiempo especificado, de lo contrario `False`.

---

### 7. `moveJ_IK(target, speed, acceleration)`
**Propósito:**  
Mueve el robot a una posición cartesiana dada utilizando cinemática inversa, moviendo las articulaciones del robot.

**Parámetros de entrada:**  
- **target** (`list` o `np.array`): Coordenadas cartesianas de destino `[x, y, z, rx, ry, rz]`.  
- **speed** (`float`): Velocidad de movimiento.  
- **acceleration** (`float`): Aceleración de movimiento.

**Retorno:**  
- **bool**: Retorna `True` si se alcanza el objetivo dentro del tiempo especificado, de lo contrario `False`.

---

### 8. `moveJ(target_q, speed, acceleration)`
**Propósito:**  
Mueve el robot a una posición articular dada.

**Parámetros de entrada:**  
- **target_q** (`list` o `np.array`): Posiciones articulares de destino `[q1, q2, q3, q4, q5, q6]`.  
- **speed** (`float`): Velocidad de movimiento.  
- **acceleration** (`float`): Aceleración de movimiento.

**Retorno:**  
- **bool**: Retorna `True` si se alcanza el objetivo dentro del tiempo especificado, de lo contrario `False`.

---

### 9. `getActualJointPosition()`
**Propósito:**  
Obtiene las posiciones actuales de las articulaciones del robot.

**Parámetros de entrada:**  
- No tiene parámetros de entrada.

**Retorno:**  
- **list**: Retorna una lista con las posiciones articulares actuales `[q1, q2, q3, q4, q5, q6]`.

---

### 10. `getActualTCPPose()`
**Propósito:**  
Obtiene las coordenadas actuales del TCP (Tool Center Point) del robot en el espacio cartesiano.

**Parámetros de entrada:**  
- No tiene parámetros de entrada.

**Retorno:**  
- **list**: Retorna una lista con las coordenadas cartesianas actuales `[x, y, z, rx, ry, rz]` del TCP.

---

### 11. `descendRobotZ(z, speed, acceleration)`
**Propósito:**  
Desciende al robot en la dirección Z de su posición actual, para agarrar o dejar un objeto.

**Parámetros de entrada:**  
- **z** (`float`): Distancia en metros que se desea descender.  
- **speed** (`float`): Velocidad de movimiento.  
- **acceleration** (`float`): Aceleración de movimiento.

**Retorno:**  
- **bool**: Retorna `True` si se alcanza la posición de destino dentro del tiempo especificado, de lo contrario `False`.

---

### 12. `ascendRobotZ(z, speed, acceleration)`
**Propósito:**  
Asciende al robot en la dirección Z de su posición actual, luego de agarrar o dejar un objeto.

**Parámetros de entrada:**  
- **z** (`float`): Distancia en metros que se desea ascender.  
- **speed** (`float`): Velocidad de movimiento.  
- **acceleration** (`float`): Aceleración de movimiento.

**Retorno:**  
- **bool**: Retorna `True` si se alcanza la posición de destino dentro del tiempo especificado, de lo contrario `False`.

---

### 13. `setTcp(z_offset)`
**Propósito:**  
Establece un nuevo offset para el TCP cuando se usa una pinza más larga.

**Parámetros de entrada:**  
- **z_offset** (`float`): Desplazamiento que se debe aplicar al TCP.

**Retorno:**  
- **bool**: Retorna `True` si se actualiza el TCP correctamente, de lo contrario `False`.

---

### 14. `PickAndPlace(target_pick,speed)`
**Propósito:**  
Ejecuta una rutina de pick and place (agarrar y colocar) con el robot, que incluye los siguientes pasos:  
1. Conectar al robot.  
2. Establecer el TCP.  
3. Mover a la posición de espera.  
4. Obtener las coordenadas del objeto a manipular.  
5. Mover al objeto, descender, agarrar, ascender.  
6. Mover al lugar de la bandeja, bajar, soltar, ascender.  
7. Volver a la posición inicial (home).

**Parámetros de entrada:**  
- **target_pick** (`list` o `np.array`): Coordenadas cartesianas de destino `[x, y]`.  
- **speed** (`float`): Velocidad de movimiento durante el proceso de pick and place.

**Retorno:**  
- **bool**: Retorna `True` si el proceso se ejecuta correctamente, de lo contrario `False`.

---

## Resumen
Este código proporciona una interfaz para controlar un robot industrial, realizando tareas de manipulación (como mover, agarrar y colocar objetos) de forma automatizada. La comunicación se realiza a través de interfaces de control, recepción y E/S, y se utilizan diferentes tipos de movimiento del robot, como el movimiento lineal y articular, tanto en coordenadas cartesianas como articulares.
