# Python 函数式编程

>特征:可以接受一个函数作为变量 或者返回一个函数作为返回值。解释:将函数类比成一个表达式的计算结果作为参数传递.
```
def func(x):
    return x*x
#   return func #func类似表达式一样 
```

> python中内建的map() 和reduce() 都是可以接受一个函数作为参数的。map() 可以接受两个参数 一个是函数，一个是列表类可迭代的
map的作用就是 按照某种规则将list的元素全部转换 这个规则取决于传递的function的功能。 而reduce 则是做累计操作,同样也接受两个参数 一个是函数 一个是list类 但是这里的函数有要求 他要求2个参数。也就是list中的2个元素然后计算结果 跟第三个元素进行迭代。

```python
>>> list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
['1', '2', '3', '4', '5', '6', '7', '8', '9']

>>> from functools import reduce
>>> def add(x, y):
...     return x + y
...
>>> reduce(add, [1, 3, 5, 7, 9])
25
```

filter与sorted函数 看名字就知道了 传递一个函数作为参数 进行按照某种规则进行过滤或者排序。

```python 
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
# 结果: [1, 5, 9, 15]

>>> sorted([36, 5, -12, 9, -21], key=abs) # 这里函数传递要指定关键字参数
[5, 9, -12, -21, 36]
```

高阶函数就是可以接受函数作为参数的函数 类似 参数为函数指针的函数。如果要将一个函数内部定义的函数 作为返回值 直接return 函数名 即可。函数名就是一个函数指针 指向这个函数的变量。

匿名函数 由关键字lambda 定义的表达式称为匿名函数。
`lambda x: x * x` 冒号前面的x表示匿名函数的参数。   

## 装饰器 

```python 
def xx(func): # 装饰器函数
    def aaa(*args,**kw):
        print("into func")
        tmp = func(*args,**kw)
        print("func done")
        return tmp
    return aaa
@xx #称为装饰器
def func():
    pass
```

在调用func之前会先调用xx并将func的函数指针传递进去.装饰器作用:在不影响函数功能的情况下 做一些判断处理之类的操作 用来扩展函数功能 。

##  偏函数 

>functools.partial() 用来设置某个函数的参数为指定的值并且这个参数在设置之后将成为此函数的默认参数 说白了 就是改变函数默认参数的值。返回值为一个函数 此函数被称为 偏函数。 