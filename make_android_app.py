import sys
import os
import subprocess
import argparse

root = ''

def add_line(file_name, line):
    with open(os.path.join(parser.project_name, filename), 'a') as f
        f.write(line)

def main():
    parser = argparse.ArgumentParser(description='Telex-Android init.')
    parser.add_argument('--project_name', help='Project name', default="TELEX_APP")
    parser.add_argument('--project_id', help="Project id, as 'com.something.myapp'", default="com.telex.myapp")

    args = parser.parse_args()
    
    file_uri = parser.project_id.split('.')
    
    if len(file_uri) != 3:
        print("Expected project id as 'com.something.myapp'")
        exit(-1)
            
    try:
        os.mkdir(parser.project_name)
    except OSError:
        print("Invalid project name:", parser.project_name)
        exit(-2)
        
    root = parser.project_name
        
    subprocess.run(['gradle', 'init', '--type', 'basic', '--dsl', 'groovy', '--project-name', args.project_name])
    
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
    
    os.mkdir('app')
    
    app_build_gradle = '''
apply plugin: 'com.android.application'

android {
    compileSdkVersion 25
    defaultConfig {
        applicationId ''' + args.project_id + '''
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
}

dependencies {
    implementation 'com.android.support.constraint:constraint-layout:1.1.2'
    implementation 'com.android.support:appcompat-v7:25.3.1'
}'''
    
    
add_line('app/build.gradle', app_build_gradle)    
    
app_styles = '''
<resources>

    <!-- Base application theme. -->
    <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <!-- Customize your theme here. -->
    </style>

</resources>    
'''

add_line('app/src/main/res/values/styles.xml', app_styles)
    
android_manifest = '''
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="''' + args.project_id + '''">

    <application
        android:label=" ''' + args.project_name + '''"
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

add_line('app/src/main/AndroidManifest.xml', android_manifest)

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

add_line('app/src/main/java/' + file_uri.join('/') + '/MainActivity.java', main_activity)

activity_main = '''
<?xml version="1.0" encoding="utf-8"?>
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

add_line('app/src/main/res/layout/activity_main.xml', activity_main)

if __name__ == '__main__':
    main()