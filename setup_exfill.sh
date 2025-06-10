#!/bin/bash
cd exfill

python3 -m venv env

./env/bin/python -m pip install -r requirements.txt

cat << EOF | sudo tee /usr/local/bin/exfill.py 2>&1 &>/dev/null
#!/usr/bin/env sh
$(pwd)/env/bin/python $(pwd)/exfill.py \$@
EOF

sudo chmod 555 /usr/local/bin/exfill.py
