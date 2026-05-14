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
levantar elastic en docker
abrir ollama
instalar los requirements
necesario mistral y llama2 y minilm
ollama pull mistral
mistral:latest       6577803aa9a0    4.4 GB    25 hours ago    
llama3:latest        365c0bd3c000    4.7 GB    7 days ago      
llama2:latest        78e26419b446    3.8 GB    7 days ago      
all-minilm:latest    1b226e2802db    45 MB     9 days ago  
configurar el config de jira con la api key del gpt y la del jira
