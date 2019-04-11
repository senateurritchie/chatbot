
from typing import List 
from bs4 import BeautifulSoup
from lxml import etree

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

class ChatBot:
	def __init__(self):
		self.name = None
		self.version = None
		self.Person:Author = None
		self.soup:BeautifulSoup = None

	def __repr__(self) -> str:
		return "ChatBot name<{name}>, version<{version}>".format(name=self.name, version=self.version)

	def run(self):
		xml_content:str = None;
		xsd_root:str = None;

		# with open("data.xml") as f:
		# 	xml_root = f.read()

		# with open("schema.xsd") as f:
		# 	xsd_root = f.read()

		# print(self.soup)

		xml_root = etree.parse("data.xml")
		xsd_root = etree.parse("schema.xsd")
		schema = etree.XMLSchema(xsd_root)

		print(schema)
		schema.validate(xml_root)



if __name__ == "__main__":
	bot:ChatBot = ChatBot()
	bot.name = "Khallil"
	bot.version = "2.3"
	print(bot)
	bot.run()





