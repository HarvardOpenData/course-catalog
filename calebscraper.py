import re

f = open("cleaned_catalog.txt")
contents = f.read()
f.close()
matcher=re.compile("[MTWRF]{1,5} \d{4} [AP]M - \d{4} [AP]M")
times=matcher.findall(contents)

submatcher=re.compile("([MTWRF]{1,5}) (\d{4}) ([AP]M) - (\d{4}) ([AP]M)")

for time in times:
	timeTuple=submatcher.findall(time)[0]
	newTime=[timeTuple[0],int(timeTuple[1]),int(timeTuple[3])]
	if timeTuple[2] == "PM" and timeTuple[1][0:2] != "12":
		newTime[1] += 1200
	if timeTuple[4] == "PM" and timeTuple[3][0:2] != "12":
		newTime[2] += 1200
	newTime[1]= 60*(newTime[1]//100) + (newTime[1] % 100)
	newTime[2]= 60*(newTime[2]//100) + (newTime[2] % 100)
	print(newTime)
