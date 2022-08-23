FROM python:3.10.6-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

#FROM python:3.10.6-slim
#WORKDIR /code
#COPY ./requirements.txt /code/requirements.txt
#RUN python3 -m venv venv
#RUN venv/bin/pip install --upgrade pip &&\
#    venv/bin/pip install --no-cache-dir -r /code/requirements.txt
#COPY . /code
#EXPOSE 8080
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
