import sys
import os
import subprocess
import argparse
import re

root = ''

def add_line(file_name, line):
    with open(os.path.join(root, file_name), 'a') as f:
        f.write(line)
        
def write_line(file_name, line):
    full_name = os.path.join(root, file_name)
    path = os.path.dirname(full_name)
    os.makedirs(path, exist_ok=True)
    with open(full_name, 'w') as f:
        f.write(line)
        
        
def env_path(env):
    if env not in os.environ:
        print(env, "is not set")
        exit(-3)
    if not os.path.exists(os.environ[env]):
        print("%s: '%s' not found", env, os.environ[env])
        exit(-3)


def main():

    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 7):
        print ("Shall be using at least Python 3.7")
        exit(-1)
    
    parser = argparse.ArgumentParser(description='Gempyre-Android init.')
    parser.add_argument('--project_name', help='Project name', nargs=1, default="GEMPYRE_APP")
    parser.add_argument('--android_sdk', help='Android Path', nargs=1)
    parser.add_argument('--android_ndk', help='Android NDK Path', nargs=1)
    parser.add_argument('--project_id', nargs=1, help="Project id, as 'com.something.myapp'", default="com.gempyre.myapp")
    parser.add_argument('--cmake_path', nargs=1, help="Since Android SDK default Cmake is too old, path to (at least) 3.16 is needed, dont include bin :-o",
    default= "/usr/local" if sys.platform == 'darwin' else '/usr')

    args = parser.parse_args()
    
    file_uri = args.project_id.split('.')
    
    if len(file_uri) < 2:
        print("Expected project id as 'com.something.myapp'")
        exit(-1)
     
    android_root = args.android_sdk[0] if args.android_sdk else None
    
    if not android_root:
        if 'ANDROID_HOME' in os.environ:
            android_root = os.environ['ANDROID_HOME']
        elif 'ANDROID_SDK_ROOT' in os.environ:
            android_root = os.environ['ANDROID_SDK_ROOT']
        else:
            print("Android SDK not found")
            exit(-34)    
   
    if not os.path.exists(android_root):
        print("Invalid Android SDK ", android_root)
        exit(-2)
    
    android_ndk_root = args.android_ndk[0] if args.android_ndk else None
        
    if not android_ndk_root:
        if 'ANDROID_NDK_ROOT' in os.environ:
            android_ndk_root = os.environ['ANDROID_NDK_ROOT']
        else:
            print("Android NDK not found")
            exit(-34)
            
    if not os.path.exists(android_ndk_root):
        print("Invalid Android NDK ", android_ndk_root)
        exit(-2)
            
 
    if sys.platform == 'darwin':
        env_path('AR')
        env_path('RANLIB')
        
    #env_path('ANDROID_TOOLCHAIN')
    
    if not os.path.exists(args.cmake_path + '/bin/cmake'):
        print("cmake not found at", args.cmake_path + '/bin')
        exit(-3)
    
    capture = subprocess.run([args.cmake_path + '/bin/cmake', '--version'], capture_output=True)
    m = re.match(r'cmake\s+version\s+(\d+)\.(\d+)(?:\.(\d+))?', capture.stdout.decode('ascii'))
    if not m:
        print("Cannot find cmake", capture.stderr.decode('ascii'))
        parser.print_help()
        exit(-1);
    if int(m[1]) < 3 or int(m[1]) == 3 and int(m[2]) < 11:
        print("Invalid cmake version:", capture.stdout.decode('ascii'))
        exit(-4)
        
    capture = subprocess.run(['gradle', '--version'], capture_output=True)
    ver_passed = False
    if len(capture.stderr):
        print("Error", capture.stderr).decode('ascii')
    for l in capture.stdout.decode('ascii').split('\n'):
        m = re.match(r'Gradle\s+(\d+)\.(\d+)(?:\.(\d+))?', l)
        if m:
             if int(m[1]) > 6 or int(m[1]) == 6 and int(m[2]) >= 5:
                ver_passed = True
     
    if not ver_passed:
        print("Tool old Gradle", capture.stdout.decode('ascii'))
        print("Expect 6.5...")
        exit(-1)       
             
    try:
        os.mkdir(args.project_name)
    except OSError:
        print("Invalid project name:", args.project_name)
        exit(-2)
        
    global root
    root = args.project_name + '/'
        
    gradle_call = ['gradle', 'init', '--type', 'basic', '--dsl', 'groovy', '--project-name', args.project_name]    
        
    subprocess.run(gradle_call, cwd=root)
    
    add_line('settings.gradle', "include ':app'\nrootProject.name = \"" + args.project_name + "\"\n")

    build_gradle = '''
buildscript {

    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.1.3'
    }
}

allprojects {
    repositories {
        google()
        jcenter()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}

'''
    
    add_line('build.gradle', build_gradle)
    
    os.mkdir(root + 'app')
    
    # Is filter needed? 'arm64-v8a', 
    
    osx_line = ''
    if sys.platform == 'darwin':
        osx_line = ",\n                          -DRANLIB=\"" + os.environ['RANLIB'] + "\"\n"
    
    app_build_gradle = '''
apply plugin: 'com.android.application'

android {
    compileSdkVersion 29
    buildToolsVersion "30.0.1"
    defaultConfig {
        applicationId "''' + args.project_id + '''"
        minSdkVersion 24
        targetSdkVersion 29	
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    
    externalNativeBuild {
        cmake {
          path "../Gempyre/CMakeLists.txt"
        }
    }

    defaultConfig {
        externalNativeBuild {
          ndk {
            abiFilters 'armeabi-v7a'
            }
            cmake {
                cppFlags "-std=c++17"
                version "3.11"
                arguments "-DHAS_TEST=OFF",
                          "-DHAS_BLOG=OFF",
                          "-DHAS_AFFILIATES=OFF",
                          "-DHAS_MDMAKER=OFF",
                          "-DANDROID_STL=c++_shared",
                          "-DCMAKE_ANDROID_ARCH_ABI=armeabi-v7a",
                          "-DCMAKE_ANDROID_ARCH=armv7-a" ''' + osx_line + '''
                }
            }
    }	
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    implementation 'com.android.support.constraint:constraint-layout:1.1.2'
    implementation 'androidx.appcompat:appcompat:1.1.0'   
}

'''
    write_line('local.properties', 'cmake.dir=' + args.cmake_path + '\nsdk.dir=' + android_root + '\nndk.dir=' + android_ndk_root + '\n')
    
    add_line('app/build.gradle', app_build_gradle)
    
    app_styles = '''
<resources>

    <!-- Base application theme. -->
    <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <!-- Customize your theme here. -->
    </style>

</resources>    
'''
    write_line('app/src/main/res/values/styles.xml', app_styles)
    
    android_manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="''' + args.project_id + '''">

    <application
        android:label="''' + args.project_name + '''"
        android:theme="@style/AppTheme">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
'''
    
    write_line('app/src/main/AndroidManifest.xml', android_manifest)
    
    project_name = args.project_name.replace(' ', '_')
    
    main_activity = '''
package ''' + args.project_id + ''';

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.util.Base64;

public class MainActivity extends Activity {
	private WebView webView;

    public native int callMain();

    public int onUiLoad(String url) {
            String encodedHtml = Base64.encodeToString(url.getBytes(),
            Base64.NO_PADDING);
            webView.loadData(encodedHtml, "text/html", "base64");
            return 0;
    }
    

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        System.loadLibrary("''' + project_name + '''");
        
	    webView = new WebView(this);
            setContentView(webView);

	    Thread thread = new Thread(new Runnable() {
		    public void run() {
			    callMain();
			    finish();
			    System.exit(0);
                     }
        	});
	    thread.start();
    }
}

'''
    
    write_line('app/src/main/java/' + '/'.join(file_uri) + '/MainActivity.java', main_activity)
    
    activity_main = '''<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
    />

</android.support.constraint.ConstraintLayout>
'''
    
    write_line('app/src/main/res/layout/activity_main.xml', activity_main)
    
    
    cmakelists =  '''cmake_minimum_required (VERSION 3.11)

set(NAME ''' + project_name + ''')
project (${NAME})

include(FeatureSummary)
include(GNUInstallDirs)
include(FetchContent)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DANDROID_ABI=armeabi-v7a")

FetchContent_Declare(
    gempyre_library
    GIT_REPOSITORY https://github.com/mmertama/Gempyre.git
    GIT_TAG        origin/android
    )
    
    
FetchContent_GetProperties(gempyre_library)
if(NOT gempyre_library)
  FetchContent_Populate(gempyre_library)
  add_subdirectory(${gempyre_library_SOURCE_DIR} ${gempyre_library_BINARY_DIR})
endif()

set(GEMPYRE_DIR ${gempyre_library_SOURCE_DIR})

include("${gempyre_library_SOURCE_DIR}/scripts/addResource.cmake_script")

include_directories(
    "${gempyre_library_SOURCE_DIR}/gempyrelib/include"
    include
)
    
add_library(${PROJECT_NAME} SHARED
    src/main.cpp
    gui/main.html
    )

addResource(PROJECT ${PROJECT_NAME} TARGET include/main_resource.h SOURCES gui/main.html)

link_directories(${gempyre_library_BINARY_DIR})
target_link_libraries (${PROJECT_NAME} gempyre)
'''
    write_line('Gempyre/CMakeLists.txt', cmakelists)
    
    main_cpp = ''' //This file is an example, a script generated
    #include <jni.h>
    #include <gempyre.h>
    #include "main_resource.h"
    
    extern "C" {
  
    JNIEXPORT jint JNICALL
    Java_com_gempyre_myapp_MainActivity_callMain(JNIEnv* env, jobject obj) {
        Gempyre::setJNIENV(env, obj);
        Gempyre::Ui ui({{"/main.html", Mainhtml}}, "main.html");
        Gempyre::Element(ui, "h2").setHTML("Gempyre for Android!");
        ui.run();
        return 0;
    }
    }
    '''
    
    write_line('Gempyre/src/main.cpp', main_cpp)
    
    gui_html = '''<!DOCTYPE html>
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
    '''

    write_line('Gempyre/gui/main.html', gui_html)

if __name__ == '__main__':
    main()
