from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
import unittest
from PIL import Image
from pypdf import PdfReader

SCRIPT = Path(__file__).resolve().parents[1] / '.agents/skills/handwritten-solutions/scripts/pack_pages.py'


class PackPagesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.images = []
        for n, size in enumerate(((100, 200), (200, 100))):
            path = self.root / f'{n}.png'
            Image.new('RGB', size, ('white', 'gray')[n]).save(path)
            self.images.append(path)

    def run_pack(self, out, images):
        return subprocess.run([sys.executable, str(SCRIPT), '--output', str(out), *map(str, images)], capture_output=True)

    def test_page_order_a4_and_source_preservation(self):
        hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in self.images]
        out = self.root / 'ordered.pdf'
        result = self.run_pack(out, self.images)
        self.assertEqual(result.returncode, 0, result.stderr)
        pages = PdfReader(out).pages
        self.assertEqual(len(pages), 2)
        for page, expected in zip(pages, ((100, 200), (200, 100))):
            self.assertAlmostEqual(float(page.mediabox.width), 595.2756, places=2)
            self.assertAlmostEqual(float(page.mediabox.height), 841.8898, places=2)
            resources = page['/Resources']['/XObject'].get_object()
            image = next(v.get_object() for v in resources.values() if v.get_object().get('/Subtype') == '/Image')
            self.assertEqual((image['/Width'], image['/Height']), expected)
        self.assertEqual(hashes, [hashlib.sha256(p.read_bytes()).hexdigest() for p in self.images])

    def test_existing_output_is_not_overwritten(self):
        out = self.root / 'existing.pdf'
        out.write_bytes(b'existing-content')
        result = self.run_pack(out, self.images)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(out.read_bytes(), b'existing-content')

    def test_missing_image_produces_no_pdf(self):
        out = self.root / 'missing.pdf'
        result = self.run_pack(out, [self.root / 'absent.png'])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
