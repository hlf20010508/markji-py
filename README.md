# markji-py
墨墨记忆卡-Markji Python SDK

文档： https://hlf20010508.github.io/markji-py/

## 依赖
- python >= 3.11
- aiohttp >= 3.11.14
- dataclasses-json >= 0.6.7

## 安装
```sh
pip install markji
```

## 示例
```py
import asyncio
from markji import Markji
from markji.auth import Auth
from markji.editor import AnswerLine, AudioBuilder, ParagraphBuilder
from markji.types import LanguageCode

username = "xxxx"
password = "xxxx"


async def main():
    auth = Auth(username, password)
    token = await auth.login()
    client = Markji(token)

    folder_name = "xxxx"
    folders = await client.list_folders()
    for folder in folders:
        if folder.name == folder_name:
            break

    deck_name = "xxxx"
    decks = await client.list_decks(folder.id)
    for deck in decks:
        if deck.name == deck_name:
            break

    chapters = await client.list_chapters(deck.id)
    chapter = chapters[0]

    content = []

    word = "English"
    tts = await client.tts(word, LanguageCode.EN_US)
    word = ParagraphBuilder(AudioBuilder(tts.id, word)).heading().build()
    content.append(word)
    content.append(AnswerLine)
    content.append("英语")

    content = "\n".join(content)

    card = await client.new_card(deck.id, chapter.id, content)

    print(card.content)


if __name__ == "__main__":
    asyncio.run(main())
```

输出:
```
[P#H1#[Audio#A,ID/xxxx#English]]
---
英语
```