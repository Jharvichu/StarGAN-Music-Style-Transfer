import os
import shutil
import glob
import sys

# Colores
verdeColor = "\033[1;32m"
finColor = "\033[0m"
rojoColor = "\033[1;31m"
amarilloColor = "\033[1;33m"
moradoColor = "\033[1;35m"
turquesaColor = "\033[1;36m"

# Rutas
ruta_txts = 'labels/id_lists_tagtraum/tagtraum'

# Datasets
DATASETS = [
    {
        "nombre": "LPD-5",
        "origen": "lpd_5/lpd_5_cleansed",
        "destino": "datasets_clasificados/lpd_5"
    },
    {
        "nombre": "LPD-17",
        "origen": "lpd_17/lpd_17_cleansed",
        "destino": "datasets_clasificados/lpd_17"
    }
]

def main():
    diccionario_ids = {}
    archivos_txt = glob.glob(os.path.join(ruta_txts, '*.txt'))
    print(f"{turquesaColor}[+] Mapeando géneros desde Tagtraum...{finColor}")

    try:
        # Leer los .txt y armar diccionario
        for ruta in archivos_txt:
            nombre_genero = os.path.basename(ruta).replace('id_list_', '').replace('.txt', '')
            with open(ruta, 'r', encoding='utf-8') as f:
                for linea in f:
                    track_id = linea.strip()
                    if track_id:
                        diccionario_ids[track_id] = nombre_genero       
            print(f"\t{verdeColor}[+]{finColor} {nombre_genero} mapeado.")
        total_ids = len(diccionario_ids)
        print(f"\n{turquesaColor}[+] Total de IDs únicos en diccionario: {total_ids}{finColor}\n")

        # Recorrer los datasets configurados
        for dataset in DATASETS:
            ruta_origen = dataset["origen"]
            ruta_salida = dataset["destino"]
            nombre = dataset["nombre"]
            print(f"{turquesaColor}[*] Procesando dataset: {nombre}{finColor}")

            # Verificar si la carpeta del dataset existe
            if not os.path.exists(ruta_origen):
                print(f"\t{amarilloColor}[!] No se encontró la carpeta '{ruta_origen}'. Saltando dataset...{finColor}\n")
                continue
            print(f"\t{turquesaColor}[+] Extrayendo y clasificando archivos .npz...{finColor}")

            # Crear carpetas de salida
            for genero in set(diccionario_ids.values()):
                os.makedirs(os.path.join(ruta_salida, genero), exist_ok=True)
            archivos_copiados = 0

            # Recorrer y copiar
            for raiz, _, archivos in os.walk(ruta_origen):
                for archivo in archivos:
                    if archivo.endswith('.npz'):
                        track_id = os.path.basename(raiz)
                        if track_id in diccionario_ids:
                            genero = diccionario_ids[track_id]
                            origen = os.path.join(raiz, archivo)
                            destino = os.path.join(ruta_salida, genero, f"{track_id}.npz")
                            shutil.copy2(origen, destino)
                            archivos_copiados += 1
                            if archivos_copiados % 500 == 0:
                                print(f"\t{amarilloColor}[*] Se han clasificado {archivos_copiados} canciones...{finColor}")
            print(f"\t{verdeColor}[+] Proceso de {nombre} completado. {archivos_copiados} canciones en: {ruta_salida}.{finColor}\n")
            
        print(f"{verdeColor}[+] Toda la clasificación ha finalizado con éxito{finColor}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{amarilloColor}[!] Saliendo...{finColor}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{rojoColor}[-] Error: {e}{finColor}\n")

if __name__ == '__main__':
    main()