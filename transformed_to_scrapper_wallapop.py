import os
import json
<<<<<<< HEAD
import unicodedata
# Directorios base
input_dir = "transformed_data"
output_dir = "parameters_scrapper"
=======

# Directorios base
input_dir = "../transformed_data"
output_dir = "../parameters_scrapper_wallapop"
>>>>>>> 36901b948494745d7362fd5dc38ae4a5c2c80afe

# Crear directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

<<<<<<< HEAD
def normalize_text(text):
    """
    Normaliza el texto para eliminar inconsistencias en caracteres con acentos.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

def transformar_combustible(version):
    """
    Transforma el tipo de combustible según las reglas especificadas para una versión.
    """
    if 'Combustible' in version:
        combustible = normalize_text(version['Combustible'])  # Normalizar el texto
        if 'Gasolina' in combustible:
            version['Combustible'] = 'gasoline'
        elif 'Gasoleo' in combustible:  # Nota: 'Gasoleo' después de normalizar
            version['Combustible'] = 'gasoil'

    if 'Distintivo ambiental DGT' in version:
        distintivo = normalize_text(version['Distintivo ambiental DGT'])  # Normalizar
        if '0 emisiones' in distintivo or 'ECO' in distintivo:
            version['Combustible'] = 'electric-hybrid'

    return version.get('Combustible', 'unknown')
def process_version(version, brand, model, output_path):
    """
    Procesa una versión individual y guarda un archivo JSON con sus datos.
    """
    try:
        # Obtener nombre único para la versión
        version_name = version.get("name", "unknown_version").replace(" ", "_")
        file_name = f"{brand}_{model}_{version_name}.json"
        file_path = os.path.join(output_path, file_name)

        # Transformar el combustible directamente aquí
        fuel_type = transformar_combustible(version)

        # Crear datos para la versión
        version_data = {
            "brand": brand,
            "model": model,
            "version_name": version.get("name", ""),
            "start_year": version.get("start_year", 0),
            "end_year": version.get("end_year", 0),
            "keywords": version.get("name", ""),
            "fuel_type": fuel_type  # Combustible procesado
        }

        # Guardar la versión como JSON
        with open(file_path, 'w', encoding='utf-8') as out_file:
            json.dump(version_data, out_file, indent=4)

        print(f"Guardado: {file_path}")
    except Exception as e:
        print(f"Error procesando versión: {e}")



def process_json(file_path, brand, output_path):
    """
    Procesa un archivo JSON para extraer las versiones y guardar archivos por cada una.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Obtener modelo y versiones
        model = data.get("name", "unknown_model").replace(" ", "_")
        versions = data.get("versions", [])

        # Procesar cada versión
        for version in versions:
            process_version(version, brand, model, output_path)
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")

=======
def transformar_combustible(data):
    """
    Transforma el tipo de combustible según las reglas especificadas.
    """
    if 'specs' in data:
        specs = data['specs']
        
        # Transformar el combustible
        if 'combustible' in specs:
            combustible = specs['combustible']
            if 'Gasolina' in combustible:
                specs['combustible'] = 'gasoline'
            elif 'Gasóleo' in combustible:
                specs['combustible'] = 'gasoil'
        
        # Verificar el distintivo ambiental y asignar combustible 'electric-hybrid'
        if 'Distintivo ambiental DGT' in specs:
            distintivo = specs['Distintivo ambiental DGT']
            if '0 emisiones' in distintivo or 'ECO' in distintivo:
                specs['combustible'] = 'electric-hybrid'

    return data

def process_json(file_path, brand):
    """
    Procesa un archivo JSON para extraer los parámetros necesarios.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Aplicar la transformación del combustible
        data = transformar_combustible(data)
        
        # Extraer datos
        model = data.get("name")
        versions = data.get("versions", [])
        
        # Extraer años y keywords de las versiones
        min_year = min(v.get("start_year", 0) for v in versions)
        max_year = max(v.get("end_year", 0) for v in versions)
        keywords = [v.get("name", "") for v in versions]
        
        # Construir estructura de parámetros
        return {
            "brand": brand,
            "model": model,
            "min_year": min_year,
            "max_year": max_year,
            "keywords": keywords
        }
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return None
>>>>>>> 36901b948494745d7362fd5dc38ae4a5c2c80afe

def process_directory(input_dir, output_dir):
    """
    Recorre el directorio de entrada, procesa los archivos JSON y guarda los parámetros.
    """
    for root, _, files in os.walk(input_dir):
        # Obtener la ruta relativa para replicar la estructura
        relative_path = os.path.relpath(root, input_dir)
        output_path = os.path.join(output_dir, relative_path)
        
        # Crear directorio de salida si no existe
        os.makedirs(output_path, exist_ok=True)
        
        # Procesar cada archivo JSON
        brand = os.path.basename(root)  # Nombre del subdirectorio actual
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
<<<<<<< HEAD
                
                # Procesar el archivo JSON
                process_json(file_path, brand, output_path)
=======
                output_file = os.path.join(output_path, file)
                
                # Procesar el archivo JSON
                parameters = process_json(file_path, brand)
                if parameters:
                    # Guardar parámetros en JSON
                    with open(output_file, 'w') as out_file:
                        json.dump(parameters, out_file, indent=4)
>>>>>>> 36901b948494745d7362fd5dc38ae4a5c2c80afe

if __name__ == "__main__":
    process_directory(input_dir, output_dir)
    print(f"Parámetros guardados en la carpeta '{output_dir}'")
