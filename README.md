# Campton
> Website developed for the Acton Lions Club to assist in the annual ski and skate sale.
# Getting Started
## Requirements
- Python 3.9+
- PIP
- Docker (Optional)
## Installation
```git clone https://github.com/JeffreyWangDev/Campton.git
cd Campton
py -m venv env
.\env\Scripts\activate
py -m pip install -r requirements.txt
```
## Running
1. Start venv with `.\env\Scripts\activate`
2. Run `py main.py`
Using docker
1. Build the file with `docker build . -t campton`
2. Run the file with `docker run campton`

# Features
- User Registration
- Item registration
- Item status tracker
-   Keeps track of whether items are unsold, sold, or sold and paid for
- Checkout for buyers
-   Receipt printing
- Checkout for sellers

# To-do
- [x] Docstring for all function
- [x] Organize code
- [ ] Fix all naming to snake_case
- [ ] Change all forms to a js+api
- [ ] Rewrite python to be more readable 
- [ ] Add documentation
- [ ] Add configurations to all features (maybe a generator to make a version for every type of sale)

# License
MIT License
