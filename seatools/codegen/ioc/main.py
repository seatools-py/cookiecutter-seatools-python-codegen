import os
from os.path import dirname

import click
from loguru import logger
from typing import Optional

from seatools.codegen.ioc import generate_app
from .common import extract_names
from .cmd import generate_cmd
from .django import generate_django
from .fastapi import generate_fastapi
from .flask import generate_flask
from .grpc import generate_grpc
from .scrapy import generate_scrapy, generate_scrapy_spider
from .task import generate_task
from ..utils import find_project_dir, find_package_dir


def _extract_project_package_dir(project_dir, package_dir):
    project_dir = project_dir or find_project_dir(os.getcwd())
    if not project_dir:
        logger.error('无法找到项目目录')
        exit(1)
    package_dir = package_dir or find_package_dir(project_dir)
    if not package_dir:
        logger.error('无法找到包目录')
        exit(1)
    logger.info("项目目录: {}", project_dir)
    logger.info("包目录: {}", package_dir)
    return project_dir, package_dir


def _extract_package_app_dir(package_dir, app):
    if not app:
        return package_dir
    return dirname(package_dir) + os.sep + '_'.join(extract_names(app))


@click.group()
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main() -> None:
    """代码生成命令行工具"""
    pass


@main.command()
@click.argument('app')
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='主包目录, 若不传则基于项目目录自动检索')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def startapp(app: str,
             project_dir: Optional[str] = None,
             package_dir: Optional[str] = None,
             override: Optional[bool] = False) -> None:
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    logger.info("开始生成应用[{}]模板代码", app)
    generate_app(project_dir=project_dir, package_dir=package_dir, override=override,
                 app_name=app)
    logger.info("生成应用[{}]模板代码完成", app)


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--docker', is_flag=True, default=False, help='是否生成Dockerfile文件, 默认: false')
@click.option('--docker_compose', is_flag=True, default=False,
              help='是否生成Dockerfile文件和docker-compose配置, 默认: false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def fastapi(project_dir: Optional[str] = None,
            package_dir: Optional[str] = None,
            override: Optional[bool] = False,
            app: Optional[str] = None,
            docker: Optional[bool] = False,
            docker_compose: Optional[bool] = False) -> None:
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    logger.info('开始生成[fastapi]模板代码')
    generate_fastapi(project_dir=project_dir, package_dir=package_dir, override=override,
                     docker=docker,
                     docker_compose=docker_compose,
                     app=app)
    logger.success('生成[fastapi]模板代码完成')


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--docker', is_flag=True, default=False, help='是否生成Dockerfile文件, 默认: false')
@click.option('--docker_compose', is_flag=True, default=False,
              help='是否生成Dockerfile文件和docker-compose配置, 默认: false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def flask(project_dir: Optional[str] = None,
          package_dir: Optional[str] = None,
          override: Optional[bool] = False,
          app: Optional[str] = None,
          docker: Optional[bool] = False,
          docker_compose: Optional[bool] = False):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    logger.info('开始生成[flask]模板代码')
    generate_flask(project_dir=project_dir, package_dir=package_dir, override=override,
                   docker=docker,
                   docker_compose=docker_compose,
                   app=app)
    logger.success('生成[flask]模板代码完成')


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--task_class', '--class', '--module_name', '--module', default=None,
              help='任务类名, 支持驼峰、下划线名称解析, 生成的文件名下划线分隔, 类名驼峰, 例如: HelloWorld, 生成task模板时必填该参数')
@click.option('--task_name', '--name', default="默认任务", help='任务名称, 中英文任务描述, 默认值: 默认任务')
@click.option('--is_async', '--async', is_flag=True, default=False, help='是否创建异步任务, 默认false')
@click.option('--cmd', is_flag=True, default=False, help='是否生成对应的命令行入口')
@click.option('--docker', is_flag=True, default=False,
              help='cmd参数为true时该参数生效, 是否生成Dockerfile文件, 默认: false')
@click.option('--docker_compose', is_flag=True, default=False,
              help='cmd参数为true时该参数生效, 是否生成Dockerfile文件和docker-compose配置, 默认: false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def task(project_dir: Optional[str] = None,
         package_dir: Optional[str] = None,
         override: Optional[bool] = False,
         app: Optional[str] = None,
         task_class: Optional[str] = None,
         task_name: Optional[str] = "默认任务",
         is_async: Optional[bool] = False,
         cmd: Optional[bool] = False,
         docker: Optional[bool] = False,
         docker_compose: Optional[bool] = False) -> None:
    if not task_class:
        logger.error('[--task_class]参数不能为空')
        return
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    generate_task(project_dir=project_dir, package_dir=package_dir,
                  task_class=task_class, task_name=task_name,
                  override=override, is_async=is_async, cmd=cmd,
                  docker=docker, docker_compose=docker_compose)


@main.group()
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy():
    pass


@scrapy.command('init')
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy_init(project_dir: Optional[str] = None,
                package_dir: Optional[str] = None,
                override: Optional[bool] = False,
                app: Optional[str] = None):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    generate_scrapy(project_dir=project_dir, package_dir=package_dir, override=override,
                    app=app)


@scrapy.command('genspider')
@click.argument('name')
@click.argument('domain')
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--docker', is_flag=True, default=False, help='是否生成Dockerfile文件, 默认: false')
@click.option('--docker_compose', is_flag=True, default=False,
              help='是否生成Dockerfile文件和docker-compose配置, 默认: false')
@click.help_option('-h', '--help', help='查看命令帮助')
def scrapy_genspider(name: str,
                     domain: str,
                     project_dir: Optional[str] = None,
                     package_dir: Optional[str] = None,
                     override: Optional[bool] = False,
                     app: Optional[str] = None,
                     docker: Optional[bool] = False,
                     docker_compose: Optional[bool] = False):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    generate_scrapy_spider(project_dir=project_dir, package_dir=package_dir,
                           name=name, domain=domain, override=override,
                           docker=docker,
                           docker_compose=docker_compose,
                           app=app)


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--docker', is_flag=True, default=False, help='是否生成Dockerfile文件, 默认: false')
@click.option('--docker_compose', is_flag=True, default=False,
              help='是否生成Dockerfile文件和docker-compose配置, 默认: false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def django(project_dir: Optional[str] = None,
           package_dir: Optional[str] = None,
           override: Optional[bool] = False,
           app: Optional[str] = None,
           docker: Optional[bool] = False,
           docker_compose: Optional[bool] = False):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    generate_django(project_dir=project_dir,
                    package_dir=package_dir,
                    override=override,
                    docker=docker,
                    docker_compose=docker_compose,
                    app=app)


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option('--name', default=None, help='cmd命令名称, 使用poetry run {name} 执行生成的命令, 必填')
@click.option("--app", default=None, help='startapp创建的应用名, 主应用无需填写')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.option('--docker', is_flag=True, default=False, help='是否生成Dockerfile文件, 默认: false')
@click.option('--docker_compose', is_flag=True, default=False,
              help='是否生成Dockerfile文件和docker-compose配置, 默认: false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def cmd(name: str,
        project_dir: Optional[str] = None,
        package_dir: Optional[str] = None,
        app: Optional[str] = None,
        override: Optional[bool] = False,
        docker: Optional[bool] = False,
        docker_compose: Optional[bool] = False):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    package_dir = _extract_package_app_dir(package_dir, app)
    if not name:
        logger.error('[--name]参数不能为空')
        return
    generate_cmd(project_dir=project_dir,
                 package_dir=package_dir,
                 override=override,
                 command=name,
                 docker=docker,
                 docker_compose=docker_compose,
                 app=app)


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option("--name", default=None,
              help='protobuf文件名称, proto文件仅支持在src/proto目录下, 例如存在xxx.proto, 则name应该传递xxx, 若不传递该参数, 则默认将src/proto目录下所有proto文件一起生成')
@click.option("--pyi", is_flag=True, default=False, help='是否生成pyi文件, 默认false不生成')
@click.option('--override', is_flag=True, default=False,
              help='是否覆盖代码, 不建议覆盖, 若要覆盖请确认覆盖代码是否对业务存在影响, 默认false')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def grpc(project_dir: Optional[str] = None,
         package_dir: Optional[str] = None,
         name: Optional[str] = None, pyi: Optional[bool] = False, override: Optional[bool] = False):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    proto_dir = project_dir + os.sep + 'src' + os.sep + 'proto'
    if not os.path.exists(proto_dir):
        logger.error("proto目录[{}]不存在, 无法生成pb2代码".format(proto_dir))
        return
    if not name:
        import glob
        names = [file.replace('.proto', '').split(os.sep)[-1] for file in glob.glob(os.path.join(proto_dir, '*.proto'))]
    else:
        names = [name]

    for name in names:
        generate_grpc(project_dir, package_dir, override, name, pyi=pyi)
        # 仅第一次需要override, 防止多次重复override
        override = False


if __name__ == "__main__":
    main()
