import random
import string
from database import DB

def cheekphone(phone:str) -> [bool,str]:
    """
    Checks the validity of a phone number.

    Args:
        phone (str): The phone number to check.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """

    def clean_phone(phone:str):
        cleaned = ""
        for i in phone:
            try:
                if int(i) in [1,2,3,4,5,6,7,8,9,0]:
                    cleaned+=i
            except ValueError:
                pass

        return cleaned
    cleaned = clean_phone(phone)
    return True if len(cleaned) == 10 and int(cleaned) else False, cleaned

def phone_format(n) -> str:
    """
    Formats a phone number with dashes.

    Args:
        n (str): The phone number to format.

    Returns:
        str: The formatted phone number.
    """
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]

def generate_new_id(database:str) -> str: 
    """
    Generates a new unique ID.

    Args:
        database (str): The database to generate the id for, items or user.

    Returns:
        str: A new unique ID.
    """
    if database not in ["items","user"]:
        raise Exception("Not a database")
    generated_id = ''.join(
        random.choice(
            string.ascii_lowercase +
            str(1234567890)) for x in range(7))
    db = DB()
    item = db.select(database,{"itemcustomid" if database == "item" else "sellerid":generated_id})
    if not item:
        return generated_id
    return generate_new_id(database)

