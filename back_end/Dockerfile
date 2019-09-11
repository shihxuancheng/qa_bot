FROM python:3.6
LABEL MAINTAINER shihxuancheng@gmail.com

WORKDIR /usr/src/qa_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "./bot_app.py" ]
