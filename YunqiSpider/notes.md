 mongodb集群添加管理员和用户

https://blog.csdn.net/zZ_life/article/details/78664794

添加并认证管理员 

```shell
use admin

db.createUser({
    user:"admin",
    pwd:"admin",
    roles:[{
        role:"root",
        db:"admin"
    }]
})

db.auth("admin", "admin")
```



#### 添加用户并认证用户

```shell
use yunqi

db.createUser({
    user:"test",
    pwd:"123456",
    roles:[{
        role:"dbAdmin",
        db:"yunqi"
    },{
        role:"readWrite",
        db:"yunqi"
    }]
})

db.auth("test", "123456")
```



#### 重启mongodb服务

```shell
sudo mongod --dbpath /usr/local/var/mongodb
```

#### 开启权限验证

> 开启认证也很简单，在配置文件（默认是/etc/mongodb.conf）里面加入auth = true这样一行就行了。



#### 验证登录

```shell
mongo 127.0.0.1:27017/yunqi -u test -p
```

