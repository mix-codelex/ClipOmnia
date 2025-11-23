docker build -t clipomnia-deb -f Dockerfile.build-deb .
docker create --name clipomnia_tmp clipomnia-deb
docker cp clipomnia_tmp:/output/clipomnia.deb .
docker rm clipomnia_tmp
