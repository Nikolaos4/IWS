from fastapi import APIRouter, Depends, HTTPException, status
from app.api.auth import get_current_user
from app.models.news import News
from app.models.user import User
from app.schemas.news import NewsCreate, NewsCreateResponse, NewsUpdate
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/news", tags=["news"])

@router.get("")
async def get_news(db: Session = Depends(get_db)):
    """
    Получить список новостей
    """
    news_list = db.query(News).all()
    return {
        "news": news_list
    }

@router.post("", response_model=NewsCreateResponse)
async def create_news(news_data: NewsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Создать новость
    """
    if current_user.user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create news")
    
    db_news = News(
        title=news_data.title,
        content=news_data.content,
        created_by=current_user.user_id
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    return db_news

@router.patch("/{news_id}", response_model=NewsCreateResponse)
async def update_news(news_id: int, news_data: NewsUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Изменить новость
    """
    if current_user.user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update news")
    
    db_news = db.query(News).filter(News.news_id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")

    if news_data.title is None and news_data.content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (title or content) must be provided"
        )

    if news_data.title is not None:
        db_news.title = news_data.title

    if news_data.content is not None:
        db_news.content = news_data.content

    db.commit()
    db.refresh(db_news)
    

    return db_news


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удалить новость
    """
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete news"
        )

    db_news = db.query(News).filter(News.news_id == news_id).first()
    if not db_news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News not found"
        )

    db.delete(db_news)
    db.commit()

    return None