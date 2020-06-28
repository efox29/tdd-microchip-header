import sys
import re

f = open('pic16lf15345.h')
data = f.read()
f.close()

pattern = "(typedef\s+union\s+{[\s\S]*?bits_t;)"

matches = re.findall(pattern,data,re.MULTILINE)

header = """
#ifndef VIRTUAL_XC_H
#define	VIRTUAL_XC_H

#include <stdint.h>
#include <stdlib.h>

"""


footer = "\n\nvoid virtual_xc_init(void);\nvoid virtual_xc_deinit(void);\n\n#endif	/* VIRTUAL_XC_H */"
define_statements = ""
# create dictionary to store reg and types
regs_dict ={}

if(matches):
    # open a file
    f = open("virtual_xc.h","w")
    f.write(header)
    for m in matches:   

        # tokenize with "spaces"
        temp = m.split(' ')
        """ temp[-1] get the last word and from the last word, go until the 2nd last character [:-1] so that we skipp the ;  """
        struct_type = temp[-1][:-1]
        reg_name = struct_type.split('bits_t')[0]
        
        temp = m
        # need to inject something
        first_string = temp[:m.rfind('\n')]
        inject_string = "\n    uint8_t _{reg_name};\n".format(reg_name = reg_name)
        second_string = temp[m.rfind(';\n')+1:]
        recombine_string = (first_string,second_string)
        
        m = inject_string.join(recombine_string)
        """ not sure why I had to write \r\n twice essentially, but could not get it otherwise """    
        buf = m + "\r\n" 
        
      
        regs_dict[reg_name] = struct_type
        buf = buf + "{struct_type}* REG_{reg_name};\n".format(struct_type=struct_type,reg_name=reg_name)
        define_statements = define_statements + "\n#define {reg_name} REG_{reg_name}->_{reg_name}\n#define {reg_name}bits (*REG_{reg_name})\n".format(reg_name = reg_name)
        f.write(buf)        
        f.write("\n")
    f.write(define_statements)
    f.write(footer)
    f.close()

regs_init = ""
regs_free = ""
for x in regs_dict:
    regs_init = regs_init + "REG_{reg_name} = ({struct_type}*)calloc(1,sizeof({struct_type}));\n    ".format(reg_name = x, struct_type = regs_dict[x])
    regs_free = regs_free +  "free(REG_{reg_name});\n    ".format(reg_name = x)

f = open("virtual_xc.c","w")
buf = """#include "virtual_xc.h"

void virtual_xc_init()
{{
    {regs_init}

}}
void virtual_xc_deinit()
{{
    {regs_free}
}}
""".format(regs_init = regs_init, regs_free = regs_free)

f.write(buf)
f.close()


    

