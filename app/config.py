import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuración de la aplicación"""

    APP_NAME: str = "Sales Datamart API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATAMART_PATH: str = os.getenv("DATAMART_PATH", str(BASE_DIR / "datamart"))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    def get_parquet_files(self) -> list:
        """Retorna lista de archivos parquet en /datamart"""
        datamart_dir = Path(self.DATAMART_PATH)
        if not datamart_dir.exists():
            raise FileNotFoundError(f"Directorio de datamart no encontrado: {datamart_dir}")

        parquet_files = list(datamart_dir.glob("*.parquet"))
        if not parquet_files:
            raise FileNotFoundError(f"No se encontraron archivos .parquet en {datamart_dir}")

        return parquet_files


# Instancia global de configuración
settings = Settings()