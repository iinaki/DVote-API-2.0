from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from db import SessionLocal

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.db = SessionLocal()
        try:
            response = await call_next(request)
            request.state.db.commit()  # Commit al final de la solicitud
        except Exception as e:
            request.state.db.rollback()  # Rollback en caso de error
            raise e
        finally:
            request.state.db.close()
        return response

# Dependency para obtener la sesión de la base de datos
def get_db(request: Request):
    return request.state.db