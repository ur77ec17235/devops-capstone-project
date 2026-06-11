"""
Test cases for application configuration
"""
import importlib
from unittest import TestCase
from unittest.mock import patch

import service.config as config


class TestConfig(TestCase):
    """Test application configuration"""

    def test_config_with_database_uri(self):
        """It should use DATABASE_URI when it is provided"""
        with patch.dict(
            "os.environ",
            {"DATABASE_URI": "postgresql://user:pass@host:5432/db"},
            clear=False,
        ):
            cfg = importlib.reload(config)
            self.assertEqual(
                cfg.DATABASE_URI,
                "postgresql://user:pass@host:5432/db",
            )
            self.assertEqual(
                cfg.SQLALCHEMY_DATABASE_URI,
                "postgresql://user:pass@host:5432/db",
            )
            self.assertFalse(cfg.SQLALCHEMY_TRACK_MODIFICATIONS)
            self.assertEqual(cfg.SECRET_KEY, "s3cr3t-key-shhhh")

    def test_config_builds_database_uri(self):
        """It should build DATABASE_URI when DATABASE_URI is not provided"""
        env = {
            "DATABASE_USER": "postgres",
            "DATABASE_PASSWORD": "postgres",
            "DATABASE_NAME": "postgres",
            "DATABASE_HOST": "localhost",
            "SECRET_KEY": "test-secret",
        }

        with patch.dict("os.environ", env, clear=True):
            cfg = importlib.reload(config)
            self.assertEqual(
                cfg.DATABASE_URI,
                "postgresql://postgres:postgres@localhost:5432/postgres",
            )
            self.assertEqual(
                cfg.SQLALCHEMY_DATABASE_URI,
                "postgresql://postgres:postgres@localhost:5432/postgres",
            )
            self.assertFalse(cfg.SQLALCHEMY_TRACK_MODIFICATIONS)
            self.assertEqual(cfg.SECRET_KEY, "test-secret")