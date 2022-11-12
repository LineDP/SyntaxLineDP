从下载数据，保存在../Datasets/original/下

1 将数据转成单个csv文件，该文件记录代码行以及代码文件是否有bug
    preprocess_data.py

2 将代码文件从csv转成txt格式
    preprocess_data2.py

3 java eclipse jdt 提取代码特征，保存在../Datasets/codewithast/ 和 ../Datasets/add_syntax/下


4 将代码文件转为csv格式
    preprocess_data3.py

5 提取各语法结点信息的特征
    preprocess_data4.py
    count_frequency.py

6 为RQ2准备数据
    process_ablation.py

7 删除语法信息，discussion部分使用
    remove_syntax.py