from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from random import choice
import openai

app = Flask(__name__)
def do1(numQ):
    df = pd.read_csv('https://raw.githubusercontent.com/dev7796/data101_tutorial/main/files/dataset/airbnb.csv')
    #Lets set NaN name to "Unkown" and NaN host_name to "Unknown" as well. Fill NaN values with "Unknown"
    df.fillna('Unknown', inplace=True)
    # print(",".join(list((df.columns))))
    data = []
    for i in range(int(numQ)):
        numerical = list(df.select_dtypes(np.number).columns)
        numerical.remove('id')
        categorical = list(df.select_dtypes(exclude = np.number).columns)
        aggregate = ["count", "sum", "mean", "median", "min", "max", "mode", "standard deviation", "variance"]
        n = choice(np.arange(len(categorical)-2)) + 1
        a = choice(numerical)
        c = choice(aggregate)
        text = "What is " + c + " of " + a + " when "
        for j in range(n):
            b = choice(categorical)
            text += b + " = '" + choice(df[b].unique()) + "' "
            categorical.remove(b)
            if j < n - 1:
                text += "and "
                
        data.append((i+1, text))
    return data

def do2(type, prompt, dataset):
    data = list()
    f = open("openai_APIKey.txt", "r")
    openai.api_key = f.read()
    if type == "concept":
        concept = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0.8,
        max_tokens = 200,
        messages = [
            {"role": "system", "content": "You are an encyclopedia for data science."},
            {"role": "user", "content": "What is Bonferroni Coefficient and when it is used?"},
            {"role": "assistant", "content": '''
            The Bonferroni coefficient, or Bonferroni correction, is a statistical technique used to adjust the significance level when conducting multiple hypothesis tests simultaneously. It addresses the problem of an inflated Type I error rate that occurs when performing multiple comparisons.
            In multiple hypothesis testing, as the number of tests increases, the probability of observing at least one significant result by chance also increases. The Bonferroni correction reduces the significance level for each individual test to maintain a desired overall significance level or family-wise error rate (FWER).
            The Bonferroni coefficient is calculated as the reciprocal of the number of tests being performed. It is multiplied by the desired significance level to obtain the adjusted significance level for each test. For example, if conducting 10 independent tests and aiming for an overall significance level of 0.05, the Bonferroni coefficient would be 0.05/10 = 0.005. This means that each test should be evaluated at a significance level of 0.005 to control the overall Type I error rate.
            While the Bonferroni correction is conservative, it effectively controls the FWER. However, it may increase the risk of Type II errors. Alternative methods like the Holm-Bonferroni or Benjamini-Hochberg procedures offer less conservative adjustments for specific situations.
            '''},
            {"role": "user", "content": prompt}
        ]
        )
        data.append(concept["choices"][0]["message"]["content"])
    
    elif type == "coding":
        df = pd.read_csv(dataset)
        coding = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 1.3,
    messages = [
        {"role": "system", "content": "You are a system that writes code in R for a prompt for to write code to get data from a dataset named df. You will make all assumptions needed to generate the code. As output you will strictly only give lines of code."},
        {"role": "user", "content": "Distribution of grades for juniors"},
        {"role": "assistant", "content": '''
        table(df[df$Seniority == 'Junior',]$Grade)
        '''},
        {"role": "user", "content": "Distribution of grades for seniors who major in Economics."},
        {"role": "assistant", "content": '''
        table(df[df$Seniority == 'Senior' & df$Major == 'Economics', ,]$Grade)
        '''},
        {"role": "user", "content": "Distribution of prices of rentals in Tribeca."},
        {"role": "assistant", "content": '''
        tribeca_data <- df[df$neighborhood == "Tribeca", ]
        '''},
        {"role": "user", "content": prompt + ". The columns in the dataset are" + ",".join(list((df.columns)))}
    ]
    )
        print(coding["choices"][0]["message"])
        data.append(coding["choices"][0]["message"]["content"])
    return data

@app.route('/')
def homePage():
    return render_template("home.html")


@app.route('/generateQ', methods=['POST'])
def generateQ():
    numQ = request.form['numQ']
    data = do1(numQ)
    return render_template("outputQ.html", data = data)

@app.route('/askGPT', methods=['POST'])
def askGPT():
    type, prompt, dataset = request.form['type'], request.form['question'], request.form['dataset']
    op = [prompt]
    response = do2(type, prompt, dataset)
    op.append(response[0])
    return render_template("outputGPT.html", data = op)

if __name__ == '__main__':
    # Run app on development server
    app.run(debug = True)