import os
import pandas as pd


input_dir="./result/"
output_dir="./result2/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files=os.listdir(input_dir)

for file in files:
    df=pd.read_csv(input_dir+file)
    print(file)
    # filename,test_release,line_number,file_label,line_label,EP_prediction_result=[],[],[],[],[],[]
    new_df=[]

    for _,df_ in df.groupby("filename"):
        
        filename=list(df_['filename'])
        new_filename=[]
        for item in filename:
            new_filename.append(file+item)
        df_['filename']=new_filename
        line_label=df_['line_label'].tolist()
       
        flag=line_label.count(True)>0
        file_label=[flag for _ in range(len(line_label))]
        df_['file_label']=file_label
        new_df.append(df_)
    df=pd.concat(new_df)
    df.to_csv(output_dir+file,index=False)