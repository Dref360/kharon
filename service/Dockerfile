FROM linuxserver/openssh-server:latest
RUN apk add --no-cache python3 py3-pip
COPY . /app
RUN python3 -m venv /app/venv && \
     . /app/venv/bin/activate && \
     pip3 install -r /app/requirements.txt
# NOTE: Must sleep forever at the end.
ENV HOME=/config
CMD ["/bin/bash", "-c", "/app/run.sh"]