from database import DB
from general import cheekphone, generate_new_id
class User:
    def __init__(self, seller_id:str, phone:str, name:str, address:str, city:str, state:str, zip_code:str, paid:bool = False, id = None):
        self.id = id
        self.seller_id = seller_id
        self.phone = phone
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.paid = paid
    
    @staticmethod
    def static_cheek_phone(phone:str) -> bool:
        db = DB()
        result = db.select("user",{"phone":phone})
        return True if result else False
    
    @staticmethod
    def from_database(database_responce):
        id = database_responce[0]
        seller_id = database_responce[1]
        phone = database_responce[2]
        name = database_responce[3]
        address = database_responce[4]
        city = database_responce[5]
        state = database_responce[6]
        zip_code = database_responce[7]
        paid = database_responce[8]
        return User(id=id, seller_id=seller_id, phone=phone, name=name, address=address, city=city, state=state, zip_code=zip_code, paid=paid)
    
    @staticmethod
    def from_phone(phone:str):
        db = DB()
        result = db.select("user",{"phone":phone})
        if not result:
            return None
        user = result[0]
        return User().from_database(user)
    
    @staticmethod
    def from_seller_id(seller_id:str):
        db = DB()
        result = db.select("user",{"sellerid":seller_id})
        if not result:
            return None
        user = result[0]
        return User().from_database(user)
    
    @staticmethod
    def new_from_request(request):
        phone = request.form['phonen']
        name = str(request.form['name'])
        address = str(request.form['address'])
        city = str(request.form['city'])
        state = str(request.form['state'])
        zip_code = str(request.form['zip'])
        
        valid_phone, cleaned_phone = cheekphone(phone)
        if valid_phone == False:
            raise Exception("Phone number invalid")
        
        phone_in_use_cheek = User().static_cheek_phone(cleaned_phone)
        if phone_in_use_cheek:
            raise Exception("Phone number already in use")
        
        generated_seller_id = generate_new_id("user")
        
        user = User(generated_seller_id, cleaned_phone, name, address, city, state, zip_code)
        
        return user
    
    @staticmethod
    def update_from_request(request):
        phone = request.form['phonen']
        name = str(request.form['name'])
        address = str(request.form['address'])
        city = str(request.form['city'])
        state = str(request.form['state'])
        zip_code = str(request.form['zip'])
        user_id = str(request.form['sid'])
        valid_phone, cleaned_phone = cheekphone(phone)
        if valid_phone == False:
            raise Exception("Phone number invalid")
                
        user = User(user_id, cleaned_phone, name, address, city, state, zip_code)
        
        return user
    
    def cheek_phone(self):
        return self.static_cheek_phone(self.phone)
    
    def save_to_database(self):
        if self.cheek_phone():
            data ={
                "sellerid":self.seller_id,
                "phone":self.phone,
                "address":self.address,
                "city":self.city,
                "state":self.state,
                "zip":self.zip_code,
                "paid":self.paid
            }
            db = DB()
            db.update("user",data,{"id":self.id})
            return

        data ={
            "sellerid":self.seller_id,
            "phone":self.phone,
            "address":self.address,
            "city":self.city,
            "state":self.state,
            "zip":self.zip_code,
            "paid":self.paid
        }
        db = DB()
        db.insert("user",data)
        return
    
print(User.static_cheek_phone("0"))