# comper-crawler-python


## Installation
To run this script, you'll need ```python >= 3.7``` interpreter installed on your machine. It's recomendable to use an isolated Python environment with ```venv```.

### Linux:
```sh
git clone https://github.com/igorgbianchi/comper-crawler-python
cd comper-crawler-python
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 app.py
``` 

See the results on ```output.json```.

### Example
```json
[   
    {
        "name": "Vinho Chileno Casillero del Diablo Concha y Toro Sauvignon Blanc 750ml",
        "img_url": "https://comper.vteximg.com.br/arquivos/ids/159755-292-292/56030.jpg?v=637210523685330000",
        "price": 62.99,
        "availability": true,
        "url": "https://www.comperdelivery.com.br/vinho-chileno-casillero-del-diablo-concha-y-toro-s/p"
    },
    {
        "name": "Vodka Destilada Absolut Garrafa 750ml",
        "img_url": "https://comper.vteximg.com.br/arquivos/ids/178033-292-292/1586025_1.jpg?v=637332718037630000",
        "price": 84.9,
        "availability": true,
        "url": "https://www.comperdelivery.com.br/vodka-absolut-750ml/p"
    },
    {
        "name": "Vinho Paso Grande 750ml Private Reserva Pinot Noir",
        "img_url": "https://comper.vteximg.com.br/arquivos/ids/177133-292-292/6846.jpg?v=637315393582700000",
        "price": 0,
        "availability": false,
        "url": "https://www.comperdelivery.com.br/vinho-paso-grande-750ml-private-reserva-pinot-noir/p"
    }
]
``` 