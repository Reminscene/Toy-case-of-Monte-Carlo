# 靡不有初，鲜克有终
# 开发时间：2022/3/7 19:51
import random
import numpy as np
import matplotlib.pyplot as plt
Q = np.zeros((6, 6))
R = -1*np.ones((6, 6))
R[0][4] = 0
R[1][3] = 0
R[1][5] = 100
R[2][3] = 0
R[3][1] = 0
R[3][2] = 0
R[3][4] = 0
R[4][0] = 0
R[4][3] = 0
R[4][5] = 100
R[5][1] = 0
R[5][4] = 0
R[5][5] = 100
discount_factor = 0.8
print("奖励矩阵设置如下")
print(R)
print("")
print("初始的Q矩阵设置如下")
print(Q)
print("")


def random_index(rate):
    # """随机变量的概率函数"""
    # 参数rate为list<int>
    # 返回概率事件的下标索引,注意，列表里面的数字加和应当为大于1的数字！！！！
    start = 0
    index = 0
    randnum = random.randint(1, int(sum(rate)))
    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return index


def standard(matrix):
    value = -1000
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] >= value:
                value = matrix[i][j]
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            matrix[i][j] = matrix[i][j]/value
    return matrix


action_available = [[0 for j in range(0, 6)] for i in range(0, 6)]
prob_rate = [[0 for k in range(0, 6)] for f in range(0, 6)]
for i in range(0, 6):
    for j in range(0, 6):
        if R[i][j] >= 0:
            action_available[i][j] = 1
    for j in range(0, 6):
        if R[i][j] >= 0:
            prob_rate[i][j] = 1/sum(action_available[i])
# print(action_available)
print("各个状态的动作概率如下")
print(prob_rate)
print("")
for i in range(0,6):
    for j in range(0,6):
        prob_rate[i][j] = 10*prob_rate[i][j]
# 初始条件设置完毕

times = 0
judge = 0
count = 15000

while times <= count:
    Q_prev = Q.copy()  # 将之前的Q矩阵存储起来以便判断收敛
    state = random.randint(0, 5)  # 随机生成初始状态
    while state != 5:
        state_next = random_index(prob_rate[state])  # 按照概率随机生成下一个状态
        max_Q_lst = []
        for i in range(0, 6):
            max_Q_lst.append(Q[state_next][i])  # 用来求maxQ（s‘，a’）的Q（s‘，a’）列表
        Q[state][state_next] = R[state][state_next] + discount_factor*max(Q[state_next])
        state = state_next

    if state == 5:
        state_next = random_index(prob_rate[state])  # 按照概率随机生成下一个状态
        max_Q_lst = []
        for i in range(0, 6):
            max_Q_lst.append(Q[state_next][i])  # 用来求maxQ（s‘，a’）的Q（s‘，a’）列表
        Q[state][state_next] = R[state][state_next] + discount_factor*max(Q[state_next])
    times = times + 1
    # if Q_prev.all() == Q.all():
    # judge = 1
print("最终的Q矩阵如下")
print(Q)
print("")
print("进行标准化处理，最终的Q矩阵如下")
print(standard(Q))
