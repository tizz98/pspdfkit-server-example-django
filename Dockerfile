FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD Pipfile /app/
ADD Pipfile.lock /app/
RUN pip install pipenv
RUN pipenv install --system
ADD . /app/

EXPOSE 8000
CMD ["./entrypoint.sh"]
