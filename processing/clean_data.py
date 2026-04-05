import pandas as pd

def clean_data(data):
    df = pd.DataFrame(data)

    df = df.drop_duplicates()

    df["text"] = df["text"].str.strip()
    df["author"] = df["author"].str.strip()

    return df