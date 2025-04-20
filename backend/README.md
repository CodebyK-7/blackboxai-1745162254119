# Job Portal Backend

## Setup Instructions

1. Create a PostgreSQL database named `jobportal` and a user with appropriate permissions.

2. Update the `.env` file with your PostgreSQL credentials and a secret key.

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the Flask app:
```
python app.py
```

The app will be available at `http://localhost:5000`.

## API Endpoints

- `POST /signup` - Register a new student. JSON body: email, password, full_name, academic_details, personal_details
- `POST /login` - Login student. JSON body: email, password
- `POST /logout` - Logout current user
- `GET /jobs` - Get list of available jobs (requires login)
- `POST /apply/<job_id>` - Apply for a job (requires login)

## Notes

- This is a basic prototype. For production, consider adding proper validation, error handling, and security measures.
- Frontend can be connected to these APIs for full functionality.
