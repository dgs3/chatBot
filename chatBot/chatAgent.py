from parseOutXml import Parser
from sys import maxint
from random import choice
from editdist import distance
from xml.dom.minidom import parse

class Lazarus:

	def __init__(self):
		self.p = Parser()
		self.convoDict = self.parseXml("theChat.xml")
		print self.convoDict

	def begin(self):
		print "Resurrecting"
		while True:
			input = raw_input("You: ")
			print "Matt: " + self.findBestResponse(input)

	def findBestResponse(self, input):
		bestDistance = maxint
		for query in self.convoDict:
			tempDist = distance(query, input)
			if tempDist < bestDistance and len(self.convoDict[query]) > 0:
				bestResponses = self.convoDict[query]
				bestDistance = tempDist
		return choice(bestResponses)

	def parseXml(self, path):
		doc = parse(path)
		information = self.pruneCarriageReturns(doc.firstChild)
		convo = {}
		for child in information:
			query = child
			responses = self.getResponsesFromXml(query)
			convo[query.getAttribute("query").encode("ASCII")] = responses
		return convo

	def getResponsesFromXml(self, rootNode):
		#print rootNode.firstChild.data.encode('ASCII')
		theResponses = self.pruneCarriageReturns(rootNode)
		responses = []
		for child in theResponses:
			responses.append(child.getAttribute("response").encode("ASCII"))
		return responses


	def pruneCarriageReturns(self, rootNode):
		returnList = []
		for i in range(len(rootNode.childNodes)):
			if i%2 == 1:
				returnList.append(rootNode.childNodes[i])
		return returnList	

l = Lazarus()
