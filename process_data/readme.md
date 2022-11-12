1 Converting data to a single csv file
    python preprocess_data.py

2 Converting code files from csv to txt format
    python preprocess_data2.py

3 Extracting code features with java eclipse jdt, save in "../Datasets/codewithast/" and "../Datasets/add_syntax/"
    cd ./eclipse_jdt/src/main/
    RQ1.java
    Ablation.java
    Ablation2.java
    Ablation3.java

4 Converting code files to csv format
    python preprocess_data3.py

5 Extracting the features of each syntax node information
    python preprocess_data4.py
    python count_frequency.py

6 prepare data for RQ2
    process_ablation.py

7 prepare data for discussion
    remove_syntax.py