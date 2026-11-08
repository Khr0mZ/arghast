"""Configuración propiedad de cada campaña y consultas conjuntas del visor común."""
from copy import deepcopy
import json
from pathlib import Path
from rutas import CAMPAIGNS


def paths(name):
    return {campaign: folder.config / name for campaign, folder in CAMPAIGNS.items()}


def merge_documents(documents):
    def merge(left, right):
        if isinstance(left, dict) and isinstance(right, dict):
            result = deepcopy(left)
            for key, value in right.items():
                result[key] = merge(result[key], value) if key in result else deepcopy(value)
            return result
        if isinstance(left, list) and isinstance(right, list):
            return deepcopy(left) + [deepcopy(value) for value in right if value not in left]
        if left != right:
            raise ValueError('Las configuraciones conjuntas discrepan en un campo común.')
        return deepcopy(left)
    result = {}
    for document in documents:
        result = merge(result, document)
    return result


def read(path):
    if isinstance(path, dict):
        return merge_documents([read(value) for value in path.values()])
    return json.loads(Path(path).read_text(encoding='utf-8'))
