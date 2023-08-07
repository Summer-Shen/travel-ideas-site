# travel-ideas-site

A website for sharing travel ideas based on Vue and Django. Implementation for Group Project of ICOM6034 (Website Engineering) at HKU.

## Running the backend

Please put the `db.sqlite3` file (available as part of the Moodle submission) under the `/server` directory, then run `python manage.py runserver`. You may have to modify the permissions of the `db.sqlite3` file.

After starting the server, you can access the admin UI at `http://127.0.0.1:8000/admin/ti/`.

## Running the frontend

Under the `/client` directory, run `npm install`, then run `npm run dev`. You can access the website at http://localhost:3000/.
