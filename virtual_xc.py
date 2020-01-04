import sys
import re

f = open('pic16lf15345.h')
data = f.read()
f.close()

pattern = "(typedef\s+union\s+{[\s\S]*?bits_t;)"

matches = re.findall(pattern,data,re.MULTILINE)

if(matches):
    # open a file
    f = open("virtual_xc.h","w")
    for m in matches:   
        """ not sure why I had to write \r\n twice essentially, but could not get it otherwise """    
        buf = m + "\r\n"        
        f.write(buf) 
        f.write("\n")        

    f.close()

