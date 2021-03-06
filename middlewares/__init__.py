from loader import dp
from .big_brother import BigBrother
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrother())
