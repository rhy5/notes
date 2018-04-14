# Python 函数 

```
def func(args):
    pass
# 上面是函数的定义

```

1. 函数参数 

    - 位置参数
    - 默认参数
    - 可变参数
    - 关键字参数
    - 命名关键字参数

> 位置参数：就是按照参数传递的位置进行传参。**必选位置参数**其后可以跟**默认参数** 然后是**可变参数**，然后是**命名关键字参数** 然后是**关键字参数**。其中 关键字参数之前必须有可变参数进行隔离 或者**星号**隔离

```
def func(a,b,c=10,*d,keyword,**e)
    pass
```
注意 *号在函数参数变量前面 可以理解成将这个list类型变量展开转化为元组tuple。 
**在变量前面 意思是将字典类型的变量转化成key->value类型的列表 传递给参数。

函数定义的时候 如果参数前面有一个星号表示这个是一个可变参数。如果只传递关键字参数 则函数前面必须要有个星号用来分割表示后面的参数为关键字参数。

总结一句话:python的参数传递可以理解为元组+字典的组合变形。

## 递归函数

> 总结下核心公式:定义一个调用自身的函数 然后先写一个if判断结构 然后加一句return语句，最后再写一个return 语句。
然后根据递归要求 写出判断语句和 参数计算的表达式套进去就ok。

```
def func(a):
    if xxx：
        return x;
    return func(exp(x))
```

### 切片 迭代 

>所谓切片就是对list或者元组数据类型的简便操作截取 
`a=b[0:3]` 取b的前3个元素出来 跟字符串截取一样 不过写起来 理解起来更简便 如果[]内第一个数是0的话 可以省略不填。

切片就是对list或元组的简写操作。

>迭代：如果给定一个list或tuple，我们可以通过for循环来遍历这个list或tuple，这种遍历我们称为迭代（Iteration） 

```
    for x in list:
        pass
```

> 通过collections模块的Iterable类型判断 可以判断一个对象是否可迭代。

```
>>> from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
>>> isinstance([1,2,3], Iterable) # list是否可迭代
True
>>> isinstance(123, Iterable) # 整数是否可迭代
False
```

### 列表生成

```python
# 案例1
>>> list(range(1, 11))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 案例2
>>> L = []
>>> for x in range(1, 11):
...    L.append(x * x)
...
>>> L
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

#案例3
>>> [x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

#通过观察 发现这就三for循环的一种简写方式 for循环内的表达式 放在for 前面，然后写for循环，还可以加 判断语句

>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]

>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']

```

### generator 生成器

> 一边计算一边生成的机制叫做生成器
可以节约大部分内存 。 如果要生成的list比较复杂 可以用生成器来写个函数来实现。
两种方式 建立生成器，一种用列表生成的方式 一种是定义一个函数 内部有yield关键字此关键字类似print 

```
函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
```
```python
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

>>> f = fib(6)
>>> f
<generator object fib at 0x104feaaa0>

def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)

>>> o = odd()
>>> next(o)
step 1
1
>>> next(o)
step 2
3
>>> next(o)
step 3
5
>>> next(o)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration 
```

### 迭代器 与可迭代

> 迭代 就是循环遍历 能用for 来遍历的对象都可以称为可迭代(iterable) ,能被next(x) 调用的对象称为迭代器(iterator)。
list， tuple ,str dict set 都是可迭代的。
generator和带yield的function 都是iterator.
可以用isinstance(x,iterable) 来判断x是否可迭代。

