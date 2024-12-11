FROM alpine:3.21.0

WORKDIR /app

RUN apk --no-cache add python3 py3-pip gcc python3-dev musl-dev libpcap-dev

RUN pip install python-libpcap --break-system-packages --root-user-action=ignore

# COPY inquisitor.py .

CMD tail -f
