#git clean -dffx
python3 make_android_app.py
pushd GEMPYRE_APP/
./gradlew build -x test
popd
