from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import JSONResponse
from database import get_session
from sqlalchemy.orm import Session
from typing import Any, Dict

from api.user.model.account import Account
from api.shorturl.service.shorturl_service import ShortUrlService
from api.common.response import Response
from api.common.token import verify_token
from api.common.utils.client import get_client_ip


router = APIRouter(prefix="/api/shorturl/v1")


@router.post("/shorturl")
async def create(
    request: Dict[str, Any],
    account: Account = Depends(verify_token),
    db: Session = Depends(get_session),
    response_model=Response,
):
    shorturl_service = ShortUrlService(db)

    body = request["body"]
    source = body["source"]

    shorturl = shorturl_service.create(source, account)
    db.commit() 
    return Response(body={"shorturl": shorturl})

@router.post("/shorturl/noauth")
async def create(
    request: Dict[str, Any],
    db: Session = Depends(get_session),
    response_model=Response,
):
    shorturl_service = ShortUrlService(db)

    body = request["body"]
    source = body["source"]

    account = Account(
        id = 1,
        uid = "66eb7036-0d24-4c2a-9451-fe966699515d",        
        email = "",
        status = "REGISTERED"
    )

    shorturl = shorturl_service.create(source, account)
    db.commit()
    return Response(body={"shorturl": shorturl})


@router.get("/shorturl/{url}")
async def visit_shorturl(
    url: str,
    request: Request,
    db: Session = Depends(get_session)
):
    shorturl_service = ShortUrlService(db)
    request_ip = get_client_ip(request)
    shorturl = shorturl_service.get_shorturl(url, request_ip)
    if not shorturl:
        raise ShortUrlNotExistException(url)

    db.commit() 
    return Response(body={"shorturl": shorturl})

@router.get("/shorturl/random")
async def visit_shorturl(
    url: str,
    request: Request,
    db: Session = Depends(get_session)
):
    shorturl_service = ShortUrlService(db)
    request_ip = get_client_ip(request)
    order = random.randrange(1, 5000000)
    shorturl = shorturl_service.get_shorturl_random(order)
    return Response(body={"shorturl": shorturl})
