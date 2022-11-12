import pandas as pd
import re
import copy
from init import *


for index,project in enumerate(projects):
    train_files=[]
    train_projects=copy.deepcopy(projects)
    train_projects.pop(index)

    print(train_projects)

    for train_project in train_projects:
        train_files.extend(all_releases[train_project])

    f=open("./data/"+project,'w')

    for file in train_files:
        df=pd.read_csv(data_path+file+".csv")
        codelines=df['codelines'].tolist()
        labels=df['line_label'].tolist()

        for codeline,label in zip(codelines,labels):
            if label==True:
                continue
            codeline=str(codeline)
            codeline = codeline.replace("\n", "").replace("\t", " ").replace("\/?", "").replace("\\", "")
            codeline = re.sub(r"[\W]", myreplace, codeline)
            codeline=codeline.split()
            f.write(str(codeline)+"\n")
    f.close()