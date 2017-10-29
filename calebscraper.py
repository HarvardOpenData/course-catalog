import re

f = open("cleaned_catalog.txt")
contents = f.read()
f.close()
matcher=re.compile("[MTWRF]{1,5} \d{4} [AP]M - \d{4} [AP]M")

matches = []
for str in matcher:
    for c in str:
        if c == "":
            str.split(c)
            matches.append(tuple(str))
            break

print(matches)
print(matcher.findall(contents))
