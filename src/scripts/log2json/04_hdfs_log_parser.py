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

def parse_hdfs_log_file(log_file):
    logs = []
    with open(log_file, 'r') as file:
        for line in file:
            # Dividir la línea del evento en diferentes partes
            parts = line.strip().split(' ')
            if len(parts) >= 8:
                # Extraer las diferentes partes del evento
                timestamp_parts = parts[0], parts[1]
                timestamp_str = f"{timestamp_parts[0]} {timestamp_parts[1][:6]}"
                
                # Formatear el timestamp al formato ISO 8601
                timestamp = datetime.strptime(timestamp_str, "%y%m%d %H%M%S").isoformat()

                # Extraer el hostname, servicio y mensaje
                hostname = parts[6]
                service = parts[7][4:-1]
                message = ' '.join(parts[8:])
                
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
    logs = parse_hdfs_log_file(input_file)
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
