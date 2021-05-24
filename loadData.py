import pandas as pd
import random

# 载入数据集
def loadCSV(filename, cols=[]):
    if cols:
        data = pd.read_csv(filename, usecols=cols)
    else:
        data = pd.read_csv(filename)
    # 数据的前置准备

    return data, data.columns.values


if __name__ == "__main__":
    data, columns = loadCSV("test.csv")
    print(type(data))
    # 访问行，使用切片形式
    print(data[0:10])
    # 访问列使用二维列表的形式
    print(data[["id","vendor_id"]])
    # 获得列名
    print(random.choices(columns,k=2))
