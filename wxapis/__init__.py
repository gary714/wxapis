#!/usr/bin/env python
# -*- coding= utf-8 -*-
"""
    企业微信官方 API 文档提供一套完整的接口，
    以支持开发者在企业微信平台上进行【应用开发】和【数据交互】。

    这些接口主要分为以下三大类，以适应不同场景下的需求：
        - 企业内部开发：
          https://developer.work.weixin.qq.com/document/path/90556。

        - 第三方应用开发：
          https://developer.work.weixin.qq.com/document/path/90594。

        - 服务商代开发：
          https://developer.work.weixin.qq.com/document/path/97111。

    ***请注意，并非所有可用的接口都已在以下详尽列出；
    仅罗列常见且通常被频繁使用的接口。

    每个 "接口" 都是一个元组类型数据结构，包括以下三个基本要素：
        - 接口地址：定义 API 的网络位置。

        - 请求方法：指明客户端与服务器交互方式，如 `GET`、`POST` 等。

        - 接口描述：简洁地概述该接口的功能或作用。

    典型地，调用这些 API 时采取如下模式：

        >>> from wxapis.corporate import CorpApis
        >>> from wxapis import WXWORK_SEND_APP_MESSAGE
        >>>
        >>> corpapi = CorpApis(
        >>>     corpid="",
        >>>     secret=""
        >>> )
        >>> resp = corpapi.httpReq(
        >>>     api=WXWORK_SEND_APP_MESSAGE,
        >>>     params={}
        >>> )
        >>> print(resp)

    如果需要调用未在以下列出的接口，
    则可以按照统一格式自定义元组或列表来构造接口地址和请求方法：

        >>> from wxapis.corporate import CorpApis
        >>>
        >>> corpapi = CorpApis(
        >>>     corpid="",
        >>>     secret=""
        >>> )
        >>> resp = corpapi.httpReq(
        >>>     api=(
        >>>         "https://xxx.com/xxx",
        >>>         "POST"
        >>>     ),
        >>>     params={}
        >>> )
        >>> print(resp)

    在查询相关的接口时，可以直接于本文件中查找，也可以通过 "搜索" 功能进行搜索，
    示例如下：

        >>> from wxapis import search_apis
        >>> import json
        >>>
        >>> print(
        >>>     json.dumps(
        >>>         search_apis(kw="user/list"),
        >>>         ensure_ascii=False,
        >>>         indent=4
        >>>     )
        >>> )
        [
            {
                "WXWORK_USER_LIST": [
                    "/cgi-bin/user/list?access_token=ACCESS_TOKEN",
                    "GET",
                    "获取部门成员详情。应用只能获取可见范围内的成员信息，且每种应用获取的字段有所不同，
                    在返回结果说明中会逐个说明。企业通讯录安全特别重要，
                    企业微信持续升级加固通讯录接口的安全机制，
                    以下是关键的变更点：从 2022 年 6 月 20 号 20 点开始，
                    除通讯录同步以外的基础应用（如客户联系、微信客服、会话存档、日程等），
                    以及新创建的自建应用与代开发应用，调用该接口时，
                    不再返回以下字段：头像、性别、手机、邮箱、企业邮箱、员工个人二维码、地址，
                    应用需要通过 `oauth2` 手工授权的方式获取管理员与员工本人授权的字段。
                    从 2022 年 8 月 15 日 10 点开始，\"企业管理后台 - 管理工具 - 通讯录同步\"的
                    新增 IP 将不能再调用此接口，企业可通过 \"获取成员 ID 列表\"
                    和 \"获取部门 ID 列表\"接口获取 `userid` 和部门 ID 列表。"
                ]
            }
        ]
    注意：本脚本中出现的 "py"，如无特殊说明，则指代 "Python"。
"""
import sys
import re

WXWORK_API_BASE_URL = "https://qyapi.weixin.qq.com"
WXWORK_GET_ACCESS_TOKEN = (
    "/cgi-bin/gettoken",
    "GET",
    "获取 `access_token` 是调用企业微信 API 接口的第一步，"
    "相当于创建了一个登录凭证，其它的业务 API 接口，"
    "都需要依赖于 `access_token` 来鉴权调用者身份。"
)
WXWORK_GET_USER = (
    "/cgi-bin/user/get?access_token=ACCESS_TOKEN",
    "GET",
    "读取成员。为保护企业数据与用户隐私，"
    "从 2022 年 6 月 20 号 20 点开始，"
    "新创建的自建应用与代开发应用，调用该接口时，"
    "不再返回以下字段：头像、性别、手机、邮箱、企业邮箱、"
    "员工个人二维码、地址，"
    "应用需要通过 oauth2 手工授权的方式获取管理员与员工本人授权的字段。"
)
WXWORK_CREATE_USER = (
    "/cgi-bin/user/create?access_token=ACCESS_TOKEN",
    "POST",
    "创建成员。仅通讯录同步助手或第三方通讯录应用可调用。"
    "每个部门下的部门、成员总数不能超过 3 万个。"
    "建议保证创建 `department` 对应的部门和创建成员是串行化处理。"
)
WXWORK_UPDATE_USER = (
    "/cgi-bin/user/update?access_token=ACCESS_TOKEN",
    "POST",
    "更新成员。特别地，如果 `userid` 由系统自动生成，"
    "则仅允许修改一次。"
    "新值可由 `new_userid` 字段指定。"
    "如果创建时企业邮箱为系统默认分配的，则仅允许修改一次，"
    "若创建时填入了合规的企业邮箱，则无法修改。"
    "仅通讯录同步助手或第三方通讯录应用可调用。"
    "注意，每个部门下的部门、成员总数不能超过 3 万个。"
)
WXWORK_DELETE_USER = (
    "/cgi-bin/user/delete?access_token=ACCESS_TOKEN",
    "GET",
    "删除成员。仅通讯录同步助手或第三方通讯录应用可调用。"
    "若是绑定了腾讯企业邮，则会同时删除邮箱账号。"
)
WXWORK_BATCH_DELETE_USER = (
    "/cgi-bin/user/batchdelete?access_token=ACCESS_TOKEN",
    "POST",
    "批量删除成员。仅通讯录同步助手或第三方通讯录应用可调用。"
)
WXWORK_USER_SIMPLE_LIST = (
    "/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN",
    "GET",
    "获取部门成员。企业通讯录安全特别重要，"
    "企业微信将持续升级加固通讯录接口的安全机制，"
    "以下是关键的变更点：从 2022 年 8 月 15 日 10 点开始，"
    "\"企业管理后台 - 管理工具 - 通讯录同步\""
    "的新增 IP 将不能再调用此接口，"
    "企业可通过 \"获取成员 ID 列表\" 和 \"获取部门 ID 列表\""
    "接口获取 `userid` 和部门 ID 列表。"
)
WXWORK_LIST_USER = (
    "/cgi-bin/user/list?access_token=ACCESS_TOKEN",
    "GET",
    "获取部门成员详情。应用只能获取可见范围内的成员信息，"
    "且每种应用获取的字段有所不同，在返回结果说明中会逐个说明。"
    "企业通讯录安全特别重要，企业微信持续升级加固通讯录接口的安全机制，"
    "以下是关键的变更点：从 2022 年 6 月 20 号 20 点开始，"
    "除通讯录同步以外的基础应用（如客户联系、微信客服、会话存档、日程等），"
    "以及新创建的自建应用与代开发应用，调用该接口时，"
    "不再返回以下字段：头像、性别、手机、邮箱、企业邮箱、员工个人二维码、"
    "地址，应用需要通过 `oauth2` 手工授权的方式获取管理员与员工本人授权的字段。"
    "从 2022 年 8 月 15 日 10 点开始，"
    "\"企业管理后台 - 管理工具 - 通讯录同步\""
    "的新增 IP 将不能再调用此接口，"
    "企业可通过 \"获取成员 ID 列表\" 和 \"获取部门 ID 列表\""
    "接口获取 `userid` 和部门 ID 列表。"
)
WXWORK_CONVERT_USERID_TO_OPENID = (
    "/cgi-bin/user/convert_to_openid?access_token=ACCESS_TOKEN",
    "POST",
    "userid 与 openid 互换。该接口使用场景为企业支付，"
    "在使用企业红包和向员工付款时，"
    "需要自行将企业微信的 `userid` 转成 `openid`。"
    "注：需要成员使用微信登录企业微信或者关注微信插件（原企业号）才能转成 `openid`；"
    "如果是外部联系人，请使用外部联系人 `openid` 转换转换 `openid`。"
)
WXWORK_CONVERT_OPENID_TO_USERID = (
    "/cgi-bin/user/convert_to_userid?access_token=ACCESS_TOKEN",
    "POST",
    "openid 转 userid。该接口主要应用于使用企业支付之后的结果查询。"
    "开发者需要知道某个结果事件的 `openid` 对应企业微信内成员的信息时，"
    "可以通过调用该接口进行转换查询。"
)
WXWORK_USER_AUTH_SUCCESS = (
    "/cgi-bin/user/authsucc?access_token=ACCESS_TOKEN",
    "GET",
    "登录二次验证。此接口可以满足安全性要求高的企业进行成员验证。"
    "开启二次验证后，当且仅当成员登录时，需跳转至企业自定义的页面进行验证。"
    "验证频率可在设置页面选择。企业在开启二次验证时，"
    "必须在管理端填写企业二次验证页面的 url。"
    "当成员登录企业微信或关注微信插件（原企业号）进入企业时，"
    "会自动跳转到企业的验证页面。"
    "在跳转到企业的验证页面时，会带上如下参数：`code=CODE`。"
    "企业收到 code 后，"
    "使用 \"通讯录同步助手\" 调用接口 \"根据 code 获取成员信息\" "
    "获取成员的 `userid`。"
)
WXWORK_CREATE_DEPARTMENT = (
    "/cgi-bin/department/create?access_token=ACCESS_TOKEN",
    "POST",
    "创建部门。注意，部门的最大层级为 15 层；部门总数不能超过 3 万个；"
    "每个部门下的节点不能超过 3 万个。"
    "建议保证创建的部门和对应部门成员是串行化处理。"
)
WXWORK_UPDATE_DEPARTMENT = (
    "/cgi-bin/department/update?access_token=ACCESS_TOKEN",
    "POST",
    "更新部门。应用须拥有指定部门的管理权限。"
    "如若要移动部门，需要有新父部门的管理权限。第三方仅通讯录应用可以调用。"
    "注意，部门的最大层级为 15 层；部门总数不能超过 3 万个；"
    "每个部门下的节点不能超过 3 万个。"
)
WXWORK_DELETE_DEPARTMENT = (
    "/cgi-bin/department/delete?access_token=ACCESS_TOKEN",
    "GET",
    "删除部门。应用须拥有指定部门的管理权限。第三方仅通讯录应用可以调用。"
)
WXWORK_LIST_DEPARTMENT = (
    "/cgi-bin/department/list?access_token=ACCESS_TOKEN",
    "GET",
    "获取部门列表。企业通讯录安全特别重要，"
    "企业微信将持续升级加固通讯录接口的安全机制，以下是关键的变更点："
    "从 2022 年 8 月 15 日 10 点开始，"
    "\"企业管理后台 - 管理工具 - 通讯录同步\" 的新增 IP 将不能再调用此接口，"
    "企业可通过 \"获取部门 ID 列表\" 接口获取部门 ID 列表。"
)
WXWORK_CREATE_TAG = (
    "/cgi-bin/tag/create?access_token=ACCESS_TOKEN",
    "POST",
    "创建标签。创建的标签属于该应用，只有该应用的 `secret` 才可以增删成员。"
    "注意，标签总数不能超过 3000 个。"
)
WXWORK_UPDATE_TAG = (
    "/cgi-bin/tag/update?access_token=ACCESS_TOKEN",
    "POST",
    "更新标签名字。调用的应用必须是指定标签的创建者。"
)
WXWORK_DELETE_TAG = (
    "/cgi-bin/tag/delete?access_token=ACCESS_TOKEN",
    "GET",
    "删除标签。调用的应用必须是指定标签的创建者。"
)
WXWORK_GET_TAG_USER = (
    "/cgi-bin/tag/get?access_token=ACCESS_TOKEN",
    "GET",
    "获取标签成员。无限制，但返回列表仅包含应用可见范围的成员；"
    "第三方可获取自己创建的标签及应用可见范围内的标签详情。"
)
WXWORK_ADD_TAG_USER = (
    "/cgi-bin/tag/addtagusers?access_token=ACCESS_TOKEN",
    "POST",
    "增加标签成员。调用的应用必须是指定标签的创建者；"
    "成员属于应用的可见范围。"
    "注意，每个标签下部门数和人员数总和不能超过 3 万个。"
)
WXWORK_DELETE_TAG_USER = (
    "/cgi-bin/tag/deltagusers?access_token=ACCESS_TOKEN",
    "POST",
    "删除标签成员。调用的应用必须是指定标签的创建者；"
    "成员属于应用的可见范围。"
)
WXWORK_LIST_TAG = (
    "/cgi-bin/tag/list?access_token=ACCESS_TOKEN",
    "GET",
    "获取标签列表。自建应用或通讯同步助手可以获取所有标签列表；"
    "第三方应用仅可获取自己创建的标签。"
)
WXWORK_GET_JOB_RESULT = (
    "/cgi-bin/batch/getresult?access_token=ACCESS_TOKEN",
    "GET",
    "获取异步任务结果。只能查询已经提交过的历史任务。"
)
WXWORK_INVITE_MEMBER = (
    "/cgi-bin/batch/invite?access_token=ACCESS_TOKEN",
    "POST",
    "邀请成员。企业可通过接口批量邀请成员使用企业微信，"
    "邀请后将通过短信或邮件下发通知。"
    "须拥有指定成员、部门或标签的查看权限。"
    "第三方仅通讯录应用可调用。"
)
WXWORK_GET_AGENT = (
    "/cgi-bin/agent/get?access_token=ACCESS_TOKEN",
    "GET",
    "获取指定的应用详情。企业仅可获取当前凭证对应的应用；"
    "第三方仅可获取被授权的应用。"
)
WXWORK_SET_AGENT = (
    "/cgi-bin/agent/set?access_token=ACCESS_TOKEN",
    "POST",
    "设置应用。仅企业可调用，可设置当前凭证对应的应用；"
    "第三方以及代开发自建应用不可调用。"
)
WXWORK_LIST_AGENT = (
    "/cgi-bin/agent/list?access_token=ACCESS_TOKEN",
    "GET",
    "获取 access_token 对应的应用列表。"
    "企业仅可获取当前凭证对应的应用；"
    "第三方仅可获取被授权的应用。"
)
WXWORK_CREATE_MENU = (
    "/cgi-bin/menu/create?access_token=ACCESS_TOKEN",
    "POST",
    "创建菜单。仅企业可调用；第三方不可调用。"
)
WXWORK_GET_MENU = (
    "/cgi-bin/menu/get?access_token=ACCESS_TOKEN",
    "GET",
    "获取菜单。仅企业可调用；第三方不可调用。"
)
WXWORK_DELETE_MENU = (
    "/cgi-bin/menu/delete?access_token=ACCESS_TOKEN",
    "GET",
    "删除菜单。仅企业可调用；第三方不可调用。"
)
WXWORK_SEND_APP_MESSAGE = (
    "/cgi-bin/message/send?access_token=ACCESS_TOKEN",
    "POST",
    "发送应用消息。应用支持推送文本、图片、视频、文件、图文等类型。"
    "如果部分接收人无权限或不存在，发送仍然执行，"
    "但会返回无效的部分（即 `invaliduser` 或 `invalidparty` "
    "或 `invalidtag` 或 `unlicenseduser`），"
    "常见的原因是接收人不在应用的可见范围内。"
    "权限包含应用可见范围和基础接口权限(基础账号、互通账号均可)，"
    "`unlicenseduser` 中的用户在应用可见范围内但没有基础接口权限。"
    "如果全部接收人无权限或不存在，则本次调用返回失败，`errcode` 为 81013。"
    "返回包中的 `userid`，不区分大小写，统一转为小写。"
)
WXWORK_RECALL_MESSAGE = (
    "/cgi-bin/message/recall?access_token=ACCESS_TOKEN",
    "POST",
    "撤回应用消息。本接口可以撤回 24 小时内通过发送应用消息接口推送的消息，"
    "仅可撤回企业微信端的数据，微信插件端的数据不支持撤回。"
)
WXWORK_GET_MEDIA = (
    "/cgi-bin/media/get?access_token=ACCESS_TOKEN",
    "GET",
    "获取临时素材。异步上传临时素材获取到的 `media_id`，"
    "超过 20M 需使用 Range 分块下载，且分块大小不超过 20M，"
    "否则返回错误码 830002；其他 `media_id`，若文件过大则返回错误码 830002，"
    "需使用 Range 分块下载，建议分块大小不超过 20M。"
)
WXWORK_GET_USER_INFO = (
    "/cgi-bin/auth/getuserinfo?access_token=ACCESS_TOKEN",
    "GET",
    "获取访问用户身份。该接口用于根据 code 获取成员信息。"
    "跳转的域名须完全匹配 `access_token` 对应应用的可信域名，"
    "否则会返回 50001 错误。"
)
WXWORK_GET_USER_DETAIL = (
    "/cgi-bin/auth/getuserdetail?access_token=ACCESS_TOKEN",
    "POST",
    "获取访问用户敏感信息。"
    "自建应用与代开发应用可通过该接口获取成员授权的敏感字段。"
    "成员必须在应用的可见范围内。"
)
WXWORK_GET_TICKET = (
    "/cgi-bin/ticket/get?access_token=ACCESS_TOKEN",
    "GET",
    "获取电子发票 ticket。"
)
WXWORK_GET_JSAPI_TICKET = (
    "/cgi-bin/get_jsapi_ticket?access_token=ACCESS_TOKEN",
    "GET",
    "获取企业的 jsapi_ticket。生成签名之前必须先了解一下 jsapi_ticket，"
    "jsapi_ticket 是 H5 应用调用企业微信 JS 接口的临时票据。"
    "正常情况下，jsapi_ticket 的有效期为 7200 秒，"
    "通过 `access_token` 来获取。"
    "由于获取 jsapi_ticket 的 api 调用次数非常有限"
    "（一小时内，一个企业最多可获取 400 次，且单个应用不能超过 100 次），"
    "频繁刷新 jsapi_ticket 会导致 api 调用受限，"
    "影响自身业务，开发者必须在自己的服务全局缓存 jsapi_ticket。"
)
WXWORK_GET_CHECKIN_OPTION = (
    "/cgi-bin/checkin/getcheckinoption?"
    "access_token=ACCESS_TOKEN",
    "POST",
    "获取员工打卡规则。自建应用、第三方应用和代开发应用可使用此接口，"
    "获取可见范围内指定员工指定日期的打卡规则。"
)
WXWORK_GET_CHECKIN_DATA = (
    "/cgi-bin/checkin/getcheckindata?"
    "access_token=ACCESS_TOKEN",
    "POST",
    "获取打卡记录数据。应用可通过本接口，"
    "获取可见范围内员工指定时间段内的打卡记录数据。"
)
WXWORK_GET_APPROVAL_DATA = (
    "/cgi-bin/corp/getapprovaldata?access_token=ACCESS_TOKEN",
    "POST",
    "获取审批数据（旧）。"
    "提示：推荐使用新接口 \"批量获取审批单号\" 及 \"获取审批申请详情\"，"
    "此接口后续将不再维护、逐步下线。通过本接口来获取公司一段时间内的审批记录。"
    "一次拉取调用最多拉取 100 个审批记录，可以通过多次拉取的方式来满足需求，"
    "但调用频率不可超过 600次/分。"
)
WXWORK_GET_INVOICE_INFO = (
    "/cgi-bin/card/invoice/reimburse/getinvoiceinfo?"
    "access_token=ACCESS_TOKEN",
    "POST",
    "查询电子发票。报销方在获得用户选择的电子发票标识参数后，"
    "可以通过该接口查询电子发票的结构化信息，并获取发票 PDF 文件。"
)
WXWORK_UPDATE_INVOICE_STATUS = (
    "/cgi-bin/card/invoice/reimburse/updateinvoicestatus?"
    "access_token=ACCESS_TOKEN",
    "POST",
    "更新发票状态。报销企业和报销服务商可以通过该接口对某一张发票进行锁定、"
    "解锁和报销操作。各操作的业务含义及在用户端的表现如下："
    "锁定：电子发票进入了企业的报销流程时应该执行锁定操作，"
    "执行锁定操作后的电子发票仍然会存在于用户卡包内，但无法重复提交报销。"
    "解锁：当电子发票由于各种原因，无法完成报销流程时，应执行解锁操作。"
    "执行锁定操作后的电子发票将恢复可以被提交的状态。"
    "报销：当电子发票报销完成后，应该使用本接口执行报销操作。"
    "执行报销操作后的电子发票将从用户的卡包中移除，"
    "用户可以在卡包的消息中查看到电子发票的核销信息。"
    "注意，报销为不可逆操作，请开发者慎重调用。"
)
WXWORK_UPDATE_INVOICE_STATUS_BATCH = (
    "/cgi-bin/card/invoice/reimburse/updatestatusbatch?"
    "access_token=ACCESS_TOKEN",
    "POST",
    "批量更新发票状态。发票平台可以通过该接口对某个成员的一批发票进行锁定、"
    "解锁和报销操作。"
    "注意，报销状态为不可逆状态，请开发者慎重调用。"
)
WXWORK_GET_INVOICE_INFO_BATCH = (
    "/cgi-bin/card/invoice/reimburse/getinvoiceinfobatch?"
    "access_token=ACCESS_TOKEN",
    "POST",
    "批量查询电子发票。报销方在获得用户选择的电子发票标识参数后，"
    "可以通过该接口批量查询电子发票的结构化信息。"
)
WXWORK_CREATE_APPCHAT = (
    "/cgi-bin/appchat/create?access_token=ACCESS_TOKEN",
    "POST",
    "创建群聊会话。只允许企业自建应用调用，且应用的可见范围必须是根部门。"
    "群成员人数不可超过管理端配置的 \"群成员人数上限\"，"
    "且最大不可超过 2000 人。"
    "每企业创建群数不可超过 1000/天。"
)
WXWORK_GET_APPCHAT = (
    "/cgi-bin/appchat/get?access_token=ACCESS_TOKEN",
    "GET",
    "获取群聊会话。只允许企业自建应用调用，且应用的可见范围必须是根部门；"
    "`chatid` 所代表的群必须是该应用所创建；第三方不可调用。"
)
WXWORK_UPDATE_APPCHAT = (
    "/cgi-bin/appchat/update?access_token=ACCESS_TOKEN",
    "POST",
    "修改群聊会话。只允许企业自建应用调用，且应用的可见范围必须是根部门。"
    "`chatid` 所代表的群必须是该应用所创建。群成员人数不可超过 2000 人。"
    "每企业变更群的次数不可超过 1000次/小时。"
)
WXWORK_SEND_APPCHAT_MASSAGE = (
    "/cgi-bin/appchat/send?access_token=ACCESS_TOKEN",
    "POST",
    "应用推送消息。应用支持推送文本、图片、视频、文件、图文等类型。"
    "只允许企业自建应用调用，且应用的可见范围必须是根部门。"
    "`chatid` 所代表的群必须是该应用所创建。"
    "每企业消息发送量不可超过 2万人次/分（若群有 100 人，每发一次消息算 100 人次）。"
    "未认证或小型企业不可超过 15万人次/小时；中型企业不可超过 35万人次/小时；"
    "大型企业不可超过 70万人次/小时。出于对成员的保护，"
    "每个成员在群中收到的同一个应用的消息不可超过 200条/分，1万条/天，超过会被丢弃，"
    "而接口不会报错。（若应用创建了两个群，成员张三同时在这两个群中，"
    "应用往第一个群发送 1 条消息，再往第二个群发送 2 条消息，"
    "则张三累计收到该应用 3 条消息）。"
)
WXWORK_GET_CODE_TO_SESSION_KEY = (
    "/cgi-bin/miniprogram/jscode2session?"
    "access_token=ACCESS_TOKEN",
    "GET",
    "code2Session。临时登录凭证校验接口是一个服务端 HTTPS 接口，"
    "开发者服务器使用临时登录凭证 code 获取 `session_key`、"
    "用户 `userid` 以及用户所在企业的 `corpid` 等信息。"
)
WXWORK_SET_AGENT_SCOPE = (
    "/cgi-bin/agent/set_scope?access_token=ACCESS_TOKEN",
    "POST",
    "设置授权应用可见范围。调用该接口前提是开启通讯录迁移，"
    "收到授权成功通知后可调用。"
    "企业注册初始化安装应用后，应用默认可见范围为根部门。"
    "如需修改应用可见范围，服务商可以调用该接口设置授权应用的可见范围。"
    "该接口只能使用注册完成回调事件或者查询注册状态返回的 `access_token`，"
    "调用设置通讯录同步完成后或者 `access_token` 超过 30 分钟失效"
    "（即解除通讯录锁定状态）则不能继续调用该接口。"
)
WXWORK_CONTACT_SYNC_SUCCESS = (
    "/cgi-bin/sync/contact_sync_success?"
    "access_token=ACCESS_TOKEN",
    "GET",
    "设置通讯录同步完成。该 API 用于设置通讯录同步完成，"
    "解除通讯录锁定状态，同时使通讯录迁移 `access_token` 失效。"
)


def search_apis(kw=None) -> list or str:
    """
        在【当前模块】的 `__init__.py` 文件
        中定义的 API【端点】中进行搜索。

        该函数负责在预先定义的 API 端点集合
        中查找包含特定关键字的端点。

        它主要用于开发人员在进行接口对接时快速定位相关 API。

        注意:
            - 搜索是基于【正则表达式】进行的，
              因此可以使用正则表达式语法来改善搜索精度。

            - 返回的列表中每个端点都是一个【字典】，
              格式为 `{ 端点名: 端点详情 }`。

            - 【端点详情】是一个包含 URL 路径和其他可能信息
              （如请求方法）的列表。

            - 如果搜索没有结果，会提供一条提示信息，
              并建议检查输入或拼写，或查阅官方文档。

    :param kw: (str, 可选) 用于搜索端点名称的关键字，
    不区分大小写。如果未提供，则返回所有端点。
    :return: 如果提供关键字，则返回一个匹配该关键字的端点列表；
    如果未提供关键字，则返回所有端点。
    如果没有找到任何匹配项，将返回一条提示信息。
    """
    # 获取【当前包名】
    # `__name__` 代表的是当前模块 `wxapis`
    # `__name__.split(r".")` 的值为 `["wxapis"]`
    # `module` 值为
    # `<module 'wxapis' from
    # 'E:\\wxapis\\wxapis\\__init__.py'>`
    # 其具体含义表示为：
    # 当导入一个模块时，py 会创建一个包含有关该模块的信息的【模块对象】
    # 通常情况下
    # py 中每个包（package）目录下都会有一个 `__init__.py` 文件
    # 当导入一个包时，py 会先运行该目录下的 `__init__.py` 文件
    # 在这种情况下，`__init__.py` 文件所在的目录被作为一个 py 包来处理
    module = sys.modules[__name__.split(r".")[0]]
    # 如果提供【关键字】
    # 则编译成正则表达式以进行【大小写不敏感搜索】
    if kw:
        # 在正则表达式末尾添加 `\b`
        # 这代表【单词边界】
        # 这样只会匹配后面没有其他单词字符
        # （如字母、数字或下划线）的情况
        pattern = re.compile(
            re.escape(kw) + r"\b",
            re.IGNORECASE
        )
    else:
        pattern = None
    endpoints = [
        {name: value}
        for name, value in vars(module).items()
        if
        isinstance(value, tuple)
        # 使用位置参数 `value[0]` 检查路径而非变量名
        and (not pattern or pattern.search(value[0]))
    ]
    tips = f"未找到关键字 \"{kw}\" 所在的项，" \
           f"请仔细检查输入或者拼写是否有问题。" \
           f"如果还是不能工作，请查阅企业微信 API 官方文档" \
           f"（https://developer.work.weixin.qq.com/document/path/90556）。"
    return endpoints or tips
