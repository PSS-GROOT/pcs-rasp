echo "============Build on platform $OSTYPE ================"
if [[ "$OSTYPE" == "darwin"* ]]; then 
    # unix
    docker buildx build --platform linux/amd64 -t pcs-rasp .
else 
    # window
    docker buildx build -t pcs-rasp .
fi

