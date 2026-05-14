FROM python:3.14 

WORKDIR  /code

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD [ "fastapi", "run", "main.py","--host", "0.0.0.0", "--port", "8000" ]