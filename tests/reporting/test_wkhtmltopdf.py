#
# Copyright (c) 2013-2016 BalaBit
# All Rights Reserved.
#

import os
import shutil
import tempfile

from unittest import TestCase
from tests.tools.pdfgenerator import PDFGenerator
from tests.tools.pdfvalidator import PDFValidator


class TestWkhtmltoPDF(TestCase):
    TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    CUSTOMIZATIONS_DIR = '/resources/customizations'
    SRC_FILES = ['main.html', 'cover.html', 'screen_content.png']

    def setUp(self):
        self.__working_dir = tempfile.mkdtemp()
        self._copy_files(self.SRC_FILES, self.TEST_DIRECTORY + '/resources', self.__working_dir)
        self._create_customizations_symlink()
        self._clear_results_directory()

    def tearDown(self):
        shutil.rmtree(self.__working_dir)
        pass

    def _clear_results_directory(self) -> None:
        results_dir = os.path.join(self.TEST_DIRECTORY, 'results')
        if os.path.isdir(results_dir):
            print("Removing results directory")
            shutil.rmtree(results_dir)
        self.assertFalse(os.path.isdir(results_dir))

    def _create_customizations_symlink(self) -> None:
        customizations_dir = os.path.abspath(self.TEST_DIRECTORY + self.CUSTOMIZATIONS_DIR)
        self.customizations_path = os.path.join(self.__working_dir, 'customizations')
        os.symlink(customizations_dir, self.customizations_path)
        print("\nCustomizations link created")

    def _copy_files(self, src_files: list, src_dir: str, dest_dir: str) -> None:
        for file_name in src_files:
            full_file_name = os.path.join(src_dir, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest_dir)

    def _generate_pdf(self, title: str, output_path: str) -> None:
        pdf_generator = PDFGenerator(os.path.join(self.__working_dir, 'main.html'))
        pdf_generator.set_cover(os.path.join(self.__working_dir, 'cover.html'))
        pdf_generator.set_header(os.path.join(self.customizations_path, "header.html"))
        pdf_generator.set_title(title)
        pdf_generator.set_toc_stylesheet(os.path.join(self.customizations_path, "toc.xsl"))
        pdf_generator.render_pdf(output_path)

    def test_html_convert(self) -> None:
        file = os.path.join(self.__working_dir, 'generated.pdf')
        results_path = os.path.join(self.TEST_DIRECTORY, 'results')

        self._generate_pdf('test_title', file)
        PDFValidator(results_path).assert_pdf(file, os.path.join(self.TEST_DIRECTORY, 'ref_pdf_images'))
