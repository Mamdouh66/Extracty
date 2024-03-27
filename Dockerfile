FROM python:3.11.4-slim-buster

RUN pip install poetry==1.8.2

ENV\
    POETRY_VIRTUALENVS_CREATE=false\
    POETRY_VITRUALENV_IN_PROJECT=false\
    POETRY_NO_INTERACTION=1\
    POETRY_VERSION=1.8.1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

COPY structify ./structify

RUN poetry install --no-root

CMD ["python", "-m", "structify.main.py"]g