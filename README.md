# flask_blog
纯flask实现的一个blog。
网站的整体效果：
登录页面（也是首页）：
![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP6OdRkcKO9IJ98QiarEpibKwJ74OrcrFlpqTKKElJQwf8QfibUPzrC5MlHTnaZaUytrPHCsdCLG3wyrw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

注册页面:

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP6OdRkcKO9IJ98QiarEpibKwJW3EwHMR1MykbreTWgvZzNkpxKh6Ky76yvMWvGZjoydHGZZCPicAdkLA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

这两个页面都实现了基本的验证，比如：
用户名密码为空

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP6OdRkcKO9IJ98QiarEpibKwJOpiaiaXAbnfZPcxvib9Ria8RF2pbibjeuLFAib4rjvbPTP5FQtATP9mlM1fg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

密码不正确：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP6OdRkcKO9IJ98QiarEpibKwJPmPQYJqOAWDCia7qse4JhUS5NInGylgsnvsKwXic9EUN1cicm6m8icJgBg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

正确登录后会跳转到系统主页面，长下面的样子：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2oCYb6xxT6ib3DyI5lyQVUgGkR40lWOXkJ5SyhR1wnKNdNp210g3eaCw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

页面模块：
- Header
- Footer
- 文章模块
点击主页上的模块，或者在任何文章的类别上点击，会进入下面的两个页面：
一个是列在Header上的类别，类别选中会高亮。：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2Fia0BiabtoYz4XVtH7IfC4sNoeLkIr10W3iaLSlGy2MgtuNmf3z7SlcPQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

一个是未列在Header上的类别，无高亮：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2VfkhmiaMFwNgWAlibXRSgO20nia1tlqt0caQyjuqV5qQa60Lz4ibMx3ubA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

- 文章分类tag

![](https://camo.githubusercontent.com/ec42aff413508cf5aa717dfbbbde201b9f753d07/687474703a2f2f6d6d62697a2e717069632e636e2f6d6d62697a5f706e672f4b726a78706569615a55503747766d7633554f67433836794b52746e463664503256666b686d69614d46774e6757416c6962585253674f32306e696131746c717430636151796a7571563571516136304c7a3469624d78337562412f3634303f77785f666d743d706e672674703d7765627026777866726f6d3d352677785f6c617a793d31)

- 分页模块

参考了Flask上的分页，加上用了Bootstrap的样式

- 新建/修改/删除 文章模块。

用了CK Editor，最好的编辑器之一。

新建：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2LQd7aS37pH3Dhcy2bCicRNzYygZz8xTOtvZicBAWNzibGuPX2ibVbOznwQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

修改：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2BrksHfJBze715jUibLvibHkwWPLichGg7yxcmWmA8TNSGzndbjHI5Yucg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

删除：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2McUkXGKjP7tjx3xw1cEpLoQjtTso6dv5LibLAqz1rKufVx99ajS7kbQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

- 文章详页模块

一个是对文章只有浏览权限，没有修改和删除按钮：

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2MNWttZH8uxLgpGXZhviawhzjt9cdjuSuNgO3lMaLYhWBk4yNtkLFjfQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

一个是文章的作者或者Admin用户组的用户，对文章有full control权限

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP2ExRpSGxYlbtlcgbeVNKZYURG5kFBPzhJ1u8JaAxCos1icvU6zQB1UDQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

- 权限控制模块（包括用户，权限，登录验证，管理员验证等）

![](http://mmbiz.qpic.cn/mmbiz_png/KrjxpeiaZUP7Gvmv3UOgC86yKRtnF6dP200dpibT1JibEvfsia4lYvMeM71WorsKgPfOq9eZibGNI87NKic8ItSvpRkA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1)

- 项目配置（使用instance）

