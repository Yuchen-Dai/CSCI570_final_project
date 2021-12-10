import numpy as np

delta = 30
alpha = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]
place = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


def get_alpha(idx1, idx2):
    return alpha[place[idx1]][place[idx2]]


def generate_str(base, numbers):
    for n in numbers:
        base = base[:n + 1] + base + base[n + 1:]
    return base


def preprocess(file_name):
    with open(file_name, 'r') as f:
        str1 = f.readline().strip()
        str2 = ''
        numbers1 = []
        numbers2 = []
        flag = False
        for line in f.readlines():
            line = line.strip()
            if line.isnumeric():
                numbers2.append(int(line)) if flag else numbers1.append(int(line))
            else:
                flag = True
                str2 = line
    str1 = generate_str(str1, numbers1)
    str2 = generate_str(str2, numbers2)
    return str1, str2


def Alignment(str1, str2):

    m = len(str1) + 1
    n = len(str2) + 1
    A = np.zeros((m, n), dtype='int64')
    A[:, 0] = np.arange(m) * delta
    A[0, :] = np.arange(n) * delta
    trace = np.zeros((m, n), dtype='int64')
    trace[:, 0] = 1
    trace[0, :] = 2
    for j in range(1, n):
        for i in range(1, m):
            A[i, j] = min(get_alpha(str1[i - 1], str2[j - 1]) + A[i - 1, j - 1], delta + A[i - 1, j],
                          delta + A[i, j - 1])
            trace[i, j] = np.argmin([get_alpha(str1[i - 1], str2[j - 1]) + A[i - 1, j - 1], delta + A[i - 1, j],
                                     delta + A[i, j - 1]])
    i, j = m - 1, n - 1
    op1, op2 = '', ''
    while i != 0 or j != 0:
        if trace[i, j] == 0:
            op1 = str1[i - 1] + op1
            op2 = str2[j - 1] + op2
            i -= 1
            j -= 1
        elif trace[i, j] == 1:
            op1 = str1[i - 1] + op1
            op2 = '-' + op2
            i -= 1
        elif trace[i, j] == 2:
            op1 = '-' + op1
            op2 = str2[j - 1] + op2
            j -= 1

    return op1, op2


def SpaceEfficientAlignment(str1, str2):
    m = len(str1) + 1
    n = len(str2) + 1
    B = np.zeros((m, 2))
    B[:, 0] = np.arange(m) * delta
    for j in range(1, n):
        B[0, 1] = j * delta
        for i in range(1, m):
            B[i, 1] = min(get_alpha(str1[i-1], str2[j-1]) + B[i - 1, 0], delta + B[i - 1, 1], delta + B[i, 0])
        B[:, 0] = B[:, 1]
    return B

"""
def BackwardSpaceEfficientAlignment(str1, str2):
    m = len(str1) + 1
    n = len(str2) + 1
    B = np.zeros((m, 2))
    B[:, 0] = np.arange(m) * delta
    for j in range(1,n):
        B[0, 1] = j * delta
        for i in range(1,m):
            B[i, 1] = min(get_alpha(str1[n-i], str2[m-j]) + B[i - 1, 0], delta + B[i-1, 1], delta + B[i, 0])
        B[:, 0] = B[:, 1]
    return B
"""

def DivideAndConquerAlignment(str1, str2):
    x = ""
    y = ""
    m = len(str1) + 1
    n = len(str2) + 1
    mid = int(n/2)

    if (m <= 2) | (n <= 2):
        x,y = Alignment(str1, str2)

    else:
        f = SpaceEfficientAlignment(str1, str2[0:mid])
        g = SpaceEfficientAlignment(str1[::-1], str2[mid:n][::-1])
        #g = BackwardSpaceEfficientAlignment(str1, str2[int(n / 2) + 1:n])

        sum_score = f[:,1] + g[:,1][::-1]
        q = list(sum_score).index(min(sum_score))

        left = DivideAndConquerAlignment(str1[0 : q], str2[0 : mid])
        right = DivideAndConquerAlignment(str1[q : m], str2[mid  : n])

        x = left[0] + right[0]
        y = left[1] + right[1]
    return x,y

def calc_cost(str1, str2):
    cost = 0
    for i in range(len(str1)):
        if str1[i] == '-' or str2[i] == '-':
            cost += delta
        else:
            cost += get_alpha(str1[i], str2[i])
    return cost

if __name__ == '__main__':
    s1, s2 = preprocess('input.txt')
    print(s1)
    print(s2)
    result = DivideAndConquerAlignment(s1, s2)
    print(result[0])
    print(result[1])
    print(calc_cost(result[0], result[1]))