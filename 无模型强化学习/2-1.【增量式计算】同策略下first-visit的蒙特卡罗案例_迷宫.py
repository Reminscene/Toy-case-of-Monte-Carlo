# 靡不有初，鲜克有终
# 开发时间：2022/3/9 20:53
import numpy as np
import random
import platform
import time

# 后续用增量进行加速
# 精简代码，研究终点处的情况
"情景：到达迷宫后，游戏就停止"
'''同策略是指产生数据的策略与评估和要改善的策略是同一个策略'''
prob_expansion = 100  # 为调用函数方便计算，将概率扩大了100倍，但并不影响采样结果
"""______________________________________________________定义函数_____________________________________________________"""


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


def move(state, action_number):
    [row, col] = state
    if action_number == 0:
        next_row = row - 1
        next_col = col
    if action_number == 1:
        next_row = row
        next_col = col + 1
    if action_number == 2:
        next_row = row + 1
        next_col = col
    if action_number == 3:
        next_row = row
        next_col = col - 1
    if action_number == 4:
        next_row = row
        next_col = col
    next_state = [next_row, next_col]
    return next_state


def standard(matrix):
    value = -1000
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] >= value:
                value = matrix[i][j]
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if matrix[i][j] != 0:
                matrix[i][j] = matrix[i][j]/value
            else:
                matrix[i][j] = 0
    return matrix


def get_reward(reward_lst, discount):
    state_action_lst = [[0, 0] for i in range(0, len(reward_lst))]
    for i in range(0, len(reward_lst)):
        for j in range(0, 2):
            state_action_lst[i][j] = reward_lst[i][j]
    temp_list = []
    for i in state_action_lst:
        if i not in temp_list:
            temp_list.append(i)  # 空列表用来去重
    sum_reward_list = temp_list.copy()
    for i in range(0, len(temp_list)):
        sum_reward_list[i].append(0)  # 建立两层的三维列表来存储reward之和
    count = [0 for i in range(0, len(sum_reward_list))]  # first-visit
    for i in range(0, len(sum_reward_list)):
        j = 0
        while count[i] <= 1 and j < len(reward_lst):
            if reward_lst[j][0] == sum_reward_list[i][0] and reward_lst[j][1] == sum_reward_list[i][1]:
                count[i] = count[i] + 1
                if count[i] <= 1:
                    sum_reward_list[i][2] = sum_reward_list[i][2] + reward_lst[j][2] * discount
                    j = j + 1
            elif count[i] == 1:
                sum_reward_list[i][2] = sum_reward_list[i][2] + reward_lst[j][2] * discount
                j = j + 1
            else:
                j = j + 1
    return sum_reward_list


"""______________________________________________________初始化______________________________________________________"""
# 建立抽象路网，引入可用判断矩阵，值为0则状态不可用,值为1则状态可用
available = np.ones((5, 5))
block_col = [[3], [3], [0, 1], [], [2, 3, 4]]  # 障碍物列标
for i in range(0, len(block_col)):
    if len(block_col) != 0:
        for j in block_col[i]:
            available[i][j] = 0
# print(available)
# 建立抽象路网中每一个状态的动作分布,↑→↓←⭕分别为0，1，2，3，4
action_pre = [[[0, 1, 2, 3, 4]for f in range(0, available.shape[1])] for k in range(0, available.shape[0])]
action = [[[]for f in range(0, available.shape[1])] for k in range(0, available.shape[0])]
for i in range(0, available.shape[0]):
    for j in range(0, available.shape[1]):
        if i == 0:
            action_pre[i][j].remove(0)
        if i == available.shape[0]-1:
            action_pre[i][j].remove(2)
        if j == 0:
            action_pre[i][j].remove(3)
        if j == available.shape[1]-1:
            action_pre[i][j].remove(1)
        if available[i][j] == 0:
            action_pre[i][j].clear()
# 根据障碍调整动作集合
for i in range(0, available.shape[0]):
    for j in range(0, available.shape[1]):
        if len(action_pre[i][j]) > 0:
            for k in range(0, len(action_pre[i][j])):
                next_s = move([i, j], action_pre[i][j][k])
                if available[next_s[0]][next_s[1]] != 0:
                    action[i][j].append(action_pre[i][j][k])
# 初始化学习矩阵Q
Q = np.zeros((available.shape[0]*available.shape[1], 5))
# 初始化奖励矩阵R
R = [[[]for f in range(0, 5)] for k in range(0, available.shape[0]*available.shape[1])]  # 5是动作数量，0，1，2，3，4
# 初始化策略policy,为均匀随机策略
# print(Q)
# print(R)
policy = [[[]for f in range(0, available.shape[1])] for k in range(0, available.shape[0])]
for i in range(0, available.shape[0]):
    for j in range(0, available.shape[1]):
        if len(action[i][j]) != 0:
            for k in range(0, len(action[i][j])):
                policy[i][j].append(prob_expansion/len(action[i][j]))  # 为了方便调用函数，将均匀随机策略的概率扩大了100倍，并不影响结果
# print(policy)  # policy[i][j]的含义是，第i行，第j列的状态，内部各动作发生的概率
# 初始化epsilon-greedy policy中的epsilon，以及采样次数、一次episode的长度(20)
epsilon = 0.1
sampling_times = int(input("采样次数"))  # 采样次数
episode_length = int(input("一次episode的长度"))  # 一次episode的长度
discount_factor = float(input("设置衰减系数"))  # 设置衰减系数

"""______________________________________________________采样学习_____________________________________________________"""
t = 0  # 采样次数判断变量
e = 0  # episode长度判断变量
T1 = time.perf_counter()
while t < sampling_times:
    print(t/sampling_times)  # 展示进度
    e = 0
    # print(" ")
    # print("开始第", t+1, "次采样")
    x = random.randint(0, available.shape[0]-1)
    y = random.randint(0, available.shape[1]-1)
    while available[x][y] == 0:  # 令起点不要在终点或不可用点生成
        x = random.randint(0, available.shape[0]-1)
        y = random.randint(0, available.shape[1]-1)  # 随机生成可用的状态
    r = []  # r是用来存储单次episode的收益链,结构为[[s,a,r],[s,a,r],……,[s,a,r]]
    while e < episode_length:  # 正在完成单次的episode
        r.append([])
        action_index = random_index(policy[x][y])  # 按照概率随机动作索引（从0开始的，与动作并不对应）
        r[e].append(x * available.shape[1] + y)  # 存储结构[[s,a,r],[s,a,r],……,[s,a,r]]中的s
        r[e].append(action[x][y][action_index])  # 存储结构[[s,a,r],[s,a,r],……,[s,a,r]]中的a
        [x_next, y_next] = move([x, y], action[x][y][action_index])  # 生成下一点的状态
        if [x_next, y_next] == [2, 4]:  # [2,4]是迷宫的出口
            action_number = action[x][y][action_index]
            profit = 100
            r[e].append(profit)  # 如果达到了迷宫的出口，那么在r中存储折减后100的收益,存储结构[[s,a,r],[s,a,r],……,[s,a,r]]中的r
        else:
            action_number = action[x][y][action_index]
            profit = 0
            r[e].append(profit)  # 如果没有达到迷宫的出口，那么在r中存储0的收益,# 存储结构[[s,a,r],[s,a,r],……,[s,a,r]]中的r
        x = x_next
        y = y_next
        e = e + 1
    # print("收益链为")
    # print(r)
    # print("累计收益链为")
    # print(get_reward(r))
    sum_reward = get_reward(r, discount_factor).copy()  # sum_reward的形式也是[[s,a,r],[s,a,r],……,[s,a,r]],只不过r是对应的（s，a）中总共的r
    # 根据收益链，将对应的r之和，计入R矩阵的相应位置
    for i in range(0, len(sum_reward)):
        R[sum_reward[i][0]][sum_reward[i][1]].append(sum_reward[i][2])
    for i in range(0, available.shape[0]*available.shape[1]):  # 计算学习矩阵
        for j in range(0, 5):
            if len(R[i][j]) != 0:
                Q_average = 0
                for k in range(0, len(R[i][j])):
                    Q_average = (k * Q_average + R[i][j][k]) / (k + 1)
                Q[i][j] = Q_average
    # 利用Q矩阵结果对采样概率进行epsilon-greedy改善和提升
    # print("学习矩阵为", Q)
    for i in range(0, available.shape[0] * available.shape[1]):
        if max(Q[i]) > 0:
            num = np.argmax(Q[i])  # 找到使当前状态i的Q值最大动作序号，0、1、2、3、4
            # print(num)
            index = action[i//available.shape[1]][i % available.shape[1]].index(num)  # 找到使当前动作序号所对应的策略索引
            # print(index)
            ln = len(policy[i//available.shape[1]][i % available.shape[1]])
            # print(ln)
            for j in range(0, ln):
                policy[i // available.shape[1]][i % available.shape[1]][j] = prob_expansion*epsilon/ln
            policy[i//available.shape[1]][i % available.shape[1]][index] = prob_expansion*(1-epsilon+epsilon/ln)

    # print("奖励矩阵为", R)
    # print("学习矩阵为", Q)
    t = t + 1
T2 = time.perf_counter()
print("耗时为", (T2-T1)*1000, "毫秒")

print("动作集合为")
print(action)
print("")
print("策略为")
print(policy)
print("")
print("标准化学习矩阵为", standard(Q))
