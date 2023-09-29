# Fetch Backend Internship Challenge
This is my submission for the [Fetch Backend Internship Challenge](https://fetch-hiring.s3.us-east-1.amazonaws.com/points-intern.pdf) OA

There are two components:
1. Flask application
2. Unit test

# Local Testing
To get a local copy of the Flask server app up and running for testing purposes, see below:

Note: Please feel free to message me if the instructions are not working.

## Prerequisites
If you prefer using [Docker](https://www.docker.com/), you do not need to do anything else.
<br><br>
Otherwise if you do not want to use Docker, you will need one of the following package managers installed:
- [Mambaforge](https://mamba.readthedocs.io/en/latest/mamba-installation.html)
- [pip](https://pypi.org/project/pip/)
## Installation
1. Clone the repo:
```
git clone https://github.com/rittvic/fetch-backend-oa.git
```
Make sure your current directory is the root directory of the repository.
### With Docker

To be filled

### Without Docker

<b>If you are using Mambaforge</b>

1. Create an environment with `environment.yaml` file for required dependencies. You can replace `myenv` with the desired environment name.
    ```
    mamba create -n myenv -f environment.yaml
    ```
2. Activate the new environment
    ```
    mamba activate myenv
    ```

<b>if you are using pip</b>
1. Create a virtual environment. You can replace `myenv` with the desired environment name
    ```
    python -m venv myenv
    ```
2. Activate the new virtual environment
    ```
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    ```
3. Install the required dependencies from `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
   
#### Running

You can now run the Flask server. It is set up to listen on port 8000 and all addresses (0.0.0.0) with debug enabled.
```
python server.py
```

You can also run tests. Currently, I have written one test with examples from the specification.
```
python test.py
```
