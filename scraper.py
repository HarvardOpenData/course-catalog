# Opens text file containing catalog
f=open("fas_crse_cat.txt")
contents=f.read()
f.close()

# Ugly code, but it works

courses=[]
titles=[]
# iterator
i=0 
while i < len(contents):
	# Go through the text file until we hit a six-digit string
	if contents[i:i+6].isnumeric():
		buff=[]
		k = i
		# Look backwards from the six-digit string until we find the course title
		while contents[k] != '\n':
			k -= 1
		# Compensate for inconsistent title naming
		if ':' not in contents[k+1:i].strip():
			k-=1
			# Go one more line back and find the course name and number
			while contents[k] != '\n':
				k -= 1
		buff=contents[k+1:i].strip()
		# Add the name of the course and its identifier to the buffer
		titles.append(contents[k+1:i+7].strip())
		j = i + 1
		# Look forwards unti we find the next six digit string
		while contents[j:j+6].isnumeric() != True and j < len(contents):
			j += 1
		j-=1
		# Shift backwards so we don't include the title of the next course
		while contents[j] != '\n':
			j -= 1
		# Add the course information to the buffer
		buff = buff + contents[i:j-1]
		# Add the buffer to the courses list
		courses.append(buff)
	i += 1

blacklist=['/','.','\n']
for t in range(len(titles)):
	for unsafe in blacklist:
		titles[t] = titles[t].replace(unsafe, "_")

# Write courses to text files
# Note: This creates a massive amount of text files relatively quickly.
# Only uncomment this when you're ready for your computer to hate you.
for c in range(len(courses)):
	namestring=titles[c] + ".txt"
	course=open(namestring,'a')
	course.write(courses[c])
	course.close()