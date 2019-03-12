# ThreemaToHtml

__NEVER__ leave your private key on a public computer. Keep it __private__!

## About

This tool can be used to convert a Threema Backup "threema.db" database into human readable HTML files.

## Requirements

 * Python 3

 * Decrypted database file, can be generated with [threema-decrypt](https://github.com/wilzbach/threema-decrypt)

 * [sqlcipher](https://www.zetetic.net/sqlcipher/) is required to decrypt the database

## Usage

* Copy the config.json.example file to config.json and insert your private key.

* Run:

```
./convert.py threema.db
```

* Find the files "contacts.html" and "groups.html" in the ./html/ folder.

## License

see ./LICENSE.md

## Author

Mebus, mebus.inbox@mail.ru
