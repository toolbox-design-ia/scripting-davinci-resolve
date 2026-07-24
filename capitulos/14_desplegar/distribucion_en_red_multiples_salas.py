# deploy.py — requiere Fabric
from fabric import SerialGroup

SALAS = [
    "colorista@sala-color-a.local",
    "colorista@sala-color-b.local",
    "editor@sala-edicion.local",
]

def desplegar(version: str):
    paquete = f"resolve_tools_{version}.tar.gz"
    grupo = SerialGroup(*SALAS)
    grupo.put(paquete, remote=f"/tmp/{paquete}")
    grupo.run(
        f"cd /tmp && tar xzf {paquete} && "
        f"python3 resolve_tools/install.py --force"
    )
    grupo.run(f"rm /tmp/{paquete}")
