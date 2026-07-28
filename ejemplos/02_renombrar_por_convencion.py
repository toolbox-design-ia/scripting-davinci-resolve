"""Renombrar clips del Media Pool segun una convencion.

Regla de oro: propone primero. Sin --aplicar no toca nada, de modo que
puedes revisar la lista completa antes de que se modifique un solo clip.

Convencion de ejemplo: <ESCENA>_<TOMA>_<nombre-original>
Ajusta build_name() a la convencion de tu produccion.
"""
import argparse
from importlib import import_module


def get_resolve():
    try:
        return resolve  # noqa: F821
    except NameError:
        return import_module("DaVinciResolveScript").scriptapp("Resolve")


def build_name(clip):
    """Nombre nuevo a partir de los metadatos; None si faltan datos."""
    escena = (clip.GetMetadata("Scene") or "").strip()
    toma = (clip.GetMetadata("Take") or "").strip()
    if not (escena and toma):
        return None
    original = clip.GetName()
    if original.startswith(f"{escena}_{toma}_"):
        return None  # ya cumple la convencion
    return f"{escena}_{toma}_{original}"


def walk(folder):
    clips = list(folder.GetClipList())
    for sub in folder.GetSubFolderList():
        clips.extend(walk(sub))
    return clips


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aplicar", action="store_true",
                        help="renombra de verdad (sin esto solo propone)")
    args = parser.parse_args()

    app = get_resolve()
    project = app.GetProjectManager().GetCurrentProject()
    if project is None:
        print("Abre un proyecto antes de ejecutar este script.")
        return 1

    clips = walk(project.GetMediaPool().GetRootFolder())
    cambios = [(c, build_name(c)) for c in clips]
    cambios = [(c, n) for c, n in cambios if n]

    if not cambios:
        print("Nada que renombrar: o ya cumplen la convencion, o les faltan "
              "los metadatos Scene y Take.")
        return 0

    print(f"{'APLICANDO' if args.aplicar else 'PROPUESTA (sin cambios)'} "
          f"- {len(cambios)} clips\n")
    for clip, nuevo in cambios:
        print(f"  {clip.GetName()[:40]:40} -> {nuevo}")
        if args.aplicar:
            clip.SetClipProperty("Clip Name", nuevo)

    if not args.aplicar:
        print("\nRevisa la lista y vuelve a ejecutar con --aplicar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
