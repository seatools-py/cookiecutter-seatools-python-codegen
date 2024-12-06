import os
from os.path import dirname

from .common import mkdir, create_file, str_format, extract_names


def generate_app(project_dir: str, package_dir, app_name: str,
                 override: bool = False):
    """生成一个新的应用.

    Args:
        project_dir: 项目目录
        package_dir: 包目录
        app_name: 应用名称
        override: 是否覆盖文件
    """
    # 获取源码路径
    source_dir = dirname(package_dir)
    app_name = '_'.join(extract_names(app_name))
    package_dir = source_dir + os.sep + package_dir

    def gen_app_dir():
        """生成新应用目录."""
        app_dir = source_dir + os.sep + app_name
        mkdir(app_dir)
        app_init_py = app_dir + os.sep + '__init__.py'
        create_file(app_init_py, override=override)

        boot_dir = app_dir + os.sep + 'boot'
        mkdir(boot_dir)
        boot_init_py = boot_dir + os.sep + '__init__.py'
        create_file(boot_init_py, '''
def start():
    """启动项目前置依赖."""
    from .ioc import ioc_starter
    ioc_starter()

''', override=override)
        boot_ioc_py = boot_dir + os.sep + 'ioc.py'
        create_file(boot_ioc_py, str_format('''from seatools import ioc
from ${package_name}.config import get_config_dir


def ioc_starter():
    # 运行ioc
    ioc.run(scan_package_names=[
        '${package_name}'
    ],
            config_dir=get_config_dir(),
            # 需要过滤扫描的模块, 示例: ${package_name}.xxx
            exclude_modules=[])
''', package_name=app_name), override=override)

        cmd_dir = app_dir + os.sep + 'cmd'
        mkdir(cmd_dir)
        cmd_init_py = cmd_dir + os.sep + '__init__.py'
        create_file(cmd_init_py, override=override)

        config_dir = app_dir + os.sep + 'config'
        mkdir(config_dir)
        config_init_py = config_dir + os.sep + '__init__.py'
        create_file(config_init_py, str_format('''import os


def get_project_dir():
    """获取项目目录, 建议读取的所有文件都从项目目录开始

    Returns:
        项目目录路径
    """
    return os.environ.get('PROJECT_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def get_src_dir():
    """获取包目录, 建议读取的所有代码文件都从该目录开始

    Returns:
        项目代码包目录
    """
    return get_project_dir() + os.sep + 'src'


def get_package_dir():
    """获取默认业务包目录, 建议读取的所有业务包文件都从该目录开始

    Returns:
        默认业务包目录
    """
    return get_src_dir() + os.sep + '${package_name}'


def get_extensions_dir():
    """获取拓展目录"""
    return get_project_dir() + os.sep + 'extensions'


def get_config_dir():
    """获取配置文件目录."""
    return get_project_dir() + os.sep + 'config'
''', package_name=app_name), override=override)

    gen_app_dir()

