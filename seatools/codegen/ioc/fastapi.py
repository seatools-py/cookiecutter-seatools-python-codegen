import os
from typing import Optional

from .common import mkdir, create_file, add_poetry_script, add_docker_compose_script, unwrapper_dir_name, str_format


def generate_fastapi(project_dir: str, package_dir: str, override: bool = False,
                     docker: Optional[bool] = True,
                     docker_compose: Optional[bool] = True,
                     *args, **kwargs):
    """生成fastapi模板代码

    Args:
        project_dir: 项目目录
        package_dir: 包目录
        override: 是否覆盖文件
        docker: 是否生成docker相关文件
        docker_compose: 是否生成docker-compose相关文件
    """
    project_name = unwrapper_dir_name(project_dir)
    package_name = unwrapper_dir_name(package_dir)

    def gen_fastapi_dir():
        """生成fastapi目录"""
        fastapi_dir = package_dir + os.sep + 'fastapi'
        fastapi_init_py = fastapi_dir + os.sep + '__init__.py'
        fastapi_app_py = fastapi_dir + os.sep + 'app.py'
        fastapi_exception_handler_py = fastapi_dir + os.sep + 'exception_handler.py'
        mkdir(fastapi_dir)
        create_file(fastapi_init_py, override=override)
        create_file(fastapi_exception_handler_py, '''from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from seatools.models import R
from loguru import logger


def wrapper_exception_handler(app: FastAPI) -> FastAPI:
    """给FastAPI对象增加通用异常处理

    Args:
          app: fastapi 应用程序对象
    Returns:
        fastapi 应用程序对象, 封装部分异常处理
    """

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request, exc: RequestValidationError):
        logger.warning('发生请求参数校验异常, {}', exc)
        return PlainTextResponse(R.fail(msg='参数校验不通过', code=400).model_dump_json())

    @app.exception_handler(AssertionError)
    async def assert_exception_handler(request, exc):
        logger.warning('发生断言异常, {}', exc)
        return PlainTextResponse(R.fail(msg=str(exc)).model_dump_json())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        logger.error('发生http异常, {}', exc)
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

    @app.exception_handler(404)
    async def exception_404_handler(request, exc):
        logger.warning('[404]请求不存在的路径, {}', request.url.path)
        return PlainTextResponse(R.fail(msg='资源不存在', code=404).model_dump_json())

    @app.exception_handler(Exception)
    async def exception_handler(request, exc):
        logger.error('发生未知异常, {}', exc)
        return PlainTextResponse(R.fail(msg='内部服务器错误').model_dump_json())

    return app
''', override=override)
        create_file(fastapi_app_py, str_format("""from fastapi import FastAPI
from ${package_name}.fastapi.exception_handler import wrapper_exception_handler
from seatools.models import R
from ${package_name}.config import cfg
from ${package_name}.boot import start
from ${package_name} import utils
from seatools.env import get_env
from seatools.logger.setup import setup_loguru, setup_logging, setup_uvicorn
from loguru import logger

# 启动项目依赖
start()

# 设置日志文件
setup_loguru(utils.get_log_path('${project_name}.log'), extra={'project': cfg().project_name, 'label': 'fastapi'})
setup_logging(utils.get_log_path('${project_name}.sqlalchemy.log'), 'sqlalchemy', extra={'project': cfg().project_name, 'label': 'fastapi'})
setup_uvicorn(utils.get_log_path('${project_name}.uvicorn.log'), extra={'project': cfg().project_name, 'label': 'fastapi'})
app = FastAPI(
    title='${project_name}',
    version='1.0',
    # 正式环境不显示/docs, 非正式环境才显示
    docs_url=None if get_env().is_pro() else '/docs',
)


@app.get('/')
def hello():
    logger.info('Hello ${project_name} by FastAPI!')
    return R.ok(data='Hello ${project_name} by FastAPI!')


# 异常处理
app = wrapper_exception_handler(app)
""", package_name=package_name, project_name=project_name), override=override)
        routers_dir = fastapi_dir + os.sep + 'routers'
        router_init_py = routers_dir + os.sep + '__init__.py'
        mkdir(routers_dir)
        create_file(router_init_py, override=override)

    def gen_fastapi_cmd():
        """生成fastapi命令行工具"""
        cmd_dir = package_dir + os.sep + 'cmd'
        fastapi_cmd_main_py = cmd_dir + os.sep + 'fastapi_main.py'
        create_file(fastapi_cmd_main_py, str_format('''import os
import sys
import multiprocessing
import click
from loguru import logger
from ${package_name}.config import cfg
from seatools.logger.setup import setup_loguru, setup_uvicorn, setup_logging
from ${package_name} import utils
from seatools.env import get_env
from typing import Optional
from ${package_name}.boot import start
import uvicorn


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.option('--host', default='127.0.0.1', help='服务允许访问的ip, 若允许所有ip访问可设置0.0.0.0')
@click.option('--port', default=8000, help='服务端口')
@click.option('--workers', default=1, help='工作进程数')
@click.option('--reload', default=None, help='是否热重启服务器, 默认情况下dev环境开始热重启, test与pro环境不热重启, true: 开启, false: 不开启')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         host: Optional[str] = '127.0.0.1',
         port: Optional[int] = 8000,
         workers: Optional[int] = 1,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO',
         reload: Optional[bool] = None) -> None:
    """FastAPI cmd."""
    # 如果是pyinstaller环境, 先把当前路径设置为执行路径, 以便于无参运行
    if utils.is_pyinstaller_env():
        os.environ['PROJECT_DIR'] = os.path.dirname(sys.executable)
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    if reload is None:
        reload = get_env().is_dev()

    # 启动项目依赖
    start()

    file_name = cfg().project_name + '.' + os.path.basename(__file__).split('.')[0]
    setup_loguru(utils.get_log_path('{}.log'.format(file_name)), level=log_level, extra={'project': cfg().project_name, 'label': 'fastapi'})
    setup_logging(utils.get_log_path('{}.sqlalchemy.log'.format(file_name)), 'sqlalchemy', level=log_level, extra={'project': cfg().project_name, 'label': 'fastapi'})
    setup_uvicorn(utils.get_log_path('{}.uvicorn.log'.format(file_name)), level=log_level, extra={'project': cfg().project_name, 'label': 'fastapi'})
    logger.info('运行成功, 当前项目: {}', cfg().project_name)
    uvicorn.run('${package_name}.fastapi.app:app', host=host, port=port, workers=workers, reload=reload)


if __name__ == "__main__":
    # windows 多进程需要执行该方法, linux 与 mac 执行无效不影响
    multiprocessing.freeze_support()
    main()
''', package_name=package_name), override=override)
        add_poetry_script(project_dir, str_format(
            'fastapi = "${package_name}.cmd.fastapi_main:main"',
            package_name=package_name,
        ))

        bin_dir = project_dir + os.sep + 'bin'
        bin_file = bin_dir + os.sep + 'fastapi.sh'
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
pids=$(pgrep -f '${project_name}/venv/bin/fastapi')
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
pids=$(pgrep -f '${project_name}-[A-Za-z0-9_\\\\-]*-py3.[0-9]+/bin/fastapi')
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
nohup poetry run fastapi --host 0.0.0.0 --port 8000 --env pro --workers 4 >> /dev/null 2>&1 &
echo "执行成功"
echo "退出虚拟环境"
deactivate
''', project_name=project_name), override=override)
        if docker or docker_compose:
            dockerfile_file = project_dir + os.sep + 'fastapi.Dockerfile'
            create_file(dockerfile_file, '''FROM python:3.9

WORKDIR /app

COPY . /app

# 系统时区改为上海
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

RUN poetry lock

RUN poetry install --only main

RUN poetry add fastapi uvicorn[standard]

CMD ["poetry", "run", "fastapi", "--env", "pro", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
''', override=override)

        if docker_compose:
            add_docker_compose_script(project_dir, str_format('''  fastapi:
    container_name: ${project_name}_fastapi
    build:
      context: .
      dockerfile: fastapi.Dockerfile
    image: ${project_name}_fastapi:latest
    volumes:
      - ".:/app"
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
''', project_name=project_name))

    gen_fastapi_dir()
    gen_fastapi_cmd()
