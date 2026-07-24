import json

datos_extra = json.dumps({
    "revisor": "marta.garcia",
    "prioridad": "alta",
    "referencia_ticket": "COLOR-445"
})

timeline_item.AddMarker(
    frameId=48,
    color="Yellow",
    name="revision_colorista",
    note="balancear sombras",
    duration=1,
    customData=datos_extra
)
