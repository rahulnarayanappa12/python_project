FROM python
WORKDIR /app
COPY main.py /app 
copy requirements.txt /app
RUN pip install -r requirements.txt
ENTRYPOINT python main.py
