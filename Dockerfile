FROM python:3.11

ENV PYTHONPATH='/app'

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]