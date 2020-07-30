git clean -dfx
python3 make_android_app.py
pushd TELEX_APP/
./gradlew build
popd
