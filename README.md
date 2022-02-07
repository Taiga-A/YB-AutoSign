# README

YB Network Project  -  易班网络计划

* python



## Start

**NumPy**

``` shell
 $ pip install numpy
```

对图像（验证码）矩阵的处理，以及PIL库的依赖



**Pillow**

``` shell
$ pip install Pillow
```

图像（验证码）处理，编码等



**Requests**

``` shell
$ pip install requests
```

网络请求



**Baidu AI**

[文字识别OCR (baidu.com)](https://cloud.baidu.com/doc/OCR/s/zk3h7xw5e)



**Setting**

在 Config 中 编辑您的信息 ！！！！！

> 签到内容为处理后的发送数据 
>
> loginData 为原始的登录发送数据
>
> 上面呢个解析了半天，下边呢个直接摆烂（我是懒🥚）
>
> Baidu AI 需要自己创建服务，OCR文字识别-高精度版 免费500次/天（标准版5万次，验证码预处理得好也非常好用） 



**Start**

``` shell
$ python main.py
```





## Accomplish

> 实现方式



### 农大预处理

1. 使用账户密码自动登录易班，获取 `access_token` 	`https_waf_cookie`
2. 使用上述的两个凭证获取 `cookie`
3. 使用 `cookie` 访问易班的农大跳转页，自动重定向到农大页面
4. 使用易班 `cookie` 获取农大 `Token`
5. 使用 `Token` 获取农大 `cookie`



###  百度AI预处理

6. 使用 `BaiduAI` 的API Key 和 Secret Key 获取 Baidu `Token`



### 自动签到逻辑

7. 使用农大 `cookie` 获取验证码
7. 使用 `numpy`库对验证码进行去噪处理，具体实现参考[岛屿的最大面积 ](https://leetcode-cn.com/problems/max-area-of-island/)  （必要 ！ 否则成功率下降 90% ）

​                                               ![原图](https://taiga-a-1304851750.cos.ap-beijing.myqcloud.com/others/oldCode_01.png)      ----处理---->    ![处理](https://taiga-a-1304851750.cos.ap-beijing.myqcloud.com/others/newCode_01.png)



9. 使用 Baidu `Token` 调用文字识别接口
10. 使用农大 `cookie` 发送验证码和登录信息， 若验证码错误 返回第 7 步 (max:10)
11. 签到完成



## Suggestion

放置服务器，开启定时任务，然后睡着觉把到签了😃

