# utils/image_filter/image_filter_context.py
from PIL import Image
from .filter_strategy import ImageFilterStrategy

class ImageFilterContext:
    def __init__(self, strategy: ImageFilterStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: ImageFilterStrategy):
        self._strategy = strategy

    def apply_filter(self, image: Image.Image) -> Image.Image:
        if not self._strategy:
            raise ValueError("Strategy belum ditetapkan.")
        return self._strategy.apply(image)
