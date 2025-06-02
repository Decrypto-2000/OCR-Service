from fastapi import FastAPI
from pydantic import BaseModel
from video_ocr import main
import traceback
import uvicorn

app = FastAPI()

# Define the data model for input
class FolderInput(BaseModel):
    folder_path: str = None

@app.post("/process_folder")
def process_folder(input_data: FolderInput):
    # Retrieve the folder path from the request
    folder_path = input_data.folder_path
    print(f"folder path --> {folder_path}")
    try:
        main(folder_path)
    except Exception as e:
        print(f"logging excetion {e}")
        #### add database error logging
        traceback.print_exc()
        return {"message": "Error Occured ,check database"}

    return {"message": "task completed"}

if __name__ == "__main__":
    uvicorn.run("process_video_api:app",host="0.0.0.0", port=8085)


