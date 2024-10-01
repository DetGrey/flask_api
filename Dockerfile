# Base image
FROM python:alpine3.20 

# Copy alle filer fra . til /app inde i image
COPY . /app

# Change dir (CD)
WORKDIR /app

# Install alle dependencies til dette projekt
RUN pip install -r requirements.txt

# åben port 5050 ud mod verden
EXPOSE 5050

# Start kommando når container kører
CMD [ "python", "app.py" ]
