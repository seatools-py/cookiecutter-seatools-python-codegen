import os
from typing import Optional

from .common import mkdir, create_file, add_poetry_script, add_docker_compose_script, unwrapper_dir_name, str_format


def generate_flask(project_dir: str, package_dir: str, override: bool = False,
                   docker: Optional[bool] = False,
                   docker_compose: Optional[bool] = False,
                   app: Optional[str] = None,
                   *args, **kwargs):
    """生成flask模板代码

    Args:
        project_dir: 项目目录
        package_dir: 包目录
        override: 是否覆盖文件
        docker: 是否生成docker相关文件
        docker_compose: 是否生成docker-compose相关文件
        app: 指定应用
    """
    project_name = unwrapper_dir_name(project_dir)
    package_name = unwrapper_dir_name(package_dir)

    def gen_flask_dir():
        """生成flask目录"""
        flask_dir = package_dir + os.sep + 'flask'
        flask_init_py = flask_dir + os.sep + '__init__.py'
        flask_app_py = flask_dir + os.sep + 'app.py'
        mkdir(flask_dir)
        create_file(flask_init_py, override=override)
        create_file(flask_app_py, str_format('''from flask import Flask
from seatools.models import R
from uvicorn.middleware.wsgi import WSGIMiddleware

from ${package_name}.boot import start

# 启动项目依赖
start()

app = Flask(__name__)


@app.get('/')
def hello():
    return R.ok(data='Hello ${project_name} by Flask!').model_dump()


# wsgi 转 asgi
asgi_app = WSGIMiddleware(app)
''', package_name=package_name, project_name=project_name), override=override)

    def gen_flask_cmd():
        """生成flask命令行工具"""
        cmd_dir = package_dir + os.sep + 'cmd'
        flask_cmd_main_py = cmd_dir + os.sep + 'flask_main.py'
        create_file(flask_cmd_main_py, str_format('''import os
import multiprocessing
import click
import uvicorn
from typing import Optional

from ${package_name}.boot import start


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--host', default='127.0.0.1', help='服务允许访问的ip, 若允许所有ip访问可设置0.0.0.0')
@click.option('--port', default=8000, help='服务端口')
@click.option('--workers', default=1, help='工作进程数')
@click.option('--reload', default=None, help='是否热重启服务器, 默认情况下dev环境开始热重启, test与pro环境不热重启, true: 开启, false: 不开启')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         host: Optional[str] = '127.0.0.1',
         port: Optional[int] = 8000,
         workers: Optional[int] = 1,
         reload: Optional[bool] = None) -> None:
    """Flask cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env

    # start ioc
    start()

    # start uvicorn
    uvicorn.run('${package_name}.flask.app:asgi_app', host=host, port=port, workers=workers, reload=reload)


if __name__ == "__main__":
    # windows 多进程需要执行该方法, linux 与 mac 执行无效不影响
    multiprocessing.freeze_support()
    main()
''', package_name=package_name), override=override)

        poetry_script_name = '{}_flask'.format(app) if app else 'flask'

        add_poetry_script(project_dir, str_format(
            '${poetry_script_name} = "${package_name}.cmd.flask_main:main"',
            package_name=package_name, poetry_script_name=poetry_script_name
        ))

        bin_dir = project_dir + os.sep + 'bin'
        bin_file = bin_dir + os.sep + 'flask.sh'
        create_file(bin_file, str_format('''# 获取脚本文件目录
BIN_DIR=$(dirname "$(readlink -f "$0")")
# 获取项目目录
PROJECT_DIR=$(dirname "$BIN_DIR")
echo "当前项目路径: $PROJECT_DIR"
# 进入目录
cd "$PROJECT_DIR"
echo "切换到项目目录: $PROJECT_DIR"
echo "拉取最新项目代码"
git pull
echo "切换虚拟环境"
source venv/bin/activate
echo "开始安装生产环境依赖"
poetry install --only main
echo "安装生产环境依赖完成"
echo "开始检查是否已存在运行中的进程"
pids=$(pgrep -f '${project_name}/venv/bin/flask')
if [ -z "$pids" ]; then
  echo "无正在运行中的进程, 忽略"
else
  # 通过for循环遍历所有进程ID
  for pid in $pids; do
    echo "存在正在运行中的进程: $pid, 即将终止进程..."
    kill "$pid" # 使用引号以确保ID作为参数正确传递
    if [ $? -eq 0 ]; then
      echo "进程: $pid 已被成功终止"
    else
      echo "进程: $pid 终止失败"
    fi
  done
fi
pids=$(pgrep -f '${project_name}-[A-Za-z0-9_\\\\-]*-py3.[0-9]+/bin/flask')
if [ -z "$pids" ]; then
  echo "无正在运行中的进程, 忽略"
else
  # 通过for循环遍历所有进程ID
  for pid in $pids; do
    echo "存在正在运行中的进程: $pid, 即将终止进程..."
    kill "$pid" # 使用引号以确保ID作为参数正确传递
    if [ $? -eq 0 ]; then
      echo "进程: $pid 已被成功终止"
    else
      echo "进程: $pid 终止失败"
    fi
  done
fi
# 执行命令
echo "开始执行命令"
# 执行命令 --workers 工作进程数, 正式环境可根据CPU核数设置
nohup poetry run ${poetry_script_name} --host 0.0.0.0 --port 8000 --env pro --workers 4 >> /dev/null 2>&1 &
echo "执行成功"
echo "退出虚拟环境"
deactivate
''', project_name=project_name, poetry_script_name=poetry_script_name), override=override)

        if docker or docker_compose:
            dockerfile_path = project_dir + os.sep + 'flask.Dockerfile'
            create_file(dockerfile_path, str_format('''FROM python:3.9

WORKDIR /app

COPY . /app

# 系统时区改为上海
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

RUN poetry lock

RUN poetry install --only main

RUN poetry add flask uvicorn[standard]

CMD ["poetry", "run", "${poetry_script_name}", "--env", "pro", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
''', poetry_script_name=poetry_script_name), override=override)

        if docker_compose:
            add_docker_compose_script(project_dir, str_format('''  flask:
    container_name: ${project_name}_flask
    build:
      context: .
      dockerfile: flask.Dockerfile
    image: ${project_name}_flask:latest
    volumes:
      - ".:/app"
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
''', project_name=project_name))

    gen_flask_dir()
    gen_flask_cmd()
