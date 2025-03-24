# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import Datetime, Status, UserGender, UserID, UserLevel, UserOAuth


@dataclass
class UserBasic(DataClassJsonMixin):
    """
    用户基础信息

    :param str nickname: 昵称
    :param str avatar: 头像Url
    :param UserID id: 用户ID
    """

    nickname: str
    avatar: str
    id: UserID


@dataclass
class UserBrief(UserBasic):
    """
    用户简要信息

    :param str nickname: 昵称
    :param str avatar: 头像
    :param UserLevel level: 等级
    :param str description: 描述
    :param UserGender gender: 性别
    :param UserID id: 用户ID
    """

    level: UserLevel
    description: str
    gender: UserGender


@dataclass
class User(UserBasic):
    """
    用户信息

    :param str nickname: 昵称
    :param str avatar: 头像
    :param str description: 描述
    :param UserGender gender: 性别
    :param UserID id: 用户ID
    :param Status status: 状态
    :param int self_deck_count: 自己的卡组数
    :param int mark_contribution_count: 标记贡献数
    :param int deck_count: 卡组数
    """

    description: str
    gender: UserGender
    status: Status
    self_deck_count: int
    mark_contribution_count: int
    deck_count: int


@dataclass
class Profile(UserBrief):
    """
    用户简介

    :param str nickname: 昵称
    :param str avatar: 头像
    :param UserLevel level: 等级
    :param str email: 邮箱
    :param bool email_verified: 邮箱是否验证
    :param str phone: 手机号
    :param bool phone_verified: 手机号是否验证
    :param Sequence[UserOAuth] oauths: OAuth信息
    :param UserGender gender: 性别
    :param str city: 城市
    :param str school: 学校
    :param str description: 描述
    :param str constellation: 星座 (暂无)
    :param dict alipay_oauth: 支付宝信息 (暂无)
    :param UserID id: 用户ID
    :param Datetime birthday: 生日
    """

    email: str
    email_verified: bool
    phone: str
    phone_verified: bool
    oauths: Sequence[UserOAuth]
    city: str
    school: str
    constellation: str
    alipay_oauth: dict
    birthday: Datetime = Datetime._field()


@dataclass
class Collaborator(UserBrief):
    """
    协作者

    :param str nickname: 昵称
    :param str avatar: 头像
    :param UserLevel level: 等级
    :param str description: 描述
    :param UserGender gender: 性别
    :param UserID id: 用户ID
    :param bool is_collaborator: 是否是协作者
    """

    is_collaborator: bool
