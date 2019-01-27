## Install requirements:
pip install --no-cache-dir -r requirements.txt

## Run app:
python app.py

## local envirnment base URL 
http://127.0.0.1:5000:

## Create keyword endpoint:
/keyword
#### Example payload:
{
  "keyword": "ttt"
}

## Check results endpount:
/results

#### Example payload:
{
  "keyword": "eee",
  "number": 121
}
