class PhotomosaicException(Exception):
    pass


class InvalidTypeException(PhotomosaicException, TypeError):
    pass


class InvalidShapeException(PhotomosaicException, ValueError):
    pass
