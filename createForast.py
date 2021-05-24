from ITree import ITree
from loadData import loadCSV
import random
from DPC import DPC
from classify import divide

def do(dataSetName, cols, treeDeep, froastNum, k=2):
    # 载入数据集,并获得所有列名
    data, columns = loadCSV(dataSetName, cols)
    # 森林
    froast = []
    for _ in range(froastNum):
        # 定义一个tree
        tree = ITree()
        tree.subNodes = data
        for _ in range(treeDeep):
            # 选择两列，调用DPC算法获得聚类中心
            cols = random.choices(columns, k)
            nodes = DPC(data[cols])
            # 根据聚类中心将数据分类
            divide(data, cols, nodes)
        froast.append(tree)