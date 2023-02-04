import os
import re
from xml.dom.minidom import parse

os.system("bash ./pmd-bin-6.53.0/bin/run.sh pmd -d ./PMD_data/activemq-5.2.0 -f xml -r ./result/result2.xml -R rulesets/java/unusedcode.xml")
domtree=parse("./result/result2.xml")

data=domtree.documentElement

regural=re.compile('\/.*.java',re.M)

for i,file in enumerate(data.getElementsByTagName("file")):
    filename=str(file.getAttribute("name"))
    print(i,filename[filename.rfind('/')+1:])
    for violation in file.getElementsByTagName("violation"):
        print(violation.getAttribute("beginline"))