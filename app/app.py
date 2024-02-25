from fastapi import FastAPI
from app.routes.books import router as books_router


app = FastAPI(title="Books")
app.include_router(books_router)

@app.on_event('startup')
def on_startup():
    print("Server started.")


def on_shutdown():
    print("Bye bye!")
