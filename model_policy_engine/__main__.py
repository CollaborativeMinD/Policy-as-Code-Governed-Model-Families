"""Initialize a policy deployment or publish an edited model policy."""
import argparse
from pathlib import Path

from .schema import catalog
from .store import home_path, initialize, publish


def main():
    parser = argparse.ArgumentParser(prog="python -m model_policy_engine")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("directory", type=Path)
    apply = commands.add_parser("apply")
    apply.add_argument("draft", type=Path)
    apply.add_argument("--override", type=Path)
    commands.add_parser("list")
    args = parser.parse_args()
    if args.command == "init":
        print(f"Policy deployment: {initialize(args.directory)}")
    elif args.command == "list":
        for model_id, relative in catalog().items():
            print(f"{model_id}\t{relative.as_posix()}")
    else:
        policy = publish(home_path(), args.draft, override=args.override)
        print(f"Admitted {policy.model_id} at version {policy.version}")


if __name__ == "__main__":
    main()

