#!/usr/bin/env python3
from app import create_app, appconfig

app = create_app(appconfig.BaseConfig)

if __name__ == '__main__':
    app.run(debug=True)
