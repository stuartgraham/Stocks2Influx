FROM python
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt && rm requirements.txt
CMD ["python3", "-u", "./main.py"]