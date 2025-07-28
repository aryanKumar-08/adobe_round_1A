# Round 1A - PDF Outline Extractor

## Build
docker build --platform linux/amd64 -t round1a-extractor .

## Run
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a-extractor
