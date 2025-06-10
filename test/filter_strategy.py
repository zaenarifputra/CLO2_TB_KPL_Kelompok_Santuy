from abc import ABC, abstractmethod
from PIL import Image, ImageFilter, ImageDraw, ImageFont

class ImageFilterStrategy(ABC):
    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image:
        pass

class GrayscaleFilter(ImageFilterStrategy):
    def apply(self, image: Image.Image) -> Image.Image:
        return image.convert("L")

class BlurFilter(ImageFilterStrategy):
    def apply(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.BLUR)

class WatermarkFilter(ImageFilterStrategy):
    def apply(self, image: Image.Image) -> Image.Image:
        image = image.convert("RGBA")
        watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        font = ImageFont.load_default()
        text = "StokLy"

        # Gantikan textsize() dengan textbbox() untuk kompatibilitas Pillow baru
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = image.width - text_width - 10
        y = image.height - text_height - 10

        draw.text((x, y), text, font=font, fill=(255, 0, 0, 128))

        combined = Image.alpha_composite(image, watermark)
        return combined.convert("RGB")
