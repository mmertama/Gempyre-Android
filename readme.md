# Gempyre For Android

Early version of [Gempyre](https://github.com/mmertama/Gempyre) for Android.
Or merely its is a wizard that creates a working NDK app that has a Gempyre GUI.

## To Get It Working

Gempyre for Android is currently build on Ubuntu (20.04),
other development platforms may will be possible upon interest.

### Before we begin:
* Install Android SDK (with NDK)
* Install Gradle (at least 6.5)
* Install CMake (at least 3.16)
* Install Ninja 
* Install Python 3.8

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
      


