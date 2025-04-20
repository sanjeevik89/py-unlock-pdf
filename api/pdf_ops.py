from io import BytesIO
import tempfile
from pikepdf import Pdf, PasswordError
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse


app = FastAPI()

temp = tempfile.NamedTemporaryFile()
allowed_files = {"application/pdf"}

@app.get("/")
def root():
    return PlainTextResponse(
        """
This API provides endpoints to unlock (decrypt) password-protected PDF files and compress PDF files.

POST /decryptPdf: Remove password protection from a PDF file. Requires a PDF file and the password.
POST /compressPdf: Compress a PDF file to reduce its size. Requires a PDF file.
"""
    )

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
        try:
            pdf = Pdf.open(BytesIO(contents), password=password)
            pdf.save(temp.name)
            return FileResponse(temp.name, media_type="application/pdf")   
        except PasswordError:
            raise HTTPException(status_code=401, detail="Invalid password for PDF file.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to decrypt PDF: {str(e)}")
    else:
        return { "Error": "Please upload PDF file format only."}

@app.post("/compressPdf")
async def compress( file: UploadFile = File(...)):
    '''
    file: Name of the form paramter that contains pdf file
    '''
    if file.content_type in allowed_files:
        try:
            contents = await file.read()
        except Exception:
            return {"message": "There was an error uploading the file", "exception": Exception}
        finally:
            await file.close()

        try:
            pdf = Pdf.open(BytesIO(contents))
            pdf.save(temp, recompress_flate=True, compress_streams=True)            
            print(f"Successfully compressed {file} and saved to '{temp}'")
            return FileResponse(temp.name, media_type="application/pdf")        
        except Pdf.PdfError as e:
            print(f"Error processing PDF: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    else:
        return { "Error": "Please upload PDF file format only."}