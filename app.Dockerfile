FROM python:3.8
COPY . .
WORKDIR /flask
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt 
ENTRYPOINT python run.py
EXPOSE 5000