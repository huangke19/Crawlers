集群的存在能很大程度上提高系统的稳定性，比如一个MongoDB服务器宕机了，从节点可能立刻补充进来。



1. #### 启动3个不同的mongo服务

   ```shell
   mongod --dbpath mgdata/mongodb/data/ --replSet repset
   mongod --dbpath mgdata/mongodb_slave1/data/ --port 27018 --replSet repset
   mongod --dbpath mgdata/mongodb_slave2/data/ --port 27019 --replSet repset
   
   
   mongod --dbpath mgdata/mongodb_slave1/data/ --port 27018 --replSet repset
   mongod --dbpath mgdata/mongodb_slave2/data/ --port 27019 --replSet repset
   mongod --dbpath mgdata/mongodb/data/ --port 27016 --replSet repset
   ```

2. #### 初始化副本集

   ```shell
   mongo
   user admin
   config = {_id:"repset", members:[
       {_id:0, host:"127.0.0.1:27017"},
       {_id:1, host:"127.0.0.1:27018"},
       {_id:2, host:"127.0.0.1:27019"},
   ]}
   
   # 初始化配置
   rs.initiate(config)
   
   # 查看节点信息
   
   ```

3. #### 测试自动同步

   ```shell
   use test;
   db.testdb.insert({"test":"testslave"})
   ```

4. #### 终止主节点连接，切换至从节点

   ```shell
   mongo 127.0.0.1:27018
   use test
   show tables
   db.getMongo().setSlaveOk()
   db.testdb.find()
   ```
