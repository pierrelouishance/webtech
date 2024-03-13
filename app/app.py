from fastapi.staticfiles import StaticFiles
from app.routes.books import router as books_router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Library")
app.mount("/static", StaticFiles(directory="static"))
app.include_router(books_router)

@app.on_event('startup')
def on_startup():
    print("Server started.")


def on_shutdown():
    print("Bye bye!")


@app.get("/", response_class=HTMLResponse)
async def get_accueil(request: Request):
    return templates.TemplateResponse("accueil.html", {"request": request, "title": "Accueil"})
