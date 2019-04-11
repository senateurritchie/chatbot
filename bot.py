
from typing import List 
import lxml

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
		self.xml_root = None

	def __repr__(self) -> str:
		return "ChatBot name<{name}>, version<{version}>".format(name=self.name, version=self.version)

	def run(self):
		xml_root = lxml.etree.parse("data.xml")
		xsd_root = lxml.etree.parse("schema.xsd")

		try:                                                                        
			schema = lxml.etree.XMLSchema(xsd_root)
			schema.assertValid(xml_root)
		except lxml.etree.XMLSchemaParseError as e:                                 
			print(e)                                                               
			exit(1) 
		except lxml.etree.DocumentInvalid as e:  
			print(e)                                                               
			exit(1) 
		self.xml_root = xml_root;

		help(xml_root)



if __name__ == "__main__":
	bot:ChatBot = ChatBot()
	bot.name = "Khallil"
	bot.version = "2.3"
	print(bot)
	bot.run()





