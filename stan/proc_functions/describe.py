def describe(data, by):
    return data.groupby(by).describe()  
