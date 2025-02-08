import os
import uvicorn
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


# Punto de entrada
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Railway asigna un puerto automáticamente
    uvicorn.run(app, host="0.0.0.0", port=port)
