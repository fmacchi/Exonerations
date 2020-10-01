# 14.33 Short Project: Exonerations in the United States

This project aims to explore racial disparities in the cases of wrongful convictions within the United States. 

## Usage

The .do file contains Stata regressions and intial data exploration.
The .py file contains Principal Component Analysis of the dataset, as well as the result of a k-means clustering algorithm. Various data visualizations have been included in the file, as well. 

## Data 

The data used for this project comes from The National Registry of Exonerations is a project of the Newkirk Center for Science & Society at University of California Irvine, the University of Michigan Law School and Michigan State University College of Law. After requesting the data file, one can change the directory on line 8 in the .py file
```python
df = pd.read_csv("/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/exonerations.csv")
```
Similarly, the same would be done in the .do file. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
