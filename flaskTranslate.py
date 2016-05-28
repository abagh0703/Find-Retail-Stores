from sys import argv

filename = argv[1]
fileText = ""
with open(filename, "r") as file:
	for line in file:
		ln = line
		if line.find("src=") != -1:
			index = line.find("src=")
			if line[index+5:index+9] != "http":
				#print line[index+5:index+8]
				i = index+5
				url = ""
				while (line[i] != '"'):
					url += line[i]
					i+=1
				#print url
				ln = line.replace(url, "{{ url_for('static', filename='"+url+"') }}")
		elif line.find("href=") != -1:
			index = line.find("href=")
			if line[index+6:index+10] != "http" and line[index+6] != "#" and line[index+6: index+6+len("mailto")] != "mailto":
				#print line[index+5:index+8]
				i = index+6
				url = ""
				while (line[i] != '"'):
					url += line[i]
					i+=1
				#print url
				ln = line.replace(url, "{{ url_for('static', filename='"+url+"') }}")
		fileText += ln
		
#print fileText

with open(filename, "w") as file:
	file.write(fileText)