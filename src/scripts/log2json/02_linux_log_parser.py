###############################################################################
# Fichero: linux_log_parser.py
# Descripción: Script que convierte un archivo de log de linux en json
###############################################################################

import sys
import os
import logging
import json
from pythonjsonlogger import jsonlogger
from datetime import datetime

###############################################################################
def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger

###############################################################################

def parse_log_file(log_file):
    logs = []
    with open(log_file, 'r') as file:
        for line in file:
            # Separar la línea en 4 bloques diferentes
            parts = line.strip().split(' ')
            if len(parts) >= 6:
                # Extraer los cuatro campos del evento de log
                timestamp_str = ' '.join(parts[:3])

                # Eliminar espacios extra en el timestamp
                timestamp_str = timestamp_str.replace('  ', ' ')
                timestamp = None
                formats_to_try = ["%Y %b %d %H:%M:%S", "%b %d %H:%M:%S"]

                # Intentar parsear el timestamp con diferentes formatos
                for fmt in formats_to_try:
                    try:
                        timestamp = datetime.strptime(timestamp_str, fmt)
                        break
                    except ValueError:
                        pass
                if timestamp is None:
                    continue

                # Extraer los campos del evento de log
                hostname = parts[3]
                service = parts[4].split('(')[0]
                message = ' '.join(parts[5:])

                # Crear un diccionario con los campos del evento de log
                log_entry = {
                    "timestamp": timestamp.isoformat(),
                    "hostname": hostname,
                    "service": service,
                    "message": message
                }
                logs.append(log_entry)
    return logs

###############################################################################

def main(input_file):
    logger = setup_logger()
    logs = parse_log_file(input_file)
    output_file = os.path.join(os.getcwd(), os.path.splitext(input_file)[0] + '.json')
    logger.info(f"Archivo convertido: {output_file}")

    with open(output_file, 'w') as file:
        json.dump(logs, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script_name.py input_file.log")
        sys.exit(1)
    input_file = sys.argv[1]
    main(input_file)
