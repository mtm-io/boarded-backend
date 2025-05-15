## How to work with it

### After you clone this repo create a virtual environment:

win/mac\
```console
python -m venv .venv
```

---

### Activate it:

win\
`.venv\Scripts\Activate.ps1`

mac\
`source .venv/bin/activate`

---

### Check the Virtual Environment is Active:

win\
`Get-Command python`

mac\
`which python`

<br>

> [!NOTE]
> If it shows the python binary at .venv\Scripts\python, inside of your project, then it worked.

---

### Upgrade pip:

`python -m pip install --upgrade pip`

---

### Install Packages from `requirements.txt`:

`pip install -r requirements.txt`

---

### Run the server:

` python -m uvicorn main:app --reload`

<br>

> [!IMPORTANT]
> Once you are done working on your project you should deactivate the virtual environment.
> `deactivate`
