## Dataset

The datasets are obtained from Wattanakriengkrai et. al. The datasets contain 32 software releases across 9 software projects. The datasets that we used in our experiment can be found in this [github](https://github.com/awsm-research/line-level-defect-prediction).

## Data Preprocessing

```
cd ./process_data
```

- Converting data to a single csv file

```
python preprocess_data.py
```

- Converting code files from csv to txt format

```
python preprocess_data2.py
```

- Extract code features with java eclipse jdt and save in "../Datasets/codewithast/" and "../Datasets/add_syntax/"

```
cd ./eclipse_jdt/src/main/
RQ1.java
Ablation.java
Ablation2.java
Ablation3.java
```

- Converting code files to csv format    

```
python preprocess_data3.py
```

- Extracting the features of each syntax node information

```
python preprocess_data4.py
python count_frequency.py
```

- prepare data for RQ2

```
process_ablation.py
```

- prepare data for discussion

```
remove_syntax.py
```



## Environment Setup

Run the following command under your python environment

```
pip install requirements.txt
```

## Word2Vec Model Traning

```
cd ./scripts
sh ./train_w2v.sh
```

## Generate results of SyntaxLineDP

```
cd ./scripts
sh ./train_w2v.sh
sh ./RQ1.sh
sh ./RQ2.sh
sh ./RQ3.sh
sh ./Discussion.sh
```

## Generate results of baselines

### ErrorProne

```
cd ./errorprone
```

- prepare data

```
python preprocess_data.py
python get_data.py
```

- get results

```
python generate_result.py
python generate_result2.py
```

### N-grams

```
cd ./n-grams
```

- prepare data

```
python get_data.py
```

- RQ1

```
 python RQ1.py
```

- RQ3

```
 python RQ3.py
```

### RG

```
cd ./RG
```

- RQ1

```
python RQ1.py
```

