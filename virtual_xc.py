import sys
import re

f = open('pic16lf15345.h')
data = f.read()
#print(data)
f.close()



pattern = "(typedef\s+union\s+{[\s\S]*?bits_t;)"
#pattern = "typedef\s+union"

regex = re.compile(pattern,re.MULTILINE)
# matches = [m.groups() for m in regex.finditer(data)]
matches = re.findall(pattern,data,re.MULTILINE)
# for m in matches:
#     print (m)

if(matches):
    # open a file
    f = open("parsed_file.c","w")
    for m in matches:
        print(m+"\n\n")
        f.write(m)

    f.close()

#print(rs)