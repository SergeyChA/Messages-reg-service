FROM python:latest

WORKDIR /src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

COPY . .

EXPOSE 8000

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /src/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]

