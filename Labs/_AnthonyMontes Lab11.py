# Lab 11: Exploratory Data Analysis on Student Depression Dataset

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("./Lab_11_dataset/student_depression_dataset.csv")

# ---------------------------
# Step 1: Initial Exploration
# ---------------------------
print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Descriptive Stats ---")
print(df.describe(include='all'))

# ---------------------------
# Step 2: Data Cleaning
# ---------------------------

# Rename columns for convenience
rename_map = {
    'Have you ever had suicidal thoughts ?': 'Suicidal Thoughts',
    'Family History of Mental Illness': 'Family History',
}
df.rename(columns=rename_map, inplace=True)

# Convert Yes/No to 1/0
binary_cols = ['Suicidal Thoughts', 'Family History', 'Depression']
df[binary_cols] = df[binary_cols].replace({'Yes': 1, 'No': 0})

# Convert numeric-looking columns from strings (if needed)
df['CGPA'] = pd.to_numeric(df['CGPA'], errors='coerce')

# Drop rows with missing CGPA or other key numeric values
df.dropna(subset=['CGPA', 'Sleep Duration', 'Academic Pressure', 'Financial Stress'], inplace=True)

# Encode categorical variables
df = pd.get_dummies(df, columns=['Gender', 'City', 'Profession', 'Degree'], drop_first=True)

# ---------------------------
# Step 3: Exploratory Data Analysis
# ---------------------------

# Countplot of Depression
sns.countplot(x='Depression', data=df)
plt.title("Depression Count")
plt.show()

# Histplot: Sleep Duration vs Depression
sns.histplot(data=df, x='Sleep Duration', hue='Depression', kde=True, bins=30)
plt.title("Sleep Duration vs Depression")
plt.show()

# Boxplot: CGPA vs Depression
sns.boxplot(x='Depression', y='CGPA', data=df)
plt.title("CGPA and Depression")
plt.show()

# Boxplot: Academic Pressure vs Depression
sns.boxplot(x='Depression', y='Academic Pressure', data=df)
plt.title("Academic Pressure and Depression")
plt.show()

# Heatmap: Correlation Matrix
plt.figure(figsize=(16, 10))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# Pairplot of Selected Variables
selected_cols = ['CGPA', 'Academic Pressure', 'Financial Stress', 'Sleep Duration', 'Depression']
sns.pairplot(df[selected_cols], hue='Depression')
plt.suptitle("Pairplot of Key Features", y=1.02)
plt.show()

# ---------------------------
# Observations (write your analysis here)
# ---------------------------
# - Most students reporting depression also show higher academic/work/financial pressure.
# - Lower sleep durations are associated with higher depression levels.
# - CGPA alone isn't a strong indicator.
# - Suicidal thoughts and family history are highly correlated with depression.
#
# Add more insights as you explore further!
