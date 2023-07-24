# Data files converter 


Converter is a Python console application for convertation input csv-format file to parquet or back (or other formats in future), get schema of parquet file or get help message. 


## Installation

Converter requires [Python](https://www.python.org/downloads/)  v3+ to run.
Open your command line interpreter. If you don't have 'pip' then install it: 
```sh
python -m ensurepip
```

Install the necessary libraries.
```sh
pip install pyarrow
pip install pandas
```


## Features

There are four options of this command application:

```--csv2parquet <src-filename> <dst-filename> ```: conversion mode from csv to parquet format

```--parquet2csv <src-filename> <dst-filename>``` : conversion mode from parquet to csv format

```--get-schema <filename>``` : getting a parquet file scheme

```--help ```: display of help on its use


## Usage

In command line interpreter start programm:

```sh
$python converter.py --get-schema .../salary.parquet
```

It returns:
```sh
''' 
ID: int64
  -- field metadata --
  PARQUET:field_id: '1'
Name: string
  -- field metadata --
  PARQUET:field_id: '2'
Salary: double
  -- field metadata --
  PARQUET:field_id: '3'
'''
```

```sh
$python converter.py --csv2parquet .../salary.csv .../salary.parquet
```
If you want to see the result, then go to <.../salary.parquet> and make sure the file is created.


```sh
$python converter.py --parquet2csv .../salary.parquet .../salary2.csv
```
If you want to see the result, then go to <.../salary.csv> and make sure the file is created


```sh
$python converter.py --help
```
It returns help message.
You can also enter an incorrect command or filename, and application will display a corresponding message.

