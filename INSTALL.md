# For install and get it running

```
pip install -r requirements.txt

python main.py --help

```



# For install dev

```
pip install -r requirements-dev.txt
HEADLESS=1 pytest
```


## .env file need
```
cat >> .env
PINECONE_API_KEY=
PINECONE_API_ENV=

OPENAI_API_KEY=
HEADLESS=1
```
