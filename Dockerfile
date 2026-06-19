# base image
FROM python:3.9


# work dir
WORKDIR /app


# copy
COPY . /app

# run
RUN pip install -r requirements.txt


# ports 
EXPOSE 8000


# command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]