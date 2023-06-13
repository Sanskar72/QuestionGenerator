import openai
f = open("openai_APIKey.txt", "r")
openai.api_key = f.read()

# concept = openai.ChatCompletion.create(
#     model = "gpt-3.5-turbo",
#     temperature = 0.8,
#     max_tokens = 200,
#     messages = [
#         {"role": "system", "content": "You are an encyclopedia for data science."},
#         {"role": "user", "content": "What is Bonferroni Coefficient and when it is used?"},
#         {"role": "assistant", "content": '''
#         The Bonferroni coefficient, or Bonferroni correction, is a statistical technique used to adjust the significance level when conducting multiple hypothesis tests simultaneously. It addresses the problem of an inflated Type I error rate that occurs when performing multiple comparisons.

#         In multiple hypothesis testing, as the number of tests increases, the probability of observing at least one significant result by chance also increases. The Bonferroni correction reduces the significance level for each individual test to maintain a desired overall significance level or family-wise error rate (FWER).

#         The Bonferroni coefficient is calculated as the reciprocal of the number of tests being performed. It is multiplied by the desired significance level to obtain the adjusted significance level for each test. For example, if conducting 10 independent tests and aiming for an overall significance level of 0.05, the Bonferroni coefficient would be 0.05/10 = 0.005. This means that each test should be evaluated at a significance level of 0.005 to control the overall Type I error rate.

#         While the Bonferroni correction is conservative, it effectively controls the FWER. However, it may increase the risk of Type II errors. Alternative methods like the Holm-Bonferroni or Benjamini-Hochberg procedures offer less conservative adjustments for specific situations.
#         '''},
#         {"role": "user", "content": "Explain Data Wrangling"}
#     ]
#     )

coding = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 2,
    messages = [
        {"role": "system", "content": "You are a system that writes code in R for a prompt for to write code to get data from a dataset. You will make all assumptions needed to generate the code. As output you will only give lines of code, no description is needed."},
        {"role": "user", "content": "Distribution of grades for juniors"},
        {"role": "assistant", "content": '''
        table(moody[moody$Seniority == 'Junior',]$Grade)
        '''},
        {"role": "user", "content": "Distribution of grades for seniors who major in Economics."},
        {"role": "assistant", "content": '''
        table(moody[moody$Seniority == 'Senior' & moody$Major == 'Economics', ,]$Grade)
        '''},
        {"role": "user", "content": "Distribution of prices of rentals in Tribeca."},
        {"role": "assistant", "content": '''
        tribeca_data <- airbnb_data[airbnb_data$neighborhood == "Tribeca", ]
        '''},
        {"role": "user", "content": "Compute the variance in ages for men who work in construction."}
    ]
    )

# print(concept["choices"][0]["message"]["content"])
print("===========================")
print(coding["choices"][0]["message"]["content"])