from xml.dom.minidom import Document, parse

class Parser:	


	def __init__(self):
		f = open("trueChats.xml", "r")
		self.convo = f.read()
		f.close()
		self.email = "sayles.matt@gmail.com"
		self.messageTag = "cli:message"
		self.bodyTag = "cli:body"
		self.lookingForQuery = False
		self.addTo = []

	"""Given a string and an index, returns the tag and the index of the tag"""
	def getNextTag(self, i):
		leftIndex = self.convo.index("<", i)
		rightIndex = self.convo.index(">", i)
		return (self.convo[leftIndex:rightIndex+1], leftIndex)
	
	"""Given a string, tag to find, and index, returns the tag and index of that tag"""
	def getNextSpecificTag(self, tag, i):
		indexNextTag = self.convo.index('<'+tag, i) #Take into account preceeding < char
		return self.getNextTag(indexNextTag)

	"""Given a tag, returns an attribute's value"""
	def getTagAttribute(self, tag, attr):
		attrIndex = tag.index(attr)
		attrSize = len(attr)+1 #We add one due to the equals sign
		try:
			return tag[attrIndex+attrSize:tag.index(' ', attrIndex)]
		except:
			return tag[attrIndex+attrSize:tag.index('>', attrIndex)]
	
	"""
		Given a tag, gets the information sandwitched between the two xml tags.
		The index i is the beginning of the opening tag
	"""
	def getSandwitch(self, tag, i):
		leftTag = self.getNextSpecificTag(tag, i)
		rightTag = self.getNextSpecificTag('/'+tag, i)
		return self.convo[leftTag[1]+len(leftTag[0]):rightTag[1]]
	
	def onQuery(self):
		if not self.lookingForQuery:
			self.lookingForQuery = not self.lookingForQuery
			self.addTo = []

	def onResponse(self):
		if self.lookingForQuery:
			self.lookingForQuery = not self.lookingForQuery

	def parseOutXml(self):
		currIndex = 0
		convoDict = {}
		while True:
			nextMessage = self.getNextSpecificTag(self.messageTag, currIndex)
			currIndex = nextMessage[1]
			if self.email in self.getTagAttribute(nextMessage[0], 'to'):
				self.onQuery()
				query = self.getSandwitch(self.bodyTag, currIndex).lower()
				if query not in convoDict: #We need to add the next set of responses to an older inex
					convoDict[query] = []
				self.addTo.append(convoDict.keys().index(query))
			else:
				self.onResponse()
				response = self.getSandwitch(self.bodyTag, currIndex).lower()
				for i in self.addTo:
					convoDict[convoDict.keys()[i]].append(response)
			currIndex+=len(nextMessage[0])
			if currIndex == 10872228: break
		return convoDict

	def toXml(self):
		doc = Document()
		profileNode = doc.createElement('theChat')
		profileNode.setAttribute('id', 'theChat')
		doc.appendChild(profileNode)
		chatDict = self.parseOutXml()
		#Add all values from the profile to the XML
		for key in chatDict:
			#Create a node from the current value
			node = doc.createElement("query")
			node.setAttribute("query", str(key))
			for response in chatDict[key]:
				#Make a node with the actual data
				data = doc.createElement("response")
				data.setAttribute("response",str(response))
				#Append the nodes to their parent nodes
				node.appendChild(data)
			profileNode.appendChild(node)
		outFile = open("theChat.xml", "w")
		outFile.write(doc.toprettyxml(indent='	'))
		outFile.close()

p = Parser()
p.toXml()
