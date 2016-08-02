#
# Copyright (c) 2013-2016 BalaBit
# All Rights Reserved.
#

import hashlib
import os
import shutil
import subprocess
import tempfile
from warnings import warn

from unittest import TestCase

TMP_DIFF_PATH = '/tmp/diff.png'


class PDFValidator(TestCase):
    def __init__(self, output: str):
        super().__init__()
        self.__results_path = output

    def _count_md5_from_ppm(self, temp_dir: str) -> list:
        pdf_pages_md5s = []
        files = os.listdir(temp_dir)
        sorted_files = sorted(files)
        for file in sorted_files:
            if file.endswith(".ppm"):
                data = open(os.path.join(temp_dir, file), 'rb').read()
                md5_res = hashlib.md5(data).hexdigest()
                pdf_pages_md5s.append((md5_res, file))
        return pdf_pages_md5s

    def assert_pdf(self, pdf: str, expected_folder: str) -> None:
        temp_dir = tempfile.mkdtemp()

        return_code = subprocess.call(['pdftoppm', '-aa', 'no', '-aaVector', 'no', pdf, temp_dir + '/page'])
        if return_code != 0:
            print("Warning, pdftoppm failed, trying to retry")
            return_code = subprocess.call(['pdftoppm', '-aa', 'no', '-aaVector', 'no', pdf, temp_dir + '/page'])
            self.assertEquals(return_code, 0, "pdftoppm failed")

        os.system('pdftoppm -aa no -aaVector no {input} {output}'.format(input=pdf, output=temp_dir + '/page'))
        pdf_pages_md5s = self._count_md5_from_ppm(temp_dir)
        expected_md5s = self._extract_md5s(expected_folder)

        try:
            self._test_md5s(temp_dir, expected_folder, pdf_pages_md5s, expected_md5s)
            self.assertEqual(len(expected_md5s), len(pdf_pages_md5s), "The page count of the pdf did not match.")
        except:
            if os.path.isfile(pdf):
                self._save_file_for_log(pdf, 'generated.pdf')
            raise
        finally:
            shutil.rmtree(temp_dir)

    def _number_of_different_pixels(self, reference_path: str, page_path: str) -> int:
        try:
            diff = int(subprocess.check_output(
                ['compare', '-metric', 'AE', reference_path, page_path, TMP_DIFF_PATH], stderr=subprocess.STDOUT)
            )
        except subprocess.CalledProcessError as e:
            diff = int(e.output)

        return diff

    def _test_md5s(self, temp_dir: str, expected_folder: str, page_md5s: list, expected_md5s: list) -> None:
        count = min(len(page_md5s), len(expected_md5s))

        errors = []
        for i in range(count):
            page_filename = page_md5s[i][1]
            expected_filename = expected_md5s[i][1]
            page_md5 = page_md5s[i][0]
            expected_md5 = expected_md5s[i][0]

            page_absolute_path = os.path.join(temp_dir, page_filename)
            reference_absolute_path = os.path.join(expected_folder, expected_filename)

            if page_md5 != expected_md5:
                pixel_diff = self._number_of_different_pixels(reference_absolute_path, page_absolute_path)

                if pixel_diff > 0:
                    warn('Page "{}" has {} pixel differences.'.format(expected_filename, pixel_diff))
                    self._save_file_for_log(page_absolute_path, 'error_' + expected_filename)
                    self._save_file_for_log(reference_absolute_path, 'reference_' + expected_filename)
                    self._save_file_for_log(TMP_DIFF_PATH, 'diff_' + expected_filename)

                max_pixel_diff = int(os.getenv('MAX_PIXEL_DIFF', '200'))
                if pixel_diff >= max_pixel_diff:
                    errors.append((expected_filename, page_filename))

                if len(errors) > 3:
                    warn('Too many page compare problems, skipping further pages...')
                    break

        self.assertListEqual([], errors, "Some pages were different")

    def _extract_md5s(self, folder: str) -> list:
        ref_md5s = []
        with open(os.path.join(folder, 'md5sums')) as file:
            for line in file:
                ref_md5s.append(line.rstrip('\n').split(" "))
        return ref_md5s

    def _save_file_for_log(self, file_path: str, file_name: str) -> None:
        os.makedirs(self.__results_path, exist_ok=True)
        shutil.copyfile(file_path, os.path.join(self.__results_path, file_name))
