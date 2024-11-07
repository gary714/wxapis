#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    py 的 `abc` 模块提供用于创建【抽象基类】的设施。

    在【面向对象编程】中，一个【抽象基类】
    （Abstract Base Class, ABC）
    定义【子类】应实现的【方法】和【属性】的接口。

    它允许创建【不能被实例化只能被继承】的类。

    这可以【强制子类实现特定方法或属性】，
    是一种确保某些类遵循特定接口或规则的方式。

    下面是 abc 模块中几个主要组件的详细介绍：
        - `ABC`: 这个类是所有【抽象基类】的【父类】，
          它本身就是一个【抽象类】。
          当创建新的【抽象基类】时，应该从 `ABC` 继承。

        - `abstractmethod`: 这是一个【装饰器】，
          用于【表示某个方法是抽象方法】，
          需要由【子类】提供具体实现。
          如果一个方法被标记为【抽象方法】，
          则继承它的抽象基类【不能直接实例化】，
          必须由【子类重写】这个方法后才可实例化。

    举个例子来说明如何使用 `abc.ABC` 和 `abc.abstractmethod`：

        >>> from abc import ABC, abstractmethod
        >>>
        >>>
        >>> class MyBaseClass(ABC):
        >>>     @abstractmethod
        >>>     def do_something(self):
        >>>         pass
        >>>
        >>>
        >>> class MyConcreteClass(MyBaseClass):
        >>>     def do_something(self):
        >>>         return "具体操作"

    注意：本脚本中出现的 "py"，如无特殊说明，则指代 "Python"。
         本脚本中出现的 "token"，如无特殊说明，则指代 "Access Token"。
"""
import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, \
    urlparse, urljoin, urlunparse
import requests

# `__all__` 是一个特殊的列表
# 它定义当从模块执行 `from module import *` 时应该导入哪些属性
# 如果定义了 `__all__`，只有在这个列表中的属性才会被导入
# 如果没有定义 `__all__`，那么默认导入模块中不以下划线开头的所有属性
__all__ = [
    "ApiException",
    "AbstractApis"
]
# 将当前运行的 py 文件所在的上两级目录加入到 py 的【系统路径】中
# 使得在这个【根目录】下的【模块】和【包】可以被当前文件所引用
current_file_path = Path(__file__).absolute()
# 移动到上两级目录以获取【根路径】
root_path = current_file_path.parent.parent
# 将【根路径】作为【系统路径】加入 `sys.path`
sys.path.append(str(root_path))

# 在 py 代码中，`PEP 8` 是一个【编码风格指南】
# 其中 `E402` 错误意味着【模块级别的导入语句没有出现在文件的顶部】
# 对于某个特定的行，可以在该行末尾添加一个特殊的注释
# 来告诉 linter 忽略 `E402` 错误
# 即使用 `# noqa: E402` 告诉代码检查工具忽略此行上的 `E402` 错误
from wxapis import WXWORK_API_BASE_URL  # noqa: E402


def add_qs(url: str, params: dict) -> str:
    """
        `qs` 代表 `query string`。

        `add_qs` 意即
        "Add query string(params) to url and return it."

        将查询参数添加到 URL 中并返回修改后的 URL 字符串。

        示例:
            假设 `url` 为 "http://www.example.com/"，
            `params` 为 { "key1": "value1", "key2": "value2" }，
            函数将返回
            "http://www.example.com?key1=value1&key2=value2"。

    :param url: (str): 需要添加查询参数的基础 URL。
    :param params: (dict): 需要添加到 URL 查询字符串的参数字典。
    :return: (str): 添加查询参数后的完整 URL 字符串。
    """
    if not params:
        return url
    # 【解析原始 URL】：
    # 传入的 URL 最终解析为如下结构：
    # ParseResult(
    # scheme="https",
    # netloc="qyapi.weixin.qq.com",
    # path="/cgi-bin/gettoken",
    # params="",
    # query="",
    # fragment=""
    # )
    parsed_url = urlparse(url)
    # 将【新参数】和【原有查询参数】合并
    query_params = dict(parse_qsl(parsed_url.query))
    query_params.update(params)
    # 重新组合 URL 并返回
    # 使用 `urlunparse` 方法
    final_url = urlunparse(
        (
            # 代表 URL 的方案（协议）
            # 例如 "http" 或 "https"
            parsed_url.scheme,
            # 代表【网络位置】
            # 通常包括【域名】和可能的【端口】
            # 例如 "www.example.com:80"
            parsed_url.netloc,
            # 服务器上资源的路径
            # 例如 "/index.html"
            parsed_url.path,
            # 包含附加到路径后面用分号隔开的参数
            # 不过这个部分不是所有的 URL 都有
            # 并且不如查询字符串（`query string`）常用
            parsed_url.params,
            # 通过 `urlencode` 方法将 `query_params` 字典
            # 转换为一个适合 URL 查询字符串格式的字符串
            # 例如，如果 `query_params` 是
            # { "key1": "value1", "key2": "value2" }
            # 则转换后为 "key1=value1&key2=value2"
            urlencode(query_params),
            # URL 中的片段部分，也称为锚点（anchor）
            # 通常用于直接定位到页面内部某个特定位置
            # 它位于井号（#）之后，例如 "#section1"
            parsed_url.fragment
        )
    )
    return final_url


class ApiException(Exception):
    """
        `ApiException` 类是一个【自定义异常类】。

        它的作用是在 API 调用过程中提供一种【标准化】的【错误处理】方法：
           - 当 API 调用发生错误时，可以通过抛出 `ApiException` 实例
             来通知调用者具体的错误情况。
             它继承 py 内置的 `Exception` 基类，
             这意味着 `ApiException` 是一个完整意义上的异常类型，
             可以被【捕获】和【处理】，就像处理任何其他内置异常一样。

           - 通过在异常类中定义 `err_code` 和 `err_msg` 属性，
             可以非常方便地访问到【错误码】和【错误信息】。
             这通常是与第三方 API 交互时非常有用的功能，
             因为【第三方服务】会返回特定的【错误码】和【描述信息】来表示不同类型的错误。

        py 中的异常基类 `Exception` 是所有【内置非系统退出异常类】的基类。

            (
                它是用户定义异常的基础。

                当 py 脚本遇到错误时，它会引发一个异常，
                如果这个异常没有被【处理】或【捕获】，那么程序将终止并显示错误信息。

                `Exception` 类是从一个更基础的类 `BaseException` 继承而来。

                不过，对于大多数应用程序来说，应该从 `Exception` 类【派生自定义异常子类】，
                而不是从 `BaseException` 派生。

                下面是一些关键点：
                    - 当程序运行时出现错误，py 都会抛出一个异常。

                    - 用户可以通过继承 `Exception` 类来定义自己的异常类型。

                    - 异常对象通常包含有关错误的描述信息（存储在其参数中）。

                    - 捕获和处理异常使用 `try...except` 语句块。

                    - 使用 `raise` 关键字抛出自定义或内置的异常。

                下面是使用 py 异常的一个简单例子：

                    >>> try:
                    >>>     # 可能引发异常的代码
                    >>>     result = 10 / 0
                    >>> except ZeroDivisionError as e:
                    >>>     # 捕获到了 Exception 或其子类之一所代表的任何异常
                    >>> print(f"An error occurred: {e}.")

                在上面的代码中，尝试执行除以零操作（它会引发一个 `ZeroDivisionError`），
                这个错误是 `Exception` 的子类。

                因此，在 `except ZeroDivisionError as e:` 块中捕获这个错误，
                并打印出一条错误消息。

                总结来说，py 中的 `Exception` 是标准库中
                所有【非系统退出类别错误】和【用户自定义异常类型】的基础，
                并且它提供一种结构化处理程序运行时问题的方式。
            )
    """

    def __init__(self, err_code: int, err_msg: str):
        """
            此构造函数用于创建一个包含【错误代码】和【错误信息】的对象。

        :param err_code: 错误代码，一个【整数】表示特定的【错误类型】。
        :param err_msg: 错误信息，一个【字符串】描述错误的【详细信息】。
        """
        self.err_code = err_code
        self.err_msg = err_msg

    def __str__(self):
        """
             创建对象的【字符串表示】，包含【错误信息】。

             此方法用于生成对象的【非正式字符串表示形式】，
             通常用于【打印】和【日志记录】。

             输出格式包括【错误码】和【错误消息】。

        :return: 格式化的字符串，
        显示红色的错误信息及其对应的错误码和错误消息。
        """
        return f"\033[31m错误信息" \
               f"[<错误码>：{self.err_code}, " \
               f"<错误消息>：{self.err_msg}]\033[0m"


class AbstractApis(ABC):
    """
        定义一个名为 `AbstractApis` 的【抽象基类】，
        它使用 py 的 ABC(Abstract Base Classes) 模块来创建。

        `ABC` 模块用于定义抽象基类，这是一种【不能实例化】
        (不能创建对象)的特殊类型的类，通常用作其他类的【基础模板】。

        在 `AbstractApis` 类中，使用 `@abstractmethod` 装饰器
        来标记一系列方法为【抽象方法】。

        这意味着任何继承 `AbstractApis` 的子类都必须实现这些方法才能实例化。

        如果子类没有完全实现这些抽象方法，则它也将成为一个抽象类，不能被实例化。

        代码中定义的方法大多都是与【访问令牌】(token)相关的操作。

            (
                在应用程序与第三方服务交互时，
                通常需要使用【访问令牌】来【验证身份】和【授权请求】。

               以下是抽象方法的主要作用：
                   【企业内部开发】：
                   面向【企业内部开发人员】或【行业】定制 ISV，通过开放接口与【企业内部系统】实现对接，
                   满足企业【个性化需求】。
                       - `get_token()`: 应当被重写以【返回】当前有效的【访问令牌】。

                通过将这些操作定义为抽象方法，该类【强制任何子类都必须提供这些功能】。

                对于不同类型的 API 访问方式或第三方服务，
                具体如何获取和刷新令牌可能有所不同；
                因此将它们作为抽象方法留给具体子类去实现更合适。
            )

        关于类中涉及到的私有方法：
            - 私有属性/方法只是一种【约定】，
              通过命名来提示其他程序员该属性/方法【不应从外部直接访问】。

            - 真正使其 "私有" 的是【名称改编机制】，它使得从外部直接访问变得复杂。

            - 即便如此，由于 py 没有【强类型封装机制】，
              因此技术上仍然可以从外部访问所谓的 "私有" 属性/方法。

            - 应该遵循良好的编程实践，在适当时候使用公共和 "私有" 成员，
              并且遵守 "【最小权限原则】"，即只暴露必要的接口给其他组件。
    """

    @abstractmethod
    def get_token(self) -> str:
        """
            应当被重写以返回当前有效的访问令牌。

            【获取 `token`】。

                为了安全考虑，开发者请勿将 `token` 返回给前端，
                需要开发者保存在后台，所有访问企业微信 API 的请求由后台发起。

                获取 `token` 是调用企业微信 API 接口的第一步，
                相当于创建一个【登录凭证】，其它的业务 API 接口，
                都需要依赖于 `token` 来鉴权调用者身份。

                因此开发者，在使用业务接口前，要明确 `token` 的颁发来源，
                使用正确的 `token`。

                每个应用有【独立】的 secret，获取到的 `token` 只能【本应用使用】，
                所以每个应用的 `token` 应该分开来获取。

                开发者需要【缓存】 `token`，用于后续接口的调用
                （注意：不能频繁调用 `gettoken` 接口，否则会受到【频率拦截】）。

                当 `token` 失效或过期时，需要【重新获取】。

                `token` 的有效期通过返回的 `expires_in` 来传达，
                正常情况下为 7200 秒（2 小时）。

                由于企业微信每个应用的 `token` 是彼此独立的，
                所以进行缓存时需要【区分应用】来进行存储。

                `token` 至少保留 512 字节的存储空间。

                企业微信可能会出于运营需要，提前使 `token` 失效，
                开发者应实现 `token` 失效时重新获取的逻辑。

                企业微信官方 API 接口文档地址：
                【https://developer.work.weixin.qq.com/document/path/91039】

        :return:
        :raises: (NotImplementedError) 当定义一个抽象类，
                 并且希望这个类的子类必须实现某些方法时，
                 可以在这些方法中使用 `raise NotImplementedError`。
                 这样当这个方法没有在子类中被实现（即子类没有重写或具体化该方法），
                 而直接调用时，py 会抛出 `NotImplementedError` 异常，
                 提示调用者或开发者该方法仍然需要实现。
        """
        raise NotImplementedError

    def __replace(self, url: str) -> str:
        """
            替换企业微信 API 接口的 URL 中包含的【访问令牌占位符】。

                (
                    如将 "https://qyapi.weixin.qq.com/cgi-bin/user/get?
                    access_token=ACCESS_TOKEN" 替换为
                    "https://qyapi.weixin.qq.com/cgi-bin/user/get?
                    access_token=-aIVbALkwyv5o9Eh9TCZMd65ZLbK..."。
                )

            此方法将遍历 `token_mapping` 字典，
            查找 URL 中是否存在对应的【访问令牌占位符】，
            如果发现，则调用相应的获取令牌方法，并替换 URL 中的占位符。

            如果在 `url` 中找不到任何指定类型的访问令牌占位符，
            则返回未修改的 `url`。

        :param url: (str): 包含访问令牌占位符的原始 URL。
        :return: (str): 替换访问令牌后获得的新 URL。
        """
        # 创建【令牌类型】与【获取方法】的【映射字典】
        # 如果后期有需要添加其它类型服务的 `token` 实现逻辑
        # 则只需要往映射字典里面添加对应的映射关系即可
        token_mapping = {
            "ACCESS_TOKEN": self.get_token,
        }
        # 遍历映射字典并执行替换
        for placeholder, getter in token_mapping.items():
            if placeholder in url:
                return url.replace(placeholder, getter())
        # 如果没有找到匹配项，则返回原始 URL
        # 有些 API 接口不需要进行替换
        # 如 "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        return url

    def __post(self, url: str, params: dict) -> dict:
        """
            处理 POST 请求的私有方法。

            该方法将参数转换为 JSON 格式并发送 POST 请求到指定的 URL，
            然后返回响应的 JSON 解析结果。

        :param url: 需要发送 POST 请求的 URL。
        :param params: 需要在 POST 请求体中传递的参数字典。
        :return: 服务器返回的响应内容，通常是一个 JSON 对象。
        """
        # 调用 `json` 模块中的 `dumps` 函数
        # 将 py 对象转换为 JSON 格式的字符串
        # 参数 `ensure_ascii=False` 意味着转换过程
        # 不会将非 ASCII 字符转义成 `\uXXXX` 形式
        # 允许输出实际的 Unicode 字符
        # `.encode("utf-8")`：将上一步得到的 JSON 字符串
        # 编码为 UTF-8 格式的字节串（bytes）
        # 这通常是为满足 HTTP 请求体中发送数据时对格式的要求
        data = json.dumps(
            params,
            ensure_ascii=False
        ).encode("utf-8")
        # `.json()` 方法解析服务器返回响应体
        # 中的 JSON 数据，并将其转换回 py 对象
        resp = requests.post(
            url=self.__replace(url=url),
            data=data
        ).json()
        return resp

    def __get(self, url: str, params: dict) -> dict:
        """
            处理 GET 请求的私有方法。

            该方法通过指定的 URL 和【参数字典】来发送 GET 请求，
            并返回响应数据的 JSON 格式。

         :param url: (str) 请求的 URL 地址。
        :param params: (dict) 一个包含请求参数的字典。
        :return: 返回服务器响应的 JSON 对象。
        """
        params_url = add_qs(
            url=url,
            params=params
        )
        # `.json()` 方法解析服务器返回响应体
        # 中的 JSON 数据，并将其转换回 py 对象
        resp = requests.get(
            url=self.__replace(url=params_url)
        ).json()
        return resp

    def httpReq(self, api: list or tuple, params: dict = None) -> dict:
        """
            发起 HTTP 请求，支持【失败重试机制】。

            根据传入的 `api`，
            该函数会决定是发起 `GET` 或 `POST` 请求。

            `api` 应当是一个包含请求的【相对路径】
            以及【请求方式】（"GET" 或 "POST"）的元组或列表。

            如果请求成功，将返回解析后的 JSON 数据字典；
            如果请求失败，则会抛出 `ApiException` 异常。

        :param api: 包含请求的短路径字符串和
        请求方法 ("GET" 或 "POST") 的元组或列表。
        :param params: 请求所需携带的参数字典，可选参数，默认为 None。
        :return: 请求响应转换成的 JSON 格式字典对象。
        """
        resp = dict()
        # `api` 是一个包含【请求路径】和【请求方法】的元组或列表
        # 如: ("/cgi-bin/gettoken", "GET", "xxx")
        short_url = api[0]
        method = api[1]
        url = urljoin(WXWORK_API_BASE_URL, short_url)
        for retry in range(3):
            if method.upper() == "POST":
                resp = self.__post(
                    url=url,
                    params=params
                )
            elif method.upper() == "GET":
                resp = self.__get(
                    url=url,
                    params=params
                )
            err_code = resp.get("errcode")
            err_msg = resp.get("errmsg")
            if err_code == 0:
                return resp
            raise ApiException(
                err_code=err_code,
                err_msg=err_msg
            )
