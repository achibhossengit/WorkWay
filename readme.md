# Work Way: Django REST Framework Project

This project, named "Work Way," is a job portal platform built using Django and Django REST Framework (DRF). It allows employers to post job opportunities and manage applications, while job seekers can apply for jobs and manage their profiles. The platform includes features for job categorization, application reviews, and user management.

---

## Features

### User Management
- Two user types: Employers and Job Seekers.
- Employers can manage their job postings and review applications.
- Job Seekers can apply for jobs, upload resumes, and manage applications.

### Job Management
- Employers can create, update, and delete job postings.
- Jobs are categorized into categories.
- Detailed job descriptions, requirements, and statuses.

### Applications and Reviews
- Job Seekers can apply for jobs and view application statuses.
- Employers can review applications and provide ratings and comments.

### API Documentation
- Swagger Documentation: https://work-way.vercel.app/api/v1/swagger/
- ReDoc Documentation: https://work-way.vercel.app/api/v1/redoc/
  
---

## Installation and Setup

1. Clone the repository:
    ```bash
    https://github.com/achibhossengit/WorkWay/
    cd WorkWay
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

---

## API Endpoints

### Base URL
`/api/v1/`

### Authentication
- `POST /auth/token/login/` - Obtain a token.
- `POST /auth/token/logout/` - Logout.

### Jobs
- **List All Jobs**: `GET /jobs/`
- **Create a Job**: `POST /jobs/` (Employers only)
- **Retrieve a Job**: `GET /jobs/{id}/`
- **Update a Job**: `PUT /jobs/{id}/` (Employers only)
- **Delete a Job**: `DELETE /jobs/{id}/` (Employers only)

### Categories
- **List All Categories**: `GET /categories/`
- **Create a Category**: `POST /categories/` (Admin only)
- **Retrieve a Category**: `GET /categories/{id}/`
- **Update a Category**: `PUT /categories/{id}/` (Admin only)
- **Delete a Category**: `DELETE /categories/{id}/` (Admin only)

### Category-Specific Jobs
- **List Jobs in a Category**: `GET /categories/{category_id}/jobs/`

### Applications
- **List Applications by Jobseeker**: `GET /jobseekers/{jobseeker_id}/applications/`
- **Apply for a Job**: `POST /jobseekers/{jobseeker_id}/applications/`
- **Update an Application**: `PUT /jobseekers/{jobseeker_id}/applications/{id}/`
- **Delete an Application**: `DELETE /jobseekers/{jobseeker_id}/applications/{id}/`

### Reviews
- **List Reviews for Jobseeker**: `GET /jobseekers/{jobseeker_id}/reviews/`
- **Add a Review for Jobseeker**: `POST /jobseekers/{jobseeker_id}/reviews/`
- **List Reviews for Employer**: `GET /employers/{employer_id}/reviews/`

### Employer-Specific Jobs
- **List Jobs by Employer**: `GET /employers/{employer_id}/jobs/`
- **List Applications for a Job**: `GET /employers/{employer_id}/jobs/{job_id}/applications/`

---

## API Documentation
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

---

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request.

---

## License
This project is licensed under the BSD License.

