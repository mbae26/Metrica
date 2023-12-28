import os
import logging

from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BaseRequests = declarative_base()
BaseResults = declarative_base()

instance_dir = os.path.join('.', 'instance')
os.makedirs(instance_dir, exist_ok=True)


class Request(BaseRequests):
    __tablename__ = 'requests'
    user_id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    submission_time = Column(String, nullable=False)
    status = Column(String, default='PENDING')
    task_type = Column(String, default='classification')

    def __repr__(self):
        return f"<Request(user_id='{self.user_id}', email='{self.email}', \
            submission_time='{self.submission_time}', status='{self.status}', \
                task_type='{self.task_type}')>"

engine_requests = create_engine(f"sqlite:///{instance_dir}/requests.db")
BaseRequests.metadata.create_all(engine_requests)
SessionRequests = sessionmaker(bind=engine_requests)


class Result(BaseResults):
    __tablename__ = 'results'

    user_id = Column(String, primary_key=True)
    task_type = Column(String, nullable=False)
    performance_metrics = Column(JSON)

    def __repr__(self):
        return f"<Result(user_id='{self.user_id}', task_type='{self.task_type}', performance_metrics='{self.performance_metrics}')>"


engine_results = create_engine(f"sqlite:///{instance_dir}/results.db")
BaseResults.metadata.create_all(engine_results)
SessionResults = sessionmaker(bind=engine_results)


def add_request(user_id, email, submission_time, task_type):
    session = SessionRequests()
    new_request = Request(user_id=user_id, email=email,
                        submission_time=submission_time, task_type=task_type)
    try:
        session.add(new_request)
        session.commit()
        logging.info("Added request for user %s to database", user_id)
    except SQLAlchemyError as e:
        logging.error("Error adding request for user %s to database: %s", user_id, e)
        session.rollback()
        raise
    finally:
        session.close()


def update_request_status(user_id, new_status):
    session = SessionRequests()
    try:
        request = session.query(Request).get(user_id)
        if request:
            request.status = new_status
            session.commit()
            logging.info("Updated status of request %s to %s", user_id, new_status)
        else:
            logging.warning("Request %s not found", user_id)
    except SQLAlchemyError as e:
        logging.error("Error updating status of request %s to %s: %s", user_id, new_status, e)
        session.rollback()
        raise
    finally:
        session.close()


def get_pending_requests():
    session = SessionRequests()
    try:
        return session.query(Request).filter(Request.status == 'PENDING').all()
    except SQLAlchemyError as e:
        logging.error("Error fetching pending requests: %s", e)
        raise
    finally:
        session.close()


def add_result(user_id, task_type, performance_metrics):
    session = SessionResults()
    new_result = Result(user_id=user_id, task_type=task_type,
                        performance_metrics=performance_metrics)
    try:
        session.add(new_result)
        session.commit()
        logging.info("Added result for user %s to database", user_id)
    except SQLAlchemyError as e:
        logging.error("Error adding result for user %s to database: %s", user_id, e)
        session.rollback()
        raise
    finally:
        session.close()


def get_result_by_id(user_id):
    session = SessionResults()
    try:
        result = session.query(Result).get(user_id)
        if result:
            return result
        else:
            logging.warning("Result for user %s not found", user_id)
            return None
    except SQLAlchemyError as e:
        logging.error("Error fetching result for user %s: %s", user_id, e)
        raise
    finally:
        session.close()
