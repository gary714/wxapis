# wxapis
> `wxapis` 是一个封装了企业微信接口（API）的工具包。它提供了一个统一的入口和规范，以便于开发者在使用企业微信相关接口时能够更为方便快捷。

## 简介
* 本工具包专为企业微信内部开发而设计，旨在简化 [企业微信内部开发](https://developer.work.weixin.qq.com/document/path/90556) 过程中与 API 交互的复杂度。
* 当前版本不支持 [第三方应用开发](https://developer.work.weixin.qq.com/document/path/90594) 和 [服务商代开发](https://developer.work.weixin.qq.com/document/path/97111) ，未来可能会根据需求进行扩展。
* 目前已经集成了大多数常用的企业微信 API，并为每个接口提供易于理解的常量名称。请注意，并非所有官方接口都已经被包含在本工具包中。

## 使用
### 安装
* 安装 `wxapis` 可以非常简单，通过以下命令即可完成：

    ```shell script
    pip install wxapis
    ```

### 示例
* 假设您想要获取特定成员的信息，有两种方法可以找到相关接口：一是直接查阅企业微信官方接口文档；二是使用我们包中提供的搜索功能进行查询。以下是如何使用搜索功能的示例：

    ```shell script
    from wxapis import search_apis
    import json
    
    print(
        json.dumps(
            search_apis(kw="user"),
            ensure_ascii=False,
            indent=4
        )
    )
    ```

* 通过关键词 "user" 搜索得到的结果会列出所有相关的接口信息，如下所示：

    ```shell script
    [
        {
            "WXWORK_GET_USER": [
                "/cgi-bin/user/get?access_token=ACCESS_TOKEN",
                "GET",
                "读取成员。为保护企业数据与用户隐私，从 2022 年 6 月 20 号 20 点开始，新创建的自建应用与代开发应用，调用该接口时，不再返回以下字段：头像、性别、手机、邮箱、企业邮箱、员工个人二维码、地址，应用需要通过 oauth2 手工授权的方式获取管理员与员工本人授权的字段。"
            ]
        },
        {
            "WXWORK_CREATE_USER": [
                "/cgi-bin/user/create?access_token=ACCESS_TOKEN",
                "POST",
                "创建成员。仅通讯录同步助手或第三方通讯录应用可调用。每个部门下的部门、成员总数不能超过 3 万个。建议保证创建 `department` 对应的部门和创建成员是串行化处理。"
            ]
        },
        {
            "WXWORK_UPDATE_USER": [
                "/cgi-bin/user/update?access_token=ACCESS_TOKEN",
                "POST",
                "更新成员。特别地，如果 `userid` 由系统自动生成，则仅允许修改一次。新值可由 `new_userid` 字段指定。如果创建时企业邮箱为系统默认分配的，则仅允许修改一次，若创建时填入了合规的企业邮箱，则无法修改。仅通讯录同步助手或第三方通讯录应用可调用。注意，每个部门下的部门、成员总数不能超过 3 万个。"
            ]
        },
        {
            "WXWORK_DELETE_USER": [
                "/cgi-bin/user/delete?access_token=ACCESS_TOKEN",
                "GET",
                "删除成员。仅通讯录同步助手或第三方通讯录应用可调用。若是绑定了腾讯企业邮，则会同时删除邮箱账号。"
            ]
        },
        {
            "WXWORK_BATCH_DELETE_USER": [
                "/cgi-bin/user/batchdelete?access_token=ACCESS_TOKEN",
                "POST",
                "批量删除成员。仅通讯录同步助手或第三方通讯录应用可调用。"
            ]
        },
        {
            "WXWORK_USER_SIMPLE_LIST": [
                "/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN",
                "GET",
                "获取部门成员。企业通讯录安全特别重要，企业微信将持续升级加固通讯录接口的安全机制，以下是关键的变更点：从 2022 年 8 月 15 日 10 点开始，\"企业管理后台 - 管理工具 - 通讯录同步\"的新增 IP 将不能再调用此接口，企业可通过 \"获取成员 ID 列表\" 和 \"获取部门 ID 列表\"接口获取 `userid` 和部门 ID 列表。"
            ]
        },
        {
            "WXWORK_LIST_USER": [
                "/cgi-bin/user/list?access_token=ACCESS_TOKEN",
                "GET",
                "获取部门成员详情。应用只能获取可见范围内的成员信息，且每种应用获取的字段有所不同，在返回结果说明中会逐个说明。企业通讯录安全特别重要，企业微信持续升级加固通讯录接口的安全机制，以下是关键的变更点：从 2022 年 6 月 20 号 20 点开始，除通讯录同步以外的基础应用（如客户联系、微信客服、会话存档、日程等），以及新创建的自建应用与代开发应用，调用该接口时，不再返回以下字段：头像、性别、手机、邮箱、企业邮箱、员工个人二维码、地址，应用需要通过 `oauth2` 手工授权的方式获取管理员与员工本人授权的字段。从 2022 年 8 月 15 日 10 点开始，\"企业管理后台 - 管理工具 - 通讯录同步\"的新增 IP 将不能再调用此接口，企业可通过 \"获取成员 ID 列表\" 和 \"获取部门 ID 列表\"接口获取 `userid` 和部门 ID 列表。"
            ]
        },
        {
            "WXWORK_CONVERT_USERID_TO_OPENID": [
                "/cgi-bin/user/convert_to_openid?access_token=ACCESS_TOKEN",
                "POST",
                "userid 与 openid 互换。该接口使用场景为企业支付，在使用企业红包和向员工付款时，需要自行将企业微信的 `userid` 转成 `openid`。注：需要成员使用微信登录企业微信或者关注微信插件（原企业号）才能转成 `openid`；如果是外部联系人，请使用外部联系人 `openid` 转换转换 `openid`。"
            ]
        },
        {
            "WXWORK_CONVERT_OPENID_TO_USERID": [
                "/cgi-bin/user/convert_to_userid?access_token=ACCESS_TOKEN",
                "POST",
                "openid 转 userid。该接口主要应用于使用企业支付之后的结果查询。开发者需要知道某个结果事件的 `openid` 对应企业微信内成员的信息时，可以通过调用该接口进行转换查询。"
            ]
        },
        {
            "WXWORK_USER_AUTH_SUCCESS": [
                "/cgi-bin/user/authsucc?access_token=ACCESS_TOKEN",
                "GET",
                "登录二次验证。此接口可以满足安全性要求高的企业进行成员验证。开启二次验证后，当且仅当成员登录时，需跳转至企业自定义的页面进行验证。验证频率可在设置页面选择。企业在开启二次验证时，必须在管理端填写企业二次验证页面的 url。当成员登录企业微信或关注微信插件（原企业号）进入企业时，会自动跳转到企业的验证页面。在跳转到企业的验证页面时，会带上如下参数：`code=CODE`。企业收到 code 后，使用 \"通讯录同步助手\" 调用接口 \"根据 code 获取成员信息\" 获取成员的 `userid`。"
            ]
        }
    ]
    ```

* 如上所示，返回结果是一个字典列表，其中每个字典包含三个关键部分：一是 API 路径段（自动补全完整 URL），二是请求方法（GET 或 POST），三是该接口的描述性注释。
* 假设您要获取某位成员详细信息，您可按照如下方式调用对应 API：

    ```shell script
    from wxapis import WXWORK_GET_USER
    from wxapis.corporate import CorpApis
    from wxapis.abstract import ApiException
    import json
    
    try:
        wx = CorpApis(
            corpid="", # 填写您公司 ID
            agentid="", # 填写您应用 ID
            secret="" # 填写您应用密钥
        )
        users = wx.httpReq(
            api=WXWORK_GET_USER,
            params={
                "userid": "" # 填写要查询的用户 ID
            }
        )
        print(
            json.dumps(
                users,
                ensure_ascii=False,
                indent=4
            )
        )
    except ApiException as err:
        print(str(err))
    ```

* 最终返回的用户详情如下：

    ```shell script
    {
        "errcode": 0,
        "errmsg": "ok",
        "userid": "",
        "name": "",
        "department": [],
        "position": "",
        "status": 1,
        "isleader": 0,
        "extattr": {
            "attrs": []
        },
        "telephone": "",
        "enable": 1,
        "hide_mobile": 0,
        "order": [],
        "alias": "",
        "is_leader_in_dept": [],
        "direct_leader": []
    }
    ```

* 在使用我们的企业微信 API 接口包时，您可能会发现并非所有的企业微信官方 API 接口都被直接封装在包中。如果您需要访问未被定义的接口，您可以轻松地自定义一个接口元组或列表来实现这一需求。在构建自定义接口元组或列表时，请确保至少包含两个必要的元素：接口的短路径和 HTTP 请求方法（如 GET 或 POST）。这两项是调用任何企业微信 API 时不可或缺的信息。至于其他参数，根据实际请求需求来决定是否添加。依然以获取某成员的信息为例：

    ```shell script
    from wxapis.corporate import CorpApis
    from wxapis.abstract import ApiException
    import json

    try:
        wx = CorpApis(
            corpid="", # 填写您公司 ID
            agentid="", # 填写您应用 ID
            secret="" # 填写您应用密钥
        )
        users = wx.httpReq(
            # 使用元组或者列表，且前两项元素的内容固定，即请求短路径和请求方法
            api=(
                "/cgi-bin/user/get?access_token=ACCESS_TOKEN",
                "GET"
            ),
            params={
                "userid": "" # 填写要查询的用户 ID
            }
        )
        print(
            json.dumps(
                users,
                ensure_ascii=False,
                indent=4
            )
        )
    except ApiException as err:
        print(str(err))
    ```

* 最终返回的用户详情如下：

    ```shell script
    {
        "errcode": 0,
        "errmsg": "ok",
        "userid": "",
        "name": "",
        "department": [],
        "position": "",
        "status": 1,
        "isleader": 0,
        "extattr": {
            "attrs": []
        },
        "telephone": "",
        "enable": 1,
        "hide_mobile": 0,
        "order": [],
        "alias": "",
        "is_leader_in_dept": [],
        "direct_leader": []
    }
    ```

### 高级
* 除标准 API 调用外，本工具包还提供了执行特定操作例如向某个应用发送消息等高级功能。安装本工具包后，在系统路径中将自动添加一个专门命令以便发送消息至企业微信应用。如下所示：

    ```
    $ which smsg
    /d/Python/Python38/Scripts/smsg

    $ smsg --help
    usage: smsg.py [-h] -c CORPID -s SECRET -i AGENTID -m MESSAGE [-a FIELD] [-f {json,yaml}]
               [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

    发送企业微信内部应用消息。
    
    optional arguments:
      -h, --help            显示此帮助信息并退出。
      -c CORPID, --corpid CORPID
                            企业微信的企业 id。可以在企业微信管理后台获取此 id。此选项为必须选项。
      -s SECRET, --secret SECRET
                            与企业微信内应用关联的 secret。secret 用于验证身份并加密通讯过程，可在企业微信管理后台找到。此选项为必须选项。
      -i AGENTID, --agentid AGENTID
                            企业微信内应用的 agent id，代表了应用实体，在企业微信中唯一标识一个应用。请确保传入正确的 agent id。此选项为必须选项。
      -m MESSAGE, --message MESSAGE
                            要发送给企业微信应用的消息文本内容。此选项为必须选项。
      -a FIELD, --field FIELD
                            消息体字段，格式为 "k=v"，添加或覆盖参数 `message` 中字段的值，例如 "-a text.content=xxx"。此选 项为可选选项。
      -f {json,yaml}, --format {json,yaml}
                            定义参数 `message` 文本内容的解析格式，默认为 "json"。此选项为可选选项。
      -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            设置输出日志级别，默认为 "INFO"，在命令行传入时不区分大小写，比如传入 "DEBUG" 和传入 "debug" 一 样。此选项为可选选项。

    ```

* 根据命令行参数指南，您可以轻松地通过相应命令向企业微信中发送消息：

    ```
    PS E:\PycharmProjects\self\wxapis> smsg --corpid "" --agentid "" --secret "" --message '{\"touser\": \"\", \"agentid\": "", \"msgtype\": \"text\", \"text\": {\"content\": \"这是测试！\"}, \"safe\": 0, \"enable_id_trans\":0, \"enable_duplicate_check\": 0}' -a "text.content=test!!!"
    INFO:root:发送消息[{'touser': '', 'agentid': '', 'msgtype': 'text', 'text': {'content': 'test!!!'}, 'safe': 0, 'enable_id_trans': 0, 'enable_duplicate_check': 0}]。
    INFO:root:任务执行："True"。
    ```

* 如果您需要审查消息发送详情，请确保设置合适的日志级别以便获得详细输出：

    ```
    PS E:\PycharmProjects\self\wxapis> smsg --corpid "" --agentid "" --secret "" --message '{\"touser\": \"\", \"agentid\": "", \"msgtype\": \"text\", \"text\": {\"content\": \"这是测试！\"}, \"safe\": 0, \"enable_id_trans\":0, \"enable_duplicate_check\": 0}' -a "text.content=test!!!" --level debug
    DEBUG:root:Namespace(agentid='', corpid='', field=['text.content=test!!!'], format='json', level='DEBUG', message='{"touser": "", "agentid": '', "msgtype": "text", "text": {"content": "这是测试！"}, "safe": 0, "enable_id_trans":0, "enable_duplicate_check": 0}', secret='')
    DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): qyapi.weixin.qq.com:443
    DEBUG:urllib3.connectionpool:https://qyapi.weixin.qq.com:443 "POST /cgi-bin/message/send?access_token=xxx HTTP/11" 200 124
    INFO:root:发送消息[{'touser': '', 'agentid': '', 'msgtype': 'text', 'text': {'content': 'test!!!'}, 'safe': 0, 'enable_id_trans': 0, 'enable_duplicate_check': 0}]。
    INFO:root:任务执行："True"。
    ```
