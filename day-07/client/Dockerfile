FROM alpine:3.21.0

RUN apk --no-cache add ncftp tcpdump

WORKDIR /app

COPY test.sh .

ENTRYPOINT /bin/sh test.sh

# CMD tail -f /dev/null


