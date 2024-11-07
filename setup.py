#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    此脚本用于 py 打包和分发工具 `setuptools`。

    主要用来定义如何【安装】和【分发】此 py 项目。

    (
        `setuptools` 是 py 的一个库，它旨在简化打包和分发 py 项目的过程。

        `setuptools` 库官方文档地址：
        【https://setuptools.pypa.io/en/latest/】

        `setuptools` 提供一系列命令和工具，使开发者能够轻松创建可重用的 py 包，
        并管理它们的依赖关系、版本、发布等。

        `setuptools` 是 `distutils` 的增强版，它在原有基础上增加许多新特性和功能。

        它由 `PEP 517` 和 `PEP 518` 标准支持，该标准定义 py 项目的构建要求。

            (
                `PEP 517` 官方文档地址：【https://peps.python.org/pep-0517/】
                `PEP 518` 官方文档地址：【https://www.python.org/dev/peps/pep-0518/】
            )

        随着时间推移，`setuptools` 已经成为 py 包创建和管理的事实标准。

        `setuptools` 库主要功能：
            - 安装包：允许用户安装和卸载 py 包。

            - 依赖关系管理：自动处理包依赖项，并确保在安装包时自动下载需要的依赖包。

            - 打包和分发：提供工具来轻松打包 py 代码，并将其分发给其他用户。
              这通常是通过创建 `.egg` 或 `.wheel` 文件完成的。

            - 版本管理：确保可以为软件包指定版本号以及在需要时指定最小或确切的依赖版本。

            - 扩展构建：针对一些需要编译 C 语言扩展等复杂情况提供支持。

            - 测试支持：集成设置测试套件并运行测试用例的能力。

            - 生成脚本：允许自动创建可以调用软件包中函数的命令行脚本。

            - 声明性配置：使用 `setup.cfg` 或 `pyproject.toml` 文件对项目进行配置，
              而不是全部通过编写 `setup.py` 脚本来完成。

        使用 `setuptools` 创建一个新项目一般会涉及以下步骤：
            - 创建 `setup.py` 文件，在其中定义项目信息
              （比如项目名、版本、描述等）以及任何相关依赖项。

            - 可选地使用其他配置文件如 `setup.cfg` 或
              `pyproject.toml` 来进一步细化设置（例如定义元数据或选项）。

            - 使用 `setuptools` 提供的命令
              （如 `python setup.py sdist bdist_wheel`）来打包项目。

        随着 py 包管理器 pip 的成熟以及 `wheel` 格式的广泛接受，
        现代 py 打包流程往往更倾向于使用这些工具而非直接操作 `setuptools`。

        不过，`setuptools` 仍然是整个生态系统中一个非常重要且不可或缺的组成部分。
    )

    注意：本文档中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import os
from setuptools import setup, find_packages


def read_requirements():
    """
        读取【项目根目录】下的 `requirements.txt` 文件
        并提取所有依赖项。

        如果文件存在，则打开并按行读取，
        去除每行末尾的空白字符后返回一个列表；
        如果文件不存在，则返回一个空列表。

    :return:
    """
    requirements_path = "requirements.txt"
    if not os.path.exists(requirements_path):
        return []
    with open(
            file=requirements_path,
            mode="r",
            encoding="utf-8"
    ) as reqs_file:
        reqs = [
            req.strip()
            for req in reqs_file.readlines()
        ]
        return reqs


def read_long_description():
    """
        读取【项目根目录】下的 `README.rst` 文件
        并提取完整的长描述文本。

        如果文件存在，则打开并读取文件内容，
        作为长描述文本返回；
        如果文件不存在，则返回一个空字符串。

    :return:
    """
    readme_path = "README.rst"
    if not os.path.exists(readme_path):
        return ""
    with open(
            file=readme_path,
            mode="r",
            encoding="utf-8"
    ) as desc_file:
        long_description = desc_file.read()
        return long_description


setup(
    # 指定包的【名称】
    # 在 `PyPI` 或其他索引服务器上应该是唯一的
    name="wxapis",
    # 给出包的【简短描述】
    description="企业微信服务端 API 操作库。",
    # 提供一个【详细描述】
    long_description=read_long_description(),
    # 指定包描述的【内容类型】
    # 指出包的长描述（long description）是
    # 用 `reStructuredText` 格式编写的
    long_description_content_type="text/x-rst",
    # 指定项目的【主页链接】
    # 通常是指向项目的【官方仓库】或者专门为该项目建立的【网站】
    url="https://github.com/gary714/wxapis",
    # 声明项目使用的【许可证】
    # "MIT" 表示该软件包采用 `MIT` 许可证
    # 这是一种宽松的【开源许可证】
    # 允许人们自由地使用、复制、修改和发布软件
    license="MIT",
    # 指定软件包的【作者名称】
    author="gary",
    # 指定作者的【电子邮件地址】
    author_email="mepmb@sina.com",
    # 用于分类和标记包
    # `PyPI` 使用它们来组织和搜索包
    classifiers=[
        # 表明软件包采用一个被开源倡议
        # （Open Source Initiative, OSI）认可的 `MIT` 许可证
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    # 用于定义一些与包相关联的关键字
    # 以便用户在 `PyPI` 上搜索时能找到这个软件包
    keywords="WeChat,WxWork",
    # 允许提供额外的链接信息
    # 这些链接将会显示在 `PyPI` 的项目页面上
    # 提供给用户额外资源如文档、源代码等参考资料
    project_urls={
        # 项目主页
        "Homepage": "https://github.com/gary714/wxapis",
        # 标明有额外文档资源可以访问
        "Documentation": "https://github.com/gary714/wxapis",
        # 显示源代码所在位置
        "Source": "https://github.com/gary714/wxapis"
    },
    # 明确列出哪些【平台】适用这个软件包
    # 以便用户和自动化工具知道【兼容性信息】
    platforms=["Linux", "Windows"],
    # 定义映射字典
    # 告诉 `setuptools` 在哪里找到
    # 【源代码文件】来构建 py 包
    # 字典中的【键】是【包名称】，【空字符】串键表示【根包】
    # 【值】是相应【源代码所在目录路径】
    # "." 表示【当前目录】
    package_dir={"": "."},
    # 使用 `setuptools` 提供的 `find_packages()` 函数
    # 自动查找并包含所有应该被打包为部分安装包的子目录
    # （通常是那些含有 `__init__.py` 文件的目录）
    packages=find_packages(),
    # 直接指定【版本号】
    version="1.0.0",
    # 配置涉及到 `setuptools_scm` 插件
    # 它使用源码管理（SCM）系统（如 git）来发现项目版本
    use_scm_version={
        "relative_to": __file__,
        "local_scheme": "no-local-version"
    },
    # 列出在运行时需要满足的【依赖项】
    # 确保在安装此软件之前这些依赖项也将被安装
    install_requires=read_requirements(),
    # `entry_points` 是一种【声明式】方式
    # 来创建【可执行脚本】和【插件系统】
    entry_points={
        # 使用户可以通过【命令行】直接运行某些函数
        # 而不必通过 py 解释器
        "console_scripts": [
            "smsg = wxapis.smsg:main",
        ]
    },
)
