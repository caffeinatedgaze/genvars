from pydantic_settings import BaseSettings


class SomeSettings(BaseSettings):
    flag: bool = False


class OutOfFocus:
    pass
