"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import Sequence
from markji.types import _Datetime, UserGender, UserID, UserLevel, UserOAuth


@dataclass
class Profile(DataClassJsonMixin):
    """
    Profile 用户信息

    :param nickname: 昵称
    :param avatar: 头像Url
    :param level: 用户等级信息
    :param email: 邮箱
    :param email_verified: 邮箱是否验证
    :param phone: 手机号
    :param phone_verified: 手机号是否验证
    :param oauths: 第三方登录信息
    :param gender: 性别
    :param city: 城市
    :param school: 学校
    :param birthday: 生日
    :param description: 个人描述
    :param constellation: 星座 (暂无)
    :param alipay_oauth: 支付宝信息 (暂无)
    :param id: 用户ID
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
    birthday: _Datetime = _Datetime._field()
