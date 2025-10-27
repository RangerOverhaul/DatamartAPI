import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Configuración de la aplicación"""

    APP_NAME: str = "Sales Datamart API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATAMART_PATH: str = os.getenv("DATAMART_PATH", str(BASE_DIR / "datamart"))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Firebase Config
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")

    # JWT Config
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 5))

    ALLOWED_ORIGINS: list = [ #Local
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