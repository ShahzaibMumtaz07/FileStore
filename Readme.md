# File-Store

File-Store is a Django REST API for dealing with files upload and serving.

## Installation
Requires Python 3.9.11.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to run the following command.

```bash
pip install -r requirements.txt
```

## Usage
This project requires a .env file for running. .env_sample has been added for your reference.
Use following command for running the local instance.
```bash
python manage.py runserver 0.0.0.0:8000
```

## Test
```
python manage.py test tests
```

## Test Coverage
###Run coverage script
```bash
bash coverage_test.sh
```
### Coverage Report
| Name               | Stmts | Miss | Cover | Missing                                                                                  |
|--------------------|-------|------|-------|------------------------------------------------------------------------------------------|
| api/models.py      | 46    | 0    | 100%  |                                                                                          |
| api/serializers.py | 78    | 0    | 100%  |                                                                                          |
| api/urls.py        | 4     | 0    | 100%  |                                                                                          |
| api/views.py       | 267   | 20   | 95%   | 105-106, 123-124, 162-163, 254-255, 321-322, 338-339, 376-377, 447-448, 463-464, 500-501 |
## License
[MIT](https://choosealicense.com/licenses/mit/)