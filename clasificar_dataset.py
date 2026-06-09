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
ruta_dataset = 'lpd_5/lpd_5_cleansed' 
ruta_salida = 'dataset_limpio'

def main():
    diccionario_ids = {}
    archivos_txt = glob.glob(os.path.join(ruta_txts, '*.txt'))
    print(f"{turquesaColor}[+] Mapeando géneros desde Tagtraum...{finColor}")
    try:
        # Leer los .txt y armar el diccionario
        for ruta in archivos_txt:
            nombre_genero = os.path.basename(ruta).replace('id_list_', '').replace('.txt', '')
            os.makedirs(os.path.join(ruta_salida, nombre_genero), exist_ok=True)
            with open(ruta, 'r', encoding='utf-8') as f:
                for linea in f:
                    track_id = linea.strip()
                    if track_id:
                        diccionario_ids[track_id] = nombre_genero       
            print(f"\t{verdeColor}[+]{finColor} {nombre_genero} mapeado.")
        total_ids = len(diccionario_ids)
        print(f"\n{turquesaColor}[+] Total de IDs únicos en diccionario: {total_ids}{finColor}")
        print(f"{turquesaColor}[+] Extrayendo y clasificando archivos .npz...{finColor}")
        archivos_copiados = 0
        # Recorrer dataset original y copiar
        for raiz, _, archivos in os.walk(ruta_dataset):
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
        print(f"\n{verdeColor}[+] Proceso completado. Se ordenaron {archivos_copiados} canciones en la carpeta: {ruta_salida}.{finColor}\n")
    except KeyboardInterrupt:
        print(f"\n\n{amarilloColor}[!] Saliendo...{finColor}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{rojoColor}[-] Error: {e}{finColor}\n")

if __name__ == '__main__':
    main()