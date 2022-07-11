from io import BytesIO
import tempfile
from pikepdf import Pdf
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse


app = FastAPI()

temp = tempfile.NamedTemporaryFile()
allowed_files = {"application/pdf"}

@app.post("/decryptPdf")
async def decrypt( file: UploadFile = File(...), password: str = Form(...)):
    '''
    file: Name of the form paramter that contains protected pdf file
    password: User/Owner password of pdf file
    '''
    if file.content_type in allowed_files:
        try:
            contents = await file.read()       
        except Exception:
            return {"message": "There was an error uploading the file", "exception": Exception}
        finally:
            await file.close()

        pdf = Pdf.open(BytesIO(contents), password=password)
        pdf.save(temp.name)
        return FileResponse(temp.name, media_type="application/pdf")   
    else:
        return { "Error": "Please upload PDF file format only."}
