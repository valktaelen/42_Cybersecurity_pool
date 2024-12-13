FROM alpine:3.21.0

WORKDIR /app

RUN apk --no-cache add python3 py3-pip gcc python3-dev

RUN pip install scapy --break-system-packages --root-user-action=ignore

# COPY inquisitor.py .

CMD tail -f
