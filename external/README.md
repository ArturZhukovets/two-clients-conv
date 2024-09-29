# Frontend for bank.

* clone repository: `git clone git@git.nordicwise.com:business/frontend-for-bank-external.git` or `git clone https://git.nordicwise.com/business/frontend-for-bank-external.git`.
* copy `.env.example` -> `.env`
* set variables in `.env`
* copy `init_db.json.example` -> `L7X_DB_INIT_JSON_PATH`
* update json-file by path `L7X_DB_INIT_JSON_PATH`
* `chmod a=r <L7X_DB_INIT_JSON_PATH>`
* `chown 40300:40300 <L7X_SSL_CERTIFICATE_PATH>`
* `chown 40300:40300 <L7X_SSL_PRIVATE_KEY_PATH>`
* run `./run.sh`
* remove json-file by path `L7X_DB_INIT_JSON_PATH`
* run `./stop.sh`
* run `./run.sh`
* open in browser `https://localhost:8081/gui/` (or other port from `L7X_FRONTEND_PORT`)
