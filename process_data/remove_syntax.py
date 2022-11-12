#discussion

import pandas as pd
from utils import *
import json
nodes=["IfStatement", "SimpleName", "InfixExpression", "Assignment", "Expression", "Block", "MethodInvocation"]
input_dir="../Datasets/preprocessed_data3/"

for node in nodes:
    output_dir="../Datasets/discussion/remove_{}/".format(node)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files=os.listdir(input_dir)
    for file in files:
        df=pd.read_csv(input_dir+file)
        asts=df['ast'].tolist()
        new_ast=[]
        for ast in asts:
            ast=ast.replace("\'{}\', ".format(node),"")
            ast=ast.replace("\'{}\']".format(node),"]")
            new_ast.append(ast)
        df['ast']=new_ast
        df.to_csv(output_dir+file,index=False)
        