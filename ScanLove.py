#!/usr/bin/python  
import argparse  
from termcolor import colored  
import subprocess  
import signal  
import sys  
from concurrent.futures import ThreadPoolExecutor  
from pyfiglet import Figlet  
from datetime import datetime  

def Show_banner(text):  
    """  
    Imprime en la pantalla el texto proporcionado con un diseño ASCII.  

    Args:  
        text (str): El texto a imprimir con el diseño ASCII.  

    Returns:  
        None  
    """  
    figlet = Figlet(font="rozzo")    
    ascii_art = figlet.renderText(text)  
    try:  
        lolcat_process = subprocess.Popen(['lolcat'], stdin=subprocess.PIPE)  
        lolcat_process.communicate(input=ascii_art.encode())  
    except FileNotFoundError:    
        print(ascii_art)  

def Banner():  
    """  
    Imprime el banner y la información inicial del programa.  

    Returns:  
        None  
    """  
    Show_banner("SCANLOVE")  
    print("@puerto4444")  
    print("-" * 30)  

def Close(sig, frame):  
    """  
    Maneja la interrupción del programa al presionar Ctrl+C.  

    Args:  
        sig (signal): El signal de interrupción.  
        frame (frame): El frame actual del programa.  

    Returns:  
        None  
    """  
    print(colored(f"\n☕ Exit...", "red"))  
    sys.exit(1)  

signal.signal(signal.SIGINT, Close)  

def Arguments():  
    """  
    Parsea los argumentos de la línea de comando.  

    Returns:  
        tuple: Un tuple que contiene la dirección IP objetivo y el nombre del archivo de texto.  
    """  
    parser = argparse.ArgumentParser(description="Descubre Hosts activos")  
    parser.add_argument('-t', '--target', required=True, dest="target",  
                        help="Ex: -t 192.168.0.1-255")  
    parser.add_argument('--save', nargs='?', const='reporte.txt', default=None,  
                        help='Guarda los resultados en un archivo de texto.')  
    args = parser.parse_args()  
    return args.target, args.save  

def Valid_target(target):  
    """  
    Valida el formato de la dirección IP o rango proporcionado.  

    Args:  
        target (str): La dirección IP o rango a validar.  

    Returns:  
        list: Una lista de direcciones IP válidas.  
    """  
    target_split = target.split(".")  
    if len(target_split) != 4:  
        print(colored(f"\n[!] Formato de IP inválido: {target}\n", "red"))  
        return []  
    
    three_octets = '.'.join(target_split[:3])  
    last_octet = target_split[3]  
    
    if "-" in last_octet:  
        try:  
            start, end = map(int, last_octet.split("-"))  
            if start > end or start < 0 or end > 255:  
                print(colored(f"\n[!] Rango de IP inválido: {target}\n", "red"))  
                return []  
            return [f"{three_octets}.{i}" for i in range(start, end + 1)]  
        except ValueError:  
            print(colored(f"\n[!] Formato de rango de IP inválido: {target}\n", "red"))  
            return []  
    else:  
        try:  
            if not 0 <= int(last_octet) <= 255:  
                print(colored(f"\n[!] Octeto final fuera de rango: {target}\n", "red"))  
                return []  
            return [target]  
        except ValueError:  
            print(colored(f"\n[!] Octeto final no es un número: {target}\n", "red"))  
            return []  

def Discovery_host(target):  
    """  
    Envía un ping a la dirección IP proporcionada para verificar si el host está activo.  

    Args:  
        target (str): La dirección IP a verificar.  

    Returns:  
        str: La dirección IP activa, o None si el host no responde.  
    """  
    try:  
        discovery = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)  
        if discovery.returncode == 0:  
            print(colored(f"\n\tHost: {target} UP", "green", attrs=["bold"]))  
            return target  
    except subprocess.TimeoutExpired:  
        pass  
    return None  

def Save_results(results, name_archive='reporte.txt'):  
    """  
    Guarda los resultados del escaneo en un archivo de texto.  

    Args:  
        resultados (list): Lista de direcciones IP activas.  
        nombre_archivo (str): Nombre del archivo de salida.  

    Returns:  
        None  
    """  
    try:  
        with open(name_archive, 'w') as f:  
            f.write("=== Reporte de Escaneo de Red ===\n")  
            f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")  
            f.write("=" * 35 + "\n\n")  
            
            if results:  
                f.write("Hosts Activos Encontrados:\n")  
                for host in results:  
                    f.write(f"- {host} UP\n")  
            else:  
                f.write("No se encontraron hosts activos.\n")  
        print(colored(f"\n[+] Reporte de texto generado: {name_archive}", "yellow"))  
    except Exception as e:  
        print(colored(f"\n[!] Error al guardar el archivo de texto: {e}", "red"))  

def main():  
    Banner()  
    target, generar_txt = Arguments()    
    targets = Valid_target(target)  
    if not targets:  
        print(colored("[!] No hay direcciones IP válidas para escanear.", "red"))  
        sys.exit(1)  
    
    results = []  
    with ThreadPoolExecutor(max_workers=100) as executor:  
        for result in executor.map(Discovery_host, targets):  
            if result:  
                results.append(results)  
    if generar_txt:  
        Save_results(results, generar_txt)

if __name__ == "__main__":  
    main()
