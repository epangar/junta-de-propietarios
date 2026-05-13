# Views

En una API REST con FastAPI no se renderizan plantillas HTML, porque la vista real será Angular.
Esta carpeta se mantiene para respetar el patrón MVC solicitado:

- Controllers: reciben HTTP y validan entrada/salida con Pydantic.
- Services: contienen reglas de negocio, seguridad y casos de uso.
- Models: contienen acceso a SQLite y consultas SQL.
- Views: representadas externamente por Angular.
