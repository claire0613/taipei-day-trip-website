from werkzeug.security import generate_password_hash,check_password_hash
class User():
    def __init__(self,name='',email='',password=''):
        self._name=name
        self.__email=email
        self._password_hash=generate_password_hash(password)
        
    @property
    def email(self):
        return self.__email
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,new_name):
        self._name = new_name
        
    @property   
    def password(self):
       raise AttributeError('password is not a readable attribute!')
   
    @password.setter
    def password(self,new_password):
       self._password_hash=generate_password_hash(new_password)
       print(f'{self._password_hash}  to  {new_password}')
        
    def verify_password(self,password):
        return check_password_hash(self._password_hash,password)