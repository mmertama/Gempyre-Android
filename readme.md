# Gempyre For Android

Early version of [Gempyre](https://github.com/mmertama/Gempyre) for Android.
Or merely its is a wizard that creates a working NDK app that has a Gempyre GUI.

## To Get It Working

Using Gempyre for Android is currently building on Linux (or actually Ubuntu 20.04). Therefore for non-Linux platforms
I advice to 1) Install Virtualbox 2) install Lubuntu (20.x) 3) Install android studio (available at Snap) etc. as in prequisities. 

### Prequisities, before we begin:
* Install Android SDK (with NDK) (e.g. snap install-android-studio --classic)
* Install Gradle (at least 6.5) (e.g. sudo sudo add-apt-repository ppa:cwchien/gradle && sudo apt-get update && sudo apt upgrade gradle)
* Install CMake (at least 3.16) (e.g. sudo apt-get install cmake)
* Install Ninja  (e.g. sudo apt-get install ninja-build)
* Install Python 3.8 (shall already be there)

### Call Wizard:
 There is a Wizard that you can modify
 Run <code>python3 make_android_app.py --help</code>
 to see available options, but run with default values
 'should' be ok (WoMM)
 
 It generates a folder (GEMPYRE_APP by default).
 Int that folder there is 'Gempyre' folder, that contains a
 C++ Cmake project that can be modified for your own purposes.
 
 To build it, call standard gradle build:
 <code>./gradlew build -x test</code>
 
 ### Example
 The Wizard generated Gempyre C++ application looks something like this:
 <pre>
 #include <jni.h>
 #include <gempyre.h>
 #include "main_resource.h"
   
  ANDROID_MAIN() {
     Gempyre::setDebug(Gempyre::DebugLevel::Debug, true); // true shall use syslog, that in android is logcat!
     Gempyre::setJNIENV(env, obj);
     Gempyre::Ui ui({{"/main.html", Mainhtml}}, "main.html");
     Gempyre::Element(ui, "h2").setHTML("Gempyre for Android!");
     ui.run();
     return 0;
 }
 </pre>
  
 This example application just writes a "Gempyre for Android!" in the given header (see <code>gui/main.hml</code>). More exampes in the [Gempyre](https://github.com/mmertama/Gempyre) repositiry.   
 
 ### Useful commands
 #### Build
 <code>./gradlew build -x test</code>
 #### Install
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb -s </code><mark>device-id</mark><code> install </code><mark>path_to_apk</mark></code>
 #### Uninstall
 Needed prior to re-install. </br>
 <code> ${ANDROID_SDK_ROOT}/platform-tools/adb -s </code><mark>device-id</mark><code> uninstall </code><mark>product_id</mark> </code>
 #### Start for debugger
 For Android Studio attach to process. </br>
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb shell am start -n "</code><mark>product_id</mark><code>/.MainActivity" -D</code>
 #### List Devices
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb devices</code>
  
      


