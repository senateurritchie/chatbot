
from typing import List 
import lxml
from lxml import etree
from enum import Enum
from pylev3 import Levenshtein
from pylev3 import classic_levenshtein,damerau_levenshtein
import re
from operator import itemgetter

import random

class AddressItemType(Enum):
	PERSONAL = "personal"
	PROFESIONAL = "profesional"


		
class AddressItem:
	"""docstring for AddressItem"""
	def __init__(self,value,t:AddressItemType):
		self.value = value
		self.type = t

	def __repr__(self) -> str:
		return "type<{type}>, value<{value}>".format(type=self.type,value=self.value)



class Phone(AddressItem):
	"""docstring for Phone"""
	def __init__(self, value, t:AddressItemType):
		super().__init__(value,t)

	def __repr__(self) -> str:
		return "Phone "+super().__repr__()

class Email(AddressItem):
	"""docstring for Email"""
	def __init__(self, value,t:AddressItemType):
		super().__init__(value,t)

	def __repr__(self) -> str:
		return "Email "+super().__repr__()
		

class Address:
	def __init__(self):
		self.emails : List[Email] = []
		self.website = None 
		self.phones : List[Phone] = []

	def __repr__(self) -> str:

		emails:str = ",\n".join([repr(i) for i in self.emails])
		phones:str = ",\n".join([repr(i) for i in self.phones])
		return "Address website<{website}>, \n{emails}, \n{phones}".format(website=self.website,emails=emails,phones=phones)

class Person:
	def __init__(self):
		self.name = None
		self.address:Address = None

	def __repr__(self) -> str:
		return "Author name<{name}>, \n{address}".format(name=self.name,address=self.address)


class ChatBot:
	def __init__(self):
		self.name = None
		self.website = None
		self.version = None
		self.welcomeText:str = None
		self.questions:list = []
		self.author:Person = None
		self.xml_root = None
		self.isChating:bool = False 
		self.initialized:bool = False 

	def __repr__(self) -> str:
		return "ChatBot name<{name}>, version<{version}>, \n{author}".format(name=self.name, version=self.version,author=self.author)

	def selectQuestion(self,q:str):
		"""
		cette fonction cherche dans la base de memoire
		la reponse ideal à cette question.
		"""

		prog = re.compile("(.+)?(?P<choices>\{\{.+?\}\})(.+)?")

		keywords:list = q.split(" ")
		kwt = [re.compile(" *({}) *".format(re.escape(i))) for i in keywords if i]

		# gestion des questions
		choices:list = []
		for index,i in enumerate(self.questions):

			if i.tag =="Question":
				for l in i.find("Labels"):

					def repl(e):
						mask = e.group('choices')
						data = e.groups()

						for ee in data:
							if ee is not None:
								if ee == mask:
									for eee in ee.strip("{}").split("|"):
										h = [p.strip() if p != mask else eee.strip()  for p in data if p is not None]

							
										h = " ".join(h)
										t = damerau_levenshtein(q,h)
										kwl = []

										for tt in kwt:
											m = re.search(tt,h)
											if m:
												kwl.append(m.group(0).strip())

										choices.append((t,len(kwl),index,h,kwl))


					text:str = l.text.lower()
					if re.match(prog,text):
						m = re.sub(prog,repl,text)
					else:
						t = damerau_levenshtein(q,text)
						kwl = []

						for tt in kwt:
							m = re.search(tt,text)
							if m:
								kwl.append(m.group(0).strip())


						choices.append((t,len(kwl),index,text,kwl))


		# le choix de la question predefinie
		choices = sorted(choices,key=itemgetter(1), reverse=True)
		choices = sorted(choices,key=itemgetter(0))
		choice = choices[0];

		return choice;

	def checkForMarkers(self,e:re.Match):

		if e.group("MARKER") == "NAME":
			return self.name.strip()
		else:
			choices = e.group("MARKER").split("|")
			return random.choice(choices).strip()


	def selectAnswer(self,choice:tuple):
		"""
		permet de selectionner une reponse à partir
		du choix d'une question.
		"""
		reg = re.compile("\{\{(?P<MARKER>.+?)\}\}")

		if choice[1] == 0:
			responses = self.questions[len(self.questions)-1].find("Responses")
		else:
			responses = self.questions[choice[2]].find("Responses")

		response = random.choice(responses)
		responseText = response.find('Labels').find("Label").text
		responseText = re.sub(reg,self.checkForMarkers,responseText)

		return responseText;
	

	def run(self):
		xml_root = etree.parse("data.xml")
		xsd_root = etree.parse("schema.xsd")

		try:                                                                        
			schema = etree.XMLSchema(xsd_root)
			schema.assertValid(xml_root)
		except etree.XMLSchemaParseError as e:                                 
			print(e)                                                               
			exit(1) 
		except etree.DocumentInvalid as e:  
			print(e)                                                               
			exit(1) 
		self.xml_root = xml_root;

		# on recupere les informations de <Settings>
		settings = xml_root.find("Settings")
		self.welcomeText = settings.find("Welcome").text
		for item in settings:
			if item.tag == "Name":
				self.name = item.text
			elif item.tag == "Version":
				self.version = item.text
			elif item.tag == "Website":
				self.website = item.text
			elif item.tag == "Author":
				self.author = Person()
				self.author.name = item.find('Name').text
				address = Address()
				addressTag = item.find('Address')
				address.website = addressTag.find('Website').text
				for i in addressTag.find('Emails'):
					address.emails.append(Email(i.text,i.get('type')))

				for i in addressTag.find('Phones'):
					address.phones.append(Phone(i.text,i.get('type')))

				self.author.address = address

		# on recupere les questions
		self.questions = xml_root.find("Questions")
		self.isChating = True

		print(self.welcomeText+"\n")



		while self.isChating:
			q:str = str(input(">>> ")).lower()
			choice = self.selectQuestion(q)
			response:str = self.selectAnswer(choice)
			print("[Reponse]: "+response)
			print("\n")
			

	



if __name__ == "__main__":
	bot:ChatBot = ChatBot()
	bot.run()