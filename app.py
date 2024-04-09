import uvicorn
import zipfile
import secrets
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Annotated

from product_logic import dm_decode, dm_encode
from config import directory, host, port


app = FastAPI(title="DM Converter", version="0.2")


class Item(BaseModel):
    file_name: str = "code"
    roll_codes: List[str]


@app.post(
        path="/create/",
        name="Create DataMatrixCodes",
        tags=["Converter"]
        )
async def create_code(row: Item):
    """Преобразование кодов в DM и сохранение в архив"""
    zip_name = f"example{secrets.token_hex(nbytes=16)}.zip"
    code_zip = zipfile.ZipFile(directory + zip_name, mode="a")
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


@app.post(
        path="/read/",
        name="Read DataMatrixCodes",
        tags=["Converter"]
        )
async def read_dmcode(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as DataMatrixCode.png")
    ],
):
    """Преобразование DM в коды и сохранение в файл"""
    codes = []
    for file in files:
        codes.append(dm_decode(file.file, file.filename))
    with open("codes.txt", "w") as file:
        for code in codes:
            file.write(f"{code}\n")
    zip_name = f"code_{secrets.token_hex(nbytes=16)}.zip"
    zip = zipfile.ZipFile(directory + zip_name, mode="w")
    zip.write("codes.txt")
    response = FileResponse(
        path=directory + zip_name,
        filename=zip_name,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={zip_name}"}
    )
    return response


@app.post(
        path="/read-zip/",
        name="Read library DataMatrixCodes",
        tags=["Converter"]
        )
async def read_library_dmcode():
    pass


@app.get("/")
async def main():
    content = """
<body>
<h1>DataMatrixConverter</h1>
<a href="/docs/">swager</a>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run("app:app", host=host, port=port, reload=True)
