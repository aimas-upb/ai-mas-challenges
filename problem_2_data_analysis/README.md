# The exploratory data analysis challenge

We have merged in one csv file the results for **the Bacalaureat Sessions from [2015, 2017]**. 
Exploratory Data Analysis is an important work in the area of data science, it refers to the 
critical process of performing initial investigations on data. We  challenge you to investigate 
on this data so as to discover patterns, to spot anomalies, to test hypothesis and to check assumptions with the help of summary statistics and graphical representations.

Can we learn something useful from this dataset about the education system in Romania?

Surprise us with your findings!

## Getting Started

Examples and inspiration sources for exploratory data analysis:
* Kaggle completitions and kernels can offer good inspiration
**https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python**
https://www.kaggle.com/pavansanagapati/a-simple-tutorial-on-exploratory-data-analysis
https://www.kaggle.com/rchattergoon/avocado-prices-across-the-usa 

You can use whatever tool you feel comfortable exploring this data.

## Submission Format

**Send us a report with you findings.** 

It can be a kaggle kernel, a python notebook, a PDF document 
or any format that we can visualize directly (min software requirements and preferably no 
processing required).

## Dataset overview

Rezultate Bacalaureat Sesiunea I 2017, II 2017, I 2016, II 2016, I 2015, II 2015

The source of the datasets can be found @ http://data.gov.ro/dataset?tags=bacalaureat.

We have made some small adjustments to "II 2015" data and merged them together in on CSV file 
`Rezultate_Bacalaureat_Sesiunea_I_II_2015_2017.csv.zip`.

We have added a column `Dataset` which specifies the source of the rows.


| Dataset  | Row count |
| ------------- | ------------- |
| 1_2015  | 168939  |
| 1_2016  | 137338  |
| 1_2017  | 135513  |
| 2_2015  | 55126  |
| 2_2016  | 42297  |
| 2_2017  | 39451  |


\* II 2015 - Missing columns: `Unitate (SIIIR)`, `Unitate (SIRUES)`. Unique column for this 
dataset: `Scoala` 
```
