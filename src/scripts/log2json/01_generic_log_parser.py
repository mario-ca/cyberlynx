###############################################################################
# Fichero: log_parser.py
# Descripción: Script que convierte un archivo de log de syslog en json
###############################################################################

import sys
import os
import logging
import json
from pythonjsonlogger import jsonlogger

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
            parts = line.strip().split(' ', 3)
            if len(parts) == 4:
                # Extraer los cuatro campos del evento de log
                timestamp = parts[0]
                hostname = parts[1]
                service = parts[2]
                message = parts[3]
                
                # Crear un diccionario con los campos del evento de log
                log_entry = {
                    "timestamp": timestamp,
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
