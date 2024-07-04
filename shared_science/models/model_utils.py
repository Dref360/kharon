# type: ignore
import json
from typing import Generic, TypeVar, Optional, List

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as
from pydantic.v1.main import ModelMetaclass
from sqlalchemy.orm import registry
from sqlmodel import TypeDecorator, JSON, SQLModel, Field, Column, Session

T = TypeVar("T")

recursive_custom_encoder = jsonable_encoder

mapper_registry = registry()


class ResourceSQLModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_read_allow: str = ""

    @property
    def resource_name(self):
        return f"{self.__class__.__name__}-{self.id}"

    def add_user(self, email: str, session: Session):
        # SQLLite doesn't support array type so that's a bummer
        self.user_read_allow = ",".join(self.user_read_allow.split(",") + [email])
        session.add(self)
        session.commit()
        session.refresh(self)


"""
Taken from:
https://github.com/tiangolo/sqlmodel/issues/63
"""


def pydantic_column_type(pydantic_type):
    class PydanticJSONType(TypeDecorator, Generic[T]):
        impl = JSON()

        def __init__(
            self,
            json_encoder=json,
        ):
            self.json_encoder = json_encoder
            super(PydanticJSONType, self).__init__()

        def bind_processor(self, dialect):
            impl_processor = self.impl.bind_processor(dialect)
            dumps = self.json_encoder.dumps
            if impl_processor:

                def process(value: T):
                    if value is not None:
                        if isinstance(pydantic_type, ModelMetaclass):
                            # This allows to assign non-InDB models and if they're
                            # compatible, they're directly parsed into the InDB
                            # representation, thus hiding the implementation in the
                            # background. However, the InDB model will still be returned
                            value_to_dump = pydantic_type.from_orm(value)
                        else:
                            value_to_dump = value
                        value = recursive_custom_encoder(value_to_dump)
                    return impl_processor(value)

            else:

                def process(value):
                    if isinstance(pydantic_type, ModelMetaclass):
                        # This allows to assign non-InDB models and if they're
                        # compatible, they're directly parsed into the InDB
                        # representation, thus hiding the implementation in the
                        # background. However, the InDB model will still be returned
                        value_to_dump = pydantic_type.from_orm(value)
                    else:
                        value_to_dump = value
                    value = dumps(recursive_custom_encoder(value_to_dump))
                    return value

            return process

        def result_processor(self, dialect, coltype) -> T:
            impl_processor = self.impl.result_processor(dialect, coltype)
            if impl_processor:

                def process(value):
                    value = impl_processor(value)
                    if value is None:
                        return None

                    data = value
                    # Explicitly use the generic directly, not type(T)
                    full_obj = parse_obj_as(pydantic_type, data)
                    return full_obj

            else:

                def process(value):
                    if value is None:
                        return None

                    # Explicitly use the generic directly, not type(T)
                    full_obj = parse_obj_as(pydantic_type, value)
                    return full_obj

            return process

        def compare_values(self, x, y):
            return x == y

    return PydanticJSONType
