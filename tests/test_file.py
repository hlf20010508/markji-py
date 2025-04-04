# :project: markji-py
# :author: L-ING
# :copyright: (C) 2025 L-ING <hlf01@icloud.com>
# :license: MIT, see LICENSE for more details.

import json
import os
import struct
import unittest
import wave
from typing import cast

from PIL import Image

from markji.types import (
    AudioInfo,
    FileSource,
    ImageInfo,
    LanguageCode,
    MaskItem,
    TTSInfo,
)
from tests import AsyncTestCase


class TestFile(AsyncTestCase):
    async def test_upload(self):
        image_path = "test_image.jpeg"
        image_size = (256, 256)
        image = Image.new("RGB", image_size)
        image.save(image_path)
        self.addCleanup(os.remove, image_path)

        file = await self.client.upload_file(image_path)
        image_info = cast(ImageInfo, file.info)

        self.assertEqual((image_info.width, image_info.height), image_size)

        with open(image_path, "rb") as f:
            file = await self.client.upload_file(f)
        image_info = cast(ImageInfo, file.info)

        self.assertEqual((image_info.width, image_info.height), image_size)

        audio_path = "test_audio.mp3"
        with wave.open(audio_path, "w") as wf:
            wf.setparams((44100, 1, 2, 1, "NONE", "not compressed"))
            wf.writeframes(struct.pack("<h", 0))
        self.addCleanup(os.remove, audio_path)

        file = await self.client.upload_file(audio_path)
        audio_info = cast(AudioInfo, file.info)

        self.assertEqual(audio_info.source, FileSource.UPLOAD)

        with open(audio_path, "rb") as f:
            file = await self.client.upload_file(f)

        self.assertEqual(audio_info.source, FileSource.UPLOAD)

    async def test_tts(self):
        text = "Hello, world!"
        file = await self.client.tts(text, LanguageCode.EN_US)
        tts_info = cast(TTSInfo, file.info)

        self.assertEqual(tts_info.source, FileSource.TTS)
        self.assertTrue(len(tts_info.content_slices) > 0)
        self.assertEqual(tts_info.content_slices[0].text, text)

        file = await self.client.tts(text, "en-US")

        self.assertEqual(tts_info.source, FileSource.TTS)

    async def test_mask(self):
        mask_data = [MaskItem(0, 0, 128, 128, 1)]

        mask = await self.client.upload_mask(mask_data)

        self.assertEqual(mask.mime, "markji/mask")

        mask_data = [
            {
                "top": 128,
                "left": 128,
                "width": 64,
                "height": 64,
                "index": 2,
                "type": "rect",
            }
        ]

        mask = await self.client.upload_mask(mask_data)

        self.assertEqual(mask.mime, "markji/mask")

        mask_path = "mask.msk1"
        with open(mask_path, "w") as f:
            json.dump(mask_data, f)
        self.addCleanup(os.remove, mask_path)

        mask = await self.client.upload_mask(mask_path)

        self.assertEqual(mask.mime, "markji/mask")


if __name__ == "__main__":
    unittest.main()
