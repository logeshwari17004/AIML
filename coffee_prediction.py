import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Title
st.title("☕ Coffee Prediction Using Decision Tree (ID3 Algorithm)")

# Sample dataset
data = {
    'Weather': ['Sunny', 'Rainy', 'Overcast', 'Sunny', 'Rainy', 'Sunny', 'Overcast', 'Rainy', 'Sunny', 'Rainy'],
    'TimeOfDay': ['Morning', 'Morning', 'Afternoon', 'Afternoon', 'Evening', 'Morning', 'Morning', 'Afternoon', 'Evening', 'Morning'],
    'SleepQuality': ['Poor', 'Good', 'Poor', 'Good', 'Poor', 'Good', 'Poor', 'Good', 'Good', 'Poor'],
    'Mood': ['Tired', 'Fresh', 'Tired', 'Energetic', 'Tired', 'Fresh', 'Tired', 'Tired', 'Energetic', 'Tired'],
    'BuyCoffee': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Yes']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Encode features
X = df.drop('BuyCoffee', axis=1)
y = df['BuyCoffee']
X_encoded = pd.get_dummies(X)

# Train Decision Tree using ID3 (entropy)
clf = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf.fit(X_encoded, y)

# Show tree
st.subheader("🌳 Decision Tree Visualization")
fig, ax = plt.subplots(figsize=(12, 6))
plot_tree(clf, feature_names=X_encoded.columns, class_names=clf.classes_, filled=True)
st.pyplot(fig)

# Prediction section
st.subheader("🔮 Make a Prediction")
weather = st.selectbox("Weather", ['Sunny', 'Rainy', 'Overcast'])
timeofday = st.selectbox("Time of Day", ['Morning', 'Afternoon', 'Evening'])
sleep = st.selectbox("Sleep Quality", ['Good', 'Poor'])
mood = st.selectbox("Mood", ['Fresh', 'Tired', 'Energetic'])

# Prepare input
input_data = {
    'Weather': [weather],
    'TimeOfDay': [timeofday],
    'SleepQuality': [sleep],
    'Mood': [mood]
}
input_df = pd.DataFrame(input_data)
input_encoded = pd.get_dummies(input_df)

# Align columns with training set
input_encoded = input_encoded.reindex(columns=X_encoded.columns, fill_value=0)

# Predict
prediction = clf.predict(input_encoded)[0]
st.markdown(f"### 🎯 Prediction: {'☕ Yes, Buy Coffee' if prediction == 'Yes' else '🚫 No, Don’t Buy Coffee'}")

# Feature importance
st.subheader("📊 Feature Importance")
importances = clf.feature_importances_
for feature, importance in zip(X_encoded.columns, importances):
    if importance > 0:
        st.write(f"- **{feature}**: {importance:.2f}")
