import string
import random

from app import crud
from sqlalchemy.orm import Session

def generate_short_code(length : int = 6) -> str :
    characters = string.ascii_letters + string.digits

    return "".join(random.choices(characters, k=length))

def generate_unique_short_code(db : Session) -> str:
    while True:
        code = generate_short_code()

        if not crud.get_url_by_short_code(db, code):
            return code
