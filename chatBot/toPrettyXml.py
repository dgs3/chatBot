##Parse the xml data out of the original chats file and into a new file

inFile = open("Chats.xml", "r")
outFile = open("trueChats.xml", "w")
inLine = inFile.readline()
lineCount = 1
while inLine != "":
	try:
		if inLine[0:4] != "From" and inLine[0:2] != "To" and inLine[0:7] != "Message":
			if inLine[-2] == '>' or inLine[-1] == '>':	
				outFile.write(inLine[0:-1])
			elif inLine[-2] == '=' or inLine[1] == '=': #-2 because the last char is \n
				outFile.write(inLine[0:-2])
	except IndexError:
		pass
	inLine = inFile.readline()
	print "Processed Line: " + str(lineCount)
	lineCount+=1

inFile.close()
outFile.close()
