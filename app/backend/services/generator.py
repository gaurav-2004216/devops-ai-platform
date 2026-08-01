def generate_dockerfile(language):

    if language == "Python":
        return """FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
"""

    elif language == "Node.js":
        return """FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
"""

    elif language == "Java":
        return """FROM eclipse-temurin:17

WORKDIR /app

COPY . .

CMD ["java","-jar","app.jar"]
"""

    return "Language not supported."
