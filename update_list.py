import requests
import re

def obtener_enlaces():
    urls_fuentes = [
        "https://raw.githubusercontent.com/GuuS-DeV/p-m3u/main/Deportes.m3u",
        "https://raw.githubusercontent.com/Iptv-Tv/TDT_Honduras/main/Honduras.m3u"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    enlaces_encontrados = []

    for url in urls_fuentes:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                # Buscamos el formato estándar de M3U
                enlaces = re.findall(r'#EXTINF:.*,(.*)\n(http.*)', r.text)
                enlaces_encontrados.extend(enlaces)
        except:
            continue
    return enlaces_encontrados

def actualizar_m3u():
    canales = obtener_enlaces()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except:
        lineas = ["#EXTM3U\n"]

    # MANTENEMOS solo tus canales manuales (los que no dicen AUTO-ACTUALIZADO)
    nuevas_lineas = []
    skip = False
    for linea in lineas:
        if "AUTO-ACTUALIZADO" in linea:
            skip = True
            continue
        if skip and linea.startswith("http"):
            skip = False
            continue
        if not skip:
            nuevas_lineas.append(linea)

    # AGREGAMOS los nuevos encontrados
    if canales:
        for nombre, link in canales[:30]: # Traemos los mejores 30
            nuevas_lineas.append(f'#EXTINF:-1 group-title="AUTO-ACTUALIZADO", {nombre.strip()}\n{link}\n')
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.writelines(nuevas_lineas)
        print(f"¡Éxito! Se actualizaron {len(canales[:30])} canales dinámicos.")
    else:
        print("No se pudo conectar con las fuentes de respaldo.")

if __name__ == "__main__":
    actualizar_m3u()
