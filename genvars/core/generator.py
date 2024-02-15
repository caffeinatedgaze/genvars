from pathlib import Path
from typing import Sequence, Any

from pydantic_settings import BaseSettings


def get_env_vars_md(
        settings_class: type[BaseSettings],
):
    """
    Create a Markdown table describing the environment variables read by `settings_class`
    """
    title = settings_class.__name__
    headers = ["Variable", "Type", "Default", "Description"]
    rows = []

    for k, v in settings_class.model_json_schema()["properties"].items():
        if "type" in v:
            type_ = v["type"]
        else:
            if v.get("anyOf"):
                type_ = ", ".join(map(lambda x: x["type"], v["anyOf"]))
            else:
                # type_ = ", ".join(map(lambda x: x["type"], v["default"]))
                continue

        rows.append(
            [
                "`" + k.upper() + "`",
                type_,
                v.get("default", ""),
                v.get("description", ""),
            ]
        )

    table = make_markdown_table(title, [headers] + rows)
    return table


#
def make_markdown_table(title: str, rows: Sequence[Sequence[str]]) -> str:
    """
    Take a table, with headers given as first row, and return a markdown string.

    Ex input
        [["Name", "Age", "Height"],
         ["Jake", 20, "5'10"],
         ["Mary", 21, "5'7"]]

    Source
        https://gist.github.com/ohmerhe/b8ed8113cc20ed8bc9193c12b3a315c4
    """
    if len(rows) == 0 or len(rows[0]) == 0:
        return ""

    markdown = "\n"
    markdown += f"### {title}\n\n"
    markdown += "|" + "|".join(rows[0]) + "|\n"
    markdown += "|" + "|".join(["--------------"] * len(rows[0])) + "|\n"

    for row in rows[1:]:
        markdown += "|" + "|".join(str(x) for x in row) + "|\n"

    return markdown


def discover_classes(modules: list[Any]) -> set[Any]:
    settings_classes = set()
    for module in modules:
        for name in dir(module):
            obj = getattr(module, name)
            if (
                    isinstance(obj, type)
                    and issubclass(obj, BaseSettings)
                    and obj is not BaseSettings
            ):
                settings_classes.add(obj)

    return settings_classes


def generate(settings_classes: set[Any], output_file: Path):
    tables = []
    for settings_class in settings_classes:
        table = get_env_vars_md(
            settings_class=settings_class,
        )
        tables.append(table)

    start_of_region: str = "<!-- begin env -->"
    end_of_region: str = "<!-- end env -->"

    old_file_contents = output_file.read_text()

    tables_str = "\n".join(tables)
    new_file_contents = (
            old_file_contents[
            : old_file_contents.index(start_of_region) + len(start_of_region)
            ]
            + tables_str
            + old_file_contents[old_file_contents.index(end_of_region):]
    )

    output_file.write_text(new_file_contents)
