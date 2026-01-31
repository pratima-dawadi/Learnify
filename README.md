# Learnify

Learnify is an online learning platform built using **Django** and **Django REST Framework**.
It allows students to enroll in courses and track lesson progress, while instructors manage courses and lessons.

## Features
- User authentication and role-based access control
- Course and lesson management
- Student enrollment and lesson completion tracking

## Roles and Permissions
### Instructor
- Create and manage courses
- Add and manage lessons within courses

### Student
- Browse available courses
- Enroll in courses
- Mark lessons as completed
- Track course completion progress


## Setup and Instructions

### 1. Clone the Repository

To get started, first clone the repository to your local machine:

```bash
https://github.com/pratima-dawadi/Learnify.git
cd Learnify
```

### 2. Add environment variables
Create a .env file based on the provided sample-env file:

```bash
cp sample-env .env
```
Then edit `.env` accordingly


### 3. Build and start the container

To build and run the container run following command:

```bash
docker compose up --build
```
> **Note**: Use docker-compose (with hyphen) if you're using an older version of Docker.

Access the api documentation on [localhost:{your_port}/docs/](http://localhost:8000/docs/)

### 4. Seed initial data
Once docker container is started, open new terminal and run following command to seed the data:
```bash
docker compose exec web python manage.py seed_data
```
> This will populate:
>- An Instructor account
>- A Student account
>- Courses and lessons

## Login Credentials

| Role      | Email                 | Password   |
|-----------|-----------------------|------------|
| Instructor     | `instructor@gmail.com`     | `instructor123` |
| Student | `student@gmail.com` | `student123`   |


To be a user, register first and then log in. After logging in, you can access protected endpoints using your access token.