#手机客户端

##**STATUS结果码对照表**
|status结果码|状态|
| --------------  | :---: |
| 1 | 成功 |
|2|未知错误|
|3|订单状态改变|
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

##**绑定商家**
#####物流人员绑定商家
```
POST /merchant/bind_merchant
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
POST /merchant/unbind_merchant
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
{"status":1,"body":null}
or
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

