#手机客户端

##**STATUS结果码对照表**
|status结果码|状态|
| --------------  | :---: |
|1|成功|
|2|未知错误|
|3|订单状态改变|
|4|密码错误|
|5|超时|
|6|已存在|
|7|不存在|
|9|权限不足|
|11|验证码为空|
|12|验证码错误|
|13|非法操作|

##**订单状态码对照表**
|status|状态|
| --------------  | :---: |
|1|待处理|
|2|已确认|
|3|配送中|
|4|已完成|
|5|已撤单|

##**订单平台ID对照表**
|平台ID|平台|
| --------------  | :---: |
|01|淘点点|
|02|饿了么|
|03|美团外卖|
|10|电话订单|
|11|其他平台|

##**二维码生成**
```
QRcode/method createqr(type, qrtext)
```
|参数|平台|
| --------------  | :---: |
|type|生成类型：1、订单；2、绑定|
|qrtext|订单号 & 商家ID|

##**验证码调用**
```
AlinApi/method createverfiycode(phone, count)
```
|参数|平台|
| --------------  | :---: |
|type|生成类型：1、订单；2、绑定|
|qrtext|订单号 & 商家ID|

##**物流人员注册**
#####物流人员注册
```
POST /sender/register
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* password(_Required_|string)-密码
* reg_code(_Required_|string)-验证码，测试值：1234
###**Request**
```
{"username":18215606355,"password":"132456","reg_code":"1234"}
```
###**Return**
```
{"status":1,"body":{"private_token":"qwertyuiopqwertyuiopqwertyuiopqw"}}
or
{"status":6,"body":null}
or
{"status":12,"body":null}
```

##**验证码**
#####物流人员注册获取验证码
```
POST /sender/req_verify
```
###**Parameters**
* phone(_Required_|string)-待验证手机，必须为手机号
###**Request**
```
{"phone":18215606355}
```
###**Return**
```
{"status":1,"body":{"verify_code":"123456"}}
or
{"status":2,"body":null}
```

##**登录**
#####物流人员登录
```
POST /sender/login
```
###**Parameters**
* username(_Required_|string)-用户名，必须为手机号
* password(_Required_|string)-密码
###**Request**
```
{"username":18215606355,"password":"132456"}
```
###**Return**
```
{"status":1,"body":{"private_token":"qwertyuiopqwertyuiopqwertyuiopqw"}}
or
{"status":7,"body":null}
or
{"status":4,"body":null}
```

##**绑定商家**
#####物流人员绑定商家
```
POST /sender/bind_merchant
```
###**Parameters**
* merchant_id(_Required_|string)-绑定商家id
* private_token(_Required_|string)-当前用户token
* time_stamp(_Required_|string)-二维码时间戳
* username(_Optional_|string)-当前用户名
###**Request**
```
{"merchant_id":1,"private_token":"18215606355","time_stamp":1413524216}
```
###**Return**
```
{"status":1,"body":{"merchant_id":1,"merchant_name":"burgerking"}}
```


##**解绑商家**
#####物流人员解除绑定商家
```
POST /sender/unbind_merchant
```
###**Parameters**
* merchant_id(_Required_|string)-解绑定商家id
* private_token(_Required_|string)-当前用户token
###**Request**
```
{"merchant_id":1,"private_token":"18215606355"}
```
###**Return**
```
{"status":1,"body":null}
```
##**绑定订单**
#####物流人员绑定配送订单
```
POST /sender/bind_orders
```
###**Parameters**
* orders_id(_Required_|array)-订单id数组
* private_token(_Required_|string)-当前用户token
###**Request**
```
{"orders_id":[{"order_id":"2014101601000000120001"},{"order_id":"2014101601000000120001"}],"private_token":"18215606355"}
```
###**Return**
```
{"status": 1, "body": {"bind_list": [{"phone": "13438101510", "name": "\u602a\u8700\u9ecd\u7cbe\u54c1\u5916\u5356", "dish_list": [{"count": 1, "price": 13.0, "name": "\u8700\u9ecd\u817f\u6392\u996d"}], "address": "\u7535\u5b50\u79d1\u6280\u5927\u5b66\u672c\u79d1\u4e5d\u680b", "order_id": "2015030803000000040017", "merchant_id": "00000004"}], "fail_list": []}}or
{"status":4,"body":{"fail_list":[{"order_id":"2014101601000000120001"},{"order_id":"2014101601000000120001"}]}}
or
{"status":13,"body":{"fail_list":[{"order_id":"2014101601000000120001"},{"order_id":"2014101601000000120001"}]}}
```

##**完成订单**
#####物流人员一键完成配送订单
```
POST /sender/finish_orders
```
###**Parameters**
* orders_id(_Optional_|array)-有问题订单id数组
* private_token(_Required_|string)-当前用户token
###**Request**
```
{"orders_id":[{"order_id":"2014101601000000120001"},{"order_id":"2014101601000000120001"}],"private_token":"18215606355"}
```
###**Return**
```
{"status":1,"body":null}
```

##**查询当前订单**
#####物流人员获取已扫订单
```
POST /sender/get_bind_orders
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
###**Request**
```
{"private_token":"18215606355"}
```
###**Return**
```
{"status":1,"body":[{"order_id":"20140000000","name":"xxx","merchant_id":"1","phone":"1300000000","address":"258","dish":[{"name":"xx","count":"1","price":12.0},{"name":"xx","count":"1","price":12.0}]},{"order_id":"20140000000","name":"xxx","merchant_id":"1","phone":"1300000000","address":"258","dish":[{"name":"xx","count":"1","price":12.0},{"name":"xx","count":"1","price":12.0}]}]}
```

##**上传GPS坐标**
#####物流人员上传GPS坐标
```
POST /sender/gps_renew
```
###**Parameters**
* lng(_Required_|float)-当前GPS经度坐标
* lat(_Required_|float)-当前GPS纬度坐标
* private_token(_Required_|string)-当前用户token
###**Request**
```
{"lng":102.45213,"lat":86.14256,private_token:"18215606355"}
```
###**Return**
```
{"status":1,"body":null}
or
{"status":3,"body":{"orders_id":[{"order_id":2014101601000001240003},{"order_id":2014101601000001240003}]}}
```

##**获取绑定信息**
#####物流人员个人中心显示信息
```
POST /sender/info
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
###**Request**
```
{private_token:"18215606355"}
```
###**Return**
```
{"status":1,"body":{"merchants":[{"merchant_id":00000001,"merchant_name":"burgerking","sended":50},{"merchant_id":00000001,"merchant_name":"burgerking","sended":50}]}}
```

##**查询**
#####查询外卖信息
```
POST /website/search
```
###**Parameters**
* search(_Required_|string)-订单号或手机号
###**Request**
```
{“search”:"18215606355"}
```
###**Return**
```
{"status":1,"body":{"meal_list":[{"status":3,"update_time":"2014-10-19 20:11:11+08:00","sender_name":"sender","address":null,"lat":108.51234,"lng":25.12387,"name":"burgerking"},{"status":3,"update_time":"2014-10-19 20:11:11+08:00","sender_name":"sender","address":null,"lat":108.51234,"lng":25.12387,"name":"burgerking"}]}}
or
{"status":1,"body":{"meal_list":[{"status":2,"name":"burgerking","address":"test"}]}}
or
{"status":1,"body":{"meal_list":[{"status":1,"name":"burgerking","address":"test"}]}}
or
{"status"9,"body":{}}
```
##**更改密码**
#####物流人员更改密码
```
POST /sender/change_password
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* password(_Required_|string)-当前用户密码
* new_password(_Required_|string)-新密码
###**Request**
```
{"private_token":"18215606355","password":"123456","new_password":"1234567"}
```
###**Return**
```
{"status":1,"body":{}}
```

##**忘记密码**
#####物流人员忘记密码
```
POST /sender/forget_password
POST /sender/new_password
```
###**Parameters**
* phone(_Required_|string)-用户帐号
###**Request**
```
{"phone":"18215606355"}
```
###**Return**
```
{"status":1,"body":{}}
```

###**Parameters**
* verify_code(_Required_|string)-验证码
* phone(_Required_|string)-用户帐号
* new_password(_Required_|string)-新密码
###**Request**
```
{"phone":"18215606355","verify_code":"123456","new_password":"1234567"}
```
###**Return**
```
{"status":1,"body":{}}
```

##**获取今日配送信息**
#####物流人员获取今日已配送信息
```
POST /sender/get_today_info
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
###**Request**
```
{private_token:"18215606355"}
```
###**Return**
```
{"status": 1, "body": {"merchants": [{"sended": [{"platform": 3, "online_pay": false, "alin_id": "2015030303000000010003", "phone": "18215606355", "price": 18.0, "send_time": "2015-03-03 16:53:36+08:00", "plat_num": "5"}, {"platform": 3, "online_pay": false, "alin_id": "2015030303000000010002", "phone": "13438835711", "price": 12.0, "send_time": "2015-03-03 16:25:57+08:00", "plat_num": ""}], "merchant_id": "00000001", "merchant_name": "IECtest"}, {"sended": [{"platform": 1, "online_pay": true, "alin_id": "2015010303000000010022", "phone": "15008236070", "price": 13.0, "send_time": "2015-03-04 13:52:49+08:00", "plat_num": ""}, {"platform": 3, "online_pay": false, "alin_id": "2015010302000000010004", "phone": "13438839803", "price": 12.0, "send_time": "2015-03-04 13:52:11+08:00", "plat_num": ""}], "merchant_id": "00000002", "merchant_name": "guaishushu"}]}}
```

##**获取未处理订单数量**
#####物流人员获取绑定商家的未处理订单数量
```
POST /sender/get_pre_orders
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
###**Request**
```
{private_token:"18215606355"}
```
###**Return**
```
{"status": 1, "body": {"merchants": [{"count": 0, "merhcant_id": "2"}, {"count": 1, "merhcant_id": "1"}]}}
```