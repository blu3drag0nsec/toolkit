#!/bin/bash
#git clone https://github.com/MuirlandOracle/up-http-tool --depth 1 up && 
cd up

python3 -m venv env

./env/bin/python -m pip install -r requirements.txt

cat << EOF | sudo tee /usr/local/bin/up 2>&1 &>/dev/null
#!/usr/bin/env sh
$(pwd)/env/bin/python $(pwd)/up \$@
EOF

sudo chmod 555 /usr/local/bin/up
