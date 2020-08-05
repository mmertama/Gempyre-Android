# Gempyre For Android

Early version

## To Get It Working

Gempyre for Android is currently build on Ubuntu (20.04),
other development platforms may will be possible upon interest.

### Before we begin:
* Install Android SDK
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
 
  
   
      


