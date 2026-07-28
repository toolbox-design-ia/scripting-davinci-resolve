# Ejemplos listos para ejecutar

Scripts autocontenidos para probar la API sin montar nada. Ábrelos desde la
consola de Resolve (**Workspace > Console**, pestaña Py3) o ejecútalos desde
la terminal si tienes activado *Preferences > System > General > External
scripting using*.

| Archivo | Qué hace | Escribe algo |
| --- | --- | --- |
| `00_comprobar_conexion.py` | Confirma que la API responde y muestra versión y proyecto | No |
| `01_inventario_de_proyecto.py` | Lista timelines, clips y sus metadatos clave | No |
| `02_renombrar_por_convencion.py` | Renombra clips del Media Pool según una regla | Solo con `--aplicar` |
| `03_informe_de_timeline.py` | Vuelca la timeline activa a CSV | Crea un CSV |

Empieza siempre por `00`: si ese falla, ninguno de los demás funcionará.
