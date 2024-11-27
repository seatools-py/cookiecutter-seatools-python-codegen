import os
from typing import Optional


def _dfs_find_project_dir(place: str):
    check_files = [place + os.sep + 'pyproject.toml', place + os.sep + 'requirements.txt']
    if any([file for file in check_files if os.path.exists(file)]):
        return place
    parent = os.path.dirname(place)
    if place == parent:
        return None
    return _dfs_find_project_dir(parent)


def find_project_dir(place: str) -> Optional[str]:
    """查找项目目录的绝对路径, 若找不到则返回None."""
    assert place, '当前路径未识别'
    return _dfs_find_project_dir(place)


def find_package_dir(project_dir: str) -> Optional[str]:
    """查询项目的包路径, 若找不到则返回None."""
    assert project_dir, '项目路径无法识别'
    import toml
    with open(project_dir + os.sep + 'pyproject.toml', 'r', encoding='utf-8') as f:
        config = toml.load(f)
    package_name = config['tool']['coverage']['run']['source'][0]
    package_dir = project_dir + os.sep + 'src' + os.sep + package_name
    if os.path.exists(package_dir):
        return package_dir
    return None

