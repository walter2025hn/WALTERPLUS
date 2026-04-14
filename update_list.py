import requests
import re

def obtener_peliculas_y_series():
    # Estas fuentes contienen listas de películas y series directas (VOD)
    fuentes = [
        "https://raw.githubusercontent.com/LuchitoIPTV/Series/main/Series.m3u",
        "https://raw.githubusercontent.com/Kodi-Libre/Kodi-Libre/master/Peliculas.m3u",
        "https://raw.githubusercontent.com/tomasm93/m3u8/master/Peliculas.m3u"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    contenido_total = []

    for url in fuentes:
        try:
            print(f"Buscando contenido en: {url}")
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                # Extraemos la info y el link directo al archivo de video (.mp4, .mkv, .m3u8 de video)
                enlaces = re.findall(r'(#EXTINF:.*,.*\nhttp.*)', r.text)
                contenido_total.extend(enlaces)
        except:
            continue
    return contenido_total

def actualizar_m3u():
    items_vod = obtener_peliculas_y_series()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    # 1. Leemos tu lista actual para no borrar tus canales deportivos
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas_actuales = f.readlines()
    except:
        lineas_actuales = ["#EXTM3U\n"]

    # 2. Quitamos contenido VOD viejo para no tener enlaces caídos
    final_lineas = []
    for linea in lineas_actuales:
        if "PELICULA" not in linea.upper() and "SERIE" not in linea.upper():
            final_lineas.append(linea)

    # 3. Agregamos las nuevas películas y series
    if items_vod:
        for item in items_vod[:100]: # Traemos las primeras 100 para probar
            # Aseguramos que tengan la etiqueta de grupo para que tu app las separe bien
            info_corregida = item.replace("#EXTINF:-1", '#EXTINF:-1 group-title="PELICULAS Y SERIES"')
            final_lineas.append(info_corregida + "\n")
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.writelines(final_lineas)
        print(f"¡Listo! Se agregaron {len(items_vod[:100])} películas y series a la carta.")
    else:
        print("No se encontró contenido VOD en las fuentes.")

if __name__ == "__main__":
    actualizar_m3u()
