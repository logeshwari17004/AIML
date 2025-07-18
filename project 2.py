import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

# Seed for reproducibility
np.random.seed(42)

# Generate synthetic employee working hour data
employee_ids = [f"EMP_{i:03d}" for i in range(1, 31)]
date_range = pd.date_range("2025-07-01", periods=30, freq="D")

data = {
    "Date": np.tile(date_range, len(employee_ids)),
    "Employee_ID": np.repeat(employee_ids, len(date_range)),
    "Working_Hours": np.random.uniform(4, 10, size=len(employee_ids) * len(date_range)).round(2)
}

df = pd.DataFrame(data)
df.to_csv("employee_working_hours.csv", index=False)

# Read and explore data
df = pd.read_csv("employee_working_hours.csv")
print("First 5 rows:\n", df.head())
print("\nDescriptive statistics:\n", df.describe())
print("\nUnique value counts:\n", df.nunique())

# Total and average hours per employee
total_hours = df.groupby("Employee_ID")["Working_Hours"].sum().sort_values(ascending=False)
avg_daily = df.groupby("Employee_ID")["Working_Hours"].mean()

# Add low/high hour flags
threshold_low = 5
threshold_high = 9
df["Low_Hour_Flag"] = df["Working_Hours"] < threshold_low
df["High_Hour_Flag"] = df["Working_Hours"] > threshold_high

print("\nLow Hour Flag Sample:\n", df[["Employee_ID", "Working_Hours", "Low_Hour_Flag"]].head())
print("\nHigh Hour Flag Sample:\n", df[["Employee_ID", "Working_Hours", "High_Hour_Flag"]].head())
print("\nAverage daily working hours per employee:\n", avg_daily)

# Plot top 10 employees by total working hours
top10 = total_hours.head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top10.index, y=top10.values)
plt.xticks(rotation=45)
plt.title("Top 10 Employees By Total Working Hours")
plt.ylabel("Hours")
plt.tight_layout()
plt.show()

# Scrape book titles and prices
url = "http://books.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article', class_='product_pod')

book_data = []
for book in books:
    try:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.strip()
        print(f"Title: {title}\nPrice: {price}\n")
        book_data.append({"Title": title, "Price": price})
    except Exception as e:
        print(f"Error parsing book: {e}")
        continue

# Save scraped data
books_df = pd.DataFrame(book_data)
books_df["Price"] = books_df["Price"].str.replace("£", "", regex=False)
books_df["Price"] = pd.to_numeric(books_df["Price"], errors="coerce")

books_df.to_csv("scraped_books.csv", index=False)

print("\nScraped Book Data:\n", books_df.head())


