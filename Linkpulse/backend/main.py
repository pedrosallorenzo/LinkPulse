from fastapi import FastAPI, Depends, BackgroundTasks, Body
from backend.models import User, Link
from backend.schemas import UserRead, UserCreate
from backend.database import SessionLocal, engine
from backend.user_manager import fastapi_users
from backend.email_alert import send_email_alert
import aiohttp
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rotas de autenticação e usuários
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

# Rota para adicionar link do usuário
@app.post("/links")
def add_link(
    url: str = Body(..., embed=True),
    db: Session = Depends(SessionLocal),
    user=Depends(current_active_user)
):
    link = Link(url=url, user_id=user.id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"message": "Link adicionado com sucesso", "link": link.url}

# Verificação de status dos links + envio de alerta por e-mail
@app.get("/status")
async def check_links(background_tasks: BackgroundTasks, user=Depends(current_active_user), db: Session = Depends(SessionLocal)):
    user_links = db.query(Link).filter(Link.user_id == user.id).all()
    offline_links = []

    async with aiohttp.ClientSession() as session:
        for link in user_links:
            try:
                async with session.get(link.url, timeout=5) as resp:
                    if resp.status != 200:
                        offline_links.append(link.url)
            except:
                offline_links.append(link.url)

    if offline_links:
        background_tasks.add_task(
            send_email_alert,
            user.email,
            "[LinkPulse] Link(s) offline",
            f"Estes links estão offline: {', '.join(offline_links)}"
        )

    return {"offline": offline_links}
