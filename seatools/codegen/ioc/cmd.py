import os
from typing import Optional

from .common import mkdir, create_file, extract_names, add_poetry_script, str_format, add_docker_compose_script, \
    unwrapper_dir_name


def generate_cmd(project_dir: str, package_dir: str, override: bool = False,
                 command: str = None,
                 extra_import: Optional[str] = '',
                 extra_run: Optional[str] = '',
                 docker: Optional[bool] = True,
                 docker_compose: Optional[bool] = True,
                 **kwargs):
    """生成poetry cmd命令

    Args:
        project_dir: 项目目录
        package_dir: 包目录
        override: 是否覆盖文件
        command: 命令名称, 生成的cmd命令可使用 poetry run {command} 运行
        extra_import: 生成的cmd需要额外执行的导入
        extra_run: 生成的cmd需要额外执行的逻辑
        docker: 是否生成docker相关文件
        docker_compose: 是否生成docker-compose相关文件
        app: 指定应用
    """
    project_name = unwrapper_dir_name(project_dir)
    package_name = unwrapper_dir_name(package_dir)
    cmd_dir = package_dir + os.sep + 'cmd'
    cmd_init_py = cmd_dir + os.sep + '__init__.py'
    mkdir(cmd_dir)
    # 该文件不覆盖, 防止影响其他逻辑
    create_file(cmd_init_py)
    names = extract_names(command)
    cmd_name = '_'.join(names)
    names.append('main')
    cmd_main_name = '_'.join(names)
    cmd_py = cmd_dir + os.sep + cmd_main_name + '.py'
    create_file(cmd_py, str_format('''import os
import click
from typing import Optional

from ${package_name}.boot import start
${extra_import}

@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev') -> None:
    """${command} cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env

    # start ioc
    start()

    ${extra_run}

if __name__ == "__main__":
    main()
''', package_name=package_name, command=command, extra_import=extra_import, extra_run=extra_run), override=override)
    add_poetry_script(project_dir, str_format('${command} = "${package_name}.cmd.${cmd_main_name}:main"',
                                              package_name=package_name,
                                              command=command,
                                              cmd_main_name=cmd_main_name))
    bin_dir = project_dir + os.sep + 'bin'
    mkdir(bin_dir)
    bin_file = bin_dir + os.sep + cmd_name + '.sh'
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
pids=$(pgrep -f '${project_name}/venv/bin/${command}')
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
pids=$(pgrep -f '${project_name}-[A-Za-z0-9_\\\\-]*-py3.[0-9]+/bin/${command}')
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
poetry run ${command} --env pro >> /dev/null 2>&1
echo "执行成功"
echo "退出虚拟环境"
deactivate
''', project_name=project_name, command=command), override=override)

    if docker or docker_compose:
        dockerfile_file = project_dir + os.sep + cmd_name + '.Dockerfile'
        create_file(dockerfile_file, str_format('''FROM python:3.9

WORKDIR /app

COPY . /app

# 系统时区改为上海
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

RUN poetry lock

RUN poetry install --only main

CMD poetry run ${command} --env pro
''', command=command), override=override)

    if docker_compose:
        add_docker_compose_script(project_dir, str_format('''  ${cmd_name}:
    container_name: ${project_name}_${cmd_name}
    build:
      context: .
      dockerfile: ${cmd_name}.Dockerfile
    image: ${project_name}_${cmd_name}:latest
    volumes:
      - ".:/app"
''', project_name=project_name, cmd_name=cmd_name))
