# Personal Blog Site

This is a demo personal blogging site that was created to include in my portfolio.

![myblog](https://user-images.githubusercontent.com/50628520/112199567-66750600-8c36-11eb-8fcb-9ccbaebd33a0.jpg)


## Live Preview
[Click Here](https://personal-blog-site-ten.vercel.app/)

## Local Preview

1. Create a python virtual environment
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment
   ```bash
   source venv/bin/activate
   ```
3. Install the requirements
   ```bash
   pip install -r "requirements.txt"
   ```
4. Create a `.env` file in a project root directory and set all the environment variables based on the provided `.env.sample` example.
   
5. Migrate the database
   ```bash
   python manage.py migrate
   ```
6. Run the development server
   ```bash
   python manage.py runserver
   ```
7. Preview: http://127.0.0.1:8000

Note: If you want to open the admin panel go to http://127.0.0.1:8000/admin, and make sure you have an admin account.
To create admin account run the following command.
```bash
   python manage.py createsuperuser
```


Happy Coding !!
