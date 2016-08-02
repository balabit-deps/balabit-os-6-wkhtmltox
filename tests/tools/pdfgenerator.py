import subprocess


class PDFGeneratorEx(Exception):
    """ Exception thrown by PDFGenerator when generation fails. """
    pass


class PDFGenerator:
    WKHTML_BINARIES = '/wkhtmltox/static-build/precise-amd64/app/bin/wkhtmltopdf'

    def __init__(self, html_path: str):
        self._page_size = 'A4'
        self._title = None
        self._footer_path = None
        self._header_path = None
        self._cover_path = None
        self._toc_stylesheet = None
        self._body_path = html_path

    def set_footer(self, html_path: str) -> None:
        self._footer_path = html_path

    def set_header(self, html_path: str) -> None:
        self._header_path = html_path

    def set_cover(self, html_path: str) -> None:
        self._cover_path = html_path

    def set_body(self, html_path: str) -> None:
        self._body_path = html_path

    def set_page_size(self, page_size: str) -> None:
        self._page_size = page_size

    def set_title(self, title: str) -> None:
        self._title = title

    def set_toc_stylesheet(self, toc_stylesheet: str) -> None:
        self._toc_stylesheet = toc_stylesheet

    def render_pdf(self, target_path: str) -> None:
        cmd = [
            self.WKHTML_BINARIES,
            '-q',
            '--page-size',
            self._page_size,
            '--margin-top',
            '35',
            '--header-spacing',
            '10'
        ]

        if self._title:
            cmd += ['--title', self._title]

        if self._footer_path:
            cmd += ['--footer-html', self._footer_path]
        else:
            cmd += ['--footer-center', '[page] / [topage]', '--footer-font-name', 'times', '--footer-font-size', '12']

        if self._header_path:
            cmd += ['--header-html', self._header_path]

        if self._cover_path:
            cmd += ['cover', self._cover_path]

        cmd += ['toc']

        if self._toc_stylesheet:
            cmd += ['--xsl-style-sheet', self._toc_stylesheet]

        cmd += [self._body_path, target_path]

        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            raise PDFGeneratorEx("Error running wkhtmltopdf; return_code='{}' output='{}'".format(
                error.returncode, error.output))
