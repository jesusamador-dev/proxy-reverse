from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from starlette.responses import JSONResponse, Response

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/{path:path}")
async def consume_external_service(path: str, request: Request):
    base_url = "https://ffm.cycmovil.com/"
    full_url = f"{base_url}/{path}"  # Complementar la URL con el path

    try:
        headers = {}
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        body = await request.json()

        # Preparar la solicitud al servicio externo
        req = requests.post(full_url, headers=headers, json=body)

        # Devolver la respuesta tal cual como viene del servicio externo
        return Response(content=req.content, status_code=req.status_code, media_type=req.headers.get("Content-Type"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@app.get("/mayra")
async def consume_endpoint(request: Request):  # Elimina el parámetro 'path' innecesario
    try:
        base_url = 'https://api.odysseyaimodel.com/mapa/gmaps'
        params = {  # Define los parámetros en un diccionario
            "y": 3632,
            "x": 1800,
            "zoom": 13,
            "layers": "MapaBAZ"
        }

        try:
            req = requests.get(base_url, params=params, timeout=10, stream=True)
            req.raise_for_status()

            content = b"".join(chunk for chunk in req.iter_content(chunk_size=8192))

            return Response(
                content=content,  # Ahora 'content' son bytes
                status_code=req.status_code,
                media_type=req.headers.get("Content-Type")
            )
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error al comunicarse con el servicio externo: {str(e)}")

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
