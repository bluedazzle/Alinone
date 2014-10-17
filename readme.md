#Alinone 外卖整合平台

Alinone外卖物流管理系统（以下简称Alinone）为商家提供了良好高效的物流管理系统，为消费者提供了及时的外卖位置查询服务，解决了外卖平台下单之后的问题。
同时，Alinone具备完善的数据统计功能，能方便商家快速生成各类数据报表。

##项目版本：V0.1

# API version

**host: https://alinone.cn**

**api_version: v1**

#概要

1. API请求格式：host + api_version + 请求地址
2. API返回格式：
```
json:{"status":1,"body":{}}
```
status返回操作结果码,body包含返回信息，如果无返回信息，body为null
3. status结果码对照表：
status结果码|状态
--------------  | ---
1| 成功
2|未知错误
6|已存在
7|不存在
9|权限不足
11|验证码为空
12|验证码错误
13|非法操作

#api 书写格式规范：
1. 标题使用H1。eg:

>#商家
2. api接口说明使用H2加粗。eg:
>##**绑定商家**
3. api请求地址使用代码段，格式：请求类型+请求地址。eg：
```
POST /merchant/bind/
```
4. api参数使用无序列表,格式：参数名(是否必须|参数类型)-参数说明。eg：
###**Parameters**
* merchant_id(_Required_|string)-绑定商家id
* private_token(_Required_|string)-当前用户token
* time_stamp(_Required_|string)-二维码时间戳
* username(_Optional_|string)-当前用户名

5. api返回参数格式.eg:
###**return**
```
{"status":1,"body":null}
```

##完整示例:

#商家
##**绑定商家**
```
POST /merchant/bind/
```
###**Parameters**
* merchant_id(_Required_|string)-绑定商家id
* private_token(_Required_|string)-当前用户token
* time_stamp(_Required_|string)-二维码时间戳
* username(_Optional_|string)-当前用户名
###**Return**
```
{"status":1,"body":null}
```