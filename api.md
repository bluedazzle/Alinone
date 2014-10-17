#手机客户端
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

##**完成订单**
#####物流人员一键完成配送订单
```
POST /sender/finish_orders
```
###**Parameters**
* orders_id(_Required_|array)-完成订单到id数组
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
{"status":1,"body":{"merchant":[{"merchant_id":00000001,"merchant_name":"burgerking","sended":50},{"merchant_id":00000001,"merchant_name":"burgerking","sended":50}]}}
```