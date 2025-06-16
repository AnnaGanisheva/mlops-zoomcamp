# Deployment with Docker

To build docker image you need to rum 
```docker build -t duration-predictor .```

Then to run script for duration prediction you need to execute, chenging value to desired year and month
```docker run duration-predictor --year <value> --month <value>```

## Homework Results

**Question 1. Notebookl**

6.24

**Question 2. Preparing the output**

66M

**Question 3. Creating the scoring script**
To convert notebook into script run ```jupyter nbconvert --to script <notebook name>```

In our case
 
```jupyter nbconvert --to script starter.ipynb```

**Question 4. Virtual environment. Hash for Scikit-Learn**

sha256:057b991ac64b3e75c9c04b5f9395eaf19a6179244c089afdebaad98264bff37c

**Question 5. Parametrize the script**
 To predict execute ```python starter.py --year=2023 --month=5```
 14.29


**Question 6. Docker container**
```docker run duration-predictor --year 2023 --month 5```
0.19
