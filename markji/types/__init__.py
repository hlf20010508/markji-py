"""
:project: markji-py
:author: L-ING
:copyright: (C) 2025 L-ING <hlf01@icloud.com>
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from datetime import datetime
from enum import StrEnum
from typing import Sequence, NewType, Type

# 8位
# eg. 20251234
UserID = NewType("UserID", int)
FolderID = NewType("FolderID", str)
DeckID = NewType("DeckID", str)
ChapterID = NewType("ChapterID", str)
ChapterSetID = NewType("ChapterSetID", str)
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


class _Datetime(datetime):
    def _to_str(self) -> str:
        # 2025-12-34T12:34:56.789Z
        return self.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    @classmethod
    def _field(cls: Type[_Datetime]):
        # default serialize and deserialize methods
        return field(
            metadata=config(encoder=lambda dt: dt._to_str(), decoder=cls.fromisoformat),
        )


@dataclass
class UserLevel(DataClassJsonMixin):
    """
    Enum
    用户等级

    :param level: 等级
    :param description: 等级描述
    """

    level: int
    description: str


@dataclass
class UserOAuth(DataClassJsonMixin):
    """
    用户授权

    :param type: 授权类型
    :param appid: 授权AppID
    :param username: 用户名
    """

    type: str
    appid: str
    username: str


@dataclass
class UserBrief(DataClassJsonMixin):
    """
    用户简要信息

    :param nickname: 昵称
    :param avatar: 头像Url
    :param id: 用户ID
    """

    nickname: str
    avatar: str
    id: UserID


@dataclass
class FolderItem(DataClassJsonMixin):
    """
    FolderItems 文件夹项目

    :param object_id: 对象ID
    :param object_class: 对象类
    """

    object_id: str
    object_class: FolderItemObjectClass


@dataclass
class DeckAccessSetting(DataClassJsonMixin):
    """
    卡组访问设置

    :param validation_enabled: 是否启用验证
    """

    validation_enabled: bool


@dataclass
class TTSInfo(DataClassJsonMixin):
    """
    语音合成信息

    :param text: 文本
    :param locale: 语言代码
    """

    text: str
    locale: LanguageCode


@dataclass
class FileInfo(DataClassJsonMixin):
    """
    文件信息

    :param source: 文件来源 (语音)
    :param content_slices: 语音合成信息
    :param width: 宽度 (图片)
    :param height: 高度 (图片)
    :param description: 描述 (图片)
    """

    source: FileSource | None = None
    content_slices: Sequence[TTSInfo] | None = None
    width: int | None = None
    height: int | None = None
    description: str | None = None


@dataclass
class File(DataClassJsonMixin):
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
    expire_time: _Datetime = _Datetime._field()
