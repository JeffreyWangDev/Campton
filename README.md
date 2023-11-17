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
### Build it yourself
> 1. Start venv with `.\env\Scripts\activate`
> 2. Run `py main.py`
> #### Using docker
> > 1. Build the file with `docker build . -t campton`
> > 2. Run the file with `docker run campton`
### Prebuild version 
> 1. Run `docker pull ghcr.io/jeffreywangdev/campton:main` (replace main with the tag, all tags can be found [here](https://github.com/JeffreyWangDev/Campton/pkgs/container/campton))
> 2. Run `docker run -p 80:80 -v campton-data:/app/data ghcr.io/jeffreywangdev/campton:main` (replace the first number in -p with what port is needed)

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
