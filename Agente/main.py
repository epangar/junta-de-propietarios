from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile

from agent.agent import run_agent

app = FastAPI(title="Excel → SQLite Agent")


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = await run_agent(tmp_path)

    return JSONResponse(result)