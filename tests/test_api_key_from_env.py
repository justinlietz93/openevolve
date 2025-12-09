"""
Tests for api_key from_env configuration feature
"""

import os
import tempfile
import unittest

from openevolve.config import Config, LLMModelConfig


class TestApiKeyFromEnv(unittest.TestCase):
    """Tests for api_key from_env parameter handling in configuration"""

    def setUp(self):
        """Set up test environment variables"""
        self.test_env_var = "TEST_OPENEVOLVE_API_KEY"
        self.test_api_key = "test-secret-key-12345"
        os.environ[self.test_env_var] = self.test_api_key

    def tearDown(self):
        """Clean up test environment variables"""
        if self.test_env_var in os.environ:
            del os.environ[self.test_env_var]

    def test_api_key_from_env_in_model_config(self):
        """Test that api_key can be loaded from environment variable via from_env"""
        model_config = LLMModelConfig(name="test-model", api_key={"from_env": self.test_env_var})

        self.assertEqual(model_config.api_key, self.test_api_key)

    def test_api_key_direct_value(self):
        """Test that direct api_key value still works"""
        direct_key = "direct-api-key-value"
        model_config = LLMModelConfig(name="test-model", api_key=direct_key)

        self.assertEqual(model_config.api_key, direct_key)

    def test_api_key_none(self):
        """Test that api_key can be None"""
        model_config = LLMModelConfig(name="test-model", api_key=None)

        self.assertIsNone(model_config.api_key)

    def test_api_key_from_env_missing_env_var(self):
        """Test that missing environment variable raises ValueError"""
        with self.assertRaises(ValueError) as context:
            LLMModelConfig(name="test-model", api_key={"from_env": "NONEXISTENT_ENV_VAR_12345"})

        self.assertIn("NONEXISTENT_ENV_VAR_12345", str(context.exception))
        self.assertIn("is not set", str(context.exception))

    def test_api_key_dict_without_from_env_key(self):
        """Test that dict without from_env key raises ValueError"""
        with self.assertRaises(ValueError) as context:
            LLMModelConfig(name="test-model", api_key={"wrong_key": "value"})

        self.assertIn("from_env", str(context.exception))

    def test_api_key_from_env_in_llm_config(self):
        """Test that api_key from_env works at LLM config level"""
        yaml_config = {
            "log_level": "INFO",
            "llm": {
                "api_base": "https://api.openai.com/v1",
                "api_key": {"from_env": self.test_env_var},
                "models": [{"name": "test-model", "weight": 1.0}],
            },
        }

        config = Config.from_dict(yaml_config)

        self.assertEqual(config.llm.api_key, self.test_api_key)
        # Models should inherit the resolved api_key
        self.assertEqual(config.llm.models[0].api_key, self.test_api_key)

    def test_api_key_from_env_per_model(self):
        """Test that api_key from_env can be specified per model"""
        # Set up a second env var for testing
        second_env_var = "TEST_OPENEVOLVE_API_KEY_2"
        second_api_key = "second-secret-key-67890"
        os.environ[second_env_var] = second_api_key

        try:
            yaml_config = {
                "log_level": "INFO",
                "llm": {
                    "api_base": "https://api.openai.com/v1",
                    "models": [
                        {
                            "name": "model-1",
                            "weight": 1.0,
                            "api_key": {"from_env": self.test_env_var},
                        },
                        {"name": "model-2", "weight": 0.5, "api_key": {"from_env": second_env_var}},
                    ],
                },
            }

            config = Config.from_dict(yaml_config)

            self.assertEqual(config.llm.models[0].api_key, self.test_api_key)
            self.assertEqual(config.llm.models[1].api_key, second_api_key)
        finally:
            if second_env_var in os.environ:
                del os.environ[second_env_var]

    def test_api_key_from_env_in_evaluator_models(self):
        """Test that api_key from_env works in evaluator_models"""
        yaml_config = {
            "log_level": "INFO",
            "llm": {
                "api_base": "https://api.openai.com/v1",
                "models": [{"name": "evolution-model", "weight": 1.0, "api_key": "direct-key"}],
                "evaluator_models": [
                    {
                        "name": "evaluator-model",
                        "weight": 1.0,
                        "api_key": {"from_env": self.test_env_var},
                    }
                ],
            },
        }

        config = Config.from_dict(yaml_config)

        self.assertEqual(config.llm.evaluator_models[0].api_key, self.test_api_key)

    def test_yaml_file_loading_with_from_env(self):
        """Test loading api_key from_env from actual YAML file"""
        yaml_content = f"""
log_level: INFO
llm:
  api_base: https://api.openai.com/v1
  api_key:
    from_env: {self.test_env_var}
  models:
  - name: test-model
    weight: 1.0
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                config = Config.from_yaml(f.name)
                self.assertEqual(config.llm.api_key, self.test_api_key)
            finally:
                os.unlink(f.name)

    def test_mixed_api_key_sources(self):
        """Test mixing direct api_key and from_env in same config"""
        yaml_config = {
            "log_level": "INFO",
            "llm": {
                "api_base": "https://api.openai.com/v1",
                "api_key": "llm-level-direct-key",
                "models": [
                    {
                        "name": "model-with-env",
                        "weight": 1.0,
                        "api_key": {"from_env": self.test_env_var},
                    },
                    {"name": "model-with-direct", "weight": 0.5, "api_key": "model-direct-key"},
                ],
            },
        }

        config = Config.from_dict(yaml_config)

        self.assertEqual(config.llm.api_key, "llm-level-direct-key")
        self.assertEqual(config.llm.models[0].api_key, self.test_api_key)
        self.assertEqual(config.llm.models[1].api_key, "model-direct-key")


if __name__ == "__main__":
    unittest.main()
