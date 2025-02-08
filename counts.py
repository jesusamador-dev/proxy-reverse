import json

def count_gerencias(data, territory_id=0):
    gerencias_count = 0
    territorios = data.get("resultado", {}).get("territorios", [])

    # Si el usuario ingresa 0, contar todas las gerencias en todos los territorios
    if territory_id == 0:
        for territorio in territorios:
            for zona in territorio.get("zonas", []):
                for region in zona.get("regiones", []):
                    gerencias_count += len(region.get("gerencias", []))
    else:
        # Buscar el territorio especificado por IdTerritorio
        territory = next((t for t in territorios if t["IdTerritorio"] == territory_id), None)
        if territory:
            for zona in territory.get("zonas", []):
                for region in zona.get("regiones", []):
                    gerencias_count += len(region.get("gerencias", []))
        else:
            print(f"Territorio con ID {territory_id} no encontrado.")

    return gerencias_count

# Leer el archivo JSON principal (geo.json)
with open('./jsons/geo.json', 'r', encoding='utf-8') as file:
    data_geo = json.load(file)

# Leer el archivo JSON con el filtro de geografía (filtro.json)
with open('./jsons/gerencias.json', 'r', encoding='utf-8') as file:
    data_filtro = json.load(file)

# Solicitar el ID del territorio al usuario
territory_id = int(input("Ingrese el ID del territorio (0 para todos): "))

# Contar las gerencias en el archivo geo.json
gerencias_total = count_gerencias(data_geo, territory_id)
print(f"Total de gerencias en geo.json: {gerencias_total}")

# Contar las gerencias en el filtro de geografía
gerencias_filtro = data_filtro.get("filtroGeografia", {}).get("Gerencias", [])
gerencias_filtro_count = len(gerencias_filtro)
print(f"Total de gerencias en filtro.json: {gerencias_filtro_count}")

# Comparar los resultados
if gerencias_total == gerencias_filtro_count:
    print("El número de gerencias coincide con el filtro de geografía.")
else:
    print("El número de gerencias no coincide con el filtro de geografía.")
