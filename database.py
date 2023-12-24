from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base = declarative_base()


class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    submission_time = Column(String, nullable=False)
    status = Column(String, default='PENDING')
    task_type = Column(String, default='CLASSIFICATION')
    
    def __repr__(self):
        return f"<Request(user_id='{self.user_id}', submission_time='{self.submission_time}', status='{self.status}', task_type='{self.task_type}')>"


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    eval_summary = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    f1_score = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    ece = Column(Float, nullable=True)  # Example Error Calibration Error (ECE)

    def __repr__(self):
        return f"<Result(id='{self.id}', eval_summary='{self.eval_summary}', task_type='{self.task_type}', f1_score='{self.f1_score}', precision='{self.precision}', recall='{self.recall}', ece='{self.ece}')>"


# Database setup
engine = create_engine('sqlite:///requests.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Database operations
def add_request(user_id, submission_type, task_type):
    session = Session()
    new_request = Request(user_id=user_id, submission_type=submission_type, task_type=task_type)
    try:
        session.add(new_request)
        session.commit()
        logging.info("Added request for user %s to database", user_id)
    except Exception as e:
        logging.error("Error adding request for user %s to database: %s", user_id, e)
        session.rollback()
        raise
    finally:
        session.close()


def update_request_status(request_id, new_status):
    session = Session()
    try:
        request = session.query(Request).filter(Request.id == request_id).first()
        if request:
            request.status = new_status
            session.commit()
            logging.info("Updated status of request %s to %s", request_id, new_status)
    except Exception as e:
        logging.error("Error updating status of request %s to %s: %s", request_id, new_status, e)
        session.rollback()
        raise
    finally:
        session.close()


def get_pending_requests():
    session = Session()
    try:
        pending_requests = session.query(Request).filter(Request.status == 'PENDING').all()
        return pending_requests
    except Exception as e:
        logging.error("Error fetching pending requests: %s", e)
        raise
    finally:
        session.close()


def add_result(eval_summary, task_type, metrics):
    session = Session()
    new_result = Result(
        eval_summary=eval_summary,
        task_type=task_type,
        f1_score=metrics.get('f1_score'),
        precision=metrics.get('precision'),
        recall=metrics.get('recall'),
        ece=metrics.get('ece')
    )
    try:
        session.add(new_result)
        session.commit()
        logging.info("Added result to database")
    except Exception as e:
        logging.error("Error adding result to database: %s", e)
        session.rollback()
        raise
    finally:
        session.close()


def get_result_by_id(result_id):
    session = Session()
    try:
        result = session.query(Result).filter(Result.id == result_id).first()
        return result
    except Exception as e:
        logging.error("Error fetching result with id %s: %s", result_id, e)
        raise
    finally:
        session.close()