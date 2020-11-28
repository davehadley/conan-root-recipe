
if [ ! -d "venv" ]
then
    python3 -m venv venv \
    && source venv/bin/activate \
    && python -m pip install conan pre-commit isort mypy black flake8;
fi

source venv/bin/activate
export CONAN_HOOK_ERROR_LEVEL=40