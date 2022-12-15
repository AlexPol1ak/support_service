FROM python:3.10

WORKDIR support/

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "manage.py" , "runserver"]