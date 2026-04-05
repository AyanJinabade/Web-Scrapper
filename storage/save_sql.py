from sqlalchemy import create_engine

def save_to_sql(df):
    engine = create_engine("sqlite:///data.db")
    df.to_sql("quotes", engine, if_exists="replace", index=False)