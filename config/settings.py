from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    deepseek_api_key: str
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"

    temperature: float = 0.0
    max_tokens: int = 512
    timeout: int = 60
    max_retries: int = 2

    output_dir: str = "./reports"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
