FROM python:3.12.0-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ /app/

ENV FLASK_APP=todolist_app
ENV ENVIRONMENT="development.py"
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]