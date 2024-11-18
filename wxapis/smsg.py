#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    py Module `flatten-dict`:
        `flatten-dict` 是一个 py 模块，
        它提供一种方法来将【嵌套字典】（即包含其他字典作为其值的字典）
        平铺成【扁平结构】，
        以及将扁平结构的字典重新【嵌套化】。

        `flatten-dict` 文档地址：
        https://github.com/ianlini/flatten-dict/blob/master/README.rst。

        这个模块非常有用，尤其是在处理嵌套结构复杂的 JSON 数据
        或者需要在数据库和内存表示之间进行转换时。

        主要功能包括 `flatten` 和 `unflatten` 方法：
            - `flatten` 方法：将【嵌套字典】转换为【扁平结构】的字典。

            - `unflatten` 方法：将扁平化后的字典重新转换成嵌套字典。
              它是 `flatten` 操作的【逆过程】。

        示例：
            >>> from flatten_dict import flatten, unflatten
            >>>
            >>> nested_dict = {
            >>>     "a": 1,
            >>>     "b": {
            >>>         "c": 2,
            >>>         "d": {
            >>>             "e": 3
            >>>         }
            >>>     }
            >>> }
            >>> flat_dict = flatten(nested_dict, reducer="dot")
            >>> print(flat_dict)
            >>>
            >>> re_nested_dict = unflatten(flat_dict, splitter="dot")
            >>> print(re_nested_dict == nested_dict)
            {"a": 1, "b.c": 2, "b.d.e": 3}
            True

    py Module `dict-recursive-update`:
        此库提供用于【递归更新】 py 字典的功能。

        基本上，`recursive_update` 方法允许将两个嵌套字典合并在一起，
        其中第二个字典中的值会更新到第一个字典中去，
        如果遇到嵌套的字典，则会递归地执行这个更新过程。

        `dict-recursive-update` 文档地址：
        https://github.com/Maples7/dict-recursive-update/blob/master/README.rst。

        示例：
            >>> from dict_recursive_update import recursive_update
            >>>
            >>> dict1 = {"a": 1, "b": {"c": 2, "d": 4}}
            >>> dict2 = {"b": {"c": 3, "e": 5}}
            >>> recursive_update(dict1, dict2)
            >>> print(dict1)
            {"a": 1, "b": {"c": 3, "d": 4, "e": 5}}

    py Module `itertools`:
        py 中的 `itertools` 模块是标准库的一部分，
        它提供一系列用于【高效循环】操作的【迭代器】。

        这个模块包含许多非常有用的函数来创建各种复杂的迭代模式，
        以减少编写和维护嵌套循环的需要。

        `chain` 方法是 `itertools` 模块中提供的一个函数，
        它用于【将多个迭代器链接在一起，形成一个单独的连续迭代器】。

        使用 `chain` 时，可以传递两个或多个迭代器作为参数，
        然后通过结果迭代器按顺序访问所有输入迭代器中的元素。

        示例：
            >>> from itertools import chain
            >>>
            >>> list1 = [1, 2, 3]
            >>> list2 = [4, 5, 6]
            >>> combined = chain(list1, list2)
            >>> for item in combined:
            >>>     print(item)
            1
            2
            3
            4
            5
            6

    此脚本最终通过【命令行】执行。

    命令行示例：
        不传入额外参数的情况：
            python3 smsg.py --corpid "" \
            --secret "" \
            --message '{\
            \"touser\": \"\", \
            \"agentid\": , \
            \"msgtype\": \"text\", \
            \"text\": {\"content\": \"这是测试！\"}, \
            \"safe\": 0, \
            \"enable_id_trans\":0, \
            \"enable_duplicate_check\": 0\
            }'

        传入额外参数的情况：
            python3 smsg.py --corpid "" \
            --secret "" \
            --message '{\
            \"touser\": \"\", \
            \"agentid\": , \
            \"msgtype\": \"text\", \
            \"text\": {\"content\": \"这是测试！\"}, \
            \"safe\": 0, \
            \"enable_id_trans\":0, \
            \"enable_duplicate_check\": 0\
            }' \
            -a "text.content=Hello!"

    注意：本脚本中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import argparse
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import chain
from pathlib import Path
from dict_recursive_update import recursive_update
from flatten_dict import unflatten
import yaml

# 将当前运行的 py 文件所在的上两级目录加入到 py 的【系统路径】中
# 使得在这个【根目录】下的【模块】和【包】可以被当前文件所引用
current_file_path = Path(__file__).absolute()
# 移动到上两级目录以获取【根路径】
root_path = current_file_path.parent.parent
# 将【根路径】作为【系统路径】加入 `sys.path`
sys.path.append(str(root_path))

# 指定发送消息到企业微信应用中时被允许的消息体格式
FILE_FORMATS = ["json", "yaml"]
# `PARSERS` 是一个字典
# 其【键】为【文件格式】的字符串
# （与 `FILE_FORMATS` 列表中的项相对应）
# 【值】为【解析】这些文件格式内容的【函数】
PARSERS = {
    "json": json.loads,
    "yaml": yaml.safe_load
}
LOG_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL"
]


def case_insensitive(log_level: str) -> str:
    """
        转换【日志级别】输入为【大写】，
        并验证是否是有效的日志级别。

        此函数将输入的日志级别字符串【不区分大小写】地转换为【大写形式】，
        并检查其是否属于预定义的【有效日志级别】列表中。

    :param log_level:
    :return:
    """
    upper_case = log_level.upper()
    if upper_case not in LOG_LEVELS:
        raise argparse.ArgumentTypeError(
            f"\"{log_level}\" 不是一个有效的日志级别！"
        )
    return upper_case


def merge_fields(msg: str, msg_format: str, fields: list) -> dict:
    """
        将【消息字符串】和【字段列表】合并为一个字典。

        此函数接受一个消息字符串和一系列 "键=值" 格式的字段，
        将这些字段解析成字典，
        再将得到的字典与原始的消息字符串按照键的层级结构递归地进行更新合并。

        例如，命令行输入如下：
            python3 smsg.py --corpid "" \
            --secret "" \
            --message '{\
            \"touser\": \"\", \
            \"agentid\": , \
            \"msgtype\": \"text\", \
            \"text\": {\"content\": \"这是测试！\"}, \
            \"safe\": 0, \
            \"enable_id_trans\":0, \
            \"enable_duplicate_check\": 0\
            }' \
            -a "text.content=Hello!!!"

        最终返回如下结构的字典：
            {
                "touser": "",
                "agentid": "",
                "msgtype": "text",
                "text": {"content": "Hello!!!"},
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0
            }

        注意：函数内部首先将每个字段拆分为独立的键值对，
            并将它们平铺在一个列表中；
            然后创建一个扁平化字典；
            最后使用 `unflatten` 方法恢复任何嵌套结构，
            并通过 `recursive_update` 方法与原始消息进行递归更新和合并。

    :param msg: 需要合并到的【原始消息字符串】。
    :param msg_format: 【消息格式化方式】，
    用于指定如何解析原始消息。
    :param fields: 包含 "键=值" 对的字段列表，
    其中每个字段可以使用空格分隔多个键值对。
    键值对中的键支持使用点号 "." 来表示嵌套结构。
    :return: 合并后包含所有信息的字典。
    如果存在嵌套结构，将以递归方式进行合并。
    """
    parser = PARSERS.get(msg_format)
    if not fields:
        return parser(msg)
    # 将命令行传入的例如 `-a touser=xxx -a agentid=xxx`
    # 转化为 `[[touser=xxx], [agentid=xxx]]`
    split_fields = [field.split() for field in fields]
    # 将 `[[touser=xxx], [agentid=xxx]]`
    # 转化为 `[touser=xxx, agentid=xxx]`
    # `*` 是 py 的解包（unpack）操作符
    # 它将 `split_fields` 中的每个【子列表】
    # 作为独立的参数传递给后面的函数
    # `chain()` 函数来自 `itertools` 模块
    # 其作用是接受多个迭代器作为参数
    # 并将它们链在一起形成一个新的迭代器
    # 该新迭代器依次产生每个原始迭代器中的元素
    # 对于上面给出的解包后参数
    # `chain([1, 2], [3, 4], [5])` 将
    # 生成元素序列：1, 2, 3, 4, 5
    # 最后 `list()` 函数是将 `chain()` 函数
    # 生成的【迭代器】转换成一个【列表】
    last_fields = list(chain(*split_fields))
    # 将 `[touser=xxx, agentid=xxx]`
    # 转化为 `{"touser": "xxx", "agentid": "xxx"}`
    flat_dict = {
        k: v
        for k, v in (
            field.split(sep=r"=", maxsplit=1)
            for field in last_fields
        )
    }
    # 将例如 `{"text.content": "xxx"}`
    # 转化为 `{"text": {"content": xxx}}`
    unflat = unflatten(flat_dict, splitter="dot")
    result = recursive_update(
        default=parser(msg),
        custom=unflat
    )
    return result


def send_wx_msg(args) -> bool:
    """
        发送消息到企业微信。

        此函数使用给定参数构建并发送消息到企业微信。

        参数 args 包含：
            - `message`: 字符串，待发送的【消息内容】。

            - `field`: 列表，
              【附加字段】以 "key=value" 格式添加到消息。

            - `format`: 字符串，指定如何格式化 `message` 参数。

            - `corpid`: 字符串，用于认证的企业 ID。

            - `secret`: 字符串，用于认证的应用密钥。

    :return:
    """
    # 默认情况下设置为 `False`
    success = False
    message = merge_fields(
        msg=args.message,
        msg_format=args.format,
        fields=args.field
    )
    from wxapis.abstract import ApiException
    from wxapis.corporate import CorpApis
    from wxapis import WXWORK_SEND_APP_MESSAGE
    try:
        corp_api = CorpApis(
            corpid=args.corpid,
            agentid=args.agentid,
            secret=args.secret
        )
        corp_api.httpReq(
            api=WXWORK_SEND_APP_MESSAGE,
            params=message
        )
    except (ApiException, TypeError) as err:
        logging.error(msg=str(err))
    else:
        # 如果没有异常发生，则设置为 `True`
        success = True
        logging.info(
            msg=f"\033[32m发送消息[{message}]。\033[0m"
        )
    return success


def async_send_wx_msg(args_list: list) -> None:
    """
        使用线程池【并发】地发送微信消息。

        此函数接收一个参数列表，
        每个参数是传递给 `send_wx_msg` 函数的元组或字典。
        它使用最多 3 个工作线程的线程池来并发执行消息发送任务。

        每当一个任务完成时，会记录一条信息表示该任务是否完成。

    :param args_list: 一个列表，
    其中包含传递给 `send_wx_msg` 的参数集。
    每个列表项应是一个元组或字典，作为单独发送操作的参数。
    :return: 此函数不返回任何值。
    """
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(send_wx_msg, args)
            for args in args_list
        ]
        for future in as_completed(futures):
            # 检查 `send_wx_msg` 函数是否成功执行
            if future.result():
                logging.info(
                    msg=f"\033[32m任务执行："
                        f"\"{str(future.done())}\"。\033[0m"
                )


def main() -> None:
    """
        主函数，负责【初始化日志配置】，
        并根据参数【发送企业微信消息】。

        此函数首先根据提供的日志等级参数初始化日志系统。

        然后，它解析命令行参数，
        并调用 `async_send_wx_msg` 函数
        来处理消息发送的具体逻辑。

        使用:
           python smsg.py
           --corpid ""
           --agentid ""
           --secret ""
           --message '{\"touser\": \"\", \"agentid\": "",
           \"msgtype\": \"text\", \"text\": {\"content\": \"这是测试！\"},
           \"safe\": 0, \"enable_id_trans\":0, \"enable_duplicate_check\": 0}'
           -a "text.content=test!!!"

           或者：
            smsg --corpid ""
            --agentid ""
            --secret ""
            --message '{\"touser\": \"\", \"agentid\": "",
            \"msgtype\": \"text\", \"text\": {\"content\": \"这是测试！\"},
            \"safe\": 0, \"enable_id_trans\":0, \"enable_duplicate_check\": 0}'
            -a "text.content=test!!!"

    :return: 此函数不返回任何值。
    """
    parser = argparse.ArgumentParser(
        add_help=False,
        description="发送企业微信内部应用消息。"
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="显示此帮助信息并退出。"
    )
    parser.add_argument(
        "-c",
        "--corpid",
        required=True,
        help="企业微信的企业 id。"
             "可以在企业微信管理后台获取此 id。"
             "此选项为必须选项。"
    )
    parser.add_argument(
        "-s",
        "--secret",
        required=True,
        help="与企业微信内应用关联的 secret。"
             "secret 用于验证身份并加密通讯过程，"
             "可在企业微信管理后台找到。"
             "此选项为必须选项。"
    )
    parser.add_argument(
        "-i",
        "--agentid",
        required=True,
        help="企业微信内应用的 agent id，"
             "代表了应用实体，在企业微信中唯一标识一个应用。"
             "请确保传入正确的 agent id。"
             "此选项为必须选项。"
    )
    parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="要发送给企业微信应用的消息文本内容。"
             "此选项为必须选项。"
    )
    parser.add_argument(
        "-a",
        "--field",
        action="append",
        help="消息体字段，格式为 \"k=v\"，"
             "添加或覆盖参数 `message` 中字段的值，"
             "例如 \"-a text.content=xxx\"。"
             "此选项为可选选项。"
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=FILE_FORMATS,
        default="json",
        help="定义参数 `message` 文本内容的解析格式，"
             "默认为 \"json\"。"
             "此选项为可选选项。"
    )
    parser.add_argument(
        "-l",
        "--level",
        choices=LOG_LEVELS,
        default="INFO",
        type=case_insensitive,
        help="设置输出日志级别，默认为 \"INFO\"，"
             "在命令行传入时不区分大小写，"
             "比如传入 \"DEBUG\" 和传入 \"debug\" 一样。"
             "此选项为可选选项。"
    )
    args = parser.parse_args()
    # `logging` 模块中配置日志记录功能基本参数设置函数
    # 设置日志记录器（logger）将会处理
    # 哪些最低层级（level）的日志信息
    logging.basicConfig(
        # 使用 `getattr()` 内置函数动态获取
        # `logging` 模块中预定义日志级别属性
        # 假设 `args.level` 的值是 "DEBUG"
        # 那么 `getattr(logging, args.level)`
        # 就等价于 `logging.DEBUG`
        level=getattr(
            logging,
            args.level
        )
    )
    logging.debug(msg=args)
    async_send_wx_msg(args_list=[args])


if __name__ == "__main__":
    main()
