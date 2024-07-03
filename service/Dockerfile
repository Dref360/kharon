FROM linuxserver/openssh-server:latest
RUN apk add --no-cache python3 py3-pip
# NOTE: Must sleep forever at the end.
CMD ["sh", "-c", "python3 -m http.server 8080"]