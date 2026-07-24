import DaVinciResolveScript as dvr
from dataclasses import dataclass, field
from enum import Enum
from typing import List

def get_active_timeline():
    resolve = dvr.scriptapp("Resolve")
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if project is None:
        raise RuntimeError("No hay ningún proyecto abierto en Resolve.")
    timeline = project.GetCurrentTimeline()
    if timeline is None:
        raise RuntimeError("No hay ninguna timeline activa.")
    return timeline
