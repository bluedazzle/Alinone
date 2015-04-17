# alinone商家手机端api

标签（空格分隔）： api

---

##**STATUS结果码对照表**
|status结果码|状态|
| --------------  | :---: |
|0|待审核|
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

**host: http://alinone.cn**

**api_version: v1**

**api地址：http://alinone.cn/api/v1/**

##**获取验证码**
#####商家app注册获取验证码
```
POST /merhcant/get_verify
```
###**Parameters**
* phone(_Required_|string)-手机号
###**Request**
```
{"phone":18215606355}
```
###**Return**
```
{"status":1,"body":{"verify_code":"123456"}}
or
{"status":2,"body":null}
or
{"status":12,"body":null}
```

##**商家注册**
#####商家app注册
```
POST /merhcant/register
```
###**Parameters**
* phone(_Required_|string)-用户名，必须为手机号
* password(_Required_|string)-密码
* verify_code(_Required_|string)-验证码
* merchant_name(_Required_|string)-店铺名称
###**Request**
```
{"phone":18215606355,"password":"132456","verify_code":"1234","merchant_name":"test"}
```
###**Return**
```
{"status":0,"body":null}
or
{"status":6,"body":null}
or
{"status":12,"body":null}
```

##**登录**
#####商家登录
```
POST /merchant/login
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
{
    "status": 1,
    "body": {
        "private_token": "2gflURY1mieOQDdNu0AqvJn37I4tGa9M",
        "merchant_name": "IECtest"
    }
}
or
{"status":7,"body":null}
or
{"status":0,"body":null}
or
{"status":4,"body":null}
```

##**更改密码**
#####商家更改密码
```
POST /merchant/change_password
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* password(_Required_|string)-当前用户密码
* new_password(_Required_|string)-新密码
###**Request**
```
{"private_token":"18215606355","password":"123456","new_password":"1234567"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "password changed success"
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "auth failed"
    }
}
or
{
    "status": 4,
    "body": {
        "msg": "password not correct"
    }
}
```


##**更改名称**
#####商家更改名称
```
POST /merchant/change_info
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* merhcant_name(_Required_|string)-新名称
###**Request**
```
{"private_token":"18215606355","password":"123456","new_password":"1234567"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "merhcant info change success"
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "auth failed"
    }
}
```


##**忘记密码**
#####商家忘记密码
```
POST /merchant/get_verify
POST /merchant/new_password
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
{
    "status": 1,
    "body": {
        "msg": "password resest success"
    }
}
or
{
    "status": 12,
    "body": {
        "msg": "verify code not correct"
    }
}
```

##**新订单**
#####商家定时获取新订单信息及平台信息
```
POST /merchant/get_new
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
###**Request**
```
{"private_token":"18215606355","password":"123456"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "today_total": 23,
        "ele_status": true,
        "have_new": false,
        "mei_status": null,
        "msg": "no new order",
        "total_money": 0
    }
}
or
{
    "status": 1,
    "body": {
        "today_total": 24,
        "ele_status": true,
        "mei_message": "用户名或密码不正确，请重新输入",
        "have_new": false,
        "mei_status": false,
        "msg": "no new order",
        "total_money": 0
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "auth failed"
    }
}
```


##**待处理订单查询**
#####商家查询待处理订单
```
POST /merchant/get_new_detail
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
###**Request**
```
{"private_token":"18215606355","username":"12345678"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "pending orders get success",
        "order_list": [
            {
                "order_id_alin": "2015041711000000010004",
                "finished_by": null,
                "order_id_old": "1111",
                "send_time": 1429231441,
                "real_price": 18,
                "phone": "18215606355",
                "address": "KB258",
                "id": 3893,
                "dishs": [
                    {
                        "dish_price": 2,
                        "dish_count": 2,
                        "id": 6162,
                        "dish_name": "可口可乐"
                    },
                    {
                        "dish_price": 1,
                        "dish_count": 2,
                        "id": 6161,
                        "dish_name": "珍珠大吊饭"
                    },
                    {
                        "dish_price": 12,
                        "dish_count": 1,
                        "id": 6160,
                        "dish_name": "宫保鸡丁"
                    }
                ],
                "order_time": 1429231441,
                "day_num": "5",
                "pay": true,
                "bind_sender": null,
                "note": "",
                "platform": 11,
                "status": 1,
                "qr_path": "order2015041711000000010004.png",
                "promotion": null,
                "origin_price": 18,
                "plat_num": "5"
            },
            {
                "order_id_alin": "2015041711000000010005",
                "finished_by": null,
                "order_id_old": "1111",
                "send_time": 1429231441,
                "real_price": 18,
                "phone": "18215606355",
                "address": "KB258",
                "id": 3894,
                "dishs": [
                    {
                        "dish_price": 2,
                        "dish_count": 2,
                        "id": 6165,
                        "dish_name": "可口可乐"
                    },
                    {
                        "dish_price": 1,
                        "dish_count": 2,
                        "id": 6164,
                        "dish_name": "珍珠大吊饭"
                    },
                    {
                        "dish_price": 12,
                        "dish_count": 1,
                        "id": 6163,
                        "dish_name": "宫保鸡丁"
                    }
                ],
                "order_time": 1429231441,
                "day_num": "6",
                "pay": true,
                "bind_sender": null,
                "note": "",
                "platform": 11,
                "status": 1,
                "qr_path": "order2015041711000000010005.png",
                "promotion": null,
                "origin_price": 18,
                "plat_num": "5"
            }
        ]
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "auth failed"
    }
}
```



##**订单**
#####商家查询已处理订单
```
POST /merchant/get_handle_orders
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* page(_Optional_|integer)-分页
###**Request**
```
{"private_token":"18215606355","username":"12345678","page":1}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "order_list": [
            {
                "order_id_alin": "2015041603000000010001",
                "finished_by": null,
                "order_id_old": "1",
                "send_time": 1429120273,
                "real_price": 12,
                "phone": "18215606355",
                "address": "本科24栋203",
                "id": 3607,
                "dishs": [],
                "order_time": 1429120273,
                "day_num": "",
                "pay": true,
                "bind_sender": {
                    "status": "",
                    "active_time": 1429052838,
                    "update_time": null,
                    "offline_num": 0,
                    "is_verify": false,
                    "online_num": 0,
                    "nick": "",
                    "offline_money": 0,
                    "online_money": 0,
                    "phone": "15597362217",
                    "verify_code": null,
                    "last_login": 1429052722,
                    "lat": null,
                    "lng": null,
                    "today_sends": 0,
                    "id": 132
                },
                "note": "",
                "platform": 3,
                "status": 2,
                "qr_path": "order2015041603000000010001.png",
                "promotion": "",
                "origin_price": 12,
                "plat_num": ""
            }
        ],
        "total": 1,
        "page": 1,
        "total_page": 1
    }
}
or
{
    "status": 13,
    "body": {
        "msg": "auth failed"
    }
}
```


##**接受订单**
#####商家接受待处理订单
```
POST /merchant/ensure_order
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* order_id(_Required_|string)-接受订单号
###**Request**
```
{"private_token":"18215606355","username":"12345678","order_id":"12345678"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "accept order success"
    }
}
```


##**生成订单**
#####商家生成新订单
```
POST /merchant/create_order
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* address(_Required_|string)-地址
* phone(_Required_|string)-订餐电话
* platform(_Required_|integer)-平台类型
* price(_Required_|float)-价格
* if_pay(_Required_|bool)-是否在线支付
* create_time(_Required_|string)-配送时间
###**Request**
```
{"username":"18215606355","private_token":"PF0VTvtiUfMH76cmpObSYnK3Q+JaldzI","address":"2015032603000000010003","phone":"18215606456","platform":"10","price":"18.0","if_pay":true,"create_time":14758697}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "create new order success"
    }
}
```


##**拒绝订单**
#####商家拒绝待处理订单
```
POST /merchant/refuse_order
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* order_id(_Required_|string)-接受订单号
###**Request**
```
{"private_token":"18215606355","username":"12345678","order_id":"12345678"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "refuse order success"
    }
}
```

##**添加平台**
#####商家添加平台
```
POST /merchant/add_platform
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* platform_type(_Required_|string)-平台类型
* account(_Required_|string)-平台账户
* password(_Required_|string)-平台密码
###**Request**
```
{"username":"18215606355","private_token": "2gflURY1mieOQDdNu0AqvJn37I4tGa9M","platform_type":3,"account":"xxx","password":"1234456"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "platform add success"
    }
}
```

##**删除平台**
#####商家删除平台
```
POST /merchant/del_platform
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* platform_type(_Required_|string)-平台类型
###**Request**
```
{"username":"18215606355","private_token": "2gflURY1mieOQDdNu0AqvJn37I4tGa9M","platform_type":3}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "platform delete success"
    }
}
```

##**添加物流**
#####商家添加物流人员
```
POST /merchant/add_sender
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
###**Request**
```
{"username":"18215606355","private_token": "2gflURY1mieOQDdNu0AqvJn37I4tGa9M"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "bind_pic": "bind142786920400000001.png",
        "msg": "get qrcode success"
    }
}
```

##**获取物流**
#####商家获取物流人员列表
```
POST /merchant/get_senders
```
###**Parameters**s
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
###**Request**
```
{"username":"18215606355","private_token": "2gflURY1mieOQDdNu0AqvJn37I4tGa9M"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "get sender list success",
        "sender_list": [
            {
                "phone": "18215606355",
                "nick": "sender"
            }
        ]
    }
}
```

##**删除物流**
#####商家删除物流人员
```
POST /merchant/delete_sender
```
###**Parameters**
* private_token(_Required_|string)-当前用户token
* username(_Required_|string)-用户名，手机号
* sender(_Required_|string)-删除物流人员手机号
###**Request**
```
{"private_token":"18215606355","private_token": "2gflURY1mieOQDdNu0AqvJn37I4tGa9M","sender":"18233333333"}
```
###**Return**
```
{
    "status": 1,
    "body": {
        "msg": "delete sender success"
    }
}
```

