from pydantic_settings import BaseSettings


class Settings (BaseSettings):
    Db_password:str
    Db_username:str
    Db_host:str
    Db_port:str
    Db_name:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    

    class Config:
        env_file ='.env'
    
settings = Settings()

    
