from schemas.operations import Operations
from sqlmodel import Session
import json

def save_operation(session: Session, op_name: str, input_dict: dict, result: str):
    record = Operations(
        operation=op_name,
        input_data=json.dumps(input_dict),
        result=result
    )
    session.add(record)
    session.commit()
    session.refresh(record)
