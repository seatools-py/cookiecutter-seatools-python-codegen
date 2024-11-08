@REM 安装依赖
pip install twine setuptools
@REM 安装
python setup.py sdist bdist_wheel
@REM 上传
twine upload dist/*
