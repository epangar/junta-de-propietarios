# Junta de Propietarios

Proyecto para gestionar la junta de propietarios de una comunidad..


# Instalar y levantar el frontend
Abrir un terminal:
npm install -g @angular/cli

En el terminal, navegar a frontend\junta-de-propietarios

npm install
ng serve


# Instalar y levantar el backend
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```