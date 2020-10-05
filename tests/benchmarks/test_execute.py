import pytest

import datetime
import random
from asgiref.sync import async_to_sync
from datetime import date
from typing import List

import strawberry


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "items",
    [25, 100, 250],
)
def test_execute(benchmark, items):
    birthday = datetime.datetime.now()
    pets = ("cat", "shark", "dog", "lama")

    @strawberry.type
    class Pet:
        id: int
        name: str

    @strawberry.type
    class Patron:
        id: int
        name: str
        age: int
        birthday: date
        tags: List[str]

        @strawberry.field
        def pets(self) -> List[Pet]:
            return [
                Pet(
                    id=i,
                    name=random.choice(pets),
                )
                for i in range(5)
            ]

    @strawberry.type
    class Query:
        @strawberry.field
        def patrons(self, info) -> List[Patron]:
            return [
                Patron(
                    id=i,
                    name="Patrick",
                    age=100,
                    birthday=birthday,
                    tags=["go", "ajax"],
                )
                for i in range(items)
            ]

    schema = strawberry.Schema(query=Query)

    query = """
        query something{
          patrons {
            id
            name
            age
            birthday
            tags
            pets {
                id
                name
            }
          }
        }
    """
    result = benchmark(async_to_sync(schema.execute), query)
    assert not result.errors
    assert len(result.data["patrons"]) == items
