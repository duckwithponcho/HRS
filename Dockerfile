FROM python

WORKDIR /server

COPY pythonLibs.txt .

RUN pip install --no-cache-dir -r pythonLibs.txt

COPY game-server/ ./

EXPOSE 8000

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
