FROM ubuntu:latest

RUN useradd -m -s /bin/bash user

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv

COPY . .

RUN chown user:user ./

RUN python3 -m venv venv
ENV PATH="/venv/bin:$PATH"

RUN . venv/bin/activate && pip install -r requirements.txt

RUN chmod 777 contacts.db

USER user

CMD ["python3", "bot.py"]
