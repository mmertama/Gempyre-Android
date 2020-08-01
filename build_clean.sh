git clean -dffx
export AR=$(find ${ANDROID_HOME} -name arm-linux-androideabi-ar | head -n 1)
export RANLIB=$(find ${ANDROID_HOME} -name arm-linux-androideabi-ranlib | head -n 1)
python3 make_android_app.py
pushd GEMPYRE_APP/
./gradlew build
popd
