"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Dict, List, NewType, Optional, Type, TypeVar, cast

# 8位
# eg. 20251234
UserID = NewType("UserID", int)
FolderID = NewType("FolderID", str)
DeckID = NewType("DeckID", str)
ChapterID = NewType("ChapterID", str)
CardID = NewType("CardID", str)
CardRootID = NewType("CardRootID", str)
FileID = NewType("FileID", str)


class UserGender(StrEnum):
    """
    Enum 用户性别

    MALE: 男
    FEMALE: 女
    SECRECY: 保密
    """

    MALE = "MALE"
    FEMALE = "FEMALE"
    SECRECY = "SECRECY"


class Status(StrEnum):
    """
    Enum 文件夹状态

    NORMAL: 正常
    """

    NORMAL = "NORMAL"


class FolderItemObjectClass(StrEnum):
    """
    Enum 文件夹项目对象类

    FOLDER: 文件夹
    DECK: 卡组
    """

    FOLDER = "FOLDER"
    DECK = "DECK"


class DeckSource(StrEnum):
    """
    Enum 卡组来源

    SELF: 自己创建
    FORK: 收藏他人
    """

    SELF = "SELF"
    FORK = "FORK"


class FileSource(StrEnum):
    """
    Enum 文件来源 (语音)

    UPLOAD: 上传
    TTS: 语音合成
    """

    UPLOAD = "UPLOAD"
    TTS = "TTS"


class LanguageCode(StrEnum):
    """
    Enum 语言代码
    """

    AR_DZ = "ar-DZ"
    AR_AE = "ar-AE"
    AR_EG = "ar-EG"
    AR_BH = "ar-BH"
    AR_QA = "ar-QA"
    AR_KW = "ar-KW"
    AR_LY = "ar-LY"
    AR_MA = "ar-MA"
    AR_SA = "ar-SA"
    AR_TN = "ar-TN"
    AR_SY = "ar-SY"
    AR_YE = "ar-YE"
    AR_IQ = "ar-IQ"
    AR_JO = "ar-JO"
    AM_ET = "am-ET"
    GA_IE = "ga-IE"
    ET_EE = "et-EE"
    BG_BG = "bg-BG"
    PL_PL = "pl-PL"
    FA_IR = "fa-IR"
    DA_DK = "da-DK"
    DE_AT = "de-AT"
    DE_DE = "de-DE"
    DE_CH = "de-CH"
    RU_RU = "ru-RU"
    FR_BE = "fr-BE"
    FR_FR = "fr-FR"
    FR_CA = "fr-CA"
    FR_CH = "fr-CH"
    FIL_PH = "fil-PH"
    FI_FI = "fi-FI"
    KM_KH = "km-KH"
    GU_IN = "gu-IN"
    KO_KR = "ko-KR"
    NL_BE = "nl-BE"
    NL_NL = "nl-NL"
    GL_ES = "gl-ES"
    CA_ES = "ca-ES"
    CS_CZ = "cs-CZ"
    HR_HR = "hr-HR"
    LV_LV = "lv-LV"
    LT_LT = "lt-LT"
    RO_RO = "ro-RO"
    MT_MT = "mt-MT"
    MR_IN = "mr-IN"
    MS_MY = "ms-MY"
    BN_BD = "bn-BD"
    MY_MM = "my-MM"
    AF_ZA = "af-ZA"
    NB_NO = "nb-NO"
    PT_BR = "pt-BR"
    PT_PT = "pt-PT"
    JA_JP = "ja-JP"
    SV_SE = "sv-SE"
    SK_SK = "sk-SK"
    SL_SI = "sl-SI"
    SW_KE = "sw-KE"
    SW_TZ = "sw-TZ"
    SO_SO = "so-SO"
    TE_IN = "te-IN"
    TA_LK = "ta-LK"
    TA_SG = "ta-SG"
    TA_IN = "ta-IN"
    TH_TH = "th-TH"
    TR_TR = "tr-TR"
    CY_GB = "cy-GB"
    UR_PK = "ur-PK"
    UR_IN = "ur-IN"
    UK_UA = "uk-UA"
    UZ_UZ = "uz-UZ"
    ES_NI = "es-NI"
    ES_AR = "es-AR"
    ES_PY = "es-PY"
    ES_PA = "es-PA"
    ES_PR = "es-PR"
    ES_BO = "es-BO"
    ES_GQ = "es-GQ"
    ES_DO = "es-DO"
    ES_EC = "es-EC"
    ES_CO = "es-CO"
    ES_CR = "es-CR"
    ES_CU = "es-CU"
    ES_HN = "es-HN"
    ES_US = "es-US"
    ES_PE = "es-PE"
    ES_MX = "es-MX"
    ES_SV = "es-SV"
    ES_GT = "es-GT"
    ES_VE = "es-VE"
    ES_UY = "es-UY"
    ES_ES = "es-ES"
    ES_CL = "es-CL"
    HE_IL = "he-IL"
    EL_GR = "el-GR"
    HU_HU = "hu-HU"
    SU_ID = "su-ID"
    IT_IT = "it-IT"
    HI_IN = "hi-IN"
    ID_ID = "id-ID"
    EN_IE = "en-IE"
    EN_AU = "en-AU"
    EN_PH = "en-PH"
    EN_CA = "en-CA"
    EN_KE = "en-KE"
    EN_US = "en-US"
    EN_ZA = "en-ZA"
    EN_NG = "en-NG"
    EN_TZ = "en-TZ"
    EN_HK = "en-HK"
    EN_SG = "en-SG"
    EN_NZ = "en-NZ"
    EN_IN = "en-IN"
    EN_GB = "en-GB"
    VI_VN = "vi-VN"
    JV_ID = "jv-ID"
    ZH_CN = "zh-CN"
    ZH_TW = "zh-TW"
    ZH_HK = "zh-HK"
    ZU_ZA = "zu-ZA"


class FileMIME(StrEnum):
    """
    Enum 文件MIME类型

    AUDIO_MPEG: 音频
    IMAGE_JPEG: 图片
    """

    AUDIO_MPEG = "audio/mpeg"
    IMAGE_JPEG = "image/jpeg"


A = TypeVar("A", bound="UserLevel")


@dataclass
class UserLevel:
    """
    Enum
    用户等级

    :param level: 等级
    :param description: 等级描述
    """

    level: int
    description: str

    @classmethod
    def _from_json(cls: Type[A], data: Optional[Dict]) -> Optional[A]:
        if data is None:
            return None

        level = cast(int, data.get("level"))
        description = cast(str, data.get("level_description"))

        if level or description:
            return cls(level=level, description=description)
        else:
            return None


B = TypeVar("B", bound="UserOAuth")


@dataclass
class UserOAuth:
    """
    用户授权

    :param type: 授权类型
    :param appid: 授权AppID
    :param username: 用户名
    """

    type: str
    appid: str
    username: str

    @classmethod
    def _from_json(cls: Type[B], data: Optional[Dict]) -> Optional[B]:
        if data is None:
            return None

        type = cast(str, data.get("type"))
        appid = cast(str, data.get("appid"))
        username = cast(str, data.get("username"))

        if type or appid or username:
            return cls(type=type, appid=appid, username=username)
        else:
            return None


C = TypeVar("C", bound="UserBrief")


@dataclass
class UserBrief:
    """
    用户简要信息

    :param nickname: 昵称
    :param avatar: 头像Url
    :param id: 用户ID
    """

    nickname: str
    avatar: str
    id: UserID

    @classmethod
    def _from_json(cls: Type[C], data: Optional[Dict]) -> Optional[C]:
        if data is None:
            return None

        nickname = cast(str, data.get("nickname"))
        avatar = cast(str, data.get("avatar"))
        id = cast(UserID, data.get("id"))

        if nickname or avatar or id:
            return cls(nickname=nickname, avatar=avatar, id=id)
        else:
            return None


D = TypeVar("D", bound="FolderItem")


@dataclass
class FolderItem:
    """
    FolderItems 文件夹项目

    :param object_id: 对象ID
    :param object_class: 对象类
    """

    object_id: str
    object_class: FolderItemObjectClass

    @classmethod
    def _from_json(cls: Type[D], data: Optional[Dict]) -> Optional[D]:
        if data is None:
            return None

        object_id = cast(str, data.get("object_id"))
        object_class = FolderItemObjectClass(data.get("object_class"))

        if object_id or object_class:
            return cls(object_id=object_id, object_class=object_class)
        else:
            return None


E = TypeVar("E", bound="DeckAccessSetting")


@dataclass
class DeckAccessSetting:
    """
    卡组访问设置

    :param validation_enabled: 是否启用验证
    """

    validation_enabled: bool

    @classmethod
    def _from_json(cls: Type[E], data: Optional[Dict]) -> Optional[E]:
        if data is None:
            return None

        validation_enabled = cast(bool, data.get("validation_enabled"))

        if validation_enabled:
            return cls(
                validation_enabled=validation_enabled,
            )
        else:
            return None


F = TypeVar("F", bound="TTSInfo")


@dataclass
class TTSInfo:
    """
    语音合成信息

    :param text: 文本
    :param locale: 语言代码
    """

    text: str
    locale: LanguageCode

    @classmethod
    def _from_json(cls: Type[F], data: Optional[Dict]) -> Optional[F]:
        if data is None:
            return None

        text = cast(str, data.get("text"))
        locale = LanguageCode(data.get("locale"))

        if text or locale:
            return cls(text=text, locale=locale)
        else:
            return None


G = TypeVar("G", bound="FileInfo")


@dataclass
class FileInfo:
    """
    文件信息

    :param source: 文件来源 (语音)
    :param content_slices: 语音合成信息
    :param width: 宽度 (图片)
    :param height: 高度 (图片)
    :param description: 描述 (图片)
    """

    source: Optional[FileSource]
    content_slices: Optional[List[TTSInfo]]
    width: Optional[int]
    height: Optional[int]
    description: Optional[str]

    @classmethod
    def _from_json(cls: Type[G], data: Optional[Dict]) -> Optional[G]:
        if data is None:
            return None

        source = data.get("source")
        if source is not None:
            source = FileSource(source)
        content_slices = [
            cast(TTSInfo, TTSInfo._from_json(tts_info))
            for tts_info in cast(List, data.get("content_slices", []))
        ]
        width = cast(int, data.get("width"))
        height = cast(int, data.get("height"))
        description = cast(str, data.get("description"))

        if source or content_slices or width or height or description:
            return cls(
                source=source,
                content_slices=content_slices,
                width=width,
                height=height,
                description=description,
            )
        else:
            return None


H = TypeVar("H", bound="File")


@dataclass
class File:
    """
    文件

    :param info: 文件信息
    :param size: 文件大小
    :param mime: MIME类型
    :param url: 文件Url
    :param id: 文件ID
    :param expire_time: 过期时间
    """

    info: FileInfo
    size: int
    mime: FileMIME
    url: str
    id: FileID
    expire_time: datetime

    @classmethod
    def _from_json(cls: Type[H], data: Optional[Dict]) -> Optional[H]:
        if data is None:
            return None

        info = cast(FileInfo, FileInfo._from_json(data.get("info")))
        size = cast(int, data.get("size"))
        mime = FileMIME(data.get("mime"))
        url = cast(str, data.get("url"))
        id = cast(FileID, data.get("id"))
        expire_time = datetime.fromisoformat(cast(str, data.get("expire_time")))

        return cls(
            info=info,
            size=size,
            mime=mime,
            url=url,
            id=id,
            expire_time=expire_time,
        )
