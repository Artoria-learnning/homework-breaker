"""按参数顺序将已核验的图片拼为A4 PDF，不修改源图片。"""
from pathlib import Path
import argparse
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('images', type=Path, nargs='+')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('输出已存在，请指定新版本路径。')
    for src in args.images:
        if not src.is_file():
            parser.error(f'图片不存在：{src}')
        with Image.open(src) as image:
            image.verify()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    pdf = canvas.Canvas(str(args.output), pagesize=A4)
    pdf.setTitle('仿手写解题页')
    pdf.setAuthor('AI辅助生成；参照用户授权样本')
    for src in args.images:
        image = ImageReader(str(src))
        iw, ih = image.getSize()
        scale = min(width / iw, height / ih)
        dw, dh = iw * scale, ih * scale
        pdf.drawImage(image, (width-dw)/2, (height-dh)/2, dw, dh, mask='auto')
        pdf.showPage()
    pdf.save()
    result = PdfReader(str(args.output))
    if len(result.pages) != len(args.images):
        raise RuntimeError('PDF页数与输入图片数不一致。')
    print(f'{args.output.resolve()} ({len(result.pages)}页)')


if __name__ == '__main__':
    main()
