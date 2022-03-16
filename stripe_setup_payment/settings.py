from typing import List

from pydantic import BaseSettings, constr, HttpUrl


class Settings(BaseSettings):
    STRIPE_API_KEY: constr(regex=r'sk_.*')
    HOST: HttpUrl = 'http://127.0.0.1:4242'
    PAYMENT_METHOD_TYPES: List[str] = ['sepa_debit', 'card']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'