from fastapi import FastAPI, UploadFile, File
import pandas as pd

from agent.agent import run_agent

app = FastAPI(title="Excel → SQLite Inspector")


def normalize_columns(df):
    df.columns = (
        df.columns
        .astype(str)
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def clean_df(df: pd.DataFrame):
    # 🔥 elimina NaN para evitar errores JSON
    return df.where(pd.notnull(df), None)


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    sheets = pd.read_excel(file.file, sheet_name=None, engine="openpyxl")

    for name in sheets:
        sheets[name] = normalize_columns(sheets[name])
        sheets[name] = clean_df(sheets[name])

    result = await run_agent(sheets)

    return {
        "status": "processed",
        "result": result
    }