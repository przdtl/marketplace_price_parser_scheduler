from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):

    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_USER: str
    MONGODB_PASS: str

    @property
    def mongodb_dsn(self) -> str:
        return 'mongodb://{}:{}@{}:{}'.format(self.MONGODB_USER, self.MONGODB_PASS, self.MONGODB_HOST, self.MONGODB_PORT)

    model_config = SettingsConfigDict(env_file='.env')
