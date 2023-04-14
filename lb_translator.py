import time
import pandas as pd
from deep_translator import GoogleTranslator
import os


# Create an instance of the Translator class
translator = GoogleTranslator()

# Read the CSV file into a pandas dataframe
df = pd.read_csv("material.csv")

# Iterate over each row in the dataframe
word_count = 0

for index, row in df.iterrows():
    # Get the French word from the current row
    french_word = str(row["French"])
    english_word = str(row["English"])
    german_word = str(row["German"])
    italian_word = str(row["Italian"])

    print(index, french_word, english_word, german_word, italian_word)
    len_word = len(french_word)

    if word_count > 5:
        word_count = 0
        time.sleep(1.1)

    # Translate the French word to English, German, and Italian

    if english_word == 'nan':
        english_translation = GoogleTranslator(source="fr", target="en").translate(french_word)
        df.at[index, "English"] = english_translation
        word_count += int(len_word / 6.)

    if german_word == 'nan':
        german_translation = GoogleTranslator(source="fr", target="de").translate(french_word)
        df.at[index, "German"] = german_translation
        word_count += int(len_word / 6.)

    if italian_word == 'nan':
        italian_translation = GoogleTranslator(source="fr", target="it").translate(french_word)
        df.at[index, "Italian"] = italian_translation
        word_count += int(len_word / 6.)

    df.to_csv("material_temp.csv", index=False)

# Write the updated dataframe to the same CSV file
df = pd.read_csv("material_temp.csv")
flag = 0
for index, row in df.iterrows():
    french_word = str(row["French"])
    english_word = str(row["English"])
    german_word = str(row["German"])
    italian_word = str(row["Italian"])
    if french_word == 'nan' or english_word == 'nan' or german_word == 'nan' or italian_word == 'nan':
        flag = 1
        os.remove("material_temp.csv")
        print('Er-1')

if flag == 0:
    df.to_csv("material.csv", index=False)
    os.remove("material_temp.csv")