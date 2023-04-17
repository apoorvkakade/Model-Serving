FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python save_model.py

EXPOSE 7000

CMD ["bentoml","serve","service:svc","--port","7000"]