
if [ ! -d "venv" ]
then
    python3 -m venv venv \
    && source venv/bin/activate \
    && python -m pip install conan;
fi

source venv/bin/activate
