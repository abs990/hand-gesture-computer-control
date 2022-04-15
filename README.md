<h1 align="center"> Hand-gesture based Computer Control </h1> <br>

## Start-up order
1. Executor
2. Control server
3. Gesture client
4. Unity (optional)

## Development environment

```
Python                                            3.7.0
Unity                                             2021.2.19f1
```

## Python package versions
```
absl-py                                           1.0.0
attrs                                             21.4.0
certifi                                           2021.10.8
charset-normalizer                                2.0.12
click                                             8.0.4
cycler                                            0.11.0
Flask                                             2.0.3
fonttools                                         4.29.1
idna                                              3.3
importlib-metadata                                4.11.2
itsdangerous                                      2.1.0
Jinja2                                            3.0.3
keyboard                                          0.13.5
kiwisolver                                        1.3.2
MarkupSafe                                        2.1.0
matplotlib                                        3.5.1
mediapipe                                         0.8.9.1
numpy                                             1.21.5
opencv-contrib-python                             4.5.5.62
packaging                                         21.3
Pillow                                            9.0.1
pip                                               21.2.2
protobuf                                          3.19.4
PyDbLite                                          3.0.4
pyobjc                                            8.4.1
pyobjc-core                                       8.4.1
pyobjc-framework-Accessibility                    8.4.1
pyobjc-framework-Accounts                         8.4.1
pyobjc-framework-AddressBook                      8.4.1
pyobjc-framework-AdServices                       8.4.1
pyobjc-framework-AdSupport                        8.4.1
pyobjc-framework-AppleScriptKit                   8.4.1
pyobjc-framework-AppleScriptObjC                  8.4.1
pyobjc-framework-ApplicationServices              8.4.1
pyobjc-framework-AppTrackingTransparency          8.4.1
pyobjc-framework-AudioVideoBridging               8.4.1
pyobjc-framework-AuthenticationServices           8.4.1
pyobjc-framework-AutomaticAssessmentConfiguration 8.4.1
pyobjc-framework-Automator                        8.4.1
pyobjc-framework-AVFoundation                     8.4.1
pyobjc-framework-AVKit                            8.4.1
pyobjc-framework-BusinessChat                     8.4.1
pyobjc-framework-CalendarStore                    8.4.1
pyobjc-framework-CallKit                          8.4.1
pyobjc-framework-CFNetwork                        8.4.1
pyobjc-framework-ClassKit                         8.4.1
pyobjc-framework-CloudKit                         8.4.1
pyobjc-framework-Cocoa                            8.4.1
pyobjc-framework-Collaboration                    8.4.1
pyobjc-framework-ColorSync                        8.4.1
pyobjc-framework-Contacts                         8.4.1
pyobjc-framework-ContactsUI                       8.4.1
pyobjc-framework-CoreAudio                        8.4.1
pyobjc-framework-CoreAudioKit                     8.4.1
pyobjc-framework-CoreBluetooth                    8.4.1
pyobjc-framework-CoreData                         8.4.1
pyobjc-framework-CoreHaptics                      8.4.1
pyobjc-framework-CoreLocation                     8.4.1
pyobjc-framework-CoreMedia                        8.4.1
pyobjc-framework-CoreMediaIO                      8.4.1
pyobjc-framework-CoreMIDI                         8.4.1
pyobjc-framework-CoreML                           8.4.1
pyobjc-framework-CoreMotion                       8.4.1
pyobjc-framework-CoreServices                     8.4.1
pyobjc-framework-CoreSpotlight                    8.4.1
pyobjc-framework-CoreText                         8.4.1
pyobjc-framework-CoreWLAN                         8.4.1
pyobjc-framework-CryptoTokenKit                   8.4.1
pyobjc-framework-DataDetection                    8.4.1
pyobjc-framework-DeviceCheck                      8.4.1
pyobjc-framework-DictionaryServices               8.4.1
pyobjc-framework-DiscRecording                    8.4.1
pyobjc-framework-DiscRecordingUI                  8.4.1
pyobjc-framework-DiskArbitration                  8.4.1
pyobjc-framework-DVDPlayback                      8.4.1
pyobjc-framework-EventKit                         8.4.1
pyobjc-framework-ExceptionHandling                8.4.1
pyobjc-framework-ExecutionPolicy                  8.4.1
pyobjc-framework-ExternalAccessory                8.4.1
pyobjc-framework-FileProvider                     8.4.1
pyobjc-framework-FileProviderUI                   8.4.1
pyobjc-framework-FinderSync                       8.4.1
pyobjc-framework-FSEvents                         8.4.1
pyobjc-framework-GameCenter                       8.4.1
pyobjc-framework-GameController                   8.4.1
pyobjc-framework-GameKit                          8.4.1
pyobjc-framework-GameplayKit                      8.4.1
pyobjc-framework-ImageCaptureCore                 8.4.1
pyobjc-framework-IMServicePlugIn                  8.4.1
pyobjc-framework-InputMethodKit                   8.4.1
pyobjc-framework-InstallerPlugins                 8.4.1
pyobjc-framework-InstantMessage                   8.4.1
pyobjc-framework-Intents                          8.4.1
pyobjc-framework-IntentsUI                        8.4.1
pyobjc-framework-IOSurface                        8.4.1
pyobjc-framework-iTunesLibrary                    8.4.1
pyobjc-framework-KernelManagement                 8.4.1
pyobjc-framework-LatentSemanticMapping            8.4.1
pyobjc-framework-LaunchServices                   8.4.1
pyobjc-framework-libdispatch                      8.4.1
pyobjc-framework-LinkPresentation                 8.4.1
pyobjc-framework-LocalAuthentication              8.4.1
pyobjc-framework-LocalAuthenticationEmbeddedUI    8.4.1
pyobjc-framework-MailKit                          8.4.1
pyobjc-framework-MapKit                           8.4.1
pyobjc-framework-MediaAccessibility               8.4.1
pyobjc-framework-MediaLibrary                     8.4.1
pyobjc-framework-MediaPlayer                      8.4.1
pyobjc-framework-MediaToolbox                     8.4.1
pyobjc-framework-Metal                            8.4.1
pyobjc-framework-MetalKit                         8.4.1
pyobjc-framework-MetalPerformanceShaders          8.4.1
pyobjc-framework-MetalPerformanceShadersGraph     8.4.1
pyobjc-framework-MetricKit                        8.4.1
pyobjc-framework-MLCompute                        8.4.1
pyobjc-framework-ModelIO                          8.4.1
pyobjc-framework-MultipeerConnectivity            8.4.1
pyobjc-framework-NaturalLanguage                  8.4.1
pyobjc-framework-NetFS                            8.4.1
pyobjc-framework-Network                          8.4.1
pyobjc-framework-NetworkExtension                 8.4.1
pyobjc-framework-NotificationCenter               8.4.1
pyobjc-framework-OpenDirectory                    8.4.1
pyobjc-framework-OSAKit                           8.4.1
pyobjc-framework-OSLog                            8.4.1
pyobjc-framework-PassKit                          8.4.1
pyobjc-framework-PencilKit                        8.4.1
pyobjc-framework-Photos                           8.4.1
pyobjc-framework-PhotosUI                         8.4.1
pyobjc-framework-PreferencePanes                  8.4.1
pyobjc-framework-PushKit                          8.4.1
pyobjc-framework-Quartz                           8.4.1
pyobjc-framework-QuickLookThumbnailing            8.4.1
pyobjc-framework-ReplayKit                        8.4.1
pyobjc-framework-SafariServices                   8.4.1
pyobjc-framework-SceneKit                         8.4.1
pyobjc-framework-ScreenCaptureKit                 8.4.1
pyobjc-framework-ScreenSaver                      8.4.1
pyobjc-framework-ScreenTime                       8.4.1
pyobjc-framework-ScriptingBridge                  8.4.1
pyobjc-framework-SearchKit                        8.4.1
pyobjc-framework-Security                         8.4.1
pyobjc-framework-SecurityFoundation               8.4.1
pyobjc-framework-SecurityInterface                8.4.1
pyobjc-framework-ServiceManagement                8.4.1
pyobjc-framework-ShazamKit                        8.4.1
pyobjc-framework-Social                           8.4.1
pyobjc-framework-SoundAnalysis                    8.4.1
pyobjc-framework-Speech                           8.4.1
pyobjc-framework-SpriteKit                        8.4.1
pyobjc-framework-StoreKit                         8.4.1
pyobjc-framework-SyncServices                     8.4.1
pyobjc-framework-SystemConfiguration              8.4.1
pyobjc-framework-SystemExtensions                 8.4.1
pyobjc-framework-UniformTypeIdentifiers           8.4.1
pyobjc-framework-UserNotifications                8.4.1
pyobjc-framework-UserNotificationsUI              8.4.1
pyobjc-framework-VideoSubscriberAccount           8.4.1
pyobjc-framework-VideoToolbox                     8.4.1
pyobjc-framework-Virtualization                   8.4.1
pyobjc-framework-Vision                           8.4.1
pyobjc-framework-WebKit                           8.4.1
pyparsing                                         3.0.7
python-dateutil                                   2.8.2
python-dotenv                                     0.19.2
requests                                          2.27.1
setuptools                                        58.0.4
six                                               1.16.0
typing_extensions                                 4.1.1
urllib3                                           1.26.9
Werkzeug                                          2.0.3
wheel                                             0.37.1
zipp                                              3.7.0
```

## Acknowledgments
1. Google Mediapipe - https://google.github.io/mediapipe/solutions/hands.html
2. 2D Hand pose estimation - https://notrocketscience.blog/gentle-introduction-to-2d-hand-pose-estimation-approach-explained/
3. Python keyboard control - https://stackabuse.com/guide-to-pythons-keyboard-module/
4. Python mouse control - https://web.archive.org/web/20111229234504/http://www.geekorgy.com:80/index.php/2010/06/python-mouse-click-and-move-mouse-in-apple-mac-osx-snow-leopard-10-6-x/