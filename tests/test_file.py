# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

from email.mime import audio
from typing import cast
import unittest
from PIL import Image
import os
import wave
import struct
from markji.types import AudioInfo, FileSource, ImageInfo, LanguageCode, TTSInfo
from tests import AsyncTestCase, ENV
from markji import Markji
from markji.auth import Auth


class TestFile(AsyncTestCase):
    async def test_upload(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        image_path = "test_image.jpeg"
        image_size = (256, 256)
        image = Image.new("RGB", image_size)
        image.save(image_path)

        file = await client.upload_file(image_path)
        image_info = cast(ImageInfo, file.info)

        self.assertEqual((image_info.width, image_info.height), image_size)

        with open(image_path, "rb") as f:
            file = await client.upload_file(f)
        image_info = cast(ImageInfo, file.info)

        self.assertEqual((image_info.width, image_info.height), image_size)

        os.remove(image_path)

        audio_path = "test_audio.mp3"
        with wave.open(audio_path, "w") as wf:
            wf.setparams((44100, 1, 2, 1, "NONE", "not compressed"))
            wf.writeframes(struct.pack("<h", 0))

        file = await client.upload_file(audio_path)
        audio_info = cast(AudioInfo, file.info)

        self.assertEqual(audio_info.source, FileSource.UPLOAD)

        with open(audio_path, "rb") as f:
            file = await client.upload_file(f)

        self.assertEqual(audio_info.source, FileSource.UPLOAD)

        os.remove(audio_path)

    async def test_tts(self):
        auth = Auth(ENV.username, ENV.password)
        token = await auth.login()
        client = Markji(token)

        text = "Hello, world!"
        file = await client.tts(text, LanguageCode.EN_US)
        tts_info = cast(TTSInfo, file.info)

        self.assertEqual(tts_info.source, FileSource.TTS)
        self.assertTrue(len(tts_info.content_slices) > 0)
        self.assertEqual(tts_info.content_slices[0].text, text)

        file = await client.tts(text, "en-US")

        self.assertEqual(tts_info.source, FileSource.TTS)


if __name__ == "__main__":
    unittest.main()
