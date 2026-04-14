import requests
import re

def obtener_enlaces():
    url_fuente = "https://www.cablevisionhd.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url_fuente, headers=headers, timeout=15)
        # Extrae los enlaces .m3u8 de la página
        enlaces = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.m3u8', response.text)
        return list(set(enlaces))
    except:
        return []

def actualizar_m3u():
    enlaces_nuevos = obtener_enlaces()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    if not enlaces_nuevos:
        print("No se encontraron links nuevos.")
        return

    # 1. Leemos lo que ya tienes para no borrar tus canales de Honduras
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas_actuales = f.readlines()
    except FileNotFoundError:
        lineas_actuales = ["#EXTM3U\n"]

    # 2. Filtramos para quitar los links viejos de ESPN/Cablevision y dejar lo demás
    nuevas_lineas = []
    for linea in lineas_actuales:
        # Si la línea no contiene links viejos de la web, la dejamos
        if "cablevision" not in linea.lower():
            nuevas_lineas.append(linea)

    # 3. Agregamos los links nuevos al final
    for link in enlaces_nuevos:
        nuevas_lineas.append(f"#EXTINF:-1, Canal Actualizado\n{link}\n")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)
    print("¡Lista actualizada manteniendo tus canales anteriores!")

if __name__ == "__main__":
    actualizar_m3u()
