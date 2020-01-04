import sys
import re

f = open('pic16lf15345.h')
data = f.read()
#print(data)
f.close()


#
pattern = "typedef\s+union\s+\{(\n.+)+bits_t;"

regex = re.compile(pattern,re.MULTILINE)
# matches = [m.groups() for m in regex.finditer(data)]
matches = re.search(pattern,data,re.MULTILINE)
# for m in matches:
#     print (m)

if(matches):
    for m in matches.regs:
        start = matches.start()
        end = matches.end()
        print(data[start:end]+'\n\n')

#print(rs)