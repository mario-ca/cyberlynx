###############################################################################
# Fichero: bgl_log_parser.py
# Descripción: Script que convierte un archivo de log de bgl en json
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
    with open(log_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 8:
                # Ajustar índices correctos para timestamp y hostname
                timestamp_str = parts[4]
                hostname = parts[3]

                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d-%H.%M.%S.%f")
                except ValueError:
                    print(f"Error de parsing del timestamp en el evento: {line}")
                    continue  

                # Extraer el mensaje correctamente
                message = ' '.join(parts[7:])

                # Crear un diccionario con los campos del evento de log
                log_entry = {
                    "timestamp": timestamp.isoformat(),
                    "hostname": hostname,
                    "service": "unknown",
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
