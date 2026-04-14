import requests
import re

def obtener_enlaces():
    # Intentamos entrar a una sección más específica de deportes si existe
    url_fuente = "https://www.cablevisionhd.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        response = requests.get(url_fuente, headers=headers, timeout=20)
        # Buscamos enlaces que tengan .m3u8 o patrones de servidores comunes de IPTV
        enlaces = re.findall(r'(https?://[^\s"\'<>]+(?:\.m3u8|\.ts)[^\s"\'<>]*)', response.text)
        
        # Si no encuentra nada, buscamos tokens o IDs de canales (esto es más avanzado)
        if not enlaces:
            print("No se detectaron enlaces directos, buscando fuentes alternativas...")
            # Aquí el script intenta buscar dentro de iframes o scripts
            enlaces = re.findall(r'source:\s*"([^"]+)"', response.text)
            
        return list(set(enlaces))
    except Exception as e:
        print(f"Error: {e}")
        return []

def actualizar_m3u():
    enlaces_nuevos = obtener_enlaces()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas_actuales = f.readlines()
    except:
        lineas_actuales = ["#EXTM3U\n"]

    # Filtramos para quitar links que ya no sirven de ESPN o anteriores intentos
    nuevas_lineas = []
    skip = False
    for linea in lineas_actuales:
        if "#EXTINF" in linea and ("ESPN" in linea.upper() or "ACTUALIZADO" in linea.upper()):
            skip = True
            continue
        if skip:
            skip = False
            continue
        nuevas_lineas.append(linea)

    # Si encontramos algo en la web, lo metemos con el formato correcto
    if enlaces_nuevos:
        for i, link in enumerate(enlaces_nuevos):
            if i < 15: # Limitamos a los primeros 15 para no saturar
                nuevas_lineas.append(f'#EXTINF:-1 tvg-logo="" group-title="DEPORTES", CANAL NUEVO {i+1}\n{link}\n')
        print(f"Se agregaron {len(enlaces_nuevos)} enlaces nuevos.")
    else:
        print("La web no entregó enlaces compatibles hoy.")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

if __name__ == "__main__":
    actualizar_m3u()
