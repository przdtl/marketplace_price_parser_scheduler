from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_USER: str
    MONGODB_PASS: str

    MARKETPLACE_PRICE_PARSER_SERVICE_HOST: str
    MARKETPLACE_PRICE_PARSER_SERVICE_PORT: int

    @property
    def mongodb_dsn(self) -> str:
        return 'mongodb://{}:{}@{}:{}'.format(self.MONGODB_USER, self.MONGODB_PASS, self.MONGODB_HOST, self.MONGODB_PORT)

    model_config = SettingsConfigDict(env_file='.env')
