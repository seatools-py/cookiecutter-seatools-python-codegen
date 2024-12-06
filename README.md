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
```

- 创建一个CMD工具
```shell
# 创建一个CMD, 使用 cookiecutter-seatools-python 主项目包时无需配置--app, 使用新建应用需要传递该值
seatools-codegen.exe cmd --name [命令名称] [--app [应用]]
# 示例
seatools-codegen.exe cmd --name xxx
# poetry运行
poetry run xxx
# linux运行
bash bin/xxx.sh
```

- 生成FastAPI项目模板
```shell
# 生成FastAPI模板, 使用 cookiecutter-seatools-python 主项目包时无需配置--package_dir, 使用新建应用需要传递该值
seatools-codegen.exe fastapi [--app [应用]]

# 运行
```
