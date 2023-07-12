class FactoryStuffNotCallableError(Exception):
    """工厂中的对象不可调用"""

    def __init__(self, *args: object) -> None:
        pass


class FactoryStuffInstanceNotMatchError(Exception):
    """工厂中的对象类型不匹配（不是预设的类的实例）"""

    def __init__(self, *args: object) -> None:
        pass


class SourceNotSupportError(Exception):
    """不支持的小说来源"""

    def __init__(self, *args: object) -> None:
        pass
