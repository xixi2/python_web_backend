# 给set()函数传入一个字符串s，则会创建一个由s中每个元素做为单个元素的集合。
words = set("hello")
print('words: {0}'.format(words))

# 若想要将整个字符串s作为集合中的一个元素，写法如下
words01 = {"hello"}
print('words01: {0}'.format(words01))

# 求一个空集和一个仅有一个元素（一个字符串）的集合的并集和交集
word02 = set({})
s = "world"
word03 = word02 | {s}
print('word03: {0}'.format(word03))
word04 = word02 & {s}
print('word04: {0}'.format(word04))

# 求两个集合的交集
word05 = {"hello"}
word06 = {"hello", "world"}
word07 = word05.union(word06)               # 并集
print('word07: {0}'.format(word07))
word08 = word05.symmetric_difference(word06)   # 返回两个集合中不重复的元素集合。
print('word08: {0}'.format(word08))
word09 = word05.intersection(word06)        # 交集
print('word09: {0}'.format(word09))


# 求两个集合中不重合的元素的集合
x = {"apple", "banana", "cherry"}
y = {"google", "runoob", "apple"}
z = x.symmetric_difference(y)
print('z: {0}'.format(z))
