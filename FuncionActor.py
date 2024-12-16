from fastapi import FastAPI, HTTPException
import pandas as pd
import os

# Definir la ruta del archivo CSV
resultado_cast_path = os.path.join(os.path.dirname(__file__), 'resultado_cast.csv')
funcion_actor_path = os.path.join(os.path.dirname(__file__), 'FuncionActor.csv')

app = FastAPI()

# Cargar los datasets
try:
    resultado_cast = pd.read_csv(resultado_cast_path)
    funcion_actor = pd.read_csv(funcion_actor_path)
except FileNotFoundError as e:
    raise HTTPException(status_code=500, detail=f"Error al cargar los archivos: {str(e)}")

@app.get("/actor/{actor_name}")
@app.get("/actor/{actor_name}")
def obtener_retorno_actor(actor_name: str):
    # Convertir el nombre del actor a minúsculas para la comparación
    actor_name_normalizado = actor_name.lower()
    
    # Filtrar las películas del actor
    peliculas_actor = resultado_cast[resultado_cast['name'].str.lower() == actor_name_normalizado]
    
    if peliculas_actor.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")

    # Obtener los IDs de las películas
    movie_ids = peliculas_actor['movie_id'].tolist()
    
    # Filtrar las ganancias de las películas en FuncionActor
    ganancias_actor = funcion_actor[funcion_actor['id'].isin(movie_ids)]
    
    # Calcular el retorno total y promedio
    retorno_total = ganancias_actor['revenue'].sum()
    cantidad_peliculas = len(ganancias_actor)
    
    if cantidad_peliculas > 0:
        retorno_promedio = round(retorno_total / cantidad_peliculas, 2)
    else:
        retorno_promedio = 0.0  # Si no hay películas, el retorno promedio es 0

    # Formatear los retornos con signo de dólar
    retorno_total_formateado = f"${retorno_total:,.2f}"
    retorno_promedio_formateado = f"${retorno_promedio:,.2f}"

    return {
        "actor": actor_name,
        "cantidad de peliculas en que actuó": cantidad_peliculas,
        "revenue_total": retorno_total_formateado,
        "revenue_promedio": retorno_promedio_formateado
    }