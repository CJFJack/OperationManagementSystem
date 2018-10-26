CMS(Config Manager System: 运维管理平台)
==============================================

[![Build Status](https://img.shields.io/travis/rust-lang/rust.svg)](https://img.shields.io/travis/rust-lang/rust.svg)
[![Python Version](https://img.shields.io/badge/Python--2.7-paasing-green.svg)](https://img.shields.io/badge/Python--2.7-paasing-green.svg)
[![Django Version](https://img.shields.io/badge/Django--1.11.15-paasing-green.svg)](https://img.shields.io/badge/Django--1.11.15-paasing-green.svg)

> CMS现有功能:

- 统计Dashboard
    - 报警统计
    - RDS资源统计
    - ECS资源统计
- 系统管理
    - ECS管理
    - 应用管理
    - 应用族管理
    - SLB管理
- 发布管理
    - 配置管理
    - Jenkins管理
    - 发布申请
- 报警管理

## 部署

### 安装依赖

```
pip install -r requirements.txt
```

### 安装 MySQL 并创建数据库 cms


### 修改配置


MySQL 配置修改 settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cms',
        'USER': 'root',
        'PASSWORD': 'xxxx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


```

阿里云接口认证配置 settings.py:
```
ACCESS_KEY_ID = 'XXXXXXXXXX'
ACCESS_KEY_SECRET = 'XXXXXXXXXXXXXX'

```


Jenkins 配置 settings.py:
```
JENKINS_URL = 'http://jenkins.dev.com'
JENKINS_USER = 'xxxx'
JENKINS_PASS = 'xxxxxx'

```


发布文件生成路径配置 settings.py:
```
DEPLOY_DIR_PATH = r'D:\release'

```

修改允许访问IP settings.py:
```
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

```


### 初始化数据
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default_user

```


### 运行服务器

```
python manage.py runserver 0:8888
```


### 管理员登录

```
访问 http://localhost:8888
默认管理员账号：admin
默认管理员密码：Python@123
```

### 交流
![赞赏](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/wxzs.png)
![微信](https://raw.githubusercontent.com/CJFJack/ConfigManager/master/doc/images/wx.png)

QQ: 398741302

![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_login.png)
![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_alarm_report.png)
![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_rds_report.png)
![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_config_manager.png)
![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_ecs_manager.png)
![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_deploy_apply.png)
![cms](https://raw.githubusercontent.com/CJFJack/OperationManagementSystem/master/doc/images/oms_jenkins_job_manage.png)