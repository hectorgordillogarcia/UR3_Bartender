import json
import time
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def ejecutar_movimiento(bebida):
    logging.info(f"INICIANDO MOVIMIENTO: Recogiendo {bebida}")
    time.sleep(20)  # Simulación de movimiento (20 segundos)
    logging.info("MOVIMIENTO COMPLETADO: Bebida entregada")
    with open("eleccion.json", "w") as f:
        json.dump({"estado": "libre"}, f)

def main():
    while True:
        try:
            with open("eleccion.json", "r") as f:
                data = json.load(f)
                if data.get("estado") == "ocupado":
                    ejecutar_movimiento(data["eleccion"])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        time.sleep(1)

if __name__ == "__main__":
    print("Sistema de brazo robótico inicializado. Esperando órdenes...")
    main()