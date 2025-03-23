"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import Datetime, UserGender, UserID, UserLevel, UserOAuth


@dataclass
class Profile(DataClassJsonMixin):
    """
    Profile 用户信息

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

    nickname: str
    avatar: str
    level: UserLevel
    email: str
    email_verified: bool
    phone: str
    phone_verified: bool
    oauths: Sequence[UserOAuth]
    gender: UserGender
    city: str
    school: str
    description: str
    constellation: str
    alipay_oauth: dict
    id: UserID
    birthday: Datetime = Datetime._field()
