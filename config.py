# config.py
import argparse
import os
import re
from dataclasses import dataclass


class ConfigError(Exception):
    pass


@dataclass
class AppConfig:
    package_name: str
    repo: str  # URL или путь к файлу
    mode: str  # "real" или "test"
    version: str
    ascii_tree: bool
    max_depth: int
    reverse: bool
    d2: bool


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+([\-+].*)?$")


def parse_args(argv=None) -> AppConfig:
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей npm-пакетов."
    )
    parser.add_argument(
        "-n", "--package-name", required=True, help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "-r",
        "--repo",
        required=True,
        help="URL репозитория или путь к файлу тестового репозитория",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["real", "test"],
        required=True,
        help="Режим работы: real или test",
    )
    parser.add_argument(
        "-v",
        "--version",
        required=True,
        help="Версия пакета (например 1.2.3)",
    )
    parser.add_argument(
        "-a",
        "--ascii",
        dest="ascii_tree",
        action="store_true",
        help="Вывод зависимостей в виде ASCII-дерева",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        required=True,
        help="Максимальная глубина анализа зависимостей (>=1)",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Режим вывода обратных зависимостей",
    )
    parser.add_argument(
        "--d2",
        action="store_true",
        help="Вывести описание графа в формате D2",
    )

    args = parser.parse_args(argv)

    # Дополнительная валидация
    if not args.package_name.strip():
        raise ConfigError("Параметр --package-name не может быть пустым")

    if args.mode == "test":
        # repo должен быть существующим файлом
        if not os.path.isfile(args.repo):
            raise ConfigError(
                f"В тестовом режиме --repo должен указывать на существующий файл, "
                f"но '{args.repo}' не найден"
            )

    if args.max_depth is None or args.max_depth <= 0:
        raise ConfigError("--max-depth должен быть целым числом > 0")

    if not args.version.strip():
        raise ConfigError("Параметр --version не может быть пустым")

    # Можно смягчить проверку, но базовая semver-проверка не повредит
    if not SEMVER_RE.match(args.version):
        # Не фатально, но предупредим
        print(
            f"Предупреждение: версия '{args.version}' не похожа на semver (x.y.z), "
            f"npm все равно может ее принять.",
        )

    cfg = AppConfig(
        package_name=args.package_name.strip(),
        repo=args.repo.strip(),
        mode=args.mode,
        version=args.version.strip(),
        ascii_tree=bool(args.ascii_tree),
        max_depth=args.max_depth,
        reverse=bool(args.reverse),
        d2=bool(args.d2),
    )

    return cfg


def print_config(cfg: AppConfig) -> None:
    """Этап 1: вывести все настраиваемые параметры в формате ключ=значение."""
    print("Конфигурация:")
    print(f"package_name={cfg.package_name}")
    print(f"repo={cfg.repo}")
    print(f"mode={cfg.mode}")
    print(f"version={cfg.version}")
    print(f"ascii_tree={cfg.ascii_tree}")
    print(f"max_depth={cfg.max_depth}")
    print(f"reverse={cfg.reverse}")
    print(f"d2={cfg.d2}")
    print()
