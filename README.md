# Cookiecutter-seatools-python-codegen

Cookiecutter-seatools-python 代码生成拓展包

## 仓库地址:
1. https://github.com/seatools-py/cookiecutter-seatools-python-codegen
2. https://gitee.com/seatools-py/cookiecutter-seatools-python-codegen

## Cookiecutter-seatools-python 模板项目地址
1. https://github.com/seatools-py/cookiecutter-seatools-python
2. https://gitee.com/seatools-py/cookiecutter-seatools-python

## Seatools 工具包地址
1. https://github.com/seatools-py/seatools
2. https://gitee.com/seatools-py/seatools

## 安装
安装命令: `poetry add seatools-codegen`
windows工具`seatools-codegen.exe`, linux工具`seatools-codegen`

## 使用示例 （以windows工具为例）
- 创建新应用
```shell
# 创建一个新应用, 单应用项目无需使用, cookiecutter-seatools-python 项目模板自带一个默认的主应用包
seatools-codegen.exe startapp [应用名称]
# 示例
seatools-codegen.exe startapp xxx
# 查看命令帮助
seatools-codegen.exe startapp --help
```

- 创建一个CMD工具
```shell
# 创建一个CMD, 使用 cookiecutter-seatools-python 主项目包时无需配置--app, 使用新建应用需要传递该值
seatools-codegen.exe cmd --name [命令名称]
# 示例
seatools-codegen.exe cmd --name xxx
# poetry运行
poetry run xxx
# linux运行
bash bin/xxx.sh
```

- 创建一个任务
```shell
# 创建一个任务
seatools-codegen.exe task --class xxx_task --name Xxx任务
# 创建异步任务
seatools-codegen.exe task --class async_xxx_task --name Xxx异步任务 --async
# 创建带cmd的任务
seatools-codegen.exe task --class xxx_task --name XXX任务 --cmd
# poetry运行
poetry run xxx_task
# linux运行
bash bin/xxx_task.sh
```

- 生成FastAPI项目
```shell
# 生成FastAPI模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
seatools-codegen.exe fastapi
# 安装依赖
poetry add fastapi uvicorn[standard]
# poetry运行
poetry run fastapi
# linux运行
bash bin/fastapi.sh
```

- 生成Flask项目
```shell
# 生成Flask模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
seatools-codegen.exe fastapi
# 安装依赖
poetry add flask uvicorn[standard]
# poetry运行
poetry run flask
# linux运行
bash bin/flask.sh
```

- 生成Django项目
```shell
# 生成Django模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
seatools-codegen.exe django
# 安装依赖
poetry add django uvicorn[standard]
# poetry运行
poetry run django_runserver
# linux运行
bash bin/django.sh
```

- 生成Scrapy项目
```shell
# 生成Django模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
seatools-codegen.exe scrapy init
# 生成Scrapy爬虫
seatools-codegen.exe scrapy genspider xxx xxx.com
# poetry运行爬虫
poetry run xxx
# linux运行爬虫
poetry run xxx
```
