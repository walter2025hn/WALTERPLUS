import requests
import re

def obtener_enlaces():
    # Usaremos una fuente que recopila enlaces de diversas webs de deportes
    # Esta es una fuente de ejemplo que suele ser más amigable con scripts
    urls_fuentes = [
        "https://raw.githubusercontent.com/m3u4u/m3u4u/main/deportes.m3u", # Ejemplo de lista externa
        "https://pastebin.com/raw/L9u6vD7S" # Ejemplo de enlaces temporales
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    enlaces_encontrados = []

    for url in urls_fuentes:
        try:
            print(f"Probando fuente: {url}")
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_status == 200:
                # Busca cualquier cosa que parezca un link de video .m3u8
                links = re.findall(r'(https?://[^\s"\'<>]+(?:\.m3u8|\.ts)[^\s"\'<>]*)', r.text)
                enlaces_encontrados.extend(links)
        except:
            continue
            
    return list(set(enlaces_encontrados))

def actualizar_m3u():
    enlaces_nuevos = obtener_enlaces()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas_anteriores = f.readlines()
    except:
        lineas_anteriores = ["#EXTM3U\n"]

    # Limpiamos los canales "Auto-Actualizados" viejos para no llenar la lista de basura
    nuevas_lineas = [l for l in lineas_anteriores if "AUTO-TV" not in l and "http" not in l or "github" in l]

    if enlaces_nuevos:
        for i, link in enumerate(enlaces_nuevos[:20]): # Solo los primeros 20 para probar
            nuevas_lineas.append(f'#EXTINF:-1 group-title="DEPORTES AUTOMATICOS", AUTO-TV {i+1}\n{link}\n')
        print(f"¡Éxito! Se agregaron {len(enlaces_nuevos[:20])} canales.")
    else:
        print("No se encontraron enlaces en las fuentes alternativas.")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

if __name__ == "__main__":
    actualizar_m3u()
