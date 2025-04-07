import arrow

from django.test import TestCase

from main.utils import get_time_from_file_stem, get_frame_stems_in_range


FPS = 12
VIDEO_SECONDS = 30
API_CALL_SECONDS = 30


class UtilsTestCase(TestCase):
    def test_get_time_from_file_stem(self):
        file_stem = '20250405_223006-0014'
        result = get_time_from_file_stem(file_stem)

        expected = arrow.get('2025-04-05T22:30:06').shift(seconds=14 / 12)
        self.assertEqual(result, expected)

    def test_get_frame_stems_in_range(self):
        key_frame_stem = '20250405_223006-0012'  # 第 1 秒的第 12 幀

        stems = get_frame_stems_in_range(
            key_frame_stem=key_frame_stem,
            fps=FPS,
            seconds=VIDEO_SECONDS
        )

        self.assertEqual(len(stems), FPS * VIDEO_SECONDS)
        # 向前移一輪（上一段時間）
        self.assertTrue(stems[0].startswith('20250405_222951'))
        self.assertTrue(stems[0].endswith('-0193'))
        # 後面應該還在這一段
        self.assertTrue(stems[-1].startswith('20250405_223006'))
        self.assertTrue(stems[-1].endswith('-0192'))
