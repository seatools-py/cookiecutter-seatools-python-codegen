import os
from .common import mkdir, create_file, add_poetry_script, str_format, add_docker_compose_script, unwrapper_dir_name


def generate_django(project_dir: str, package_dir: str, override: bool = False, *args, **kwargs):
    """生成django模板代码"""
    project_name = unwrapper_dir_name(project_dir)
    package_name = unwrapper_dir_name(package_dir)
    name = package_dir.replace('\\', '/').strip('/').split('/')[-1]

    def gen_django_dir():
        """生成django目录"""
        django_dir = package_dir + os.sep + 'django'
        django_init_py = django_dir + os.sep + '__init__.py'
        asgi_py = django_dir + os.sep + 'asgi.py'
        wsgi_py = django_dir + os.sep + 'wsgi.py'
        settings_py = django_dir + os.sep + 'settings.py'
        urls_py = django_dir + os.sep + 'urls.py'
        manage_py = django_dir + os.sep + 'manage.py'
        mkdir(django_dir)
        create_file(django_init_py, override=override)
        create_file(asgi_py, '''"""
ASGI config for {name} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{name}.django.settings')

application = get_asgi_application()
'''.format(name=name), override=override)
        create_file(wsgi_py, '''"""
WSGI config for {name} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{name}.django.settings')

application = get_wsgi_application()
'''.format(name=name), override=override)
        create_file(settings_py, str_format('''"""
Django settings for ${name} project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from ${package_name}.config import get_project_dir

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(get_project_dir())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6!)+gylet!9xxo_)6o^9su**!xz2+e6vpr-ev1=3hjzc60_=v1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '${name}.django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '${name}.django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
''', name=name, project_dir=project_dir, package_name=package_name), override=override)
        create_file(urls_py, '''"""
URL configuration for {name} project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
'''.format(name=name), override=override)
        create_file(manage_py, '''import os
import sys
from typing import List


def run(django_args: List[str]):
    # 启动django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{name}.django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(django_args)


if __name__ == '__main__':
    run(sys.argv)
'''.format(name=name), override=override)

    def gen_django_cmd():
        """生成django cmd命令行工具"""
        cmd_dir = package_dir + os.sep + 'cmd'
        django_cmd_main_py = cmd_dir + os.sep + 'django_main.py'
        create_file(django_cmd_main_py, str_format('''import os
import sys
import click
from loguru import logger
from ${package_name}.logger import setup_loguru, setup_logging
from ${package_name}.config import cfg, get_config_dir
from typing import Optional
from seatools import ioc
from ${package_name}.django.manage import run


@click.command()
@click.option('--project_dir', default=None, help='项目目录, 未打包无需传该参数, 自动基于项目树检索')
@click.option('--env', default='dev', help='运行环境, dev=测试环境, test=测试环境, pro=正式环境, 默认: dev')
@click.option('--log_level', default='INFO',
              help='日志级别, DEBUG=调试, INFO=信息, WARNING=警告, ERROR=错误, CRITICAL=严重, 默认: INFO')
@click.option('--django_args', default='', help='django 运行参数, 例如启动web服务: runserver, 默认空')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO',
         django_args: Optional[str] = '') -> None:
    """Django cmd."""
    if project_dir:
        os.environ['PROJECT_DIR'] = project_dir
    if env:
        os.environ['ENV'] = env
    # 运行ioc
    ioc.run(scan_package_names='${package_name}',
            config_dir=get_config_dir(),
            # 过滤扫描的模块
            exclude_modules=[],
            )
    file_name = cfg().project_name + '.' + os.path.basename(__file__).split('.')[0]
    setup_loguru('{}.log'.format(file_name), level=log_level, label='django')
    setup_logging('{}.sqlalchemy.log'.format(file_name), 'sqlalchemy', level=log_level, label='django')
    setup_logging('{}.django.log'.format(file_name), 'django', level=log_level, label='django')
    logger.info('运行成功, 当前项目: {}', cfg().project_name)
    # 启动django
    django_args_list = [item.strip() for item in django_args.split(' ') if item.strip()]
    # django 基于sys.argv[0]处理, 这里覆盖sys.argv[0]为当前文件来保证poetry正常运行
    sys.argv[0] = __file__
    django_args_list = [sys.argv[0], *django_args_list]
    logger.info('[django]启动参数: {}', django_args_list)
    run(django_args_list)


if __name__ == "__main__":
    main()
''', package_name=package_name), override=override)
        add_poetry_script(project_dir, str_format(
            'django = "${package_name}.cmd.django_main:main"',
            package_name=package_name,
        ))

        bin_dir = project_dir + os.sep + 'bin'
        bin_file = bin_dir + os.sep + 'django.sh'
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
pids=$(pgrep -f '${project_name}/venv/bin/django')
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
pids=$(pgrep -f '${project_name}-[A-Za-z0-9_\\\\-]*-py3.[0-9]+/bin/django')
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
# 执行命令
nohup poetry run django --django_args "runserver 0.0.0.0:8000" --env pro >> /dev/null 2>&1 &
echo "执行成功"
echo "退出虚拟环境"
deactivate
''', project_name=project_name), override=override)

        dockerfile_file = project_dir + os.sep + 'django.Dockerfile'
        create_file(dockerfile_file, str_format('''FROM python:3.9

WORKDIR /app

COPY . /app

# 系统时区改为上海
RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip

RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple poetry

RUN poetry lock

RUN poetry install --only main

RUN poetry add django==4.2.11

CMD ["poetry", "run", "django", "--env", "pro", "--django_args", "runserver 0.0.0.0:8000"]
''', project_name=project_name), override=override)
        add_docker_compose_script(project_dir, str_format('''  django:
    container_name: ${project_name}_django
    build:
      context: .
      dockerfile: django.Dockerfile
    image: ${project_name}_django:latest
    volumes:
      - ".:/app"
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
''', project_name=project_name))

    gen_django_dir()
    gen_django_cmd()
