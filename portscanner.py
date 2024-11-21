import socket
import csv
import time
from concurrent.futures import ThreadPoolExecutor
import os

def scan_port(ip, port, timeout=1):
    """
    Escanea un puerto específico en una dirección IP.
    
    :param ip: Dirección IP a escanear.
    :param port: Puerto a verificar.
    :param timeout: Tiempo de espera en segundos.
    :return: Tupla (ip, puerto, abierto: bool)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            return (ip, port, result == 0)
    except Exception:
        return (ip, port, False)

def save_to_csv(file_name, data):
    """
    Guarda los datos en un archivo CSV, incluyendo encabezados si el archivo no existe.
    
    :param file_name: Nombre del archivo CSV.
    :param data: Lista de diccionarios con datos a escribir.
    """
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["ip", "puerto abierto", "fecha", "hora"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def scan_ports(ip, start_port=1, end_port=65535, max_threads=100):
    """
    Escanea un rango de puertos en una dirección IP y exporta los resultados de los puertos abiertos a un archivo CSV.
    
    :param ip: Dirección IP a escanear.
    :param start_port: Puerto inicial.
    :param end_port: Puerto final.
    :param max_threads: Número máximo de hilos.
    """
    print(f"Escaneando puertos en {ip}...")
    csv_file = "puertos_abiertos.csv"
    open_ports = []
    
    # Usar un pool de hilos para escanear puertos
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            ip, port, is_open = future.result()
            if is_open:
                print(f"Puerto abierto: {port}")
                timestamp = (time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"))
                open_ports.append({
                    "ip": ip,
                    "puerto abierto": port,
                    "fecha": timestamp[0],
                    "hora": timestamp[1]
                })
    
    # Guardar resultados en CSV
    if open_ports:
        save_to_csv(csv_file, open_ports)
        print(f"Puertos abiertos guardados en {csv_file}")
    else:
        print("No se encontraron puertos abiertos.")

if __name__ == "__main__":
    # Solicitar la IP al usuario
    ip_to_scan = input("Ingrese la dirección IP a escanear: ")
    scan_ports(ip_to_scan, start_port=1, end_port=1000, max_threads=100)
