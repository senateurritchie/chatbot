
from typing import List 

class AddressItem:
	"""docstring for AddressItem"""
	def __init__(self,value):
		self.value = value

class Phone(AddressItem):
	"""docstring for Phone"""
	def __init__(self, value):
		super().__init__(value)

class Email(AddressItem):
	"""docstring for Email"""
	def __init__(self, value):
		super().__init__(value)		
		

class Address:
	def __init__(self):
		self.emails : List[Email] = []
		self.website = None 
		self.phones : List[Phone] = []

class Person:
	def __init__(self,name):
		self.name = name
		self.website = None 
		self.address:Address = None

class Bot:
	def __init__(self):
		self.name = None
		self.version = None
		self.Person:Author = None

	def __repr__(self):
		return "Bot name<{name}>, version<{version}>".format(name=self.name, version=self.version)



if __name__ == "__main__":
	bot:Bot = Bot()
	bot.name = "Khallil"
	bot.version = "2.3"
	print(bot)





