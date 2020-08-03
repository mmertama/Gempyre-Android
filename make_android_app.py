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
        print ("Shall be using Python 3.7")
        exit(-1)
    
    parser = argparse.ArgumentParser(description='Gempyre-Android init.')
    parser.add_argument('--project_name', help='Project name', nargs=1, default="GEMPYRE_APP")
    parser.add_argument('--project_id', nargs=1, help="Project id, as 'com.something.myapp'", default="com.gempyre.myapp")
    parser.add_argument('--cmake_path', nargs=1, help="Since Android SDK default Cmake is too old, path to (at least) 3.16 is needed, dont include bin :-o",
    default= "/usr/local" if sys.platform == 'darwin' else '/usr')

    args = parser.parse_args()
    
    file_uri = args.project_id.split('.')
    
    if len(file_uri) < 2:
        print("Expected project id as 'com.something.myapp'")
        exit(-1)
        
    if 'ANDROID_HOME' not in os.environ and 'ANDROID_SDK_ROOT' not in os.environ:
        print(env, "ANDROID_HOME nor ANDROID_SDK_ROOT is not set")
        exit(-3)
 
    if sys.platform == 'darwin':
        env_path('AR')
        env_path('RANLIB')
        
    #env_path('ANDROID_TOOLCHAIN')
    
    if not os.path.exists(args.cmake_path + '/bin/cmake'):
        print("cmake not found at", args.cmake_path + '/bin')
        exit(-3)
    
    capture = subprocess.run([args.cmake_path + '/bin/cmake', '--version'], capture_output=True)
    m = re.match(r'cmake\sversion\s(\d+)\.(\d+)(?:\.(\d+))?', capture.stdout.decode('ascii'))
    if not m:
        print("Cannot find cmake", capture.stderr)
        parser.print_help()
        exit(-1);
    if int(m[1]) < 3 or int(m[1]) == 3 and int(m[2]) < 11:
        print("Invalid cmake version:", capture.stdout)
        exit(-4)
        
             
    try:
        os.mkdir(args.project_name)
    except OSError:
        print("Invalid project name:", args.project_name)
        exit(-2)
        
    global root
    root = args.project_name + '/'
        
    gradle_call = ['gradle', 'init', '--type', 'basic', '--dsl', 'groovy', '--project-name', args.project_name]    
        
    subprocess.run(gradle_call, cwd=root)
    
    add_line('settings.gradle', "include ':app'")

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
    
    app_build_gradle = '''
apply plugin: 'com.android.application'

android {
    compileSdkVersion 25
    defaultConfig {
        applicationId "''' + args.project_id + '''"
        minSdkVersion 25
        targetSdkVersion 25
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
                          "-DANDROID_STL=c++_static",
                          "-DCMAKE_ANDROID_ARCH_ABI=armeabi-v7a",
                          "-DCMAKE_ANDROID_ARCH=armv7-a",
                          "-DRANLIB=''' + os.environ['RANLIB'] if sys.platform == 'darwin' else 'None' + '''"
                }
            }
    }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    implementation 'com.android.support.constraint:constraint-layout:1.1.2'
    implementation 'com.android.support:appcompat-v7:25.3.1'    
}

'''
    write_line('local.properties', 'cmake.dir="' + args.cmake_path + '"\n')
    
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
    
    main_activity = '''
package ''' + args.project_id + ''';

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.util.Base64;

public class MainActivity extends Activity {
	private WebView webView;

    public native int callMain();

    public int onLoad(String url) {
            String encodedHtml = Base64.encodeToString(url.getBytes(),
            Base64.NO_PADDING);
            webView.loadData(encodedHtml, "text/html", "base64");
            return 0;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
	System.loadLibrary("gempyre");

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
    
    project_name = args.project_name.replace(' ', '_')
    
    cmakelists =  '''cmake_minimum_required (VERSION 3.11)

set(NAME ''' + project_name + ''')
project (${NAME}test)

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
    #include <gempyre.h>
    #include "main_resource.h"
    
    int main() {
        Gempyre::Ui ui({{"/main.html", Mainhtml}}, "main.html");
        Gempyre::Element(ui, "h2").setHTML("Gempyre for Android!");
        ui.run();
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
