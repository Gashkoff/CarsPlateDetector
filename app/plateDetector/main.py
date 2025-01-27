from fastapi import FastAPI
from router.YOLOHandler import router as yolo_router

app = FastAPI()
app.include_router(yolo_router)
