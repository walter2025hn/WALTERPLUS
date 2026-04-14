import requests

def obtener_peliculas_y_series():
    # Fuentes de repositorios que recopilan peliculas y series abiertas
    fuentes = [
        "https://iptv-org.github.io/iptv/categories/movies.m3u",
        "https://iptv-org.github.io/iptv/categories/animation.m3u", # Para series animadas/anime
        "https://raw.githubusercontent.com/LuchitoIPTV/Series/main/Series.m3u"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    contenido_encontrado = []

    for url in fuentes:
        try:
            print(f"Buscando cine y series en: {url}")
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                lineas = r.text.splitlines()
                for i in range(len(lineas)):
                    if "#EXTINF" in lineas[i]:
                        # Guardamos la info y el link (la siguiente linea)
                        contenido_encontrado.append(lineas[i])
                        contenido_encontrado.append(lineas[i+1])
        except:
            continue
    return contenido_encontrado

def actualizar_m3u():
    vode_data = obtener_peliculas_y_series()
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    # Leemos lo que ya tienes (tus canales de TV)
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            contenido_actual = f.read()
    except:
        contenido_actual = "#EXTM3U\n"

    # Filtramos para no repetir peliculas que ya esten
    nuevos_items = []
    for i in range(0, len(vode_data), 2):
        link = vode_data[i+1]
        if link not in contenido_actual:
            # Personalizamos el grupo para que tu app de IPTV los organice bien
            info = vode_data[i].replace('group-title="', 'group-title="CINE/SERIES - ')
            nuevos_items.append(info)
            nuevos_items.append(link)

    if nuevos_items:
        with open(nombre_archivo, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(nuevos_items))
        print(f"¡Éxito! Se agregaron {len(nuevos_items)//2} nuevas películas y series.")
    else:
        print("No se encontró contenido nuevo para agregar.")

if __name__ == "__main__":
    actualizar_m3u()
