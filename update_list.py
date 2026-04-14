import requests
import re

def obtener_enlaces():
    # Estas fuentes son de repositorios que se actualizan constantemente
    urls_fuentes = [
        "https://raw.githubusercontent.com/GuuS-DeV/p-m3u/main/Deportes.m3u",
        "https://raw.githubusercontent.com/Iptv-Tv/TDT_Honduras/main/Honduras.m3u"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    enlaces_encontrados = []

    for url in urls_fuentes:
        try:
            print(f"Buscando en: {url}")
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                # Extraemos los nombres y los links
                enlaces = re.findall(r'#EXTINF:.*,(.*)\n(http.*)', r.text)
                enlaces_encontrados.extend(enlaces)
        except:
            continue
            
    return enlaces_encontrados

def actualizar_m3u():
    canales = obtener_enlaces()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    # Mantenemos tus canales locales fijos (HCH, Canal 11, etc.)
    # Si quieres que el script no borre NADA de lo que ya tienes, 
    # simplemente agregaremos lo nuevo al final.
    
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            contenido_actual = f.read()
    except:
        contenido_actual = "#EXTM3U\n"

    lineas_nuevas = []
    
    if canales:
        for nombre, link in canales:
            # Solo agregamos si el link no está ya en tu lista
            if link not in contenido_actual:
                lineas_nuevas.append(f'#EXTINF:-1 group-title="AUTO-ACTUALIZADO", {nombre.strip()}\n{link}\n')
        
        # Escribimos al final del archivo para no borrar tus logos
        with open(nombre_archivo, "a", encoding="utf-8") as f:
            f.writelines(lineas_nuevas)
        print(f"¡Listo! Se agregaron {len(lineas_nuevas)} canales nuevos.")
    else:
        print("No se encontraron canales nuevos en las fuentes.")

if __name__ == "__main__":
    actualizar_m3u()
