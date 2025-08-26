def return_table_data():

    import pandas as pd

    df = pd.read_csv("log_sheet.csv")
    df = df.fillna("").astype(str)

    df = df.drop(columns = ["region", "county", "latitude", "longitude"])

    people = list(df.columns[2:])

    baggers = {}
    for person in people:
        baggers[person] = len(df[df[person] != ""])

    #sort by bag count
    baggers = {k: v for k, v in sorted(baggers.items(), key=lambda item: item[1], reverse=True)}

    for col in list(baggers.keys()) + ["metres"]:
        df[col] = df[col].apply(lambda x: x.split(".")[0])

    data = df.to_dict(orient='records')

    return baggers, data