"""Inventario del proyecto abierto: timelines, clips y metadatos clave.

Solo lectura: no modifica nada. Util como primera radiografia de un proyecto
heredado, antes de decidir que hay que ordenar.
"""
from importlib import import_module


def get_resolve():
    try:
        return resolve  # noqa: F821
    except NameError:
        return import_module("DaVinciResolveScript").scriptapp("Resolve")


def walk_folder(folder, depth=0):
    """Recorre el arbol del Media Pool y devuelve todos los clips."""
    clips = list(folder.GetClipList())
    for sub in folder.GetSubFolderList():
        clips.extend(walk_folder(sub, depth + 1))
    return clips


def main():
    app = get_resolve()
    project = app.GetProjectManager().GetCurrentProject()
    if project is None:
        print("Abre un proyecto antes de ejecutar este script.")
        return 1

    media_pool = project.GetMediaPool()
    clips = walk_folder(media_pool.GetRootFolder())
    print(f"Proyecto: {project.GetName()}")
    print(f"Clips en el Media Pool: {len(clips)}\n")

    sin_escena = 0
    for clip in clips[:40]:  # muestra acotada para no inundar la consola
        nombre = clip.GetName()
        escena = clip.GetMetadata("Scene") or ""
        resolucion = clip.GetClipProperty("Resolution")
        fps = clip.GetClipProperty("FPS")
        if not escena:
            sin_escena += 1
        print(f"  {nombre[:38]:38} {resolucion:>11} {fps:>7} fps  {escena}")

    if len(clips) > 40:
        print(f"  ... y {len(clips) - 40} clips mas")
    print(f"\nClips sin metadato Scene: {sin_escena}")

    print("\nTimelines:")
    for i in range(1, project.GetTimelineCount() + 1):
        timeline = project.GetTimelineByIndex(i)
        pistas = timeline.GetTrackCount("video")
        print(f"  {timeline.GetName()[:44]:44} {pistas} pistas de video")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
