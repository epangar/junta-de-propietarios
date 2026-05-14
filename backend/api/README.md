# API Junta de Condominios

Proyecto FastAPI con estructura MVC dentro de `app/`, archivo `main.py` en la raíz y base de datos SQLite dentro de `data/`.

## Estructura

```text
junta_condominios_mvc_root/
├── main.py
├── requirements.txt
├── .env.example
├── data/
│   └── administradora.db
└── app/
    ├── controllers/
    ├── models/
    ├── schemas/
    ├── services/
    ├── utils/
    ├── views/
    ├── config.py
    └── database.py
```

## Instalación

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Ejecutar

Desde la raíz del proyecto:

```bash
uvicorn main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Autorización en Swagger

1. Ejecuta `/auth/login` con email y password.
2. Copia el `access_token`.
3. Pulsa `Authorize`.
4. Pega solo el token, sin escribir `Bearer`.

## Base de datos

La ruta por defecto es:

```text
data/administradora.db
```

Puedes cambiarla con variable de entorno:

```env
DATABASE_PATH=data/administradora.db
```
