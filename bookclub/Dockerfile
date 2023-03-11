FROM ubuntu

# Install necessary packages
RUN apt-get update \
  &&  apt-get install -y python3 python3-pip \
  &&  apt-get install -y nginx \
  &&  pip install virtualenv \
  &&  pip install gunicorn \
  &&  virtualenv venv \
  &&  apt-get install python3.10-venv -y \
  &&  python3 -m venv venv \
  &&  /bin/bash -c "source venv/bin/activate" \
  &&  apt-get install python3-dev default-libmysqlclient-dev build-essential -y \
  &&  pip install flask_mysqldb

# Set working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip3 install -r requirements.txt

# Copy the app folder to the working directory
COPY . .
COPY gunicorn.service /etc/systemd/system/

CMD systemctl daemon-reload \
    && systemctl start gunicorn \
    && systemctl enable gunicorn \
    && systemctl start nginx \
    && systemctl enable nginx

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose port 80 for the Flask app
EXPOSE 5000

# Start the Flask app using gunicorn

CMD systemctl restart nginx \
    && systemctl restart gunicorn
CMD gunicorn --bind 0.0.0.0:5000 app:app

