import requests

url = "http://127.0.0.1:8000/summarize"
data = {"text": 
"""
Nutrients that are needed in large amounts are called
macronutrients. There are three classes of macronutrients:
carbohydrates, lipids, and proteins. These can be metabolically
processed into cellular energy. The energy from macronutrients
comes from their chemical bonds. This chemical energy is
converted into cellular energy that is then utilized to perform work,
allowing our bodies to conduct their basic functions. A unit of
measurement of food energy is the calorie. On nutrition food labels
the amount given for “calories” is actually equivalent to each calorie
multiplied by one thousand. A kilocalorie (one thousand calories,
denoted with a small “c”) is synonymous with the “Calorie” (with a
capital “C”) on nutrition food labels. Water is also a macronutrient in
the sense that you require a large amount of it, but unlike the other
macronutrients, it does not yield calories.
"""}

response = requests.post(url, json=data)
print(response.json())