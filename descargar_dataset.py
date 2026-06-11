import gdown
import tarfile
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# Colores
verdeColor = "\033[1;32m"
finColor = "\033[0m"
rojoColor = "\033[1;31m"
amarilloColor = "\033[1;33m"
moradoColor = "\033[1;35m"
turquesaColor = "\033[1;36m"

# Datasets
DATASETS = [
    {
        "nombre": "LPD-5 Cleansed (5 pistas)",
        "id": "1n9utlZKgG68RI0nG8jfnmOpdUptbYgQV",
        "archivo": "lpd_5_cleansed.tar.gz"
    },
    {
        "nombre": "LPD-17 Cleansed (17 pistas)",
        "id": "1d_YhFS_VQHrDIk5uT5Izyg3tvYlFDbie",
        "archivo": "lpd_17_cleansed.tar.gz"
    }
]

def main():
    try:
        for dataset in DATASETS:
            url = f'https://drive.google.com/uc?id={dataset["id"]}'
            archivo_destino = dataset["archivo"]
            nombre = dataset["nombre"]
            print(f"{turquesaColor}[*] Procesando: {nombre}{finColor}")
            print(f"{turquesaColor}\t[+] Descargando desde Google Drive...{finColor}")
            # Descargar archivo
            gdown.download(url, archivo_destino, quiet=False)
            print(f"{verdeColor}\t\t[+] Descarga completada con éxito.{finColor}")
            print(f"{turquesaColor}\t[+] Descomprimiendo {archivo_destino}...{finColor}")
            # Descomprimir el archivo .tar.gz de forma limpia
            with tarfile.open(archivo_destino, 'r:gz') as tar:
                if hasattr(tarfile, 'data_filter'):
                    tar.extractall(filter='data')
                else:
                    tar.extractall()
            print(f"\t\t{verdeColor}[+] Descompresión exitosa.{finColor}")
            # Borrar archivo comprimido
            os.remove(archivo_destino) 
            print(f"\t{amarilloColor}[!] Archivo temporal {archivo_destino} eliminado.{finColor}\n")
        print(f"{verdeColor}[+] Todos los datasets fueron descargados y extraídos.{finColor}\n")
    except KeyboardInterrupt:
        print(f"\n\n{amarilloColor}[!] Saliendo...{finColor}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{rojoColor}[-] Error inesperado: {e}{finColor}\n")

if __name__ == '__main__':
    main()