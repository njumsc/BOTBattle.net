## 开发者文档

### 用户接口

| url         | 方法 | 功能         |
| :---------- | :--- | :----------- |
| /userReg/   | GET  | 用户注册登录 |
| /userOut/   | GET  | 用户注销     |
| /userAct/   | GET  | 提交操作     |
| /getStatus/ | GET  | 获取游戏状态 |

##### 用户注册登陆

`GET /userReg/?name=$username`

| 参数        | 含义               |
| :---------- | :----------------- |
| `$username` | 要注册登录的用户名 |

| 返回值                | 含义                             |
| :-------------------- | :------------------------------- |
| Invalid request       | 参数错误                         |
| You have logged in    | 已经登陆                         |
| User exist            | 已登录, 但所请求的用户名已经登陆 |
| User login success    | 重新登陆成功                     |
| User register success | 用户注册成功                     |

#### 用户注销

`GET /userOut/`

| 返回值         | 含义         |
| :------------- | :----------- |
| No login       | 未登录       |
| Logout success | 用户注销成功 |

#### 提交操作

`GET /userAct/?roomid=$roomid&num1=$num1&num2=$num2`

| 参数     | 含义   |
| :------- | :----- |
| `roomid` | 房间号 |
| `num1`   | 操作1  |
| `num2`   | 操作2  |

| 返回值           | 含义         |
| :--------------- | :----------- |
| Invalid request  | 参数错误     |
| No login         | 未登录       |
| Numbers overflow | 操作不合标准 |
| Upload success   | 提交成功     |

#### 获取游戏状态

`GET /getStatus/?roomid=$roomid`

| 参数     | 含义   |
| :------- | :----- |
| `roomid` | 房间号 |

返回值样例:

```js
{
    "status": "success",
    "roomid": "fc1",
    "history": {
        "goldenNums": [
            12.6,
            9.2,
            3.2
        ],
        "userActs": {
            "frank": [
                [100.0, 0.0]
            ],
            "jack": [
                [1.15114, 15.51],
                [11.5114, 0.1551]
            ],
            "tom": [
                [2.33, 6.66],
                [5.55, 5.55]
            ]
        }
    },
    "scores": {
        "frank": 12,
        "jack": 3,
        "tom": -4
    },
    "time": 42
}
```

| 键      | 含义                               |
| :------ | :--------------------------------- |
| status  | 请求状态                           |
| roomid  | 房间名称                           |
| history | 数组, 历史黄金点数据, 从远到近排序 |
| users   | 当前房间内用户, 分数从高到低       |
| time    | 当前回合剩余时间(s)                |