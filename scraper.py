import csv
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configura Chrome sin ventana (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

def obtener_icono_url(item_id):
    url = f"https://www.wowhead.com/item={item_id}"
    driver.get(url)
    time.sleep(2)  # espera a que cargue JavaScript (ajusta si es necesario)

    elements = driver.find_elements("tag name", "ins")
    for el in elements:
        style = el.get_attribute("style")
        if style and "wow.zamimg.com/images/wow/icons/small/" in style:
            start = style.find("url(\"") + len("url(\"")
            end = style.find("\")", start)
            small_url = style[start:end]
            large_url = small_url.replace("/small/", "/large/")
            return large_url

    return None

def descargar_iconos(csv_path):
    os.makedirs("imagenes_items", exist_ok=True)

    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            item_id = row[0].strip()
            print(f"Procesando ID: {item_id}")
            url = obtener_icono_url(item_id)
            if url:
                img = requests.get(url)
                if img.status_code == 200:
                    ruta = f"imagenes_items/{item_id}.jpg"
                    with open(ruta, "wb") as out:
                        out.write(img.content)
                    print(f"[✓] Imagen guardada: {ruta}")
                else:
                    print(f"[x] No se pudo descargar la imagen para {item_id}")
            else:
                print(f"[x] Ícono no encontrado para {item_id}")

    driver.quit()

# Ejecutar
descargar_iconos("ids.csv")
