# Opens text file containing catalog
f=open("test.txt")
contents=f.read()
f.close()

# Ugly code, but it works
# iterator
i=0 
while i < len(contents):
	# Go through the text file until we hit a six-digit string
	if contents[i:i+6].isnumeric():
		j = i + 1
		while contents[j:j+6].isnumeric() != True and j < len(contents):
			j += 1
		buff=contents[i:j]
		print(buff)
	i += 1