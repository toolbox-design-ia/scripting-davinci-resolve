"""Vuelca la timeline activa a un CSV: un renglon por clip.

Sirve como parte de entrega, como lista de conformado o como base para
comparar dos versiones de una misma timeline.
"""
import csv
from importlib import import_module
from pathlib import Path


def get_resolve():
    try:
        return resolve  # noqa: F821
    except NameError:
        return import_module("DaVinciResolveScript").scriptapp("Resolve")


def main():
    app = get_resolve()
    project = app.GetProjectManager().GetCurrentProject()
    timeline = project.GetCurrentTimeline() if project else None
    if timeline is None:
        print("Abre una timeline antes de ejecutar este script.")
        return 1

    salida = Path.home() / f"{timeline.GetName()}_informe.csv"
    with open(salida, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["pista", "clip", "inicio", "fin", "duracion",
                         "archivo"])
        total = 0
        for track in range(1, timeline.GetTrackCount("video") + 1):
            for item in timeline.GetItemListInTrack("video", track):
                mpi = item.GetMediaPoolItem()
                archivo = mpi.GetClipProperty("File Path") if mpi else ""
                writer.writerow([track, item.GetName(), item.GetStart(),
                                 item.GetEnd(), item.GetDuration(), archivo])
                total += 1

    print(f"{total} clips escritos en {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
