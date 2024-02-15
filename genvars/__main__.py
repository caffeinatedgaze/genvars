import argparse
import importlib
from pathlib import Path

from genvars.core.generator import discover_classes, generate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "modules",
        nargs="+",
        help="Modules with settings to describe, e.g. common.settings config <...>",
    )
    parser.add_argument("--output", help="Output file in Markdown.")

    args = parser.parse_args()
    output = Path(args.output)

    if not output.exists():
        print(f"Output file '{output}' does not exist")
        exit(1)

    modules = []
    for name in args.modules:
        try:
            module = importlib.import_module(name)
            modules.append(module)
        except ModuleNotFoundError:
            print(f"Module '{name}' does not exist")
            exit(1)

    settings_classes = discover_classes(modules)
    generate(settings_classes, output_file=output)


if __name__ == "__main__":
    main()
