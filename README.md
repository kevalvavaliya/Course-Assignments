# Course Assignments backend

### Description
This repository contains the source code for a course assignments project, which includes functionalities for user authentication, assignment management, enhanced security features, email notifications, and Docker deployment

#### Features

1. **Authentication Endpoints for Login**
   - Implemented mock authentication service.
   - Accepts any username/password pair.
   - Returns a signed JSON Web Token (JWT) for subsequent request validation.

2. **Assignment REST API Endpoints**
   - **Create:** Creates a new assignment with data provided in the request body.
   - **Read:** Returns all assignments based on data provided in the request body.
   - **Update:** Updates assignment with data provided in the request body.
   - **Delete:** Deletes the assignment.

3. **Validation for Existing API Endpoints**
   - Added validation to enhance security.
   - Only allows the teacher who created the assignment to delete or update it.
   - Returns error message if validation fails.

4. **Notification Email to Students**
   - Sends notification email to students when an assignment is created.

5. **Docker Image Deployment**
   - Created and published private Docker image of the micro-service.
   - Deployed the Docker image on Render.

#### Usage
1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd course-assignments-project`
3. Create python environment: `python -m venv .venv`
4. Run server: `flask run` 

#### API Documentation
For detailed API documentation, refer to [API Documentation]([Swagger](https://course-assignments.onrender.com/docs)https://course-assignments.onrender.com/docs).
