"""Registry functions for installing JsonTreeBuilder into BeautifulSoup."""

from bs4 import builder

from .builder import JsonTreeBuilder


def install(debug: bool = False) -> None:
    """Register JsonTreeBuilder so it can be used as BeautifulSoup('jsoup').

    After calling install(), you can use:
        soup = BeautifulSoup(json_data, 'jsoup')

    Args:
        debug: If True, prints a confirmation message.
    """
    setattr(builder, "JsonTreeBuilder", JsonTreeBuilder)
    if "JsonTreeBuilder" not in builder.__all__:
        builder.__all__.append("JsonTreeBuilder")
    builder.builder_registry.register(JsonTreeBuilder)
    if debug:
        print("Builder installed")
