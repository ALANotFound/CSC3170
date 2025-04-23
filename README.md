# 如何运行
后端
```
python run.py
```
前端
```
cd /frontend
```
```
pnpm i
```
```
pnpm dev
```

# 数据库信息
改一改 `/backend/app/config.py`，改成你自己的数据库信息。

# 初始化
一个 Apifox 的文件夹下的所有接口都写在同一个 routes 文件下面，比如我在科室管理的代码文件 `department_routes.py` 中实现了创建科室和科室列表。每次新写一个 routes 时，在 `/backend/app/__init__.py` 当中记得 import。

# 数据表
都在 `/backend/app/models` 下，应该没有问题。如果有问题就改，不过这个不涉及前端，咱管自己改。

# Routes
虽然我们在定义接口的时候没有 Error 500，但是自己测的时候建议 `try except` 一下，有问题的话就会抛 500。

# 检查
写之前先在 Apifox 上检查自己负责的所有接口，需要检查的有 1. 数据类型 2. 是否必要（一般来说返回值是都必要，除了列表里面的 item，item 内部的属性理论上也是必要的。请求参数的话就自己判断） 3. 拼写格式（Query 参数小驼峰，JSON Body 大驼峰）。有问题及时改正，在大群里面和前端老哥说一声。

# 测试
测试接口时，先在 Apifox 的“修改接口”界面添加示例值，保存后点右上角刷新，然后点运行。看到 Params 这一页，如果 Query 和 Path 还没有参数值那再填上。Body 的数据应该不会缺，但如果缺了也看看修改接口，这个定义对不对。

# 废话
不会写就把请求参数和返回响应的格式喂给大语言模型，附上数据库定义的代码和我在 department_route.py 里面已经写好的函数，应该没问题了。


Enjoy coding!