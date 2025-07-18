import numpy as np
import pandas as pd
np.random.seed(42)  #provides random number
apartments=[f"Apt_{i}"for i in range(1,21)] #creating apartment name
dates=pd.date_range(start="2025-07-01",periods=30,freq="D")#creating dates
data={
    "Date":np.tile(dates,len(apartments)),
    "Apartment":np.repeat(apartments,len(dates)),
    "Electricity_usage":np.random.normal(loc=70,scale=5,size=len(dates)*len(apartments))
}
df=pd.DataFrame(data)
df["Electricity_usage"]=df["Electricity_usage"].round(2)
print(df)
#total usage per apartments
usage_per_apartment=df.groupby("Apartment")["Electricity_usage"].sum().sort_values(ascending=False)
print(usage_per_apartment)
daily_avg=df.groupby("Date")["Electricity_usage"].mean()
print(daily_avg)
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10,6))
sns.barplot(x=usage_per_apartment.index,y=usage_per_apartment.values)
plt.xticks(rotation=50)
plt.title("total usage per Apartment")
plt.xlabel("apartment")
plt.ylabel("total KWH")
plt.tight_layout()
plt.show()
threshold=df["Electricity_usage"].mean()+2*df["Electricity_usage"].std()
df["High_Usage_Flag"]=df["Electricity_usage"]>threshold
print(df[df["High_Usage_Flag"]==True].head())