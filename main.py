import fileinput
import re, sys, datetime


"""
文本查重
"""



def getText(d):
    # currentFile = open(d, encoding='utf-8')
    with open(d, 'r', encoding='utf-8') as f:
        txt = f.read()
    # print("原文为：", txt)
    texts = []
    texts.append(txt)
    return texts


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def msplit(s):
    seperators = ',|\.|\?|，|。|？|！'
    return re.split(seperators, s)


def readDocx(txtfile):
    print('*' * 80)
    print('文件', txtfile, '加载中……')
    t1 = datetime.datetime.now()
    paras = getText(txtfile)
    segs = []
    for p in paras:
        temp = []
        for s in msplit(p):
            if len(s) > 2:
                temp.append(s)
        if len(temp) > 0:
            segs.append(temp)
    t2 = datetime.datetime.now()
    print('加载完成，用时: ', t2 - t1)
    showInfo(segs, txtfile)
    return segs


def showInfo(text, filename='filename'):
    chars = 0
    segs = 0
    doc = []
    for p in text:
        for s in p:
            segs = segs + 1
            chars = chars + len(s)
    print('段落数: {0:>8d} 个。'.format(len(text)))
    print('短句数: {0:>8d} 句。'.format(segs))
    print('字符数: {0:>8d} 个。'.format(chars))


def compareParagraph(text1, i, text2, j, min_segment=5):
    """
    功能为比较两个段落的相似度，返回结果为两个段落中相同字符的长度与较短段落长度的比值。
    :param p1: 行
    :param p2: 列
    :param min_segment = 5: 最小段的长度
    """
    p1 = text1[i]
    p2 = text2[j]
    len1 = sum([len(s) for s in p1])
    len2 = sum([len(s) for s in p2])
    if len1 < 10 or len2 < 10:
        return []

    list = []
    for s1 in p1:
        if len(s1) < min_segment:
            continue;
        for s2 in p2:
            if len(s2) < min_segment:
                continue;
            if s2 in s1:
                list.append(s2)
            elif s1 in s2:
                list.append(s1)

    # 取两个字符串的最短的一个进行比值计算
    count = sum([len(s) for s in list])
    ratio = float(count) / min(len1, len2)
    if count > 5 and ratio > 0.1:
        print(' 发现相同内容 '.center(80, '*'))
        # print('文件1第{0:0>4d}段内容：{1}'.format(i + 1, p1))
        # print('文件2第{0:0>4d}段内容：{1}'.format(j + 1, p2))
        print("相同字符已拷贝至D:\\360MoveData\\Users\\Administrator\\Desktop\\sim.txt")
        desktop_path = "D:\\360MoveData\\Users\\Administrator\\Desktop\\"  # 新创建的txt文件的存放路径
        full_path = desktop_path + 'sim' + '.txt'  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w', encoding='utf-8')
        for item in list:
            file.write(item)
        # print('相同内容：', list)
        print('相同字符比：{1:.2f}%\n相同字符数： {0}\n'.format(count, ratio * 100))



if len(sys.argv) < 3:
    print("参数小于2.")


doc1 = readDocx(sys.argv[1])
# print("原文是：", doc1)
doc2 = readDocx(sys.argv[2])

# a = os.open("data.txt", os.O_RDONLY)  # 打开文件，并获取其文件描述符
# doc1 = os.open('D:/360MoveData/Users/Administrator/Desktop/1.txt', os.O_RDONLY)
# file = open(a, "r")  # 打开文件

# file_d1 = open(doc1, "r")

# print(file.read())
# print(file_d1.read())
# text1 = file_d1.read()
# doc2 = os.open('D:/360MoveData/Users/Administrator/Desktop/2.txt', os.O_RDONLY)
# file_d2 = open(doc2, "r")
# print(file_d2)
# text2 = file_d2.read()
# print(text2)
# texts = [text1, text2]




print('开始比对...'.center(80, '*'))
t1 = datetime.datetime.now()
if (len(doc1) > len(doc2)):
    for i in range(len(doc1)):
        if i % 100 == 0:
            print('处理进行中，已处理段落 {0:>4d} (总数 {1:0>4d} ） '.format(i, len(doc1)))
        for j in range(len(doc2)):
            compareParagraph(doc1, i, doc2, j)
else:
    for i in range(len(doc2)):
        if i % 100 == 0:
            print('处理进行中，已处理段落 {0:>4d} (总数 {1:0>4d} ） '.format(i, len(doc2)))
        for j in range(len(doc1)):
            compareParagraph(doc2, i, doc1, j)
# for i in range(len(doc1)):
#     if i % 100 == 0:
#         print('处理进行中，已处理段落 {0:>4d} (总数 {1:0>4d} ） '.format(i, len(doc1)))
#     for j in range(len(doc2)):
#         compareParagraph(doc1, i, doc2, j)
t2 = datetime.datetime.now()
print('\n比对完成，总用时: ', t2 - t1)

