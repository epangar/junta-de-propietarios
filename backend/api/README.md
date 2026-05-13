# API Junta de Condominios - MVC FastAPI + SQLite

Proyecto organizado siguiendo una variante práctica de MVC para una API REST:

```txt
app/
├── controllers/   # Capa HTTP: endpoints FastAPI
├── services/      # Casos de uso, permisos, JWT, hashing y reglas de negocio
├── models/        # Acceso a datos SQLite y sentencias SQL
├── schemas/       # Pydantic: request/response models
├── views/         # Vista externa: Angular
├── utils/         # Utilidades
├── config.py
└── database.py
```

## Ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

Swagger:

```txt
http://127.0.0.1:8000/docs
```

## Base de datos

La base está en:

```txt
data/administradora.db
```

El proyecto espera estas tablas:

- Usuario
- Balance_general
- Apartamento
- Gasto_apartamento

## Endpoints

### Auth

```txt
POST /auth/login
POST /auth/logout
```

### Resumen

```txt
GET /resumen/{anio}
GET /resumen/{anio}/categorias
```

### Balance general

```txt
GET /balance
GET /balance/rango?fecha_inicio=2025-01-01&fecha_fin=2026-01-01
POST /balance                    # solo admin
PUT /balance/{id_balance}         # solo admin
```

### Propietarios

```txt
GET /propietarios                 # solo admin
GET /propietarios/fecha           # solo admin
GET /propietarios/puerta/{puerta} # solo admin
PATCH /propietarios/{puerta}      # solo admin
POST /propietarios                # solo admin
```

### Apartamento

```txt
GET /apartamento/{puerta}         # solo propietario asociado
GET /apartamento/{puerta}/fecha   # solo propietario asociado
```

### Usuarios

```txt
POST /usuarios                    # admin o junta
PATCH /usuarios/{username}        # admin o junta
```

## Nota sobre la base entregada

En la base de datos entregada, `Apartamento` no tiene columna `puerta`; por eso el proyecto usa `id_apto` como puerta lógica.

En `Gasto_apartamento` no existe `total_gasto`; por eso la derrama se calcula sumando `monto`.

En `Balance_general` no existe `categoria`; por eso `/resumen/{anio}/categorias` devuelve una categoría general agregada.

## Login

El login soporta:

- contraseñas hasheadas con bcrypt
- texto plano solo para compatibilidad con bases antiguas de prueba

Los usuarios nuevos creados desde `POST /usuarios` siempre guardan contraseña con hash bcrypt.
