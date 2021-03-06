# Gempyre For Android
__The easiest way to make Android applications on C++__

[Gempyre](https://github.com/mmertama/Gempyre) for Android is a wizard that creates a working NDK app that has a Gempyre GUI. The wizard creates a working skeleton application that is easy to modify and extend with C/C++ libraries.

## To Get It Working

Using Gempyre for Android is currently building on Linux (or actually Ubuntu 20.04). Therefore for non-Linux platforms
I advice to 1) Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads), provide at least 20GB drive and 4GB (or even 8GB) RAM to get build going smooth  2) install [Lubuntu (20.x)](https://lubuntu.net/) 3) Install android studio (available at Snap) etc. as in prequisities. 

### Prequisities, before we begin:
* Install Android SDK (with NDK) (<code>snap install-android-studio --classic</code>)
* Install Gradle (at least 6.5) (<code>sudo sudo add-apt-repository ppa:cwchien/gradle && sudo apt-get update && sudo apt upgrade gradle</code>)
* Install CMake (at least 3.16) (<code>sudo apt-get install cmake</code>)
* Install Ninja  (<code>sudo apt-get install ninja-build</code>)
* Install Python 3.8 (shall already be there)
* You may have to install build tools (<code>sudo apt-get install build-essential</build>)

### Call Wizard:
 There is a Wizard that you can modify
 Run <code>python3 make_android_app.py --help</code>
 to see available options. 
 
 <pre>
markus@markus-pc:~/Development/Gempyre-Android$ export ANDROID_SDK_ROOT=~/Android/Sdk
markus@markus-pc:~/Development/Gempyre-Android$ export ANDROID_NDK_ROOT=~/Android/Sdk/ndk/21.3.6528147
markus@markus-pc:~/Development/Gempyre-Android$ python3 make_android_app.py --project_name MyApp --project_id com.gempyre.myapp
</pre>
 
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
 Since the UI is just HTML, it looks like this:
 
 ```
  <!DOCTYPE html>
   <html>
     <head>
      <meta charset="utf-8">
      <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
      <meta http-equiv="Pragma" content="no-cache" />
      <meta http-equiv="Expires" content="0" />
      <title>drawCanvas</title>
    </head>
    <body>
     <script src="/gempyre.js"></script>
     <h1>Hello World!</h1>
     <h2 id="h2"></h2>
    </body>
  </html>
```
 
 This example application just writes a "Gempyre for Android!" in the given header (see <code>gui/main.hml</code>). More exampes in the [Gempyre](https://github.com/mmertama/Gempyre) repositiry.   
 
 ### Useful commands
 #### Build
 <code>./gradlew build -x test </code>
 #### List Connected Devices
 Set you phone to [Debug mode](https://developer.android.com/studio/debug/dev-options).</br>
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb devices </code>
 #### Install
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb -s</code> device-id <code>install</code> path_to_apk
 #### Uninstall
 Needed prior to re-install.</br>
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb -s</code> device-id <code>uninstall</code> product_id
 #### Start for debugger
 For Android Studio attach to process. </br>
 <code>${ANDROID_SDK_ROOT}/platform-tools/adb shell am start -n "</code>product_id<code>/.MainActivity" -D</code>
 
  
      


