# setup.py
from setuptools import setup, find_packages

setup(
    name="medicalcontour",  # 包的名称
    version="0.1",  # 包的版本号
    packages=find_packages(),  # 自动发现所有模块
    install_requires=[
        "opencv-python==4.10.0.84",
        "numpy==1.26.4",
        "nibabel==5.3.2",
        "PyQt5==5.15.11",
        "PyQt5-Qt5==5.15.15",
        "PyQt5_sip==12.15.0",
        "matplotlib==3.9.2",
        "scipy==1.10.1"
    ],
    entry_points={
        'console_scripts': [
            'medicalcontour = medicalcontour.main:main',  # 通过命令行调用 main.py 中的 main() 函数
        ],
    },
    include_package_data=True,  # 包含非 Python 文件
    author="Zhiwei Tan",  # 替换为你的名字
    author_email="tanzw1024@gmail.com",  # 替换为你的邮箱
    description="A package for image segmentation and GUI testing",  # 简短描述你的包
    long_description=open('README.md').read(),  # 如果你有 README 文件，使用它
    long_description_content_type="text/markdown",  # 读取 README 文件为 Markdown 格式
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",  # 根据你的 Python 版本选择
        "License :: OSI Approved :: MIT License",  # 你可以选择 MIT 许可证或其他许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定最低 Python 版本
)
