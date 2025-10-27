from app.services.datamart import get_datamart_service, DatamartService

def get_current_datamart() -> DatamartService:
    """
    Dependency para obtener el servicio de datamart.
    Se asegura de que esté inicializado.
    """
    service = get_datamart_service()
    if service.data is None:
        raise RuntimeError("Datamart no está cargado")
    return service