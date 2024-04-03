import os
import uvicorn
import zipfile
import io
import secrets
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List

from product_logic import dm_decode, dm_encode
from config import directory, host, port


app = FastAPI(title="DM Converter")


class Item(BaseModel):
    file_name: str = "code"
    roll_codes: List[str]


@app.post(
        "/create/",
        response_class=FileResponse,
        responses={200: {"content": {"application/x-zip-compressed": {}}}}
        )
async def create_code(row: Item):
    """Преобразование кодов в DM"""
    zip_name = f"example{secrets.token_hex(nbytes=16)}.zip"
    code_zip = zipfile.ZipFile(directory + zip_name, mode='a')
    for i in range(len(row.roll_codes)):
        name = row.file_name + str(i)
        dm_encode(row.roll_codes[i], name, directory)
        code_zip.write(
            directory + name + ".png",
            name + ".png"
        )
    response = FileResponse(
        path=directory + zip_name,
        filename=zip_name,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={zip_name}"}
    )
    return response

if __name__ == "__main__":
    try:
        uvicorn.run("app:app", host=host, port=port, reload=True, log_config=None)
    except:
        print("err")
