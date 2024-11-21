import socket
import time
import csv
import os

def monitor_domain_ip(domain, interval=5, csv_file="ips_monitor.csv"):
    """
    Monitorea la dirección IP de un dominio y registra los cambios en un archivo CSV.
    
    :param domain: El dominio a monitorear (ej. "example.com").
    :param interval: Intervalo de tiempo en segundos para revisar la IP (por defecto 5 segundos).
    :param csv_file: Nombre del archivo CSV donde se guardarán los registros.
    """
    def write_to_csv(file_name, data):
        """
        Escribe un registro en el archivo CSV, incluyendo encabezados si el archivo no existe.
        
        :param file_name: Nombre del archivo CSV.
        :param data: Diccionario con los datos a escribir.
        """
        file_exists = os.path.exists(file_name)
        with open(file_name, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "nombre del dominio", "ip", "fecha", "hora"])
            
            # Escribir encabezado si el archivo es nuevo
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data)
    
    try:
        # Obtener la IP inicial
        current_ip = socket.gethostbyname(domain)
        print(f"[{time.ctime()}] IP inicial de {domain}: {current_ip}")
        
        # Inicializar contador de registros
        record_id = 1
        
        # Guardar IP inicial en el archivo CSV
        write_to_csv(csv_file, {
            "id": record_id,
            "nombre del dominio": domain,
            "ip": current_ip,
            "fecha": time.strftime("%Y-%m-%d"),
            "hora": time.strftime("%H:%M:%S")
        })
        
        while True:
            # Esperar el intervalo definido
            time.sleep(interval)
            
            # Resolver la IP nuevamente
            new_ip = socket.gethostbyname(domain)
            
            if new_ip != current_ip:
                print(f"[{time.ctime()}] La IP del dominio {domain} ha cambiado: {new_ip}")
                current_ip = new_ip  # Actualizar la IP actual
                
                # Incrementar el contador y guardar el cambio en el CSV
                record_id += 1
                write_to_csv(csv_file, {
                    "id": record_id,
                    "nombre del dominio": domain,
                    "ip": current_ip,
                    "fecha": time.strftime("%Y-%m-%d"),
                    "hora": time.strftime("%H:%M:%S")
                })
            else:
                print(f"[{time.ctime()}] La IP del dominio {domain} sigue siendo: {current_ip}")
    
    except socket.gaierror as e:
        print(f"Error al resolver el dominio {domain}: {e}")
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")

# Ejemplo de uso
if __name__ == "__main__":
    domain_to_monitor = "cerronavia.cl"
    monitor_domain_ip(domain_to_monitor, interval=5)
