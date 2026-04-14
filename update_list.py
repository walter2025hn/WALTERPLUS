import requests

def actualizar_m3u():
    # Esta es la fuente más estable que existe en GitHub
    url = "https://iptv-org.github.io/iptv/index.m3u"
    nombre_archivo = "LISTA VERSASERa.m3u"
    
    try:
        print("Conectando a la base de datos mundial...")
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            lineas = r.text.splitlines()
            nuevos_canales = []
            
            # Buscamos solo canales que te interesan (ESPN, Fox, Honduras)
            for i in range(len(lineas)):
                if "#EXTINF" in lineas[i]:
                    # Filtro inteligente: Deportes o canales de Honduras
                    if any(x in lineas[i].upper() for x in ["ESPN", "FOX SPORTS", "HONDURAS", "WIN SPORTS"]):
                        nuevos_canales.append(lineas[i]) # La info del canal
                        nuevos_canales.append(lineas[i+1]) # El link
            
            # Guardamos el archivo (esto sobrescribirá lo viejo con lo nuevo funcional)
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                f.write("\n".join(nuevos_canales))
            
            print(f"¡Éxito! Se encontraron {len(nuevos_canales)//2} canales deportivos.")
        else:
            print("La fuente principal está en mantenimiento.")
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    actualizar_m3u()
