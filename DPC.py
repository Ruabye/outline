import matplotlib.pyplot as plt
import math
import collections
from color import color
MAX_CENTER_POINT = 25
def distence(node1, node2):
    # 计算欧式距离
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def getTestData(filename):
    #读取测试数据
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            data.append( [int(i) for i in line.split()] )
    return data

def choseDC(data, dis_dict, dc_wg):
    points = []
    data_len = len(data)
    for i in range(data_len):
        for j in range(i, data_len):
            d = distence(data[i], data[j])
            dis_dict[i,j] = d
            points.append(d)
    points.sort()
    # 选择dc的真正值
    dc = points[ int( dc_wg * data_len * (data_len + 1) / 2 ) ]
    return dc


def calcRho(data, dc, dis_dict):
    # 获得归一化后的ρ
    # dc = 1001170.2715382634
    # dc = 766184.031064339 #95%
    data_len = len(data)
    # 附上初始值
    rho = [0] * data_len
    for i in range(0, data_len):
        for j in range(i+1, data_len):
            # 两点间的距离
            t = math.exp(-(dis_dict[i,j]/dc) ** 2)
            rho[i] += t
            rho[j] += t
    # 归一化
    maxrho = max(rho)
    return [i/maxrho for i in rho]
    # return rho


def calcDelta(rho, data, dis_dict):
    # 获得归一化后的δ
    data_len = len(data)
    # 附上初始值
    delta = [0] * data_len

    # 排序并返回下标 https://blog.csdn.net/qq1195365047/article/details/90295660
    rho_index_sorted = sorted(range(data_len),key=lambda x:rho[x],reverse=True)
    # 改进方法
    for i in range(1, data_len-1):
        # 取出一个下标
        di = rho_index_sorted[i]
        tmp = []
        for j in rho_index_sorted[:i]:
            tmp.append(dis_dict[min(di,j),max(di,j)])
        delta[di] = min(tmp)
    delta[rho_index_sorted[0]] = max(delta)
    # 原始方法
    # for r in range(data_len):
    #     if rho[r] == max(rho):
    #         delta[r] = max( [distence(data[r], i) for i in data] )
    #     else:
    #         tmp = []
    #         for j in range(data_len):
    #             if rho[j] > rho[r]:
    #                 tmp.append( distence(data[r], data[j]) )
    #         delta[r] = min(tmp)

    # 归一化
    maxdelta = max(delta)
    return [i/maxdelta for i in delta]
    # return delta


def getClusterCenter(rho, delta, data):
    # 计算聚类中心点在数据集中的位置

    # 计算rho*delta
    rd = [rho[i] * delta[i] for i in range(len(rho))]
    sort_rd = sorted(rd, reverse=True)
    plt.subplot(2, 1, 1)
    plt.scatter(range(1, len(sort_rd) + 1), sort_rd, s=1)
    plt.subplot(2, 1, 2)
    plt.scatter(range(1, MAX_CENTER_POINT*2+1), sort_rd[:MAX_CENTER_POINT*2], s=1)
    plt.savefig("tmp.png")
    plt.close()
    clusterCenter = int( input("图片已保存至本地，输入聚类中心点个数：") )
    # clusterCenter = 15
    centerPoint = []
    # 计算聚类中心的点的坐标
    for i in range(clusterCenter):
        v = max(rd)
        i = rd.index(v)
        centerPoint.append(i)
        rd[i] = -1
    return centerPoint


def cluster(rho, delta, data, dis_dict):
    # 计算聚类中心坐标的索引
    centerPoint = getClusterCenter(rho,delta,data)
    divide_dict = collections.defaultdict(dict)
    for i in range(len(centerPoint)):
        divide_dict[i]["x"] = []
        divide_dict[i]["y"] = []
    # 根据每个点到中心的距离划分
    data_len = len(data)
    for d in range(data_len):
        dists = [dis_dict[min(d,i), max(d,i)] for i in centerPoint]
        index = dists.index(min(dists))
        divide_dict[index]["x"].append(data[d][0])
        divide_dict[index]["y"].append(data[d][1])
    return centerPoint, divide_dict



if __name__ == "__main__":
    data = getTestData("3.txt")

    # 存储任意两点间的位置
    dis_dict = {}
    dc = choseDC(data, dis_dict, dc_wg = 0.01)
    print(dc)
    rho = calcRho(data, dc, dis_dict)
    delta = calcDelta(rho, data, dis_dict)

    # 划分聚类
    centerPoint,divide_dict = cluster(rho, delta, data, dis_dict)

    plt.clf()
    i = 0
    for k in divide_dict.keys():
        # 输出各聚类中心的坐标以及聚类下点的个数
        print(data[centerPoint[k]], ": ", len(divide_dict[k]["x"]))
        plt.scatter(divide_dict[k]["x"], divide_dict[k]["y"], s=1, c=color[i])
        i += 1
    for i in centerPoint:
        plt.scatter([data[i][0]], [data[i][1]], s=10,c="red")
    plt.show()


    # x1 = []
    # y1 = []
    # for node in data:
    #     x1.append(node[0])
    #     y1.append(node[1])
    # # 绘制子图
    # plt.subplot(1, 2, 1)
    # plt.scatter(x1, y1, s=1)
    # plt.subplot(1, 2, 2)
    # plt.scatter(rho, delta, s=1)

