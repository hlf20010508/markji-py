# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from __future__ import annotations
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from datetime import datetime
from enum import StrEnum
from typing import Sequence, NewType, Type

Path = NewType("Path", str)
"""路径"""
# 8位 eg. 20251234
UserID = NewType("UserID", int)
"""用户 ID"""
FolderID = NewType("FolderID", str)
"""文件夹 ID"""
DeckID = NewType("DeckID", str)
"""卡组 ID"""
ChapterID = NewType("ChapterID", str)
"""章节 ID"""
ChapterSetID = NewType("ChapterSetID", str)
"""章节集 ID"""
CardID = NewType("CardID", str)
"""卡片 ID"""
CardRootID = NewType("CardRootID", str)
"""卡片根 ID"""
FileID = NewType("FileID", str)
"""文件 ID"""
AccessSettingID = NewType("AccessSettingID", str)
"""访问设置 ID"""


class UserGender(StrEnum):
    """
    Enum 用户性别

    * MALE: 男
    * FEMALE: 女
    * SECRECY: 保密
    """

    MALE = "MALE"
    FEMALE = "FEMALE"
    SECRECY = "SECRECY"


class Status(StrEnum):
    """
    Enum 文件夹状态

    * NORMAL: 正常
    """

    NORMAL = "NORMAL"


class ItemObjectClass(StrEnum):
    """
    Enum 文件夹项目对象类

    * FOLDER: 文件夹
    * DECK: 卡组
    * CARD: 卡片
    """

    FOLDER = "FOLDER"
    DECK = "DECK"
    CARD = "CARD"


class DeckSource(StrEnum):
    """
    Enum 卡组来源

    * SELF: 自己创建
    * FORK: 收藏他人
    """

    SELF = "SELF"
    FORK = "FORK"


class FileSource(StrEnum):
    """
    Enum 文件来源 (语音)

    * UPLOAD: 上传
    * TTS: 语音合成
    """

    UPLOAD = "UPLOAD"
    TTS = "TTS"


class LanguageCode(StrEnum):
    """
    Enum 语言代码

    * AR_DZ: 阿拉伯语 (阿尔及利亚)
    * AR_AE: 阿拉伯语 (阿联酋)
    * AR_EG: 阿拉伯语 (埃及)
    * AR_BH: 阿拉伯语 (巴林)
    * AR_QA: 阿拉伯语 (卡塔尔)
    * AR_KW: 阿拉伯语 (科威特)
    * AR_LY: 阿拉伯语 (利比亚)
    * AR_MA: 阿拉伯语 (摩洛哥)
    * AR_SA: 阿拉伯语 (沙特阿拉伯)
    * AR_TN: 阿拉伯语 (突尼斯)
    * AR_SY: 阿拉伯语 (叙利亚)
    * AR_YE: 阿拉伯语 (也门)
    * AR_IQ: 阿拉伯语 (伊拉克)
    * AR_JO: 阿拉伯语 (约旦)
    * AM_ET: 阿姆哈拉语 (埃塞俄比亚)
    * GA_IE: 爱尔兰语 (爱尔兰)
    * ET_EE: 爱沙尼亚语 (爱沙尼亚)
    * BG_BG: 保加利亚语 (保加利亚)
    * PL_PL: 波兰语 (波兰)
    * FA_IR: 波斯语 (伊朗)
    * DA_DK: 丹麦语 (丹麦)
    * DE_AT: 德语 (奥地利)
    * DE_DE: 德语 (德国)
    * DE_CH: 德语 (瑞士)
    * RU_RU: 俄语 (俄罗斯)
    * FR_BE: 法语 (比利时)
    * FR_FR: 法语 (法国)
    * FR_CA: 法语 (加拿大)
    * FR_CH: 法语 (瑞士)
    * FIL_PH: 菲律宾语 (菲律宾)
    * FI_FI: 芬兰语 (芬兰)
    * KM_KH: 高棉语 (柬埔寨)
    * GU_IN: 古吉拉特语 (印度)
    * KO_KR: 韩语 (韩国)
    * NL_BE: 荷兰语 (比利时)
    * NL_NL: 荷兰语 (荷兰)
    * GL_ES: 加利西亚语 (西班牙)
    * CA_ES: 加泰罗尼亚语 (西班牙)
    * CS_CZ: 捷克语 (捷克)
    * HR_HR: 克罗地亚语 (克罗地亚)
    * LV_LV: 拉脱维亚语 (拉脱维亚)
    * LT_LT: 立陶宛语 (立陶宛)
    * RO_RO: 罗马尼亚语 (罗马尼亚)
    * MT_MT: 马耳他语 (马耳他)
    * MR_IN: 马拉地语 (印度)
    * MS_MY: 马来语 (马来西亚)
    * BN_BD: 孟加拉语 (孟加拉国)
    * MY_MM: 缅甸语 (缅甸)
    * AF_ZA: 南非荷兰语 (南非)
    * NB_NO: 挪威博克马尔语 (挪威)
    * PT_BR: 葡萄牙语 (巴西)
    * PT_PT: 葡萄牙语 (葡萄牙)
    * JA_JP: 日语 (日本)
    * SV_SE: 瑞典语 (瑞典)
    * SK_SK: 斯洛伐克语 (斯洛伐克)
    * SL_SI: 斯洛文尼亚语 (斯洛文尼亚)
    * SW_KE: 斯瓦希里语 (肯尼亚)
    * SW_TZ: 斯瓦希里语 (坦桑尼亚)
    * SO_SO: 索马里语 (索马里)
    * TE_IN: 泰卢固语 (印度)
    * TA_LK: 泰米尔语 (斯里兰卡)
    * TA_SG: 泰米尔语 (新加坡)
    * TA_IN: 泰米尔语 (印度)
    * TH_TH: 泰语 (泰国)
    * TR_TR: 土耳其语 (土耳其)
    * CY_GB: 威尔士语 (英国)
    * UR_PK: 乌尔都语 (巴基斯坦)
    * UR_IN: 乌尔都语 (印度)
    * UK_UA: 乌克兰语 (乌克兰)
    * UZ_UZ: 乌兹别克语 (乌兹别克斯坦)
    * ES_NI: 西班牙语 (尼加拉瓜)
    * ES_AR: 西班牙语 (阿根廷)
    * ES_PY: 西班牙语 (巴拉圭)
    * ES_PA: 西班牙语 (巴拿马)
    * ES_PR: 西班牙语 (波多黎各)
    * ES_BO: 西班牙语 (玻利维亚)
    * ES_GQ: 西班牙语 (赤道几内亚)
    * ES_DO: 西班牙语 (多米尼加共和国)
    * ES_EC: 西班牙语 (厄瓜多尔)
    * ES_CO: 西班牙语 (哥伦比亚)
    * ES_CR: 西班牙语 (哥斯达黎加)
    * ES_CU: 西班牙语 (古巴)
    * ES_HN: 西班牙语 (洪都拉斯)
    * ES_US: 西班牙语 (美国)
    * ES_PE: 西班牙语 (秘鲁)
    * ES_MX: 西班牙语 (墨西哥)
    * ES_SV: 西班牙语 (萨尔瓦多)
    * ES_GT: 西班牙语 (危地马拉)
    * ES_VE: 西班牙语 (委内瑞拉)
    * ES_UY: 西班牙语 (乌拉圭)
    * ES_ES: 西班牙语 (西班牙)
    * ES_CL: 西班牙语 (智利)
    * HE_IL: 希伯来语 (以色列)
    * EL_GR: 希腊语 (希腊)
    * HU_HU: 匈牙利语 (匈牙利)
    * SU_ID: 巽他语 (印度尼西亚)
    * IT_IT: 意大利语 (意大利)
    * HI_IN: 印地语 (印度)
    * ID_ID: 印尼语 (印度尼西亚)
    * EN_IE: 英语 (爱尔兰)
    * EN_AU: 英语 (澳大利亚)
    * EN_PH: 英语 (菲律宾)
    * EN_CA: 英语 (加拿大)
    * EN_KE: 英语 (肯尼亚)
    * EN_US: 英语 (美国)
    * EN_ZA: 英语 (南非)
    * EN_NG: 英语 (尼日利亚)
    * EN_TZ: 英语 (坦桑尼亚)
    * EN_HK: 英语 (香港)
    * EN_SG: 英语 (新加坡)
    * EN_NZ: 英语 (新西兰)
    * EN_IN: 英语 (印度)
    * EN_GB: 英语 (英国)
    * VI_VN: 越南语 (越南)
    * JV_ID: 爪哇语 (印度尼西亚)
    * ZH_CN: 中文 (中国)
    * ZH_TW: 中文 (台湾)
    * ZH_HK: 中文 (香港)
    * ZU_ZA: 祖鲁语 (南非)
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


class _SearchScope(StrEnum):
    """
    Enum 搜索范围

    * ALL: 所有
    * MINE: 我的
    * REFERENCE: 引用（无效果）
    """

    ALL = "ALL"
    MINE = "MINE"
    REFERENCE = "REFERENCE"
    DECK = "DECK"


class Datetime(datetime):
    """
    继承自 `datetime.datetime`
    """

    def _to_str(self) -> str:
        # 2025-12-34T12:34:56.789Z
        return self.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    @classmethod
    def _field(cls: Type[Datetime]):
        # default serialize and deserialize methods
        return field(
            metadata=config(encoder=lambda dt: dt._to_str(), decoder=cls.fromisoformat),
        )

    @classmethod
    def _metadata(cls: Type[Datetime]):
        # default serialize and deserialize methods
        # used when a class is inherited from another class that has a member of this type
        # and called _field() to define default serialize and deserialize methods, which
        # cause `Fields without default values cannot appear after fields with default values`
        return config(encoder=lambda dt: dt._to_str(), decoder=cls.fromisoformat)


@dataclass
class UserLevel(DataClassJsonMixin):
    """
    用户等级

    :param int level: 等级
    :param str description: 等级描述
    """

    level: int
    description: str


@dataclass
class UserOAuth(DataClassJsonMixin):
    """
    用户授权

    :param str type: 授权类型
    :param str appid: 授权AppID
    :param str username: 用户名
    """

    type: str
    appid: str
    username: str


@dataclass
class FolderItem(DataClassJsonMixin):
    """
    文件夹项目

    :param str object_id: 对象ID
    :param ItemObjectClass object_class: 对象类
    """

    object_id: str
    object_class: ItemObjectClass


@dataclass
class DeckAccessSettingBasic(DataClassJsonMixin):
    """
    卡组基本访问设置

    :param bool validation_enabled: 是否启用验证
    """

    validation_enabled: bool


@dataclass
class DeckAccessSettingBrief(DeckAccessSettingBasic):
    """
    卡组简要访问设置

    更改是否可搜索且不启用验证时返回

    :param bool validation_enabled: 是否启用验证
    :id: AccessSettingID id: 访问设置ID
    :param DeckID deck_id: 卡组ID
    :param bool is_private: 是否私有
    :param bool is_searchable: 是否可搜索
    """

    id: AccessSettingID
    deck_id: DeckID
    is_private: bool
    is_searchable: bool


@dataclass
class DeckAccessSettingInfo(DeckAccessSettingBrief):
    """
    卡组访问设置信息

    启用验证但不启用密码时返回

    :param bool validation_enabled: 是否启用验证
    :id: AccessSettingID id: 访问设置ID
    :param DeckID deck_id: 卡组ID
    :param bool is_private: 是否私有
    :param bool is_searchable: 是否可搜索
    :param bool validation_request_access: 是否需要验证
    :param bool validation_password_enabled: 是否启用密码验证
    :param bool validation_redeem_code: 是否启用验证撤回码（暂无）
    """

    validation_request_access: bool
    validation_password_enabled: bool
    validation_redeem_code: bool


@dataclass
class DeckAccessSetting(DeckAccessSettingInfo):
    """
    卡组访问设置

    启用验证密码时返回

    :param bool validation_enabled: 是否启用验证
    :id: AccessSettingID id: 访问设置ID
    :param DeckID deck_id: 卡组ID
    :param bool is_private: 是否私有
    :param bool is_searchable: 是否可搜索
    :param bool validation_request_access: 是否需要验证
    :param bool validation_password_enabled: 是否启用密码验证
    :param bool validation_redeem_code: 是否启用验证撤回码（暂无）
    :param str validation_password: 验证密码
    """

    validation_password: str


@dataclass
class CardReference(DataClassJsonMixin):
    """
    卡片引用

    :param CardRootID id: 对象ID
    :param ItemObjectClass type: 对象类
    """

    id: CardRootID
    type: ItemObjectClass = ItemObjectClass.CARD


@dataclass
class TTSItem(DataClassJsonMixin):
    """
    语音合成项目

    :param str text: 文本
    :param LanguageCode locale: 语言代码
    """

    text: str
    locale: LanguageCode


@dataclass
class MaskInfo(DataClassJsonMixin):
    """
    图片遮罩信息

    全新上传的遮罩不含 description 字段

    :param str description: 描述
    """

    description: str | None = None


@dataclass
class ImageInfo(DataClassJsonMixin):
    """
    图片信息

    :param int width: 宽度
    :param int height: 高度
    :param str description: 描述
    """

    width: int
    height: int
    description: str


@dataclass
class AudioInfo(DataClassJsonMixin):
    """
    音频信息

    :param FileSource source: 文件来源
    """

    source: FileSource


@dataclass
class TTSInfo(AudioInfo):
    """
    语音合成信息

    :param FileSource source: 文件来源
    :param Sequence[TTSItem] content_slices: 语音合成信息
    """

    content_slices: Sequence[TTSItem]


def _select_media_type(info: dict) -> Type[MaskInfo | ImageInfo | AudioInfo | TTSInfo]:
    if "width" in info and "height" in info and "description" in info:
        return ImageInfo
    elif "source" in info:
        if info["source"] == "UPLOAD":
            return AudioInfo
        elif info["source"] == "TTS":
            return TTSInfo

    return MaskInfo


@dataclass
class File(DataClassJsonMixin):
    """
    文件

    :param MaskInfo | ImageInfo | AudioInfo | TTSInfo info: 文件信息
    :param int size: 文件大小
    :param str mime: MIME类型
    :param str url: 文件Url
    :param FileID id: 文件ID
    :param Datetime expire_time: 过期时间
    """

    info: MaskInfo | ImageInfo | AudioInfo | TTSInfo = field(
        metadata=config(decoder=lambda info: _select_media_type(info).from_dict(info))
    )
    size: int
    mime: str
    url: str
    id: FileID
    expire_time: Datetime = Datetime._field()


@dataclass
class MaskItem(DataClassJsonMixin):
    """
    遮罩项目

    :param int top: 顶部位置
    :param int left: 左侧位置
    :param int width: 宽度
    :param int height: 高度
    :param int index: 索引
    :param str type: 类型
    """

    top: int
    left: int
    width: int
    height: int
    index: int
    type: str = "rect"
