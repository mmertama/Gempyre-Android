git clean -dffx
export AR=${ANDROID_HOME}/ndk/21.3.6528147/toolchains/llvm/prebuilt/darwin-x86_64/bin/arm-linux-androideabi-ar
export RANLIB=${ANDROID_HOME}/ndk/21.3.6528147/toolchains/llvm/prebuilt/darwin-x86_64/bin/arm-linux-androideabi-ranlib
python3 make_android_app.py
pushd GEMPYRE_APP/
./gradlew build
popd
