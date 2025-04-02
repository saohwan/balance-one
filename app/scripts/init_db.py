import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from app.core.database import SessionLocal, engine, Base
from app.models import Stock


def init_db() -> None:
    """데이터베이스를 초기화하고 시드 데이터를 생성합니다."""
    # 테이블 생성
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 현재 등록된 증권 개수 확인
        current_count = Stock.get_total_count(db)
        if current_count < 10:
            # 시드 데이터 생성
            seed_data = Stock.get_seed_data()
            for stock in seed_data:
                db.add(stock)
            db.commit()
            print(f"시드 데이터 {len(seed_data)}개가 생성되었습니다.")
        else:
            print(f"이미 {current_count}개의 증권이 등록되어 있습니다.")
    except Exception as e:
        print(f"데이터베이스 초기화 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
