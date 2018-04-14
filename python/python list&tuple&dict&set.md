# Python list 和 tuple（元组）

> list 可以看作是一个可变的多维数组 其只是一个保存变量的指针列表 故而可变。
> tuple 元组 更像是一个常量数组 指向的元素不可变，但是由于内部元素可以是list 所以也可以说可变。其list元素的地址不变 但是list保存的元素地址可变。所以元组也可以算是可变。但要区分变化的地方在那里 内存空间是如何的。

list 定义:

a=[1,2]

a=[]#空列表

len(a) #计算列表元素个数

a[0] #用索引取a列表的第一个元素 注意python的索引是可以正向和反向的 如 a[-1] 即取最后一个元素 a[-2] 取倒数第二个元素。
a.insert(0,'a') #在0索引的位置插入一个元素
a.pop() #删除最后一个元素 
a.pop(-1) #同上句 删除那个元素 可以指定元素的索引进行pop

列表元素的修改
a[0] = 111
可以直接赋值进行修改

由于list实质是一个指针列表 其元素都是保存了元素的内存地址的整型 所以其内部元素可以是多种数据类型的元素。

元组tuple 跟list相似
定义
b=(1,) #为区分数字的小括号 所以定义只有一个元素的元组需要加个逗号。
由于元组内部其实也是指针类型 所以可以有不同类型的元素

由于不可变 所以元组与list的区别是没有追加删除插入 赋值等操作。其他均与list无异。

```
>>> a=(1,2)
>>> a.pop()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'pop'
>>> a[0]=1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment

```
# 字典dict （map） 和set （集合）

> 字典 就是一个hash表 通过key 计算出value的位置 key为不可变类型 str int char tuple(不能含有list元素) 
dict的操作 dict.get .pop(key) 添加key 可以直接
dict['不存在的key'] = value的方式 提前用in来判断下key是否存在
```
if '不存在的key' in dict:
    pass
else:
    pass

#也可以用dict.get(key,-1) #其中如果key不存在 则返回用户自定义的数值 存在返回key对应的value 
直接用dict.get(key) 不存在时返回None
```

set是一组key的集合 由于key不能重复 所以set中的元素 都是不重复的 set 创建需要一个list 通过set()函数传入一个list即可 如果list中有重复的元素 会自动去重复。
set 添加元素 set.add(key) 可以重复添加 但不会有重复的key
删除 set.remove(key)  set 可以通过 & | 运算符 计算两个set中的交集与并集。