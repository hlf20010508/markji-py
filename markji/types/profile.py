"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Type, cast
from markji.types import _Datetime, UserGender, UserID, UserLevel, UserOAuth


@dataclass
class Profile:
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
    birthday: _Datetime
    description: str
    constellation: str
    alipay_oauth: dict
    id: UserID

    @classmethod
    def _from_json(cls: Type[Profile], data: dict) -> Profile:
        """
        从 JSON 数据创建 Profile 对象

        :param data: JSON 数据
        :return: Profile
        """

        nickname = cast(str, data.get("nickname"))
        avatar = cast(str, data.get("avatar"))
        level = cast(UserLevel, UserLevel._from_json(cast(dict, data.get("level"))))
        email = cast(str, data.get("email"))
        email_verified = cast(bool, data.get("email_verified"))
        phone = cast(str, data.get("phone"))
        phone_verified = cast(bool, data.get("phone_verified"))
        oauths = [
            cast(UserOAuth, UserOAuth._from_json(oauth))
            for oauth in cast(Sequence, data.get("oauths"))
        ]
        gender = UserGender(data.get("gender"))
        city = cast(str, data.get("city"))
        school = cast(str, data.get("school"))
        birthday = _Datetime.fromisoformat(cast(str, data.get("birthday")))
        description = cast(str, data.get("description"))
        constellation = cast(str, data.get("constellation"))
        alipay_oauth = cast(dict, data.get("alipay_oauth"))
        id = cast(UserID, data.get("id"))

        return cls(
            nickname=nickname,
            avatar=avatar,
            level=level,
            email=email,
            email_verified=email_verified,
            phone=phone,
            phone_verified=phone_verified,
            oauths=oauths,
            gender=gender,
            city=city,
            school=school,
            birthday=birthday,
            description=description,
            constellation=constellation,
            alipay_oauth=alipay_oauth,
            id=id,
        )
