# npm_reader.py
import json
import sys
from typing import Dict

from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from graph import NodeId


class RegistryError(Exception):
    pass


def fetch_json(url: str) -> dict:
    try:
        with urlopen(url) as resp:
            if resp.status >= 400:
                raise RegistryError(f"HTTP {resp.status} для {url}")
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except HTTPError as e:
        raise RegistryError(f"HTTP ошибка {e.code} для {url}") from e
    except URLError as e:
        raise RegistryError(f"Ошибка сети для {url}: {e}") from e
    except json.JSONDecodeError as e:
        raise RegistryError(f"Ошибка JSON для {url}: {e}") from e


def get_direct_dependencies(node: NodeId) -> Dict[str, str]:
    """
    Получаем прямые зависимости пакета по имени и версии через npm registry.
    Сначала пробуем /name/version, если не получилось — /name/latest.
    Возвращаем словарь {имя_зависимости: версия_или_диапазон}.
    """
    base = f"https://registry.npmjs.org/{node.name}"
    url = f"{base}/{node.version}"

    try:
        meta = fetch_json(url)
    except RegistryError as e:
        print(
            f"Предупреждение: не удалось получить {node.name}@{node.version}: {e}",
            file=sys.stderr,
        )
        print(f"Пробуем взять {node.name}@latest", file=sys.stderr)
        meta = fetch_json(f"{base}/latest")

    deps = meta.get("dependencies") or {}
    if not isinstance(deps, dict):
        return {}
    return {str(k): str(v) for k, v in deps.items()}
