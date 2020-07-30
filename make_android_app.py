import sys
import os
import subprocess
import argparse

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
    parser = argparse.ArgumentParser(description='Telex-Android init.')
    parser.add_argument('--project_name', help='Project name', nargs=1, default="TELEX_APP")
    parser.add_argument('--project_id', nargs=1, help="Project id, as 'com.something.myapp'", default="com.telex.myapp")

    args = parser.parse_args()
    
    file_uri = args.project_id.split('.')
    
    if len(file_uri) < 2:
        print("Expected project id as 'com.something.myapp'")
        exit(-1)
        
    env_path('ANDROID_HOME')
    env_path('ANDROID_SDK_ROOT')
    env_path('TELEX_DIR')
             
    try:
        os.mkdir(args.project_name)
    except OSError:
        print("Invalid project name:", args.project_name)
        exit(-2)
        
    global root
    root = args.project_name + '/'
        
    subprocess.run(['gradle', 'init', '--type', 'basic', '--dsl', 'groovy', '--project-name', args.project_name], cwd=root)
    
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
    
    app_build_gradle = '''
apply plugin: 'com.android.application'

android {
    compileSdkVersion 25
    defaultConfig {
        applicationId "''' + args.project_id + '''"
        minSdkVersion 16
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
      path "''' + root + '''/Telex/CMakeLists.txt"
    }
  }
  defaultConfig {
    externalNativeBuild {
        cmake {
            cppFlags "-std=c++17"
        }
    }
}

dependencies {
    implementation 'com.android.support.constraint:constraint-layout:1.1.2'
    implementation 'com.android.support:appcompat-v7:25.3.1'
}
'''
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

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>
'''
    
    write_line('app/src/main/res/layout/activity_main.xml', activity_main)
    
    
    telex_root = os.environ['TELEX_DIR']
    cmakelists =  '''cmake_minimum_required (VERSION 3.14)

set(NAME ''' + args.project_name.replace(' ', '_') + ''')
project (${NAME}test)

include(''' + telex_root + '''/scripts/addResource.cmake_script)

set(CMAKE_CXX_STANDARD 17)

include_directories(
     ''' + telex_root + '''/telexlib/include
    include
)

find_package (telex REQUIRED PATHS ''' + telex_root + ''')

add_compile_options(fexceptions)
add_compile_options(c++_static)

add_library(${PROJECT_NAME} SHARED
    src/main.cpp
    gui/${NAME}.html
    )

# Add Telex resources here with:  addResource(PROJECT ${PROJECT_NAME} TARGET include/${NAME}_resource.h SOURCES gui/${NAME}.html stuff/owl.png)

target_link_libraries (${PROJECT_NAME} telex)
'''
    write_line('Telex/CMakeLists.txt', cmakelists)

if __name__ == '__main__':
    main()