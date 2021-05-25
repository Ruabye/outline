from ITree import ITree
import random
from DPC import DPC
import numpy as np

def cluster(top, fi, ti, nowdeep, k=2):
    # 选择两列，调用DPC算法获得聚类中心
    cols = random.sample(range(len(top.subNodes[0])), k=k)
    print("=========={} - {}==========".format(fi, ti))
    print("选择的列为: ", cols)
    dpc_data = np.vstack((top.subNodes[:, cols[0]], top.subNodes[:, cols[1]])).T
    centerPoint, divide_dict_num = DPC(dpc_data)
    for k in divide_dict_num:
        obj = ITree(top.subNodes[centerPoint[k]], [], [])
        tmp = []
        for i in divide_dict_num[k]:
            tmp.append(top.subNodes[i])
        obj.subNodes = np.array(tmp)
        top.next.append(obj)
        nowdeep.append(obj)

def do(dataSetName, cols, treeDeep, froastNum):
    # 载入数据集,并获得所有列名
    # data, columns = loadCSV(dataSetName, cols)
    data = []
    with open(dataSetName, "r") as f:
        for line in f.readlines():
            data.append([int(i) for i in line.split()])
    data = np.array(data,dtype="int64")
    print("载入%d条数据"%len(data))
    # 森林
    froast = []
    for fi in range(froastNum):
        # 定义一个tree
        tree = ITree()
        tree.subNodes = data
        tree.value = [0,0] # 暂时没有实际意义
        # 当前深度所有叶子节点
        nowDeep = [tree]
        for ti in range(treeDeep):
            tmp = []
            for top in nowDeep:
                cluster(top, fi, ti, tmp)
            nowDeep = tmp

        # print(len(nowDeep))
        # print(nowDeep[0].value)
        # print(len(nowDeep[0].subNodes))
        # print(len(tree.next))
        # print(tree.next[0].value)
        # print(len(tree.next[0].subNodes))

        froast.append(tree)