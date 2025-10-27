import pytest
from pathlib import Path
from unittest.mock import patch
import os

from app.config import Settings


@pytest.mark.unit
class TestSettings:
    """Tests para la clase Settings"""

    def test_settings_has_datamart_path(self):
        """Settings debe tener DATAMART_PATH"""
        # Arrange & Act
        settings = Settings()

        # Assert
        assert hasattr(settings, 'DATAMART_PATH')
        assert isinstance(settings.DATAMART_PATH, str)

    def test_settings_has_base_dir(self):
        """Settings debe tener BASE_DIR"""
        # Arrange & Act
        settings = Settings()

        # Assert
        assert hasattr(settings, 'BASE_DIR')
        assert isinstance(settings.BASE_DIR, Path)

    def test_get_parquet_files_returns_list(self, test_datamart_dir, monkeypatch):
        """get_parquet_files debe retornar lista"""
        # Arrange
        settings = Settings()
        monkeypatch.setattr(settings, 'DATAMART_PATH', str(test_datamart_dir))

        # Act
        files = settings.get_parquet_files()

        # Assert
        assert isinstance(files, list)

    def test_get_parquet_files_returns_only_parquet(self, test_datamart_dir, monkeypatch):
        """Debe retornar solo archivos .parquet"""
        # Arrange
        settings = Settings()
        monkeypatch.setattr(settings, 'DATAMART_PATH', str(test_datamart_dir))

        # Act
        files = settings.get_parquet_files()

        # Assert
        for file in files:
            assert file.suffix == '.parquet'

    def test_get_parquet_files_raises_error_if_dir_not_exists(self):
        """Debe lanzar error si el directorio no existe"""
        # Arrange
        settings = Settings()
        settings.DATAMART_PATH = "/path/that/does/not/exist"

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            settings.get_parquet_files()

        assert "no encontrado" in str(exc_info.value).lower()

    def test_get_parquet_files_raises_error_if_no_files(self, tmp_path):
        """Debe lanzar error si no hay archivos parquet"""
        # Arrange
        settings = Settings()
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        settings.DATAMART_PATH = str(empty_dir)

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            settings.get_parquet_files()

        assert "no se encontraron" in str(exc_info.value).lower()

    @patch.dict(os.environ, {'DATAMART_PATH': './datamart/data'})
    def test_reads_datamart_path_from_env(self):
        """Debe leer DATAMART_PATH desde variable de entorno"""
        # Act
        settings = Settings()

        # Assert
        assert settings.DATAMART_PATH == './datamart/data'

    @patch.dict(os.environ, {'DEBUG': 'True'}) #'DEBUG': 'False'}
    def test_reads_debug_from_env_true(self):
        """Debe leer DEBUG=True desde variable de entorno"""
        # Act
        settings = Settings()

        # Assert
        assert settings.DEBUG is True
