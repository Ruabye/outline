import createForast
if __name__ == "__main__":
    # 数据集文件名
    dataSetName = "test.csv"
    # 使用的列名/列序号
    cols = []
    # 单棵树的深度
    treeDeep = 1
    # 森林中树的数目
    froastNum = 1

    createForast.do(dataSetName, cols, treeDeep, froastNum)
