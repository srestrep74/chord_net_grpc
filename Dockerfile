FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

ENV NODE_ID=0
ENV ADDRESS_THIS_NODE=0.0.0.0:50051
ENV ADDRESS_OTHER_NODE=0.0.0.0:50052

CMD ["python", "peer.py", "$NODE_ID", "$ADDRESS_THIS_NODE", "$ADDRESS_OTHER_NODE"]
