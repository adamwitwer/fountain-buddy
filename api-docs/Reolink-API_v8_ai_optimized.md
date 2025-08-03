# API Documentation: Reolink-API_v8.pdf

**Total Pages:** 361

## Table of Contents

1. [Beginning](#beginning)
2. [parameterstoGetAlarmandSetAlarm](#parameterstogetalarmandsetalarm)
3. [Response:](#response:)
4. [Response：](#response：)
5. [Response：](#response：)
6. [Response：](#response：)
7. [example:](#example:)
8. [example:](#example:)
9. [example:](#example:)
10. [auth 0:notsupport](#auth-0:notsupport)
11. [Parameter M/O Description](#parameter-m/o-description)
12. [Parameter M/O Description](#parameter-m/o-description)
13. [Parameter M/O Description](#parameter-m/o-description)
14. [Parameter M/O Description](#parameter-m/o-description)
15. [Error Response](#error-response)
16. [authenticationprocess](#authenticationprocess)
17. [error](#error)

## Beginning


Camera HTTP API
User Guide
Version 8
2023-4

Privacy Protection Notice
As a device user or datacontroller,you may collect personal dataabout o
thers. You need to abide by local privacy protection laws and regulations,
and implement measures to protect the legitimate rights and interests o
f others.
Disclaimer
We have tried our best to ensure the completeness and accuracy of the c
ontent of the document, but it is inevitable that there will be technical in
accuracies, inconsistencies with product functions and operations, or pri
ntingerrors, etc.
If you have any questions or disputes, please refer to our final interpretat
ion.

RevisionHistory Description Data
Version1.0 Initialversion 2016-06-01
Revision1
Version1.1 1. Addtheinterfaceofshortconnection 2016-11-07
Revision2 accessingCGI.
2. AddrtmpportparametertoGetNetPortand
SetNetPortinterfaces.
3. AddhourFmtparametertoGetTimeand
SetTimeinterfaces.
4. AddstreamTypeandintervalparametersto
GetFtpandSetFtpinterfaces.
5. AddscheduleparametertoGetEmailand
SetEmailinterfaces.
6. AddGetPushandSetPushinterfaces.
7. Removeenable,actionandschedule


## parameterstoGetAlarmandSetAlarm

interfaces.
8. AddemailSchedule,pushScheduleand
hourFmttoGetAbilityinterface.
Version1.2 1. AddUpgradePrepare 2019-4-26
Revision3 2. AddShutdown
3. AddGetAuthandSetAuth
4. AddGetcloudandSetcloud
5. Get3GandSet3G
6. GetP2pandSetP2p
7. AddPreview
8. Addrtmp=startandrtmp=stopand
rtmp=authforrtmp
9. PtzaddGetPtzSerialSetPtzSerial

GetPtzTatternSetPtzTatterncommand
10.CameraincreasesGetAutoFocus
SetAutoFocuscommandoffocus
11.LEDincreasesGetIrLightsSetIrLights
GetPowerLedSetPowerLedcommand
12.AddGetAudioAlarmSetAudioAlarm
13.AddHeartBeat
14.AddGetCropSetCrop
15.AddGetAutoUpgradeSetAutoUpgrade
CheckFirmwareUpgradeOnline
UpgradeStatusinsystemmode
Version1.3 1.PtzaddGetPtzSerialSetPtzSerial 2019-9-30
Revision4 GetPtzTatternSetPtzTatterncommand
2.SystemdeleteImportCfg
3.SecuritydeleteGetAuthSetAuth
4.AlarmaddSetAudioAlarm
5.Completetheresponsedcode
Version1.4 1. MergeCGIcommandsforNVRandIPC 2021-01-05
Revision5
Version1.5 1. AIaddsGetAiCfgSetAiCfgGetAiState 2021-12-03
Revison6 2. PtzaddsGetZoomFocusStartZoomFocus
GetPtzGuardSetPtzGuardGetPtzCheckState
PtzCheck
3. AlarmaddsAudioAlarmPlay
4. LEDupdatesGetWhiteLedSetWilteLed
5. SystemupdatesGetAbility
6. NetworkupdatesGetFtpV20SetFtpV20
TestFtpGetNetPortSetNetPort
7. NetworkaddsGetCertificateInfo
CertificateClearGetRtspUrl

8. videoinputupdatesSetIspGetIsp
9. EncupdatesGetEnc
10. ResponseupdatesError
Version1.6 1.Improvethedescriptionoftheexample 2022-9-6
Revison7 2.Addthedescriptionofvideopreview
3.Deletetheabandonedcommand(rtmp
start/rtmpstop/rtmpauth)
4.Addtheversionfieldtothelogincommand
5.AddGetSysCfg/SetSysCfg/GetStitch/SetStitch
commands
6.ISPaddsmulti-levelframedropandsoftlight
sensitivity
7.NVRcutanddownloadvideofileoptional
streamtype
8.Increasetheptzguardparameter
9.Increasethewhitelightsettingparameters
10.Adddescriptionforftpcommand
11.Improvethecapabilityset
12.Improvetheerrorcode
Version1.7
Revison8 AddPrivacyProtectionNoticeandDisclaimer

Contents
.................................................................................................................2
..........................................................................................................................................2
PrivacyProtectionNotice
.............................................................................................................................................6
Disclaimer
1Scope..............................................................................................................................................11
Contents
2HTTP&Json...................................................................................................................................11
2.1Protocol...............................................................................................................................11
2.2JSON....................................................................................................................................12
2.3Token...................................................................................................................................13
2.4Abbreviations......................................................................................................................13
2.5Definitions...........................................................................................................................14
2.6Commandusageexample..................................................................................................14
2.6.1Getencodingconfigurationthroughlongsessionconnection...............................15
2.NextexecutetheGetEnccommand.............................................................................................16
2.6.2Getencodingconfigurationthroughshortsessionconnection.............................21
2.7Preview...............................................................................................................................26
2.7.1rtspmodepreview...................................................................................................26
1.Preview ipc devicevideo...........................................................................................................28
2.7.2rtmpmodepreview.................................................................................................28
1.Mainstreamurl:...........................................................................................................................29
2.Extstreamurl:...............................................................................................................................29
3.Substreamurl:..............................................................................................................................29
1.Preview ipc devicevideo...........................................................................................................30
2.7.3flvmodepreview.....................................................................................................30
1.Mainstream:.................................................................................................................................30
2.Extstream:....................................................................................................................................30
3.Substream:...................................................................................................................................30
1.Preview ipc devicevideo...........................................................................................................30
2.8Reolinkipc/nvrwebreference...........................................................................................30
3Commands.....................................................................................................................................33
3.1System.................................................................................................................................33
3.1.1GetAbility.................................................................................................................33
3.1.2GetDevInfo...............................................................................................................66
3.1.3GetDevName...........................................................................................................68
3.1.4SetDevName............................................................................................................69
3.1.5GetTime...................................................................................................................70
3.1.6SetTime....................................................................................................................76
3.1.7GetAutoMaint..........................................................................................................78
3.1.8SetAutoMaint...........................................................................................................80
3.1.9GetHddInfo..............................................................................................................82
3.1.10Format....................................................................................................................83
3.1.11Upgrade.................................................................................................................84
3.1.12Restore...................................................................................................................86
3.1.13Reboot...................................................................................................................87

3.1.14UpgradePrepare....................................................................................................88
3.1.15GetAutoUpgrade....................................................................................................89
3.1.16SetAutoUpgrade....................................................................................................90
3.1.17CheckFirmware......................................................................................................91
3.1.18UpgradeOnline.......................................................................................................92
3.1.19UpgradeStatus.......................................................................................................93
3.1.20Getchannelstatus...................................................................................................95
 InterfaceDescription.........................................................................................................95
3.2Security...............................................................................................................................98
3.2.1Login.........................................................................................................................98
3.2.2Logout......................................................................................................................99
3.2.3GetUser..................................................................................................................101
3.2.4AddUser.................................................................................................................102
3.2.5DelUser..................................................................................................................104
3.2.6ModifyUser............................................................................................................105
3.2.7GetOnline...............................................................................................................106
3.2.8Disconnect.............................................................................................................107
3.2.9GetSysCfg...............................................................................................................108
3.2.10SetSysCfg..............................................................................................................110
 InterfaceDescription.......................................................................................................110
3.3Network............................................................................................................................111
3.3.1GetLocalLink...........................................................................................................111
3.3.2SetLocalLink...........................................................................................................114
3.3.3GetDdns.................................................................................................................116
3.3.4SetDdns..................................................................................................................118
3.3.5GetEmail................................................................................................................119
3.3.6SetEmail.................................................................................................................122
3.3.7GetEmailV20..........................................................................................................125
3.3.8SetEmailV20...........................................................................................................127
3.3.9TestEmail................................................................................................................129
3.3.10GetFtp..................................................................................................................131
3.3.11SetFtp...................................................................................................................134
3.3.12GetFtpV20............................................................................................................137
3.3.13SetFtpV20............................................................................................................144
3.3.14TestFtp.................................................................................................................147
3.3.15GetNtp.................................................................................................................149
3.3.16SetNtp..................................................................................................................151
3.3.17GetNetPort...........................................................................................................152
3.3.18SetNetPort...........................................................................................................154
3.3.19GetUpnp..............................................................................................................155
3.3.20SetUpnp...............................................................................................................156
3.3.21GetWifi.................................................................................................................158
3.3.22SetWifi.................................................................................................................159
3.3.23TestWifi................................................................................................................160

3.3.24ScanWifi...............................................................................................................162
3.3.25GetWifiSignal.......................................................................................................163
3.3.26GetPush................................................................................................................164
3.3.27SetPush................................................................................................................166
3.3.28GetPushV20.........................................................................................................168
3.3.29SetPushV20..........................................................................................................170
3.3.30GetPushCfg..........................................................................................................172
3.3.31SetPushCfg...........................................................................................................173
3.3.32GetP2p.................................................................................................................175
3.3.33SetP2p..................................................................................................................176
3.3.34GetCertificateInfo................................................................................................177
3.3.35CertificateClear....................................................................................................178
3.3.36GetRtspUrl...........................................................................................................179
 InterfaceDescription.......................................................................................................179
3.4Videoinput.......................................................................................................................181
3.4.1GetImage...............................................................................................................181
3.4.2SetImage................................................................................................................183
3.4.3GetOsd...................................................................................................................184
3.4.4SetOsd....................................................................................................................187
3.4.5GetIsp.....................................................................................................................189
3.4.6SetIsp.....................................................................................................................195
3.4.7GetMask.................................................................................................................198
3.4.8SetMask.................................................................................................................200
3.4.9GetCrop..................................................................................................................203
3.4.10SetCrop................................................................................................................205
3.4.11GetStitch..............................................................................................................207
3.4.12SetStitch...............................................................................................................208
 InterfaceDescription.......................................................................................................208
3.5Enc.....................................................................................................................................210
3.5.1GetEnc....................................................................................................................210
3.5.2SetEnc....................................................................................................................216
 InterfaceDescription.......................................................................................................216
3.6Record...............................................................................................................................218
3.6.1GetRec....................................................................................................................218
3.6.2SetRec....................................................................................................................220
3.6.3GetRecV20.............................................................................................................222
3.6.4SetRecV20..............................................................................................................225
3.6.5Search....................................................................................................................227
3.6.6Download...............................................................................................................232
3.6.7Snap.......................................................................................................................233
3.6.8Playback.................................................................................................................234
3.6.9NvrDownload.........................................................................................................235
 InterfaceDescription.......................................................................................................235
3.7PTZ.....................................................................................................................................238

3.7.1GetPtzPreset..........................................................................................................238
3.7.2SetPtzPreset...........................................................................................................257
3.7.3GetPtzPatrol...........................................................................................................258
3.7.4SetPtzPatrol...........................................................................................................263
3.7.5PtzCtrl....................................................................................................................265
3.7.6GetPtzSerial...........................................................................................................267
3.7.7SetPtzSerial............................................................................................................270
3.7.8GetPtzTattern.........................................................................................................271
3.7.9SetPtzTattern.........................................................................................................275
3.7.10GetAutoFocus......................................................................................................277
3.7.11SetAutoFocus.......................................................................................................278
3.7.12GetZoomFocus.....................................................................................................279
3.7.13StartZoomFocus...................................................................................................280
3.7.14GetPtzGuard........................................................................................................282
3.7.15SetPtzGuard.........................................................................................................283
3.7.16GetPtzCheckState................................................................................................284
3.7.17PtzCheck..............................................................................................................286
 InterfaceDescription.......................................................................................................286
3.8Alarm.................................................................................................................................287
3.8.1GetAlarm................................................................................................................287
3.8.2SetAlarm................................................................................................................296
3.8.3GetMdAlarm..........................................................................................................300
3.8.4SetMdAlarm...........................................................................................................314
3.8.5GetMdState............................................................................................................319
3.8.6GetAudioAlarm......................................................................................................320
3.8.7SetAudioAlarm.......................................................................................................322
3.8.8GetAudioAlarmV20................................................................................................324
3.8.9SetAudioAlarmV20................................................................................................327
3.8.10GetBuzzerAlarmV20............................................................................................328
3.8.11SetBuzzerAlarmV20.............................................................................................332
3.8.12AudioAlarmPlay...................................................................................................333
 InterfaceDescription.......................................................................................................333
3.10LED..................................................................................................................................335
3.10.1GetIrLights...........................................................................................................335
3.10.2SetIrLights............................................................................................................336
3.10.3GetPowerLed.......................................................................................................337
3.10.4SetPowerLed........................................................................................................339
3.10.5GetWhiteLed........................................................................................................340
3.10.6SetWhiteLed........................................................................................................342
3.10.7GetAiAlarm..........................................................................................................344
3.10.8SetAiAlarm...........................................................................................................347
3.10.9SetAlarmArea.......................................................................................................350
 InterfaceDescription.......................................................................................................350
3.11AI.....................................................................................................................................353

3.11.1GetAiCfg...............................................................................................................353
3.11.2SetAiCfg................................................................................................................355
3.11.3GetAiState............................................................................................................356
 InterfaceDescription...............................................................................................................356
4.Response.....................................................................................................................................358
4.1Error..................................................................................................................................358

1 Scope
The document defines a series of HTTP and HTTPS based application
programming interface, covering the System, Security, Network, Video
input, Enc, Record, PTZ, and Alarm modules.
The document applies to both IPC and NVR products,and the differences
will be explained in the commands.
2 HTTP & Json
2.1 Protocol
Support both HTTP and HTTPS. By default, http is turned off. If you need
to use the http protocol, you need to go to Settings -> Network Settings
-> Advanced Settings -> Port Settings to open the http port.

HTTP and HTTPS only support the POST method, get and set all through
it.
POST /cgi-bin/api.cgi?cmd=xxx&token=20343295&paramxxx=xxx HTTP/1.1
The payload type is a JSON or filethat is specified by Content-Type.
Content-Type = “application/octet-stream” or "application/json"
2.2 JSON
JSON (JavaScript Object Notation) is based on a subset of the JavaScript
Programming Language, Standard ECMA-262 3rd Edition - December
1999.
Request:
[
{
"cmd":string,
"action":int,
"param“:
{
"name":val, //val=stringorint
...
},
}
...
]


## Response:


[
{
"cmd":string,
"code“:int,//rspcode,0:success,others:false
"value":or"error"//"value"whencode=0,"error"when"code"=1
{
"name":val, // val=stringorint
...
},
}
...
]
2.3 Token
Token is the only global certification of developers. Token is required
whenever developers are calling each port. Normally the lease for each
token is 3600 seconds and you may regain it after it expires. Please refer
to the Login command for the methods of requiring token.
2.4 Abbreviations
For the purposes of the present document, the following abbreviations
apply:
M/O Mandatory/Optional

2.5 Definitions
For the purposes of the present document, the following definitions
apply:
initial: The initial value of the configuration.
range: The datarangeof the configuration.
value: The current value of the configuration.
action : Obtain initial, range and value when the value is 1, obtain only
the value when the value is 0.
channel : The channel number of the current device.
2.6 Command usage example
There aretwo access methods for reolink ipc/nvr:
1: Long-session access, that is, first send a login request with a user
name and password, and obtain a token, and then all subsequent
commands URL carry the token as authentication information.
2. Short session access, that is, each cgi request url carries the username
and passwordas authentication information.
The following are examples of the method of sending the GetEnc
command to obtain the encoding configuration through the long session
connection and the short session connection mode

2.6.1 Get encoding configuration through long session
connection
If you want to work over a persistent connection, you need to get the
Token by sending a login request.
1. gettoken first：
The login requesturl:
https://<camera_ip>/api.cgi?cmd=Login
The request body:
[
{
"cmd":"Login",
"param":{
"User":{
"Version":"0",
"userName":"admin",
"password":"xxxxxx"
}
}
}
]


## Response：

[
{
"cmd" : "Login",
"code" : 0,
"value" : {
"Token" : {
"leaseTime" : 3600,
"name" : "42da7586d7b82a6"
}
}
}
]

It is also possible to simulate the test through the Advanced Rest Client
Application on Google Chrome
2. Next execute the GetEnc command

When sending a request, you need to carry the token name obtained by
the login command.
The GetEnc request url:
https://<camera_ip>/api.cgi?cmd=GetEnc&token=42da7586d7b82a6
The request body:
[
{
"cmd":"GetEnc",
"action":1,
"param":{
"channel":0
}
}
]


## Response：

[
{
"cmd":"GetEnc",
"code":0,
"initial":{
"Enc":{
"audio":0,
"channel":0,
"mainStream":{
"bitRate":6144,
"frameRate":25,
"gop":2,
"height":2160,
"profile":"High",
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":256,
"frameRate":10,
"gop":4,
"height":360,
"profile":"High",
"size":"640*360",

"vType":"h264",
"width":640
}
}
},
"range":{
"Enc":[
{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[4096,5120,6144,7168,8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":2160,
"profile":["Base","Main","High"],
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",

"width":640
}
},
{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[1024,1536,2048,3072,4096,5120,6144,7168,
8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":1440,
"profile":["Base","Main","High"],
"size":"2560*1440",
"vType":"h264",
"width":2560
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
},

{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[1024,1536,2048,3072,4096,5120,6144,7168,
8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":1296,
"profile":["Base","Main","High"],
"size":"2304*1296",
"vType":"h264",
"width":2304
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
}
]
},
"value":{

"Enc":{
"audio":1,
"channel":0,
"mainStream":{
"bitRate":6144,
"frameRate":25,
"gop":2,
"height":2160,
"profile":"High",
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":256,
"frameRate":10,
"gop":4,
"height":360,
"profile":"High",
"size":"640*360",
"vType":"h264",
"width":640
}
}
}
}
]
2.6.2 Get encoding configuration through short session
connection
The short connection interface is for users to skip the process of logging
in to the IP Camera to get token. In this way, users just need the user
name and password to access the IP Camera easily. Here is how short
connection works.

The request url:
https://<camera_ip>/api.cgi?cmd=GetEnc&user=admin&password=xxxx
The request body:
[
{
"cmd":"GetEnc",
"action":1,
"param":{
"channel":0
}
}
]


## Response：

[
{
"cmd":"GetEnc",
"code":0,
"initial":{
"Enc":{
"audio":0,
"channel":0,
"mainStream":{
"bitRate":6144,
"frameRate":25,
"gop":2,
"height":2160,
"profile":"High",
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":256,
"frameRate":10,
"gop":4,
"height":360,
"profile":"High",
"size":"640*360",
"vType":"h264",
"width":640
}

}
},
"range":{
"Enc":[
{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[4096,5120,6144,7168,8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":2160,
"profile":["Base","Main","High"],
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
},

{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[1024,1536,2048,3072,4096,5120,6144,7168,
8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":1440,
"profile":["Base","Main","High"],
"size":"2560*1440",
"vType":"h264",
"width":2560
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
},
{
"audio":"boolean",
"chnBit":1,

"mainStream":{
"bitRate":[1024,1536,2048,3072,4096,5120,6144,7168,
8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":1296,
"profile":["Base","Main","High"],
"size":"2304*1296",
"vType":"h264",
"width":2304
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
}
]
},
"value":{
"Enc":{
"audio":1,
"channel":0,

"mainStream":{
"bitRate":6144,
"frameRate":25,
"gop":2,
"height":2160,
"profile":"High",
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":256,
"frameRate":10,
"gop":4,
"height":360,
"profile":"High",
"size":"640*360",
"vType":"h264",
"width":640
}
}
}
}
]
2.7 Preview
Reolink IPC supports rtsp/rtmp/flv video transmission protocol, rtmp/flv
video transmission protocol only supports h264 encoding format video,
and rtsp supports h264 and h265 encoding format video.
2.7.1 rtsp mode preview
The rtsp port is closed by default, so before using the rtsp protocol, you
need to go to Settings -> Network Settings -> Advanced Settings -> Port
Settings to open the rtsp port.

1. main stream url
rtsp://(user name):(password)@(ip address):554/Preview_(channel
number)_main
2. sub stream url
rtsp://(user name):(password)@(ip address):554/Preview_(channel
number)_sub
The following is the rtsp url of the historical version, no longer
recommended, but still compatible.
mainstream:
rtsp://(username):(password)@(ipaddress):554/h264Preview_(channelnumber)_main
rtsp://(username):(password)@(ipaddress):554/h265Preview_(channelnumber)_main
rtsp://(username):(password)@(ipaddress):554/

Substream:
rtsp://(username):(password)@(ipaddress):554/h264Preview_(channelnumber)_sub
Note:The “channelnumber” startsfrom 01


## example:

1.Preview ipc devicevideo
rtsp://admin:xxxx@192.168.123.145:554/Preview_01_main
2.Preview the video ofthe thirdchannelof nvr
rtsp://admin:xxxx@192.168.0.206:554/Preview_03_main
2.7.2 rtmp mode preview
The rtmp port is closed by default, so before using the rtmp protocol,
you need to go to Settings -> Network Settings -> Advanced Settings ->
PortSettings to open the rtmp port.

The rtmp protocol only supports videos in h264 encoding format, and
videos in h265 encoding formatare not supported yet.
1. Main stream url:
rtmp://(ip address)/bcs/channel(channel id)_main.bcs?channel=(channel
id)&stream=0&user=(user name)&password=(user password)
2. Ext stream url:
rtmp://(ip address)/bcs/channel(channel id)_ext.bcs?channel=(channel
id)&stream=0&user=(user name)&password=(user password)
3. Sub stream url:
rtmp://(ip address)/bcs/channel(channel id)_sub.bcs?channel=(channel
id)&stream=1&user=(user name)&password=(user password)
Note:The “channelid” startsfrom 0


## example:


1.Preview ipc devicevideo
rtmp://192.168.123.145/bcs/channel0_main.bcs?channel=0&stream=0&user=admin&p
assword=xxxx
2.Preview the video ofthe thirdchannelof nvr
rtmp://192.168.0.206/bcs/channel2_main.bcs?channel=2&stream=0&user=admin&pas
sword=000000
2.7.3 flv mode preview
The flv protocol only supports videos in h264 encoding format, and
videos in h265 encoding formatare not supported yet.
1. Main stream:
https://(ip address)/flv?port=1935&app=bcs&stream=channel(channel
id)_main.bcs&user=(user name)&password=(user password)
2. Ext stream:
https://(ip address)/flv?port=1935&app=bcs&stream=channel(channel
id)_ext.bcs&user=(user name)&password=(user password)
3. Sub stream:
https://(ip address)/flv?port=1935&app=bcs&stream=channel(channel
id)_sub.bcs&user=(user name)&password=(user password)
Note:The “channelid” startsfrom 0


## example:

1.Preview ipc devicevideo
https://192.168.123.145/flv?port=1935&app=bcs&stream=channel0_main.bcs&user=a
dmin&password=xxxx
2.Preview the video ofthe thirdchannelof nvr
https://192.168.0.206/flv?port=1935&app=bcs&stream=channel2_main.bcs&user=admi
n&password=xxxx
2.8 Reolink ipc/nvr web reference
The interaction between the reolink ipc/nvr web interface and the device

uses the http/https protocol, but the web also uses a private encryption
protocol (the encryption protocol processing process is more
complicated, so it is not open to the public).
At the same time, it also makes it impossible to use software such as
wareshark to captureand analyzejson datainformation.
In order to solve this problem, the web background adds the printing of
jsonlog information for sending and receiving requests.
If you want to view jason log information, visit https://(camera ip
address)?debug=1 on Google Chrome to enter the web debug mode of
the device, then type F12 on the keyboard to view the background
information. When the web is operating, you can see the web on the
Console->verbose page Sent json datainformation.

3 Commands
3.1 System
3.1.1 GetAbility
 InterfaceDescription
Itisusedtogetsystemabilityofappointeduser.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAbility&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetAbility",
"param":{
"User":{
"userName":"admin"
}
}
}
]
Fielddescription
Field Description M/O
userName Username,itshouldbeconsistedoflessthan32 M
characters,iftheusernameisNULL,thenitwouldget
currentuserability.
 Returndatadescription
Return datacorrectly

Eachdomainiscorrespondingtoafunctionalmodule.Thepermitfieldmarks
accessright,validatinginleastsignificantthreebits:themostsignificantbit
indicatesexecutionpermission,thefirstbitindicatesrevisionpermission,andthe
secondbitindicatesread/writepermission.Theverfieldindicatestheversion
number.0meansthefeatureisnotsupportedinthatversion,nonzeromeansthe
featureissupported.Differentversionnumbersindicatethosecertainfunctional
modulessupportdifferentfunctionaloptions.
[{
"cmd":"GetAbility",
"code":0,
"value":{
"Ability":{
"3g":{
"permit":0,
"ver":0
},
"abilityChn":[{
"aiTrack":{
"permit":0,
"ver":0
},
"aiTrackDogCat":{
"permit":0,
"ver":0
},
"alarmAudio":{
"permit":6,
"ver":1
},
"alarmIoIn":{
"permit":0,
"ver":0
},
"alarmIoOut":{
"permit":0,
"ver":0
},
"alarmMd":{
"permit":6,
"ver":1
},

"alarmRf":{
"permit":0,
"ver":0
},
"batAnalysis":{
"permit":0,
"ver":0
},
"battery":{
"permit":0,
"ver":0
},
"cameraMode":{
"permit":6,
"ver":0
},
"disableAutoFocus":{
"permit":0,
"ver":0
},
"enc":{
"permit":6,
"ver":1
},
"floodLight":{
"permit":0,
"ver":0
},
"ftp":{
"permit":6,
"ver":6
},
"image":{
"permit":6,
"ver":1
},
"indicatorLight":{
"permit":0,
"ver":0
},
"isp":{
"permit":6,
"ver":1
},

"isp3Dnr":{
"permit":0,
"ver":0
},
"ispAntiFlick":{
"permit":6,
"ver":1
},
"ispBackLight":{
"permit":0,
"ver":0
},
"ispBright":{
"permit":6,
"ver":1
},
"ispContrast":{
"permit":6,
"ver":1
},
"ispDayNight":{
"permit":6,
"ver":1
},
"ispExposureMode":{
"permit":0,
"ver":0
},
"ispFlip":{
"permit":6,
"ver":1
},
"ispHue":{
"permit":0,
"ver":0
},
"ispMirror":{
"permit":6,
"ver":1
},
"ispSatruation":{
"permit":6,
"ver":1
},

"ispSharpen":{
"permit":6,
"ver":1
},
"ispWhiteBalance":{
"permit":6,
"ver":0
},
"ledControl":{
"permit":6,
"ver":1
},
"live":{
"permit":4,
"ver":2
},
"mainEncType":{
"permit":0,
"ver":0
},
"mask":{
"permit":6,
"ver":1
},
"mdTriggerAudio":{
"permit":0,
"ver":0
},
"mdTriggerRecord":{
"permit":0,
"ver":0
},
"mdWithPir":{
"permit":0,
"ver":0
},
"osd":{
"permit":6,
"ver":1
},
"powerLed":{
"permit":0,
"ver":0
},

"ptzCtrl":{
"permit":0,
"ver":0
},
"ptzDirection":{
"permit":1,
"ver":0
},
"ptzPatrol":{
"permit":0,
"ver":0
},
"ptzPreset":{
"permit":0,
"ver":0
},
"ptzTattern":{
"permit":0,
"ver":0
},
"ptzType":{
"permit":0,
"ver":0
},
"recCfg":{
"permit":6,
"ver":1
},
"recDownload":{
"permit":6,
"ver":1
},
"recReplay":{
"permit":6,
"ver":1
},
"recSchedule":{
"permit":6,
"ver":2
},
"shelterCfg":{
"permit":6,
"ver":1
},

"snap":{
"permit":6,
"ver":1
},
"supportAi":{
"permit":6,
"ver":1
},
"supportAiAnimal":{
"permit":0,
"ver":0
},
"supportAiDetectConfig":{
"permit":6,
"ver":1
},
"supportAiDogCat":{
"permit":6,
"ver":1
},
"supportAiFace":{
"permit":0,
"ver":0
},
"supportAiPeople":{
"permit":6,
"ver":1
},
"supportAiSensitivity":{
"permit":6,
"ver":1
},
"supportAiStayTime":{
"permit":6,
"ver":1
},
"supportAiTargetSize":{
"permit":6,
"ver":1
},
"supportAiTrackClassify":{
"permit":0,
"ver":0
},

"supportAiVehicle":{
"permit":6,
"ver":1
},
"supportAoAdjust":{
"permit":0,
"ver":1
},
"supportFLBrightness":{
"permit":6,
"ver":1
},
"supportFLIntelligent":{
"permit":6,
"ver":1
},
"supportFLKeepOn":{
"permit":0,
"ver":0
},
"supportFLSchedule":{
"permit":6,
"ver":1
},
"supportFLswitch":{
"permit":6,
"ver":1
},
"supportGop":{
"permit":0,
"ver":1
},
"supportMd":{
"permit":6,
"ver":1
},
"supportPtzCalibration":{
"permit":0,
"ver":0
},
"supportPtzCheck":{
"permit":0,
"ver":0
},

"supportThresholdAdjust":{
"permit":6,
"ver":1
},
"supportWhiteDark":{
"permit":6,
"ver":1
},
"videoClip":{
"permit":0,
"ver":0
},
"waterMark":{
"permit":6,
"ver":1
},
"white_balance":{
"permit":6,
"ver":0
}
}],
"alarmAudio":{
"permit":6,
"ver":1
},
"alarmDisconnet":{
"permit":6,
"ver":1
},
"alarmHddErr":{
"permit":6,
"ver":1
},
"alarmHddFull":{
"permit":6,
"ver":1
},
"alarmIpConflict":{
"permit":6,
"ver":1
},
"auth":{
"permit":6,
"ver":1

},
"autoMaint":{
"permit":6,
"ver":1
},
"cloudStorage":{
"permit":0,
"ver":0
},
"customAudio":{
"permit":1,
"ver":1
},
"dateFormat":{
"permit":6,
"ver":1
},
"ddns":{
"permit":6,
"ver":9
},
"ddnsCfg":{
"permit":6,
"ver":1
},
"devInfo":{
"permit":4,
"ver":1
},
"devName":{
"permit":6,
"ver":2
},
"disableAutoFocus":{
"permit":0,
"ver":0
},
"disk":{
"permit":0,
"ver":0
},
"display":{
"permit":6,
"ver":1

},
"email":{
"permit":6,
"ver":3
},
"emailInterval":{
"permit":6,
"ver":1
},
"emailSchedule":{
"permit":6,
"ver":1
},
"exportCfg":{
"permit":4,
"ver":0
},
"ftpAutoDir":{
"permit":6,
"ver":1
},
"ftpExtStream":{
"permit":0,
"ver":0
},
"ftpPic":{
"permit":0,
"ver":0
},
"ftpSubStream":{
"permit":6,
"ver":1
},
"ftpTest":{
"permit":6,
"ver":0
},
"hourFmt":{
"permit":6,
"ver":2
},
"http":{
"permit":6,
"ver":3

},
"httpFlv":{
"permit":6,
"ver":1
},
"https":{
"permit":6,
"ver":3
},
"importCfg":{
"permit":1,
"ver":0
},
"ipcManager":{
"permit":6,
"ver":1
},
"ledControl":{
"permit":7,
"ver":1
},
"localLink":{
"permit":6,
"ver":1
},
"log":{
"permit":6,
"ver":1
},
"mediaPort":{
"permit":6,
"ver":1
},
"ntp":{
"permit":6,
"ver":1
},
"online":{
"permit":6,
"ver":1
},
"onvif":{
"permit":6,
"ver":3

},
"p2p":{
"permit":6,
"ver":1
},
"performance":{
"permit":4,
"ver":1
},
"pppoe":{
"permit":6,
"ver":0
},
"push":{
"permit":6,
"ver":1
},
"pushSchedule":{
"permit":6,
"ver":1
},
"reboot":{
"permit":1,
"ver":1
},
"recExtensionTimeList":{
"permit":6,
"ver":1
},
"recOverWrite":{
"permit":6,
"ver":1
},
"recPackDuration":{
"permit":6,
"ver":0
},
"recPreRecord":{
"permit":6,
"ver":1
},
"restore":{
"permit":1,
"ver":1

},
"rtmp":{
"permit":6,
"ver":3
},
"rtsp":{
"permit":6,
"ver":3
},
"scheduleVersion":{
"permit":6,
"ver":1
},
"sdCard":{
"permit":6,
"ver":1
},
"showQrCode":{
"permit":6,
"ver":0
},
"simMoudule":{
"permit":6,
"ver":0
},
"supportAudioAlarm":{
"permit":6,
"ver":1
},
"supportAudioAlarmEnable":{
"permit":6,
"ver":1
},
"supportAudioAlarmSchedule":{
"permit":6,
"ver":1
},
"supportAudioAlarmTaskEnable":{
"permit":6,
"ver":1
},
"supportBuzzer":{
"permit":0,
"ver":0

},
"supportBuzzerEnable":{
"permit":0,
"ver":0
},
"supportBuzzerTask":{
"permit":0,
"ver":0
},
"supportBuzzerTaskEnable":{
"permit":0,
"ver":0
},
"supportEmailEnable":{
"permit":6,
"ver":1
},
"supportEmailTaskEnable":{
"permit":6,
"ver":1
},
"supportFtpCoverPicture":{
"permit":6,
"ver":1
},
"supportFtpCoverVideo":{
"permit":6,
"ver":1
},
"supportFtpDirYM":{
"permit":6,
"ver":1
},
"supportFtpEnable":{
"permit":6,
"ver":1
},
"supportFtpPicCaptureMode":{
"permit":6,
"ver":1
},
"supportFtpPicResoCustom":{
"permit":6,
"ver":0

},
"supportFtpPictureSwap":{
"permit":6,
"ver":1
},
"supportFtpTask":{
"permit":6,
"ver":1
},
"supportFtpTaskEnable":{
"permit":6,
"ver":1
},
"supportFtpVideoSwap":{
"permit":6,
"ver":1
},
"supportFtpsEncrypt":{
"permit":6,
"ver":1
},
"supportHttpEnable":{
"permit":6,
"ver":1
},
"supportHttpsEnable":{
"permit":6,
"ver":1
},
"supportOnvifEnable":{
"permit":6,
"ver":1
},
"supportPushInterval":{
"permit":6,
"ver":1
},
"supportRecScheduleEnable":{
"permit":6,
"ver":1
},
"supportRecordEnable":{
"permit":6,
"ver":1

},
"supportRtmpEnable":{
"permit":6,
"ver":1
},
"supportRtspEnable":{
"permit":6,
"ver":1
},
"talk":{
"permit":4,
"ver":1
},
"time":{
"permit":6,
"ver":2
},
"tvSystem":{
"permit":6,
"ver":0
},
"upgrade":{
"permit":1,
"ver":2
},
"upnp":{
"permit":6,
"ver":1
},
"user":{
"permit":6,
"ver":1
},
"videoClip":{
"permit":0,
"ver":0
},
"wifi":{
"permit":0,
"ver":0
},
"wifiTest":{
"permit":6,
"ver":0

}
}
}
}]
Fielddescription
Field ver permit
abilityChn->mask 0:notsupport,1:support 1:option
Whetherprivacyzone 2:write
configurationissupported 4:read
abilityChn->image 0:notsupport,1:support 7:read&
Whethervideoparameter write&
configurationissupported option
abilityChn->isp 0:notsupport,1:support
WhetherISPparameter
configurationissupported
abilityChn->white_balance 0:notsupport,1:support
Whetherwhitebalanceis
supported
abilityChn->cameraMode 0:notsupport,1:support
Whetheranalogcameramode
switchingissupported
abilityChn->osd 0:notsupport,1:support,2:
supportosdanddistinctosd
abilityChn->waterMark 0:notsupport,1:support
WhetherwatermarkSettingsare
supported
abilityChn->enc 0:notsupportsetencodecfg,
1:supportsetencodecfg
abilityChn->live 0:notsupport1:support
main/extern/sub stream;
2:supportmain/substream

abilityChn->snap 0:notsupportsnap,1:support
snap
abilityChn->ftp 0:notsupportftp;ver>0:support
ftp
(1:supportstream
2:supportjpgpicture+stream
3:supportStream+mode
selection
4:supportjpgpicture+stream+
modeselection
5:supportStream+mode
selection+streamtypeselection
6:supportjpgpicture+stream+
modeselection+streamtype
selection)
abilityChn->recCfg 0:notsupport,1:support
Supportsvideoconfiguration
(packagetime,preview,video
delay,videocoverage)
abilityChn->recSchedule 0:notsupport,
1:supportmdrecord,
2:supportmdrecordandnormal
record
abilityChn->recDownload 0:notsupportdownloadrecord
file,1:supportdownloadrecord
file
abilityChn->recReplay 0:notsupportplaybackrecord
fileonline,1:supportplayback
recordfileonlinefile
abilityChn->ptzType 0:DoesnotsupportPTZordoes

nothavepermissiontooperate
1:supportAF
2:supportPTZ
3:supportPT
4:Simulatedballmachine
5:PTZ(GM8136SPTZ)doesnot
supportspeedadjustment
abilityChn->ptzCtrl 0:notsupport,
1:supportcontrolzoom
2:supportcontrolzoomandfocus
withslider
abilityChn->ptzPreset 0:notsupport,
1:support
WhetherPTZpresetpointsare
supported
abilityChn->ptzPatrol 0:notsupport,
1:support
WhetherPTZcruisingis
supported
abilityChn->ptzTattern 0:notsupport,
1:support
WhetherthePTZtrajectory
settingissupported
abilityChn->ptzDirection 0:support8directions+auto
scan,1:supportonly4directions,
noautoscan
abilityChn->alarmIoIn 0:notsupport,
1:support
WhetherIOalarminputis
supported

abilityChn->alarmIoOut 0:notsupport,
1:support
WhetherIOalarmoutputis
supported
abilityChn->alarmRf 0:notsupport,
1:supportRfalarmonDVR
2:Batteryipc
3:AddtheALARM/MDschedule
option
abilityChn->alarmMd 0:notsupport,
1:support
Whethermovementdetection
alarmsaresupported
abilityChn->disableAutoFocus 0:notsupportsetautofucus,
1:supportsetautofucus
abilityChn->floodLight 0:notsupportWhitelightLED,
1:supportWhitelightLED
abilityChn->battery 0:notsupport,
1:support
abilityChn->indicatorLight 0:notsupportindicatorLight,
1:supportindicatorLight
abilityChn->videoClip 0:notsupportvideoCutout
1:supportcutoutwidthand
heightcannotbemodified;
2:supportcutoutwidthand
heightcanbemodified
abilityChn->powerLed 0:notsupport,
1:support
abilityChn->mainEncType 0:mainstreamenctypeisH264
1:mainstreamenctypeisH265

abilityChn->ispDayNight 0:notsupportday_nightmode
1:supportday_nightmode
2:Supportdayandnightmode
andsupportsettingswitching
threshold
abilityChn->ispAntiFlick 0:notsupport
1:support
Whetheranti-flickerfunctionis
supporte
abilityChn->ispExposureMode 0:notsupport
1:support
Whetherexposureissupported
abilityChn->ispWhiteBalance 0:notsupport
1:support
abilityChn->ispBackLight 0:notsupport
1:support
abilityChn->isp3Dnr 0:notsupport
1:support
abilityChn->ispMirror 0:notsupport
1:support
abilityChn->ispFlip 0:notsupport
1:support
abilityChn->ispBright 0:notsupport
1:support
abilityChn->ispContrast 0:notsupport
1:support
abilityChn->ispSatruation 0:notsupport
1:support
abilityChn->ispHue 0:notsupport
1:support

abilityChn->ispSharpen 0:notsupport
1:support
abilityChn->floodLight 0:notsupport
1:Supportwhitelight,2:Support
whitelightautomaticmode
abilityChn->mdWithPir 0:notsupport
1:support
abilityChn->mdTriggerAudio 0:notsupport
1:support
abilityChn->mdTriggerRecord 0:notsupport
1:support
abilityChn->shelterCfg 0:notsupport
1:support
abilityChn->alarmAudio 0:notsupport
1:support
abilityChn->batAnalysis 0:notsupport
1:support
abilityChn->waterMark 0:notsupport
1:support
abilityChn->ledControl 0:notsupport
1:support
abilityChn->supportPtzCheck 0:notsupport
1:support
hourFmt 0:notsupport
1:supportchangehourformate
time 0:notsupport
1:Daylightsavingtimeonly
supportsSunday;
2:Supportsanydayoftheweek

tvSystem 0:notsupport
1:support
display 0:notsupport
1:support
ipcManager 0:notsupport
1:support
devInfo 0:notsupport
1:support
autoMaint 0:notsupport
1:support
restore 0:notsupport
1:support
reboot 0:notsupport
1:support
log 0:notsupport
1:support
performance 0:notsupport
1:support
upgrade 0:notsupport
1:supportmanualupgrade
2:supportmanualupgradeand
upgradeonline
importCfg 0:notsupport
1:support
exportCfg 0:notsupport
1:support
disk 0:notsupport
1:support
sdCard 0:notsupport
1:support

devName 0:notsupport
1:support


## auth 0:notsupport

1:support
user 0:notsupport
1:support
online 0:notsupport
1:support
rtsp 0:notsupport
1:support
rtmp 0:notsupport
1:support
ddns 0:notsupport
1:swan
2:3322
3:dyndns
4:swann+3322
5:swann+dyndns
6:3322+dyndns
7:swann+3332+dyndns
8:noip
9:dyndns+noip
ddnsCfg 0:Doesnotsupportentering
ddnsserveraddress
1:Supportinputddnsserver
address
email 0:Mailfunctionisnotsupported
1:Supportjpgattachment
2:Supportvideoandjpg
attachments

3:Supportvideoandjpg
attachments,supportsender
nickname
emailSchedule 0:Scheduleisnotsupported
1:Supportschedule
upnp 0:notsupport
1:support
onvif 0:notsupport
1:support
ntp 0:notsupport
1:support
mediaPort 0:notsupport
1:support
http 0:notsupport
1:support
https 0:notsupport
1:support
httpFlv 0:notsupport
1:support
p2p 0:notsupport
1:support
3g 0:notsupport
1:support
localLink 0:notsupport
1:support
pppoe 0:notsupport
1:support
Wifi 0:notsupport
1:support

Push 0:notsupport
1:support
pushSchedule 0:notsupport
1:support
Talk 0:notsupport
1:support
alarmHddErr 0:notsupport
1:support
alarmHddFull 0:notsupport
1:support
alarmDisconnet 0:notsupport
1:support
alarmIpConflict 0:notsupport
1:support
ledControl 0:notsupport
1:support
disableAutoFocus 0:notsupport
1:support
videoClip 1:Cutoutwidthandheight
cannotbemodified;
2:Cutoutwidthandheightcanbe
modified
alarmAudio 0:notsupport
1:support
cloudStorage bit0:Whethertosupportcloud
upload
bit1:Whethertosupportcloud
serviceconfiguration
bit3:Whethertosupportcloud
uploaddeployment

scheduleVersion 0:supportcmd:
“GetRec”,“SetRec”,”GetEmail”,”
SetEmail”,”GetFtp”,“SetFtp”,
“GetPush”,“SetPush”,
“GetAudioAlarm”,
“SetAudioAlarm”,
“GetCloudSchedule”,“SetCloudSch
edule”,“GetAlarm”,“SetAlarm”
1:supportcmd:
“GetRecV20”,“SetRecV20”,”
GetEmailV20”,”SetEmailV20”,”
GetFtpV20”,“SetFtpV20”,
“GetPushV20”,“SetPushV20”,
“GetAudioAlarmV20”,
“SetAudioAlarmV20”,
“GetCloudScheduleV20”,
“SetCloudScheduleV20”;
“GetMdAlarm”
“SetMdAlarm”
customAudio 0:notsupport
1:support
wifiTest 0:notsupport
1:support
simMoudule 0:notsupport
1:support
dateFormat 0:notsupport
1:support
emailInterval 0:notsupport
1:support

showQrCode 0:notsupport
1:support
ftpTest 0:notsupport
1:support
ftpSubStream 0:notsupport
1:support
ftpExtStream 0:notsupport
1:support
ftpPic 0:notsupport
1:support
ftpAutoDir 0:notsupport
1:support
recOverWrite 0:notsupport
1:support
recPackDuration 0:notsupport
1:support
recPreRecord 0:notsupport
1:support
recExtensionTimeList 0:notsupport
1:support
supportAudioAlarm 0:notsupport
1:support
supportAudioAlarmEnable 0:notsupport
1:support
supportAudioAlarmSchedule 0:notsupport
1:support
supportAudioAlarmTaskEnable 0:notsupport
1:support
supportFtpTask 0:notsupport
1:support

supportBuzzer 0:notsupport
1:support
supportBuzzerEnable 0:notsupport
1:support
supportBuzzerTask 0:notsupport
1:support
supportBuzzerTaskEnable 0:notsupport
1:support
supportRecordEnable 0:notsupport
1:support
supportRecScheduleEnable 0:notsupport
1:support
supportEmailEnable 0:notsupport
1:support
supportEmailTaskEnable 0:notsupport
1:support
supportFtpEnable 0:notsupport
1:support
supportFtpTaskEnable 0:notsupport
1:support
supportAi 0:notsupport
1:support
supportAiAnimal 0:notsupport
1:support
supportAiDetectConfig 0:notsupport
1:support
supportAiDogCat 0:notsupport
1:support
supportAiFace 0:notsupport
1:support

supportAiPeople 0:notsupport
1:support
supportAiSensitivity 0:notsupport
1:support
supportAiStayTime 0:notsupport
1:support
supportAiTargetSize 0:notsupport
1:support
supportAiVehicle 0:notsupport
1:support
supportAoAdjust 0:notsupport
1:support
supportFLBrightness 0:notsupport
1:support
supportFLIntelligent 0:notsupport
1:support
supportFLKeepOn 0:notsupport
1:support
supportFLSchedule 0:notsupport
1:support
supportFLswitch 0:notsupport
1:support
supportGop 0:notsupport
1:support
supportPtzCheck 0:notsupport
1:support
supportThresholdAdjust 0:notsupport
1:support
supportWhiteDark 0:notsupport
1:support

supportAudioAlarm 0:notsupport
1:support
supportAudioAlarmEnable 0:notsupport
1:support
supportAudioAlarmSchedule 0:notsupport
1:support
supportAudioAlarmTaskEnable 0:notsupport
1:support
supportBuzzer 0:notsupport
1:support
supportBuzzerEnable 0:notsupport
1:support
supportBuzzerTask 0:notsupport
1:support
supportBuzzerTaskEnable 0:notsupport
1:support
supportEmailEnable 0:notsupport
1:support
supportEmailTaskEnable 0:notsupport
1:support
supportFtpCoverPicture 0:notsupport
1:support
supportFtpCoverVideo 0:notsupport
1:support
supportFtpDirYM 0:notsupport
1:support
supportFtpPicCaptureMode 0:notsupport
1:support
supportFtpPicResoCustom 0:notsupport
1:support

supportFtpPictureSwap 0:notsupport
1:support
supportFtpTask 0:notsupport
1:support
supportFtpTaskEnable 0:notsupport
1:support
supportFtpVideoSwap 0:notsupport
1:support
supportFtpsEncrypt 0:notsupport
1:support
supportHttpEnable 0:notsupport
1:support
supportHttpsEnable 0:notsupport
1:support
supportOnvifEnable 0:notsupport
1:support
supportPushInterval 0:notsupport
1:support
supportRecScheduleEnable 0:notsupport
1:support
supportRecordEnable 0:notsupport
1:support
supportRtmpEnable 0:notsupport
1:support
supportRtspEnable 0:notsupport
1:support
supportAutoTrackStream 0:notsupport
1:support
Whetherthetrackingstream
configurationissupported

supportBinoStitch 0:notsupport
1:support
Whethertheadjustmentof
binocularequipmentsplicing
pictureissupported
aiTrackDogCat Whethertrackingofcatsand
dogsissupported
3.1.2 GetDevInfo
 InterfaceDescription
Itisusedtogetdeviceinformation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetDevInfo&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetDevInfo"
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[

{
"cmd":"GetDevInfo",
"code":0,
"value":{
"DevInfo":{
"B485":1,
"IOInputNum":0,
"IOOutputNum":0,
"audioNum":16,
"buildDay":"build20080734",
"cfgVer":"v3.0.0.0",
"channelNum":16,
"detail":"NVR652410104001000200000",
"diskNum":2,
"exactType":"NVR",
"firmVer":"v3.0.0.59_20080734",
"frameworkVer":1,
"hardVer":"H3MB18",
"model":"RLN16-410",
"name":"NVR",
"pakSuffix":"pak,paks",
"serial":"00000000000000",
"type":"NVR",
"wifi":0
}
}
}
]
Fielddescription
Field Description
IOInputNum ThenumberofIOinputport.
IOOutputNum ThenumberofIOoutputport.
buildDay Theestablishdate.
cfgVer Theversionnumberofconfigurationinformation.
channelNum Thechannelnumber.
detail Thedetailsofdeviceinformation.
diskNum ThenumberofUSBdiskorSDcard.
firmVer Theversionnumberofthefirmware.

hardVer Theversionnumberofthehardware.
name Devicename.
type Devicetype.
wifi WhetherWi-Fiissupported.
B485 0:no485,1:have485
exactType Producttype
frameworkVer Architectureversion
3.1.3 GetDevName
 InterfaceDescription
ItisusedtogetconfigurationofDevName.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetDevName&token=TOKEN
 PostData
Dataexample
[{
"cmd":"GetDevName",
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription

Return datacorrectly
[
{
"cmd":"GetDevName",
"code":0,
"value":{
"DevName":{
"name":"NVR"
}
}
}
]
Fielddescription
Field description
name nameofdevice
3.1.4 SetDevName
 InterfaceDescription
ItisusedtosetconfigurationofDevName.
 InterfaceCallInstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetDevName&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetDevName",
"param":{
"DevName":{
"name":"camera101"
}

}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetDevName",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.1.5 GetTime
 InterfaceDescription
Itisusedtogettimefromdevice.
 InterfaceCallInstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetTime&token=TOKEN
 PostData

Dataexample
[
{
"cmd":"GetTime",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetTime",
"code":0,
"initial":{
"Dst":{
"enable":0,
"endHour":2,
"endMin":0,
"endMon":10,
"endSec":0,
"endWeek":5,
"endWeekday":0,
"offset":1,
"startHour":2,
"startMin":0,
"startMon":3,
"startSec":0,
"startWeek":2,
"startWeekday":0
},
"Time":{
"day":1,
"hour":0,
"hourFmt":0,
"min":0,
"mon":0,

"sec":0,
"timeFmt":"DD/MM/YYYY",
"timeZone":28800,
"year":0，
"hourFmt":0
}
},
"range":{
"Dst":{
"enable":"boolean",
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"endMon":{
"max":12,
"min":1
},
"endSec":{
"max":59,
"min":0
},
"endWeek":{
"max":5,
"min":1
},
"endWeekday":{
"max":6,
"min":0
},
"offset":{
"max":2,
"min":1
},
"startHour":{
"max":23,
"min":0
},
"startMin":{
"max":59,

"min":0
},
"startMon":{
"max":12,
"min":1
},
"startSec":{
"max":59,
"min":0
},
"startWeek":{
"max":5,
"min":1
},
"startWeekday":{
"max":6,
"min":0
}
},
"Time":{
"day":{
"max":31,
"min":1
},
"hour":{
"max":23,
"min":0
},
"hourFmt":{
"max":1,
"min":0
},
"min":{
"max":59,
"min":0
},
"mon":{
"max":12,
"min":1
},
"sec":{
"max":59,
"min":0
},

"timeFmt":["MM/DD/YYYY","YYYY/MM/DD",
"DD/MM/YYYY"],
"timeZone":{
"max":43200,
"min":-46800
},
"year":{
"max":2100,
"min":1900
}
}
},
"value":{
"Dst":{
"enable":0,
"endHour":2,
"endMin":0,
"endMon":10,
"endSec":0,
"endWeek":5,
"endWeekday":0,
"offset":1,
"startHour":2,
"startMin":0,
"startMon":3,
"startSec":0,
"startWeek":2,
"startWeekday":0
},
"Time":{
"day":23,
"hour":20,
"hourFmt":0,
"min":59,
"mon":12,
"sec":40,
"timeFmt":"DD/MM/YYYY",
"timeZone":28800,
"year":2020,
"hourFmt":0
}
}
}
]

Fielddescription
Field description
Dst DaylightSavingsTime
enable EnableDaylightSavingsTime
endHour TheendofDaylightSavingsTime(Hour)
endMin TheendofDaylightSavingsTime(Minute)
endMon TheendofDaylightSavingsTime(Month)
endSec TheendofDaylightSavingsTime(Second)
endWeek TheendofDaylightSavingsTime(Week)
endWeekday TheendofDaylightSavingsTime(Day)
offset Timeoffset
startHour DaylightSavingsTimestartingtime(Hour)
startMin DaylightSavingsTimestartingtime(Minute)
startMon DaylightSavingsTimestartingtime(Month)
startSec DaylightSavingsTimestartingtime(Second)
startWeek DaylightSavingsTimestartingtime(Week)
startWeekday DaylightSavingsTimestartingtime(Day)
Time Systemtime
year Year
mon Month
day Day
hour Hour
min Minute
sec Second
timeFmt Timeformat
timeZone Timezone
hourFmt Hourformat,0isfor24hourclock，1isfor12hourclock

3.1.6 SetTime
 InterfaceDescription
Itisusedtosettimeofthedevice.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetTime&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"SetTime",
"param":{
"Dst":{
"enable":0,
"endHour":2,
"endMin":0,
"endMon":10,
"endSec":0,
"endWeek":5,
"endWeekday":0,
"offset":1,
"startHour":2,
"startMin":0,
"startMon":3,
"startSec":0,
"startWeek":2,
"startWeekday":0
},
"Time":{
"day":6,
"hour":20,
"min":9,
"mon":6,
"sec":32,
"timeFmt":"DD/MM/YYYY",
"timeZone":-28800,
"year":2016,

"hourFmt":0
}
}
}
]
Fielddescription
Field Description M/O
Dst SeealsoGetTime O
enable SeealsoGetTime O
endHour SeealsoGetTime O
endMin SeealsoGetTime O
endMon SeealsoGetTime O
endSec SeealsoGetTime O
endWeek SeealsoGetTime O
endWeekday SeealsoGetTime O
offset SeealsoGetTime O
startHour SeealsoGetTime O
startMin SeealsoGetTime O
startMon SeealsoGetTime O
startSec SeealsoGetTime O
startWeek SeealsoGetTime O
startWeekday SeealsoGetTime O
year SeealsoGetTime O
mon SeealsoGetTime O
day SeealsoGetTime O
hour SeealsoGetTime O
min SeealsoGetTime O
sec SeealsoGetTime O
timeFmt SeealsoGetTime O
timeZone SeealsoGetTime O
hourFmt SeealsoGetTime O

 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetTime",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.1.7 GetAutoMaint
 InterfaceDescription
Itisusedtogetdeviceautomaticmaintenanceinformation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAutoMaint&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetAutoMaint",
"action":1
}
]
Fielddescription
Field Description M/O

 Returndatadescription
Return datacorrectly
[
{
[
{
"cmd":"GetAutoMaint",
"code":0,
"initial":{
"AutoMaint":{
"enable":0,
"hour":0,
"min":0,
"sec":0,
"weekDay":"Sunday"
}
},
"range":{
"AutoMaint":{
"enable":"boolean",
"hour":{
"max":23,
"min":0
},
"min":{
"max":59,
"min":0
},
"sec":{
"max":59,
"min":0
},
"weekDay":[
"Everyday",
"Sunday",
"Monday",
"Tuesday",
"Wednesday",
"Thursday",
"Friday",
"Saturday"

]
}
},
"value":{
"AutoMaint":{
"enable":1,
"hour":2,
"min":0,
"sec":0,
"weekDay":"Sunday"
}
}
}
]
Fielddescription
Field description
enable Automaintainanceofenable/disableswitch
hour Hour
min Minute
sec Second
weekDay Thedayoftheweek
3.1.8 SetAutoMaint
 InterfaceDescription
Itisusedtosetdeviceautomaticmaintenanceinformation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAutoMaint&token=TOKEN
 PostData
Dataexample
[

{
"cmd":"SetAutoMaint",
"param":{
"AutoMaint":{
"enable":1,
"weekDay":"Everyday",
"hour":3,
"min":52,
"sec":4
}
}
}
]
Fielddescription
Field Description M/O
enable SeealsoGetAutoMaint O
hour SeealsoGetAutoMaint O
min SeealsoGetAutoMaint O
sec SeealsoGetAutoMaint O
weekDay SeealsoGetAutoMaint O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAutoMaint",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description

3.1.9 GetHddInfo
 InterfaceDescription
Itisusedtogetharddisksorsd-Cardinformationofdevice.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetHddInfo&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetHddInfo"
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetHddInfo",
"code":0,
"value":{
"HddInfo":[
{
"capacity":938610,
"format":1,
"mount":1,
"number":1,
"size":549219,
"storageType":1
}
]

}
}
]
Fielddescription
Field description
capacity ThecapacityofHDDorSDcard(Mb)
format Whetheritisformattedornot
id IndexforHDDorSDcard
mount Whetheritismountedornot
size Theremainingcapacity(Mb)
storageType Typeofstorage
number ExternalSATAinterface
3.1.10 Format
 InterfaceDescription
ItisusedtoformatharddisksorSD-Card.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Format&token=TOKEN
 PostData
Dataexample
[{
"cmd":"Format",
"param":{
"HddInfo":{
"id":[0]
}
}
}]

Fielddescription
Field Description M/O
id Indexoftheharddiskorsd-Cardthatyouwantto M
format.
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Format",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.1.11 Upgrade
 InterfaceDescription
Itisusedtoupgradethefirmwareofthedevice.MustsendcmdUpgradePreparefirst
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Upgrade&clearConfig=%d&token
=TOKEN
 Requestparameterdescription


## Parameter M/O Description

clearConfig M Whethertocleartheconfigurationmark

 PostData
Dataexample
Content-Type:multipart/form-data;
boundary=----WebKitFormBoundaryYkwJBwvTHAd3Nukl
Referer:https://192.168.2.232/?1466148584152
Accept-Encoding:gzip,deflate
Accept-Language:zh-CN,zh;q=0.8
------WebKitFormBoundaryYkwJBwvTHAd3Nukl
Content-Disposition:form-data;name="upgrade-package";filename="xxx.pak"
Content-Type:application/octet-stream
xxxxxxxxxxx......(Filecontent)
------WebKitFormBoundaryYkwJBwvTHAd3Nukl--
Note:Thiscommandcanonlycarryupto40Kpacketsatatime,anditneedstobe
calledseveraltimestocompletethedeviceupdate
Fielddescription
Field Description M/O
boundary Delimiter M
filename Thenameoftheupdatefile M
name Boundtobe"upgrade-package" M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Upgrade",
"code":0,
"value":{
"rspCode":200
}
}
]

Fielddescription
Field description
3.1.12 Restore
 InterfaceDescription
Itisusedtoresetallconfigurationsofthedevicetothefactorydefault.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Restore&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"Restore"
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Restore",
"code":0,
"value":{
"rspCode":200
}
}
]

Fielddescription
Field description
3.1.13 Reboot
 InterfaceDescription
Itisusedtorebootthedevice.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Reboot&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"Reboot"
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Reboot",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription

Field description
3.1.14 UpgradePrepare
 InterfaceDescription
Itisusedtocheckthattheupgradefileislegalornot.Combinedusewithcmdupgrade
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=UpgradePrepare&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"UpgradePrepare",
"action":1,
"param":
{
"restoreCfg":0,
"fileName":"XXX.pak"
}
}
]
Fielddescription
Field Description M/O
restoreCfg Whethertocleartheconfigurationmark M
fileName Thefilenameoftheupgradefile M
 Returndatadescription
Return datacorrectly
[
{

"cmd":"UpgratePrepare",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.1.15 GetAutoUpgrade
 InterfaceDescription
Itisusedtogetdeviceautomaticupgradeinformation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAutoUpgrade&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetAutoUpgrade"
}
]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly

[
{
"cmd":"GetAutoUpgrade",
"code":0,
"initial":{
"AutoUpgrade":{
"enable":1
}
},
"range":{
"AutoUpgrade":{
"enable":"boolean"
}
},
"value":{
"AutoUpgrade":{
"enable":1
}
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.1.16 SetAutoUpgrade
 InterfaceDescription
Itisusedtosetdeviceautomaticupgradeinformation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAutoUpgrade&token=TOKEN
 POSTData
Dataexample

[
{
"cmd":"SetAutoUpgrade",
"param":{
"AutoUpgrade":{
"enable":0
}
}
}
]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAutoUpgrade",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.1.17 CheckFirmware
 InterfaceDescription
Itisusedtocheckfornewupgradefileofonlineupgrades
 Interfacecallinstructions

RequestURL https://IPC_IP/api.cgi?cmd=CheckFirmware&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"CheckFirmware"
}
]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"CheckFirmware",
"code":0,
"value":{
"newFirmware":00
}
}
]
Fielddescription
Field description
rspCode Responsecode
newFirmware Newfirmware
3.1.18 UpgradeOnline
 InterfaceDescription

Itisusedtostartonlineupgradewhencheckforanewversion
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=UpgradeOnline&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"UpgradeOnline",
}
]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"UpgradeOnline",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.1.19 UpgradeStatus
 InterfaceDescription

ItisusedtoCheckfiledownloadprogressduringonlineupgrade
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=UpgradeStatus&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"UpgradeStatus"
}
]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"UpgradeStatus",
"code":0,
"value":{
"Status":{
"Persent":0,
"code":0
}
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.1.20 Getchannelstatus
 InterfaceDescription
Itisusedtogetconfigurationofchannelstatus.
 Interfacecallinstructions
RequestURL https://NVR_IP/api.cgi?cmd=Getchannelstatus&token=TOKEN
 PostData
Dataexample
[{
"cmd":"Getchannelstatus"
}]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetChannelstatus",
"code":0,
"value":{
"count":16,
"status":[
{
"channel":0,
"name":"E1X",
"online":1,
"typeInfo":"E1X"
},
{
"channel":1,
"name":"",

"online":0,
"typeInfo":""
},
{
"channel":2,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":3,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":4,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":5,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":6,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":7,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":8,
"name":"",
"online":0,
"typeInfo":""

},
{
"channel":9,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":10,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":11,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":12,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":13,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":14,
"name":"",
"online":0,
"typeInfo":""
},
{
"channel":15,
"name":"",
"online":0,
"typeInfo":""
}
]

}
}
]
Fielddescription
Field description
channel Channelnumber
name Devicename
online Whetheronlineornot
typeinfo Infomationoftype
3.2 Security
3.2.1 Login
 InterfaceDescription
ItisusedtogetToken.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Login
 POSTData
Dataexample
[{
"cmd":"Login",
"param":{
"User":{
"Version":"0",
"userName":"admin",
"password":"111111"
}
}
}]]

Fielddescription
Field Description M/O
userName Accountname,limit1~31characters. M
password Accountpassword,limit1~31characters. O
Version Loginversion O
0:Donotapplyprivateencryptionprotocol
1:Applyaprivateencryptionprotocol
Theprivateencryptionprotocolisnotprovidedexternally,so
pleaseselect0
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Login",
"code":0,
"value":{
"Token":{
"leaseTime":3600,
"name":"031465962723"
}
}
}
]
Fielddescription
Field description
leaseTime Leasetimebysecond.
name Tokenstring,lengthshouldbelessthan32characters.
3.2.2 Logout
 InterfaceDescription

ItisusedtoreleaseToken.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Logout&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"Logout",
"param":{
}
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Logout",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.2.3 GetUser
 InterfaceDescription
Itisusedtogetallusers'infomation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetUser&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetUser",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetUser",
"code":0,
"initial":{
"User":{
"level":"guest"
}
},
"range":{
"User":{
"level":["guest","admin"],
"password":{
"maxLen":31,

"minLen":6
},
"userName":{
"maxLen":31,
"minLen":1
}
}
},
"value":{
"User":[
{
"level":"admin",
"userName":"admin"
}
]
}
}
]
Fielddescription
Field description
level Usercompetence
userName Username
maxlen Maxlength
minlen Minlength
3.2.4 AddUser
 InterfaceDescription
Itisusedtosetconfigurationofuser.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=AddUser&token=TOKEN
 POSTData

Dataexample
[
{
"cmd":"AddUser",
"param":{
"User":{
"userName":"GuestUser",
"password":"123456",
"level":"guest"
}
}
}
]
Fielddescription
Field Description M/O
userName Accountname. M
password Accountpassword. M
level Usercompetence M
Note:Canaddupto20users
 Returndatadescription
Return datacorrectly
[
{
"cmd":"AddUser",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.2.5 DelUser
 InterfaceDescription
Itisusedtodelconfigurationofuser.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=DelUser&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"DelUser",
"param":{
"User":{
"userName":"TestUser"
}
}
}
]
Fielddescription
Field Description M/O
userName Accountname,limit1~31characters. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"DelUser",
"code":0,
"value":{
"rspCode":200
}
}
]

Fielddescription
Field description
rspCode Responsecode
3.2.6 ModifyUser
 InterfaceDescription
Itisusedtomodifyconfigurationofuser.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=ModifyUser&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"ModifyUser",
"action":0,
"param":{
"User":{
"userName":"admin",
"newPassword":"111111",
"oldPassword":"000000"
}
}
}]
Fielddescription
Field Description M/O
userName Accountname. M
newPassword Accountnewpassword. M
oldPassword Accountoldpassword.
 Returndatadescription

Return datacorrectly
[
{
"cmd":"ModifyUser",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.2.7 GetOnline
 InterfaceDescription
Itisusedtogetallonlusers'infomation.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetOnline&token=TOKEN
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetOnline",
"code":0,
"value":{
"User":[
{
"canbeDisconn":0,
"ip":"192.168.2.166",
"level":"admin",
"sessionId":1000,

"userName":"admin"
},
...//Theremaybemultipleonlineusers.
]
}
}
]
Fielddescription
Field description
canbeDisconn Whenthefieldvalueis1,theonlineusercanbeforcedto
disconnect.Whenthevalueis0,thereverseisthecase.
ip TheIPaddressoftheonlineuser.
level Usercompetenceforonlineusers
sessionId Sessioniddistributedtoonlineusersbythesystem,itis
usedtoforcetheusertogooffline.
userName Theonlineuser’sloginaccount.
3.2.8 Disconnect
 InterfaceDescription
Itisusedtodisconnectconfigurationofuser.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Disconnect&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"Disconnect",
"param":{
"User":{
"userName":"userName",
"sessionId":1001

}
}
}]
Fielddescription
Field Description M/O
userName Theonlineuser’sloginaccount. M
sessionId ThesessionIDwhichSystemassignedtotheonlineuser. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Disconnect",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.2.9 GetSysCfg
 InterfaceDescription
Itisusedtogettheloginlocktime.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetSysCfg&token=TOKEN
 PostData

Dataexample
[{
"cmd":"GetSysCfg",
"action":1,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Devicechannelnumber
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetSysCfg",
"code":0,
"initial":{
"SysCfg":{
"LockTime":300,
"allowedTimes":5,
"loginLock":0
}
},
"range":{
"SysCfg":{
"LockTime":{
"max":300,
"min":0
},
"allowedTimes":{
"max":5,
"min":0
},
"loginLock":"boolean"
}
},

"value":{
"SysCfg":{
"LockTime":300,
"allowedTimes":5,
"loginLock":0
}
}
}
]
Fielddescription
Field description
LockTime Loginlocktime
allowedTimes Maximumnumberofallowedattempts
loginLock Loginlockswitch
3.2.10 SetSysCfg
 InterfaceDescription
Itisusedtosetconfigurationofsystem.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetSysCfg&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetSysCfg",
"action":0,
"param":{
"SysCfg":{
"loginLock":1

}
}
}]
Fielddescription
Field Description M/O
loginLock Loginlockswitch
Note:Youcanonlysetwhethertoenabletheloginlockfunction,thenumberof
attemptsandlocktimecannotbechanged
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetSysCfg",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.3 Network
3.3.1 GetLocalLink
 InterfaceDescription
ItisusedtogetconfigurationofLocalLink.
 Interfacecallinstructions

RequestURL https://IPC_IP/api.cgi?cmd=GetLocalLink&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetLocalLink",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetLocalLink",
"code":0,
"initial":{
"LocalLink":{
"activeLink":"LAN",
"dns":{
"auto":1,
"dns1":"192.168.0.1",
"dns2":"192.168.0.1"
},
"mac":"EC:71:DB:36:8E:C7",
"static":{
"gateway":"192.168.0.1",
"ip":"192.168.0.100",
"mask":"255.255.255.0"
},
"type":"DHCP"
}
},
"range":{
"LocalLink":{
"dns":{

"auto":"boolean",
"dns1":{
"maxLen":15
},
"dns2":{
"maxLen":15
}
},
"static":{
"gateway":{
"maxLen":15
},
"ip":{
"maxLen":15
},
"mask":{
"maxLen":15
}
},
"type":["DHCP","Static"]
}
},
"value":{
"LocalLink":{
"activeLink":"LAN",
"dns":{
"auto":1,
"dns1":"192.168.2.1",
"dns2":"114.114.114.114"
},
"mac":"ec:71:db:0f:93:91",
"static":{
"gateway":"192.168.2.1",
"ip":"192.168.3.38",
"mask":"255.255.252.0"
},
"type":"DHCP"
}
}
}
]
Fielddescription

Field description
activeLink Networkconnectiontype[LAN,Wi-Fi]
mac Networkcard’shardwareaddress
type NetworkIP’sdistrbuitingway,[DHCP,Static]
Static->ip Ipaddress
Static->gateway Gatewayaddress
Static->mask Subnetmask
Dns->auto Whetherautogetddnsornot
Dns->dns1 PreferredDNSServer.
Dns->dns2 AlternateDNSserver.
3.3.2 SetLocalLink
 InterfaceDescription
ItisusedtosetconfigurationofLocalLink.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetLocalLink&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetLocalLink",
"action":0,
"param":{
"LocalLink":{
"type":"Static",
"static":{
"ip":"192.168.2.122",
"mask":"255.255.255.0",
"gateway":"192.168.2.1"
},

"dns":{
"auto":0,
"dns1":"202.96.128.166",
"dns2":"202.96.134.133"
}
}
}
}
]
Fielddescription
Field Description M/O
type NetworkIP’sdistrbuitingway,[DHCP,Static] O
Static->ip Ipaddress O
Static->gateway Gatewayaddress O
Static->mask Subnetmask O
Dns->auto Whetherautogetddnsornot[0,1] O
Dns->dns1 PreferredDNSServer. O
Dns->dns2 AlternateDNSserver. O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetLocalLink",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.3.3 GetDdns
 InterfaceDescription
ItisusedtogetconfigurationofEmail.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetDdns&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetDdns",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetDdns",
"code":0,
"initial":{
"Ddns":{
"domain":"",
"enable":1,
"password":"",
"servAddr":"dynupdate.no-ip.com", //NVR
"type":"no-ip",
"userName":""
}
},

"range":{
"Ddns":{
"domain":{
"maxLen":127
},
"enable":"boolean",
"password":{
"maxLen":127
},
"servAddr":{ //NVR
"maxLen":127,
"servAddrList":{
"Dyndns":"members.dyndns.org",
"no-ip":"dynupdate.no-ip.com"
}
},
"type":["no-ip","Dyndns"],
"userName":{
"maxLen":127
}
}
},
"value":{
"Ddns":{
"domain":"",
"enable":1,
"password":"",
"servAddr":"dynupdate.no-ip.com", //NVR
"type":"no-ip",
"userName":""
}
}
}
]
Fielddescription
Field description
domain Thedomainwhichyouset.
enable Ddnsenableswitch.
type DdnsServertype.Rangeofvalueis["3322","Dyndns"].
userName DdnsuserName.

password Ddnspassword.
servAddr Serveraddress
3.3.4 SetDdns
 InterfaceDescription
ItisusedtosetconfigurationofDDNS.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetDdns&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetDdns",
"param":{
"Ddns":{
"enable":1,
"type":"dyndns",
"userName":"username",
"password":"password",
"domain":"domain"
}
}
}
]
Fielddescription
Field Description M/O
domain Thedomainwhichyouset. O
enable Ddnsenableswitch. O
type DdnsServertype.Rangeofvalueis["3322", O
"Dyndns"].
userName DdnsuserName. O

password Ddnspassword. O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetDdns",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.3.5 GetEmail
 InterfaceDescription
ItisusedtogetconfigurationofEmail.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetEmail&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetEmail",
"action":1
}
]

Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetEmail",
"code":0,
"initial":{
"Email":{
"addr1":"",
"addr2":"",
"addr3":"",
"attachment":"picture",
"interval":"5Minutes",
"nickName":"NVR", //NVR
"password":"",
"schedule":{
"enable":0,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
},
"smtpPort":465,
"smtpServer":"smtp.gmail.com",
"ssl":1,
"userName":""
}
},
"range":{
"Email":{
"addr1":{
"maxLen":127
},
"addr2":{
"maxLen":127
},
"addr3":{
"maxLen":127

},
"attachment":["no","picture","video","onlyPicture"],
"interval":["30Seconds","1Minute","5Minutes","10Minutes",
"30Minutes"],
"nickName":{ //NVR
"maxLen":127
},
"password":{
"maxLen":31
},
"schedule":{
"enable":"boolean",
"table":{
"maxLen":168,
"minLen":168
}
},
"smtpPort":{
"max":65535,
"min":1
},
"smtpServer":{
"maxLen":127
},
"ssl":"boolean",
"userName":{
"maxLen":127
}
}
},
"value":{
"Email":{
"addr1":"",
"addr2":"",
"addr3":"",
"attachment":"picture",
"interval":"30Minutes",
"nickName":"NVR", //NVR
"password":"******",
"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

1111111111111111111111111111111111111"
},
"smtpPort":465,
"smtpServer":"smtp.gmail.com",
"ssl":1,
"userName":"***@sz-bcs.com.cn"
}
}
}
]
Fielddescription
Field description
smtpServer Emailserverofsender,atmost127characters.
smtpPort PortofEmailserver,limit1~65535.
userName Senderaddress,atmost127characters.
password Senderpassword,atmost31characters.
attachment Thetypeofemailattachment.
ssl Whethertoopentheencryptionmode,thetypeofsslis
Boolean.
interval Sendmailinterval.
addr1 Recveraddress1,atmost127characters.
addr2 Recveraddress2,atmost127characters.
addr3 Recveraddress3,atmost127characters.
Schedule->enable Whetheremailreceivethealarminformation
Schedule->table Thescheduleaboutwhenemailreceivesthealarm
information
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“GetEmailV20”
3.3.6 SetEmail
 InterfaceDescription

ItisusedtosetconfigurationofEmail.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetEmail&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetEmail",
"param":{
"Email":{
"smtpServer":"smtp.exmail.qq.com",
"smtpPort":25,
"userName":"xxx@sz-bcs.com.cn",
"password":"xxxxxx",
"attachment":"video",
"ssl":0,
"interval":"5Minutes",
"addr1":"xxx@sz-bcs.com.cn",
"addr2":"xxx@sz-bcs.com.cn",
"addr3":"xxx@sz-bcs.com.cn",
"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111"
}
}
}
}
]
Fielddescription
Field Description M/O
smtpServer Emailserverofsender,atmost127characters. O
smtpPort PortofEmailserver,limit1~65535. O
userName Senderaddress,atmost127characters. O

password Senderpassword,atmost31characters. O
attachment Thetypeofemailattachment.Rangeofvalueis["O", O
"picture","video","onlyPicture"].
Ssl Whethertoopentheencryptionmode,thetypeofssl O
isBoolean.
interval Sendmailinterval.Rangeofvalueis["30Seconds","1 O
Minute","5Minutes","10Minutes"].
addr1 Recveraddress1,atmost127characters. O
addr2 Recveraddress2,atmost127characters. O
addr3 Recveraddress3,atmost127characters. O
Schedule->en Whetheremailreceivethealarminformation[0,1] O
able
Schedule->tab Thescheduleaboutwhenemailreceivesthealarm O
le information
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetEmail",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“SetEmailV20”

3.3.7 GetEmailV20
 InterfaceDescription
It isused to get configuration ofEmail.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=GetEmailV20&token=TOKEN
 POSTData
Data example
[{
"cmd": "GetEmailV20",
"param": {
"channel": 0
}
}]
Fielddescription
Field Description M/O
 Returndatadescription
Return data correctly
[
{
"cmd" :"GetEmailV20",
"code" : 0,
"value" : {
"Email": {
"addr1" : "xxx@sz-bcs.com.cn",
"addr2" : "xxx@sz-bcs.com.cn",
"addr3" : "xxx@sz-bcs.com.cn",
"attachmentType" : 2,
"diskErrorAlert" :0,

"diskFullAlert" :0,
"enable" : 0,
"interval" : "5Minutes",
"nickName" : "NVR",
"password" : "xxxxxx",
"schedule" : {
"channel" : 0,
"table" : {
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111",
"VL" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000"
}
},
"smtpPort": 25,
"smtpServer" : "smtp.exmail.qq.com",
"ssl" : 0,
"supportTextType" : 1,
"supportVideo" : 1,
"textType" : 1,
"userName" : "xxx@sz-bcs.com.cn"
}
}
}
]
Fielddescription
Field description
smtpServer Email server of sender,at most127characters.
smtpPort Port ofEmail server,limit1~65535.

userName Sender address,at most 127characters.
password Sender password,at most31characters.
attachmentType The type ofemail attachment.
Ssl Whether toopen theencryption mode,the type ofssl is
Boolean.
interval Send mail interval.
addr1 Recver address1, at most 127characters.
addr2 Recver address2, at most 127characters.
addr3 Recver address3, at most 127characters.
Schedule->enable Start usingschedule
Schedule->table Table ofAlarmtype
nickname Corresponds tothe username
supportTextType Support thetype of Test
supportVideo Support thetype of video
textType Textof type
3.3.8 SetEmailV20
 InterfaceDescription
It isused to set configuration of Email.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=SetEmailV20&token=TOKEN
 POSTData
Data example
[{
"cmd": "SetEmailV20",
"param": {

"Email": {
"ssl": 0,
"smtpPort": 25,
"smtpServer": "smtp.exmail.qq.com",
"userName": "xxx@sz-bcs.com.cn",
"nickName": "",
"addr1": "xxx@sz-bcs.com.cn",
"addr2": "xxx@sz-bcs.com.cn",
"addr3": "xxx@sz-bcs.com.cn",
"interval": "5Minutes"
}
}
}]
Fielddescription
Field Description M/O
smtpServer Emailserver ofsender, at most127characters. O
smtpPort Portof Emailserver, limit1~65535. O
userName Senderaddress, at most 127characters. O
password Senderpassword, at most31characters. O
nickName O
Ssl Whethertoopen theencryptionmode, thetype ofssl is O
Boolean.
interval Send mailinterval. Range ofvalue is ["30 Seconds", O
"1Minute", "5 Minutes", "10 Minutes"].
addr1 Recver address1,at most127characters. O
addr2 Recver address2,at most127characters. O
addr3 Recver address3,at most127characters. O
Schedule->en Startusing schedule O
able
Schedule->tab TableofAlarmtype O
le
 Returndatadescription

Return data correctly
[
{
"cmd" :"SetEmailV20",
"code" : 0,
"value" : {
"rspCode" :200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.3.9 TestEmail
 InterfaceDescription
ItisusedtosetconfigurationofTestEmail.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=TestEmail&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"TestEmail",
"param":{
"Email":{
"addr1":"****@sz-bcs.com.cn",
"addr2":"",
"addr3":"",
"interval":"5Minutes",
"nickName":"000",
"password":"lwmypvelvexadfab",

"smtpPort":465,
"smtpServer":"smtp.qq.com",
"ssl":1,
"userName":"**********@qq.com"
}
}
}]
Fielddescription
Field Description M/O
smtpServer Emailserverofsender,atmost127characters. M
smtpPort PortofEmailserver,limit1~65535. M
userName Senderaddress,atmost127characters. M
password Senderpassword,atmost31characters. O
ssl Whethertoopentheencryptionmode,thetypeofssl M
isBoolean.
addr1 Recveraddress1,atmost127characters. O
addr2 Recveraddress2,atmost127characters. O
addr3 Recveraddress3,atmost127characters. O
nickName Correspondstotheusername O
Note:Atleastoneofthethreeaddresses(addr1,addr2,addr3)iscompleted.
 Returndatadescription
Return datacorrectly
[
{
"cmd":"TestEmail",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description

rspCode Responsecode
3.3.10 GetFtp
 InterfaceDescription
ItisusedtogetconfigurationofFtp.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetFtp&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetFtp",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetFtp",
"code":0,
"initial":{
"Ftp":{
"anonymous":0,
"autoDir":1, //NVR
"interval":30,
"maxSize":100,
"mode":0, //NVR

"password":"",
"port":21,
"remoteDir":"",
"schedule":{
"enable":0,
"table":
"22222222222222222222222222222222222222222222222222222222222222222
222222222222222222222222222222222222222222222222222222222222222222
2222222222222222222222222222222222222"
},
"server":"",
"streamType":0,
"userName":""
}
},
"range":{
"Ftp":{
"anonymous":"boolean",
"autoDir":"boolean", //NVR
"interval":{
"max":3600,
"min":1
},
"maxSize":{
"max":1024,
"min":10
},
"mode":{ //NVR
"max":2,
"min":0
},
"password":{
"maxLen":127
},
"port":{
"max":65535,
"min":1
},
"remoteDir":{
"maxLen":255
},
"schedule":{
"enable":"boolean",
"table":{

"maxLen":168,
"minLen":168
}
},
"server":{
"maxLen":127
},
"streamType":{
"max":2,
"min":0
},
"userName":{
"maxLen":127
}
}
},
"value":{
"Ftp":{
"anonymous":0,
"autoDir":1, //NVR
"interval":30,
"maxSize":100,
"mode":0,
"password":"",
"port":21,
"remoteDir":"",
"schedule":{
"enable":1,
"table":
"22222222222222222222222222222222222222222222222222222222222222222
222222222222222222222222222222222222222222222222222222222222222222
2222222222222222222222222222222222222"
},
"server":"",
"streamType":0,
"userName":""
}
}
}
]
Fielddescription
Field Description

initial TheinitialvalueoftheFtpfield.
range TherangeoftheFtpfield.
value TherealvalueoftheFtpfield.
server FTPserver,canfillintheIPaddressordomainname.
Atmost127characters.
port PortofFTPServer,Limit1~65535.
anonymous Whetheranonymousornot
userName FTPaccountname.
password FTPaccountpassword.
remoteDir FTProotdirectory.
maxSize MaximumsizeofFTPfile.
streamType Thetypesoftheuploadingfiles.0isforuploadingboth
picturesandvideos,and1isforuploadingpicturesonly.
interval WhenstreamType=0,intervalstandsforthetimeofpost
record,therangeisbetween30to1800seconds.
WhenstreamType=1,intervalstandsforthetimeinterval,
therangeisbetween1to1800seconds.
Schedule->enable Whetherftpreceivesthealarminformationornot.
Schedule->table Thescheduleaboutwhenftpreceivesthealarminformation
autoDir
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“GetFtpV20”
3.3.11 SetFtp
 InterfaceDescription
ItisusedtosetconfigurationofFtp.
 InterfaceCallInstructions

RequestURL https://IPC_IP/api.cgi?cmd=SetFtp&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"SetFtp",
"param":{
"Ftp":{
"anonymous":0,
"autoDir":1,
"bpicSingle":0,
"bvideoSingle":0,
"interval":30,
"maxSize":100,
"mode":0,
"onlyFtps":0,
"password":"",
"picInterval":60,
"picName":"",
"port":21,
"remoteDir":"",
"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
},
"server":"",
"size":"",
"streamType":0,
"userName":"",
"videoName":""
}
}
}]
Fielddescription
Field Description M/O
server FTPserver,canfillintheIPaddressordomainname. O
port PortofFTPServer. O

aonymous Whetheranonymousornot O
userName FTPaccountname.Whenthevalueofanonymousis O
(Dependon 0,theuserNamefieldisnecessary.
anonymous)
Password FTPaccountpassword.FTPaccountname.Whenthe O
(Dependon valueofaOnymousis0,thepasswordfieldis
anonymous) necessary.
remoteDir FTProotdirectory. O
maxSize MaximumsizeofFTPfile. O
streamType Thetypeoftheuploadingfiles.0isforuploadingboth O
picturesandvideos,and1isforuploadingpictures
only.
interval WhenstreamType=0,intervalstandsforthetimeof O
postrecord,therangeisbetween30to1800seconds.
WhenstreamType=1,intervalstandsforthetime
interval,therangeisbetween1to1800seconds.
Schedule->en Whetherftpreceivethealarminformation[0,1] O
able
Schedule->tab Thescheduleaboutwhenftpreceivesthealarm O
le information
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“SetFtpV20”
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetFtp",
"code":0,
"value":{
"rspCode":200
}

}
]
Fielddescription
Field Description
rspCode Responsecode
Note:Thiscommandsupportsmodel52Xonly
3.3.12 GetFtpV20
 InterfaceDescription
It isused to get configuration ofFtp.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=GetFtpV20&token=TOKEN
 POSTData
Data example
[
{
"cmd":"GetFtpV20",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return data correctly
[
{
"cmd" :"GetFtpV20",
"code" : 0,

"initial" :{
"Ftp" :{
"anonymous" : 0,
"autoDir" : 1,
"bpicSingle" : 0,
"bvideoSingle" : 0,
"enable" : 1,
"interval" : 30,
"maxSize" : 100,
"mode" :0,
"onlyFtps" :0,
"password" : "",
"picCaptureMode" : 0,
"picHeight" : 2160,
"picInterval" :60,
"picName" : "",
"picWidth" :3840,
"port": 21,
"remoteDir" : "",
"schedule" : {
"channel" : 0,
"table" : {
"AI_DOG_CAT" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111",
"TIMING" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000"
}
},

"server" :"",
"streamType" : 0,
"userName" : "",
"videoName" : ""
}
},
"range" : {
"Ftp" :{
"anonymous" : "boolean",
"autoDir" : [0,1,2,3],
"bpicSingle" : [0,1,2],
"bvideoSingle" : [0,1,2],
"enable" : "boolean",
"interval" : [5,10,15,30,60],
"maxSize" : {
"max" :1024,
"min" : 10
},
"mode" :{
"max" :2,
"min" : 0
},
"password" : {
"maxLen" : 127
},
"picCaptureMode" : [ 0,1,2,3],
"picHeight" : {
"max" :2160,
"min" : 360
},
"picInterval" :[2,5,10,15,30,60,300,600,1800],
"picName" : {
"maxLen" : 127
},
"picWidth" :{
"max" :3840,
"min" : 640
},
"port": {
"max" :65535,
"min" : 1
},
"remoteDir" : {
"maxLen" : 255

},
"schedule" : {
"channel" : 0,
"table" : {
"AI_DOG_CAT" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"AI_PEOPLE" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"AI_VEHICLE" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"MD" : {
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"TIMING" : {
"table" : {
"maxLen" : 168,
"minLen" : 168
}
}
}
},
"server" :{
"maxLen" : 127
},
"streamType" : {
"max" :6,
"min" : 0
},
"userName" : {

"maxLen" : 127
},
"videoName" : {
"maxLen" : 127
}
}
},
"value" : {
"Ftp" :{
"anonymous" : 0,
"autoDir" : 2,
"bpicSingle" : 0,
"bvideoSingle" : 0,
"enable" : 1,
"interval" : 30,
"maxSize" : 100,
"mode" :2,
"onlyFtps" :1,
"password" : "***********",
"picCaptureMode" : 3,
"picHeight" : 2160,
"picInterval" :60,
"picName" : "",
"picWidth" :3840,
"port": 21,
"remoteDir" : "*******",
"schedule" : {
"channel" : 0,
"table" : {
"AI_DOG_CAT" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111

11111111111111111111111111111111111",
"TIMING" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000"
}
},
"server" :"192.168.0.132",
"streamType" : 3,
"userName" : "ft***er",
"videoName" : ""
}
}
}
]
Fielddescription
Field Description
initial The initialvalueof theFtp field.
range The range oftheFtp field.
value The real value ofthe Ftpfield.
server FTP server, can fill in theIP address ordomain name.
At most 127characters.
port Port ofFTP Server, Limit 1~65535.
Anonymous Whether tobe anonymous
userName FTP account name.
password FTP account password.
remoteDir FTP root directory.
maxSize Maximum size ofFTP file.
streamType The types oftheuploading files. 0is for uploading both
pictures andvideos, and 1isfor uploading pictures only.
interval When streamType=0, interval stands for thetimeof post
record, the range is between 30to 1800seconds.
When streamType=1, interval stands for thetimeinterval,the
range is between 1to 1800seconds.

Schedule->enable Whether Startusing schedule ornot
Schedule->table Table ofAlarm type
autoDir Whether tocreate directories automatically
0:Create directories byyear, month and day, like:
YYYY-MM-DD
1:0:Create directories byyear, month,like:
YYYY-MM
mode Transport mode
0:Chooseactive modeorpassive modeautonomously
1:Active mode
2:Passivemode
onlyFtps Ftps switch,Whethertoselect theencryption mode
picCaptureMode Image resolution mode
0:Aclear picture
1:Standard image
2:Smooth image
Note: Clearpictures have thehighest resolution, smooth
pictures havethe lowest resolution
picHeight Pictureheight
Note: Thewidth and height oftheimage are not arbitrary and
need to match theresolution supported bytheimage
picWidth Pitcurewidth
bpicSingle Image upload mode
0:All images are retained and willnot bedeleted
1:Only thelatest image will bekept, and theothers willbe
replaced
2:Theother replacement strategy, which is different, instead
ofreplacing directly, is tofirst storethesecond image and
then deletethefirst one
bvideoSingle Video upload mode

0:All videos are retained and will not bedeleted
1:Only thelatest video will bekept, and theothers will be
replaced
2:Theother replacement strategy, which is different, instead
ofreplacing directly, is tofirst storethesecond video and
then deletethefirst one
picInterval Image upload interval
3.3.13 SetFtpV20
 InterfaceDescription
It isused to set configuration of Ftp.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=SetFtpV20&token=TOKEN
 POSTData
Data example
[{
"cmd": "SetFtpV20",
"param": {
"Ftp":{
"anonymous": 0,
"autoDir": 1,
"bpicSingle": 0,
"bvideoSingle": 0,
"enable": 1,
"interval": 30,
"maxSize": 100,
"mode": 0,
"onlyFtps": 1,
"password": "***********",
"picCaptureMode": 3,

"picHeight": 1920,
"picInterval": 60,
"picName": "",
"picWidth": 2304,
"port": 21,
"remoteDir": "hello",
"schedule": {
"channel": 0,
"table": {
"AI_DOG_CAT":
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111",
"AI_PEOPLE":
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111",
"AI_VEHICLE":
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111",
"MD":
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111",
"TIMING":
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000"
}
},
"server": "192.168.1.236",
"streamType": 6,
"userName": "ft***er",
"videoName": "sdfs"
}
}
}]
Fielddescription
Field Description M/O
server FTP server, can fillin theIP address ordomain name. O
port Portof FTP Server. O

anonymous Whethertobe anoymous ornot O
userName FTP account name. When thevalue ofanonymous is 0, O
(Depend on theuserName field is necessary.
anonymous)
Password FTP account password. FTP account name. When the O
(Depend on valueofanonymous is 0,thepassword field is
anonymous) necessary.
remoteDir FTP root directory. O
maxSize MaximumsizeofFTP file. O
streamType Thetype ofthe uploading files. 0isfor uploading both O
pictures and videos, and 1is foruploading pictures
only.
interval WhenstreamType=0, interval stands for thetimeof O
postrecord, the range is between 30to 1800seconds.
WhenstreamType=1, interval stands for thetime
interval,therange is between 1to 1800seconds.
Schedule->en WhetherStart usingschedule or not O
able
Schedule->tab TableofAlarm type O
le
mode Transport mode
 Returndatadescription
Return data correctly
[
{
"cmd" :"SetFtp",
"code" : 0,
"value" : {
"rspCode" :200
}
}

]
Fielddescription
Field description
rspCode Responsecode
3.3.14 TestFtp
 InterfaceDescription
ItisusedtosetconfigurationofTestFtp.
 InterfaceCallInstructions
RequestURL https://IPC_IP/api.cgi?cmd=TestFtp&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"TestFtp",
"action":0,
"param":{
"Ftp":{
"server":"192.168.0.132",
"port":21,
"anonymous":0,
"mode":2,
"userName":"ftpuser",
"password":"000000",
"remoteDir":"fadad",
"onlyFtps":1,
"bpicSingle":2,
"bvideoSingle":2
}
}
}]

Fielddescription
Field Description M/O
server FTPserver,canfillintheIPaddressordomainname. M
Atmost127characters.
port PortofFTPServer,Limit1~65535. M
anonymous Whetheranonymousornot M
userName FTPaccountname.FTPaccountpassword.FTP O
(Dependon accountname.Whenthevalueofanonymousis0,the
anonymous) userNamefieldisnecessary.
Password FTPaccountpassword.FTPaccountpassword.FTP O
(Dependon accountname.Whenthevalueofanonymousis0,the
anonymous) passwordfieldisnecessary.
remoteDir FTProotdirectory. M
mode Transporttype M
onlyFtps Ftpsswitch M
bpicSingle Imageuploadmode M
bvideoSingle Videouploadmode M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"TestFtp",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field Description
rspCode Responsecode

mode Transport
3.3.15 GetNtp
 InterfaceDescription
ItisusedtogetconfigurationofNTP.
 InterfaceCallInstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetNtp&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetNtp",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetNtp",
"code":0,
"initial":{
"Ntp":{
"enable":0,
"interval":1440,
"port":123,
"server":"pool.ntp.org"
}

},
"range":{
"Ntp":{
"enable":"boolean",
"interval":{
"max":65535,
"min":60
},
"port":{
"max":65535,
"min":1
},
"server":{
"maxLen":127
}
}
},
"value":{
"Ntp":{
"enable":0,
"interval":1440,
"port":123,
"server":"pool.ntp.org"
}
}
}
]
Fielddescription
Field Description
enable NTPswitch,Thevalueof1representstheopen,andthe0is
theopposite.
server NTPserver,canfillintheIPaddressordomainname.
port PortofNTPServer.
interval Timesynchronizationinterval.Limit10~65535,and0on
behalfoftheimmediatesynchronization.

3.3.16 SetNtp
 InterfaceDescription
ItisusedtosetconfigurationofSetNtp.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetNtp&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetNtp",
"param":{
"Ntp":{
"enable":1,
"server":"pool.ntp.org",
"port":123,
"interval":1440
}
}
}
]
Fielddescription
Field Description M/O
enable NTPswitch,thevalueof1representstheopen,and O
the0istheopposite.
server NTPserver,canfillintheIPaddressordomainname. O
port PortofNTPServer. O
interval Timesynchronizationinterval.Limit10~65535,and0 O
onbehalfoftheimmediatesynchronization.
 Returndatadescription

Return datacorrectly
[
{
"cmd":"SetNtp",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field Description
rspCode Responsecode
3.3.17 GetNetPort
 InterfaceDescription
ItisusedtogetconfigurationofNetPort.
 InterfaceCallInstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetNetPort&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetNetPort",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription

Return datacorrectly
[
{
"cmd":"GetNetPort",
"code":0,
"value":{
"NetPort":{
"httpEnable":0,
"httpPort":80,
"httpsEnable":1,
"httpsPort":443,
"mediaPort":9000,
"onvifEnable":1,
"onvifPort":8000,
"rtmpEnable":0,
"rtmpPort":1935,
"rtspEnable":1,
"rtspPort":554
}
}
}
]
Fielddescription
Field Description
httpPort Portofhttp.
httpsPort Portofhttps.
mediaPort Portofmedia.
onvifPort Portofonvif.
rtspPort Portofrtsp.
rtmpPort Portofrtmp.
httpEnable httpswitch
httpsEnable httpsswitch
rtmpEnable Rtmpswitch
rtspEnable Rtspswitch
onvifEnable Onvifswitch

3.3.18 SetNetPort
 InterfaceDescription
ItisusedtosetconfigurationofNetPort.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetNetPort&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"SetNetPort",
"param":{
"NetPort":{
"httpEnable":0,
"httpPort":80,
"httpsEnable":1,
"httpsPort":443,
"mediaPort":9000,
"onvifEnable":1,
"onvifPort":8000,
"rtmpEnable":0,
"rtmpPort":1935,
"rtspEnable":1,
"rtspPort":554
}
}
}]
Fielddescription
Field Description M/O
httpPort Portofhttp. O
httpsPort Portofhttps. O
mediaPort Portofmedia. O
onvifPort Portofonvif. O

rtspPort Portofrtsp. O
rtmpPort Portofrtmp. O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetNetPort",
"code":0,
"value":{
"rspCode":200
}
}
]
FieldDescription
Field Description
rspCode Responsecode
3.3.19 GetUpnp
 InterfaceDescription
ItisusedtogetconfigurationofUpnp.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetUpnp&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetUpnp",
"action":1
}

]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetUpnp",
"code":0,
"initial":{
"Upnp":{
"enable":0
}
},
"range":{
"Upnp":{
"enable":"boolean"
}
},
"value":{
"Upnp":{
"enable":0
}
}
}
]
Fielddescription
Field Description
enable Upnpswitch,Thevalueof1representstheopen,andthe0is
theopposite.
3.3.20 SetUpnp
 InterfaceDescription

ItisusedtosetconfigurationofUpnp.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetUpnp&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetUpnp",
"param":{
"Upnp":{
"enable":1
}
}
}
]
Fielddescription
Field Description M/O
enable Upnpswitch,Thevalueof1representstheopen,and O
the0istheopposite.
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetUpnp",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description

rspCode Responsecode
3.3.21 GetWifi
 InterfaceDescription
ItisusedtogetconfigurationofGetWifi.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetWifi&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetWifi",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetWifi",
"code":0,
"initial":{
"Wifi":{
"password":"",
"ssid":""
}
},
"range":{

"Wifi":{
"password":{
"maxLen":127
},
"ssid":{
"maxLen":127
}
}
},
"value":{
"Wifi":{
"password":"***********",
"ssid":"reolink_pyc"
}
}
}
]
Fielddescription
Field description
ssid Thenameofthewirelessnetwork
password Thepasswordofthewirelessnetwork
3.3.22 SetWifi
 InterfaceDescription
ItisusedtosetconfigurationofWifi.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetWifi&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetWifi",

"param":{
"Wifi":{
"ssid":"ssid",
"password":"000000"
}
}
}
]
Fielddescription
Field Description M/O
ssid Thenameofthewirelessnetwork O
password Thepasswordofthewirelessnetwork O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetWifi",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.3.23 TestWifi
 InterfaceDescription
ItisusedtosetconfigurationofTestWifi.
 Interfacecallinstructions

RequestURL https://IPC_IP/api.cgi?cmd=TestWifi&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"TestWifi",
"param":{
"Wifi":{
"ssid":"ssid",
"password":"password"
}
}
}
]
Fielddescription
Field Description M/O
ssid Thenameofthewirelessnetwork M
password Thepasswordofthewirelessnetwork O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"TestWifi",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.3.24 ScanWifi
 InterfaceDescription
ItisusedtogetconfigurationofScanWifi.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=ScanWifi&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"ScanWifi",
"param":{}
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"ScanWifi",
"code":0,
"value":{
"Wifi":[
{
"bencrypt":1,
"signal":4,
"ssid":"HUAWEI-D1FC"
},
...//Theremaybemultiplewirelessnetworks.
]
}

}
]
Fielddescription
Field description
signal Wirelesssignalstrength
(1:signal<=-60)
(2:signal<=-50)
(3:signal<=-40)
(4:signal>-40)
ssid Thenameofwirelessnetwork
bencrypt
3.3.25 GetWifiSignal
 InterfaceDescription
It isused to get configuration ofGet Wifisignal.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=GetWifiSignal&token=TOKEN
 POSTData
Data example
[
{
"cmd":"GetWifiSignal",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription

Return data correctly
[
{
"cmd" :"GetWifiSignal",
"code" : 0,
"initial" :{
"wifiSignal" : 100
},
"range" : {
"wifiSignal" : {
"max" :255,
"min" : 0
}
},
"value" : {
"wifiSignal" : 100
}
}
]
Fielddescription
Field description
wifiSignal
3.3.26 GetPush
 InterfaceDescription
ItisusedtogetconfigurationofPush.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPush&token=TOKEN
 POSTData

Dataexample
[
{
"cmd":"GetPush",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPush",
"code":0,
"initial":{
"Push":{
"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111"
}
}
},
"range":{
"Push":{
"schedule":{
"enable":"boolean",
"table":{
"maxLen":168,
"minLen":168
}
}
}
},
"value":{

"Push":{
"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111"
}
}
}
}
]
Fielddescription
Field description
Schedule->enable Whetherpushthealarminformation
Schedule->table Thescheduleaboutwhenpushthealarminformation
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“GetPushV20”
3.3.27 SetPush
 InterfaceDescription
ItisusedtosetconfigurationofPush.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPush&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPush",
"param":{
"Push":{

"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111"
}
}
}
}
]
Fielddescription
Field Description M/O
Schedule->enab Whetherpushthealarminformation[0,1] O
le
Schedule->table Thescheduleaboutwhenpushthealarminformation O
Note:Thiscommandsupportsmodel52Xonly
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPush",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“SetPushV20”

3.3.28 GetPushV20
 InterfaceDescription
It isused to get configuration ofPush.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=GetPush&token=TOKEN
 POSTData
Data example
[
{
"cmd":"GetPushV20",
"action":1,
"param": {
"channel": 0
}
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return data correctly
[
{
"cmd" :"GetPushV20",
"code" : 0,
"initial" :{
"Push" : {
"enable" : 0,
"schedule" : {
"channel" : 0,
"table" : {
//NVR "AI_PEOPLE" :

"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
//NVR "AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111"
}
}
}
},
"range" : {
"Push" : {
"enable" : "boolean",
"schedule" : {
"channel" : 0,
"table" : {
//NVR "AI_PEOPLE" : {
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
//NVR "AI_VEHICLE" : {
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"MD" : {
"table" : {
"maxLen" : 168,
"minLen" : 168
}
}
}
}
}
},
"value" : {

"Push" : {
"enable" : 1,
"schedule" : {
"channel" : 0,
"table" : {
//NVR "AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
//NVR "AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"011111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111100"
}
}
}
}
}
]
Fielddescription
Field description
Schedule->enable Schedule switch
Schedule->table Schdeule table
3.3.29 SetPushV20
 InterfaceDescription
It isused to set configuration of Push.
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=SetPush&token=TOKEN

 POSTData
Data example
[{
"cmd": "SetPushV20",
"param": {
"Push": {
"enable": 1,
"schedule": {
"channel": 0,
"table": {
"MD":
"011111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111100"
}
}
}
}
}]
Fielddescription
Field Description M/O
Schedule->en Scheduleswitch O
able
Schedule->tab Scheduletable O
le
 Returndatadescription
Return data correctly
[
{
"cmd" :"SetEmail",
"code" : 0,
"value" : {
"rspCode" :200
}
}
]

Fielddescription
Field description
rspCode Responsecode
3.3.30 GetPushCfg
 InterfaceDescription
ItisusedtogetconfigurationofPush.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPushCfg&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetPushCfg",
"action":1
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPushCfg",
"code":0,
"initial":{
"PushCfg":{
"pushInterval":0

}
},
"range":{
"PushCfg":{
"pushInterval":[20,30,60,120]
}
},
"value":{
"PushCfg":{
"pushInterval":30
}
}
}
]
Fielddescription
Field description
initial TheinitialvalueoftheFtpfield.
range TherangeoftheFtpfield.
value TherealvalueoftheFtpfield.
pushInterval Theintervalofpush
3.3.31 SetPushCfg
 InterfaceDescription
ItisusedtosetconfigurationofPush.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPushCfg&token=TOKEN
 POSTData
Dataexample
[{

"cmd":"SetPushCfg",
"param":{
"PushCfg":{
"pushInterval":30
}
}
}]
Fielddescription
Field Description M/O
pushInterval Pushinterval. O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPushCfg",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.3.32 GetP2p
 InterfaceDescription
GettP2pinformation
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetP2p&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetP2p",
"action":1
}
]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetP2p",
"code":0,
"initial":{
"P2p":{
"enable":1
}
},

"range":{
"P2p":{
"enable":"boolean"
}
},
"value":{
"P2p":{
"enable":1,
"uid":"95270000SXIPOGIJ"
}
}
}
]
Fielddescription
Field description
enable Whetherenablep2pornot
uid IPCuid
3.3.33 SetP2p
 InterfaceDescription
SetP2P
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetP2p&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetP2p",
"param":{
"P2p":{
"enable":0
}
}

}
]
Fielddescription
Field Description M/O
enable Whetherenablep2pornot O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetP2P",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.3.34 GetCertificateInfo
 InterfaceDescription
GetCertificateInfo
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetCertificateInfo&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"GetCertificateInfo",
"action":0,

"param":{}
}]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetCertificateInfo",
"code":0,
"value":{
"CertificateInfo":{
"crtName":"",
"enable":0,
"keyName":""
}
}
}
]
Fielddescription
Field description
enable Whetherenablep2pornot
uid IPCuid
3.3.35 CertificateClear
 InterfaceDescription
ClearCertificate
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=CertificateClear&token=TOKEN

 POSTData
Dataexample
[{
"cmd":"CertificateClear",
"action":0,
"param":{}
}]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"CertificateClear",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
enable Whetherenablep2pornot
uid IPCuid
3.3.36 GetRtspUrl
 InterfaceDescription
GetRtspUrl.
 Interfacecallinstructions

RequestURL https://IPC_IP/api.cgi?cmd=GetRtspUrl&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"GetRtspUrl",
"action":0,
"param":{
"channel":1
}
}]
Fielddescription
Field Description M/O
M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetRtspUrl",
"code":0,
"value":{
"rtspUrl":{
"channel":1,
"mainStream":"rtsp://192.168.1.58:554/Preview_02_main",
"subStream":"rtsp://192.168.1.58:554/Preview_02_sub"
}
}
}
]
Fielddescription
Field description
mainStream Rtspurlofmainstream
subStream Rtspurlofsubstream

3.4 Video input
3.4.1 GetImage
 InterfaceDescription
Itisusedtogetconfigurationofimage.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetImage&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetImage",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetImage",
"code":0,
"initial":{

"Image":{
"bright":128,
"channel":0,
"contrast":128,
"hue":128,
"saturation":128,
"sharpen":128
}
},
"range":{
"Image":{
"bright":{
"max":255,
"min":0
},
"channel":0,
"contrast":{
"max":255,
"min":0
},
"hue":{
"max":255,
"min":0
},
"saturation":{
"max":255,
"min":0
},
"sharpen":{
"max":255,
"min":0
}
}
},
"value":{
"Image":{
"bright":128,
"channel":0,
"contrast":128,
"hue":128,
"saturation":128,
"sharpen":128
}
}

}
]
Fielddescription
Field description
bright Brightofvideo.
contrast Contrastofvideo.
saturation Saturationofvideo.
hue Hueofvideo.
sharpen Sharpenofvideo.
3.4.2 SetImage
 InterfaceDescription
Itisusedtosetconfigurationofimage.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetImage&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetImage",
"param":{
"Image":{
"channel":0,
"bright":150,
"contrast":150,
"saturation":150,
"hue":150,
"sharpen":150
}
}

}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M
bright Brightofvideo. M
contrast Contrastofvideo. M
saturation Saturationofvideo. M
hue Hueofvideo. M
sharpen Sharpenofvideo. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetImage",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.4.3 GetOsd
 InterfaceDescription
ItisusedtogetconfigurationofOsd.
 Interfacecallinstructions

RequestURL https://IPC_IP/api.cgi?cmd=GetOsd&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetOsd",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetOsd",
"code":0,
"initial":{
"Osd":{
"bgcolor":0,
"channel":0,
"osdChannel":{
"enable":1,
"name":"Camera1",
"pos":"LowerRight"
},
"osdTime":{
"enable":1,
"pos":"TopCenter"
},
"watermark":1
}

},
"range":{
"Osd":{
"bgcolor":"boolean",
"channel":0,
"osdChannel":{
"enable":"boolean",
"name":{
"maxLen":31
},
"pos":[
"UpperLeft",
"TopCenter",
"UpperRight",
"LowerLeft",
"BottomCenter",
"LowerRight",
"OtherConfiguration"
]
},
"osdTime":{
"enable":"boolean",
"pos":[
"UpperLeft",
"TopCenter",
"UpperRight",
"LowerLeft",
"BottomCenter",
"LowerRight",
"OtherConfiguration"
]
},
"watermark":"boolean"
}
},
"value":{
"Osd":{
"bgcolor":0,
"channel":0,
"osdChannel":{
"enable":1,
"name":"Camera1",
"pos":"LowerRight"
},

"osdTime":{
"enable":1,
"pos":"TopCenter"
},
"watermark":1
}
}
}
]
Fielddescription
Field description
osdChannel->enable Cameranamedisplayswitch.
osdChannel->name Cameraname
osdChannel->pos Cameranamedisplayposition.
osdTime->enable Cameratimedisplayswitch.
osdTime->pos Cameratimedisplayposition.
bgcolor Backgroundcolor
watermark Watermark
3.4.4 SetOsd
 InterfaceDescription
ItisusedtosetconfigurationofOsd.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetOsd&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetOsd",

"param":{
"Osd":{
"channel":0,
"osdChannel":{
"enable":1,
"name":"Camera101",
"pos":"LowerRight"
},
"osdTime":{
"enable":1,
"pos":"UpperRight"
}
}
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M
osdChannel->enable Cameranamedisplayswitch. M
osdChannel->name Cameraname M
osdChannel->pos Cameranamedisplayposition. M
osdTime->enable Cameratimedisplayswitch. M
osdTime->pos Cameratimedisplayposition. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetOsd",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription

Field description
rspCode Responsecode
3.4.5 GetIsp
 InterfaceDescription
ItisusedtogetconfigurationofIsp.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetIsp&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetIsp",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetIsp",
"code":0,
"initial":{
"Isp":{

"antiFlicker":"Off",
"backLight":"Off",
"bd_day":{
"bright":128,
"dark":128,
"mode":"Auto"
},
"bd_led_color":{
"bright":128,
"dark":128,
"mode":"Auto"
},
"bd_night":{
"bright":128,
"dark":128,
"mode":"Auto"
},
"blc":128,
"blueGain":128,
"cdsType":1,
"channel":0,
"constantFrameRate":0,
"dayNight":"Auto",
"dayNightThreshold":0,
"drc":128,
"exposure":"Auto",
"gain":{
"max":62,
"min":1
},
"mirroring":0,
"nr3d":1,
"redGain":128,
"rotation":0,
"shutter":{
"max":125,
"min":0
},
"whiteBalance":"Auto"
}
},
"range":{
"Isp":{
"antiFlicker":["Other","50HZ","60HZ","Off"],

"backLight":["Off","BackLightControl","DynamicRangeControl"],
"bd_day":{
"bright":{
"max":255,
"min":0
},
"dark":{
"max":255,
"min":0
},
"mode":["Auto","Manual"]
},
"bd_led_color":{
"bright":{
"max":255,
"min":0
},
"dark":{
"max":255,
"min":0
},
"mode":["Auto","Manual"]
},
"bd_night":{
"bright":{
"max":255,
"min":0
},
"dark":{
"max":255,
"min":0
},
"mode":["Auto","Manual"]
},
"blc":{
"max":255,
"min":0
},
"blueGain":{
"max":255,
"min":0
},
"cdsType":"boolean",
"channel":0,

"constantFrameRate":[0,1],
"dayNight":["Auto","Color","Black&White"],
"dayNightThreshold":{
"max":0,
"min":0
},
"drc":{
"max":255,
"min":0
},
"exposure":["Auto","LowNoise","Anti-Smearing","Manual"],
"gain":{
"max":100,
"min":1
},
"mirroring":"boolean",
"nr3d":"boolean",
"redGain":{
"max":255,
"min":0
},
"rotation":"boolean",
"shutter":{
"max":125,
"min":0
},
"whiteBalance":["Auto","Manual"]
}
},
"value":{
"Isp":{
"antiFlicker":"Off",
"backLight":"Off",
"bd_day":{
"bright":128,
"dark":128,
"mode":"Auto"
},
"bd_led_color":{
"bright":0,
"dark":0,
"mode":"Auto"
},
"bd_night":{

"bright":128,
"dark":128,
"mode":"Auto"
},
"blc":128,
"blueGain":128,
"cdsType":0,
"channel":0,
"constantFrameRate":1,
"dayNight":"Auto",
"dayNightThreshold":73,
"drc":128,
"exposure":"Auto",
"gain":{
"max":62,
"min":1
},
"mirroring":0,
"nr3d":1,
"redGain":128,
"rotation":0,
"shutter":{
"max":125,
"min":0
},
"whiteBalance":"Auto"
}
}
}
]
Fielddescription
Field description
antiFlicker Flickerprevention,["Outdoor","50HZ","60HZ","Off"]
exposure Exposuremode,
["Auto","LowOise","Anti-Smearing","Manual"]
gain WhenthevalueofexposureisLowOiseorManual,the
(Dependon gainfieldiseffective.
exposure)
shutter WhenthevalueofexposureisAnti-SmearingorManual,

(Dependon theshutterfieldiseffective.
exposure)
whiteBalance WhiteBalance,["Auto","Manual"]
blueGain WhenthevalueofwhiteBalanceisAnti-Smearingor
(Dependon Manual,theblueGainfieldiseffective.
whiteBalance)
redGain WhenthevalueofwhiteBalanceisAnti-Smearingor
(Dependon Manual,theredGainfieldiseffective.
whiteBalance)
dayNight Day&Night,["Auto","Color","Black&White"]
backLight Backlightcompensation,
["Off","BackLightControl","DynamicRangeControl"]
Blc WhenthevalueofbackLightisBackLightControl,theblc
(Dependon fieldiseffective.
backLight)
drc WhenthevalueofbackLightisDynamicRangeControl,the
(Dependon drcfieldiseffective.
backLight)
nr3d
mirroring Videomirroring.
rotation Videorotation.
cdsType Softlightsensitiveswitch,offwhenthehardlightsensitive
effect,canusethedayandnightswitchingthreshold
adjustment,openwhenthesoftlightsensitiveeffect,can
usethedayandnightswitchingsensitivityadjustment
constantFrameRate Fixedframerateswitch,whenon,tothevideofluency
priority,whenofftothequalityofthepicturepriority

3.4.6 SetIsp
 InterfaceDescription
ItisusedtosetconfigurationofIsp.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetIsp&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"SetIsp",
"action":0,
"param":{
"Isp":{
"antiFlicker":"Off",
"backLight":"Off",
"constantFrameRate":1,
"blc":128,
"blueGain":128,
"channel":0,
"dayNight":"Auto",
"drc":128,
"exposure":"Auto",
"cdsType":0,
"gain":{
"max":62,
"min":1
},
"mirroring":0,
"nr3d":1,
"redGain":128,
"rotation":0,
"shutter":{
"max":125,
"min":0
},
"whiteBalance":"Auto",
"bd_day":{

"iAvailable":1,
"bright":128,
"dark":128,
"mode":"Auto"
},
"bd_led_color":{
"iAvailable":0,
"bright":0,
"dark":0,
"mode":"Auto"
},
"bd_night":{
"iAvailable":1,
"bright":128,
"dark":128,
"mode":"Auto"
},
"dayNightThreshold":73
}
}
}]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M
antiFlicker Flickerprevention,["Outdoor","50HZ","60HZ", M
"Off"]
exposure Exposuremode, M
["Auto","LowOise","Anti-Smearing","Manual"]
gain WhenthevalueofexposureisLowOiseorManual, M
(Dependon thegainfieldiseffective.
exposure)
shutter WhenthevalueofexposureisAnti-Smearingor M
(Dependon Manual,theshutterfieldiseffective.
exposure)
whiteBalance WhiteBalance,["Auto","Manual"] M
blueGain WhenthevalueofwhiteBalanceisAnti-Smearingor M
(Dependon Manual,theblueGainfieldiseffective.

whiteBalance)
redGain WhenthevalueofwhiteBalanceisAnti-Smearingor M
(Dependon Manual,theredGainfieldiseffective.
whiteBalance)
dayNight Day&Night,["Auto","Color","Black&White"] M
backLight Backlightcompensation, M
["Off","BackLightControl","DynamicRangeControl"]
Blc WhenthevalueofbackLightisBackLightControl,the M
(Dependon blcfieldiseffective.
backLight)
Drc WhenthevalueofbackLightis M
(Dependon DynamicRangeControl,thedrcfieldiseffective.
backLight)
nr3d M
mirroring Videomirroring. M
rotation Videorotation. M
cdsType Softlightsensitiveswitch,offwhenthehardlight M
sensitiveeffect,canusethedayandnightswitching
thresholdadjustment,openwhenthesoftlight
sensitiveeffect,canusethedayandnightswitching
sensitivityadjustment
constantFrame Fixedframerateswitch,whenon,tothevideo M
Rate fluencypriority,whenofftothequalityofthepicture
priority
 Returndatadescription
Return datacorrectly
[
{

"cmd":"SetOsd",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.4.7 GetMask
 InterfaceDescription
ItisusedtogetconfigurationofMask.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetMask&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetMask",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber M

 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetMask",
"code":0,
"initial":{
"Mask":{
"area":[
{
"block":{
"height":0,
"width":0,
"x":0,
"y":0
},
"screen":{
"height":0,
"width":0
}
}
],
"channel":0,
"enable":0
}
},
"range":{
"Mask":{
"channel":0,
"enable":"boolean",
"maxAreas":4
}
},
"value":{
"Mask":{
"area":[
{
"block":{
"height":163,
"width":121,
"x":192,
"y":143

},
"screen":{
"height":480,
"width":640
}
}
],
"channel":0,
"enable":1
}
}
}
]
Fielddescription
Field description
enable Videomaskswitch.
Block->height Blockheight.
Block->width Blockwidth.
Block->x LeftupperXaxiscoordinates
Block->y LeftupperYaxiscoordinates
Screen->height Screenheight.
Screen->width Screenwidth.
3.4.8 SetMask
 InterfaceDescription
ItisusedtosetconfigurationofMask.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetMask&token=TOKEN
 POSTData
Dataexample
[

{
"cmd":"SetMask",
"action":0,
"param":{
"Mask":{
"channel":0,
"enable":1,
"area":[
{
"screen":{
"height":720,
"width":1280
},
"block":{
"x":110,
"y":95,
"width":36,
"height":166
}
},
{
"screen":{
"height":720,
"width":1280
},
"block":{
"x":251,
"y":100,
"width":54,
"height":175
}
},
{
"screen":{
"height":720,
"width":1280
},
"block":{
"x":425,
"y":102,
"width":23,
"height":211
}
},

{
"screen":{
"height":720,
"width":1280
},
"block":{
"x":632,
"y":88,
"width":51,
"height":245
}
}
]
}
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M
enable Videomaskswitch. M
block->height Blockheight. M
block->width Blockwidth. M
block->x LeftupperXaxiscoordinates M
block->y LeftupperYaxiscoordinates M
screen->height Screenheight. M
screen->width Screenwidth. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetMask",
"code":0,
"value":{
"rspCode":200
}

}
]
Fielddescription
Field description
rspCode Responsecode
3.4.9 GetCrop
 InterfaceDescription
ItisusedtogetconfigurationofCrop.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetCrop&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"GetCrop",
"action":0, //NVR
"param":{ //NVR
"channel":0 //NVR
}
}]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{

"cmd":"GetCrop",
"code":0,
"initial":{
"Crop":{
"cropHeight":480,
"cropWidth":640,
"mainHeight":1920,
"mainWidth":2560,
"minHeight":480,
"minWidth":640,
"topLeftX":960,
"topLeftY":720
}
},
"range":{
"Crop":{
"topLeftX":{
"max":1920,
"min":0
},
"topLeftY":{
"max":1440,
"min":0
}
}
},
"value":{
"Crop":{
"channel":0, //NVR
"cropHeight":480,
"cropWidth":640,
"mainHeight":1920,
"mainWidth":2560,
"minHeight":480,
"minWidth":640,
"topLeftX":960,
"topLeftY":720
}
}
}
]
Fielddescription

Field description
rspCode Responsecode
minHeight Minimumheightofcroparea
minWidth Minimumwidthofcroparea
mainHeight heightofMainstream
mainWidth widthofMainstream
cropHeight heightofcroparea
cropWidth widthofcroparea
topLeftY Distancebetweentheupperleftcornerofthecropareaand
theupperboundary
topLeftX Distancebetweentheupperleftcornerofthecropareaand
theleftboundary
3.4.10 SetCrop
 InterfaceDescription
ItisusedtosetconfigurationofCrop.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetCrop&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"SetCrop",
"action":0,
"param":{
"Crop":{
"channel":0, //NVR
"screenWidth":2560,
"screenHeight":1920,
"cropWidth":640,
"cropHeight":480,

"topLeftX":960,
"topLeftY":720
}
}
}]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetCrop",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
minHeight Minimumheightofcroparea
minWidth Minimumwidthofcroparea
mainHeight heightofMainstream
mainWidth widthofMainstream
cropHeight heightofcroparea
cropWidth widthofcroparea
topLeftY Distancebetweentheupperleftcornerofthecropareaand
theupperboundary
topLeftX Distancebetweentheupperleftcornerofthecropareaand

theleftboundary
3.4.11 GetStitch
 InterfaceDescription
This command is used for "stitching binocular" IPC to adjust the
stitching picture
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetStitch&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"GetStitch",
"action":1
}]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetStitch",
"code":0,
"initial":{
"stitch":{
"distance":2.0,
"stitchXMove":0,

"stitchYMove":0
}
},
"range":{
"stitch":{
"distance":{
"max":20.0,
"min":2.0
},
"stitchXMove":{
"max":100,
"min":-100
},
"stitchYMove":{
"max":-100,
"min":100
}
}
},
"value":{
"stitch":{
"distance":8.100000381469727,
"stitchXMove":5,
"stitchYMove":3
}
}
}
]
Fielddescription
Field description
distance Distancebetweenimages
stitchXMove Adjustpixelshorizontally
stitchYMove Adjustpixelsvertically
3.4.12 SetStitch
 InterfaceDescription
ItisusedtosetconfigurationofStitch.

 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetStitch&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"setStitch",
"param":{
"stitch":{
"distance":8.1,
"stitchXMove":5,
"stitchYMove":3
}
}
}]
Fielddescription
Field Description M/O
distance Distancebetweenimages M
stitchXMove Adjustpixelshorizontally M
stitchYMove Adjustpixelsvertically M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetStitch",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription

Field description
3.5 Enc
3.5.1 GetEnc
 InterfaceDescription
ItisusedtogetconfigurationofEnc.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetEnc&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetEnc",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetEnc",

"code":0,
"initial":{
"Enc":{
"audio":0,
"channel":0,
"mainStream":{
"bitRate":6144,
"frameRate":25,
"gop":2,
"height":2160,
"profile":"High",
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":256,
"frameRate":10,
"gop":4,
"height":360,
"profile":"High",
"size":"640*360",
"vType":"h264",
"width":640
}
}
},
"range":{
"Enc":[
{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[4096,5120,6144,7168,8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},

"height":2160,
"profile":["Base","Main","High"],
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
},
{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[1024,1536,2048,3072,4096,5120,6144,
7168,8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":1440,
"profile":["Base","Main","High"],
"size":"2560*1440",

"vType":"h264",
"width":2560
},
"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
},
{
"audio":"boolean",
"chnBit":1,
"mainStream":{
"bitRate":[1024,1536,2048,3072,4096,5120,6144,
7168,8192],
"default":{
"bitRate":6144,
"frameRate":25,
"gop":2
},
"frameRate":[25,22,20,18,16,15,12,10,8,6,4,2],
"gop":{
"max":4,
"min":1
},
"height":1296,
"profile":["Base","Main","High"],
"size":"2304*1296",
"vType":"h264",
"width":2304
},

"subStream":{
"bitRate":[64,128,160,192,256,384,512],
"default":{
"bitRate":256,
"frameRate":10,
"gop":4
},
"frameRate":[15,10,7,4],
"gop":{
"max":4,
"min":1
},
"height":360,
"profile":["Base","Main","High"],
"size":"640*360",
"vType":"h264",
"width":640
}
}
]
},
"value":{
"Enc":{
"audio":1,
"channel":0,
"mainStream":{
"bitRate":6144,
"frameRate":25,
"gop":2,
"height":2160,
"profile":"High",
"size":"3840*2160",
"vType":"h265",
"width":3840
},
"subStream":{
"bitRate":256,
"frameRate":10,
"gop":4,
"height":360,
"profile":"High",
"size":"640*360",
"vType":"h264",
"width":640

}
}
}
}
]
Fielddescription
Field description
audio Audioswitch.
mainStream->bitRate Bitrateofmainstream.
mainStream->frameRate FrameRateofmainstream.
mainStream->profile H.264Profile.
mainStream->size Resolution.
subStream->bitRate Bitrateofsubstream.
subStream->frameRate FrameRateofsubstream.
subStream->profile H.264Profile.
subStream->size Resolution.
mainstream->height Heightofmainstream
(Thisitemisinternaluseonly,andnoneededforcmd
“SetEnc”)
mainstream->resolution Resolutionenumerateofmainstream
(Thisitemisinternaluseonly,andnoneededforcmd
“SetEnc”)
mainstream->width Widthofmainstream
(Thisitemisinternaluseonly,andnoneededforcmd
“SetEnc”)
substeram->height Heightofsubstream
(Thisitemisinternaluseonly,andnoneededforcmd
“SetEnc”)
substeram->resolution Resolutionenumerateofsubstream
(Thisitemisinternaluseonly,andnoneededfor
cmd“SetEnc”)

substeram->width Widthofsubstream
(Thisitemisinternaluseonly,andnoneededforcmd
“SetEnc”)
3.5.2 SetEnc
 InterfaceDescription
ItisusedtosetconfigurationofEnc.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetEnc&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"SetEnc",
"action":0,
"param":{
"Enc":{
"channel":0,
"audio":1,
"mainStream":{
"size":"2560*1920",
"frameRate":20,
"bitRate":4096,
"profile":"High"
},
"subStream":{
"size":"640*480",
"frameRate":10,
"bitRate":256,
"profile":"High"
}
}
}

}]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M
audio Audioswitch. M
mainStream->bitRate Bitrateofmainstream. M
mainStream->frameRate FrameRateofmainstream. M
mainStream->profile H.264Profile. M
mainStream->size Resolution. M
subStream->bitRate Bitrateofsubstream. M
subStream->frameRate FrameRateofsubstream. M
subStream->profile H.264Profile. M
subStream->size Resolution. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetEnc",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.6 Record
3.6.1 GetRec
 InterfaceDescription
Itisusedtogetconfigurationofrecord.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetRec&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetRec",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetRec",
"code":0,
"initial":{
"Rec":{
"channel":0,

"overwrite":1,
"packTime":"30Minutes", //NVR
"postRec":"1Minute",
"preRec":1,
"schedule":{
"enable":1,
"table":
"22222222222222222222222222222222222222222222222222222222222222222
222222222222222222222222222222222222222222222222222222222222222222
2222222222222222222222222222222222222"
}
}
},
"range":{
"Rec":{
"channel":0,
"overwrite":"boolean",
"packTime":["30Minutes","45Minutes","60Minutes"],
//NVR
"postRec":["15Seconds","30Seconds","1Minute","10
Minutes"],
"preRec":"boolean",
"schedule":{
"enable":"boolean"
}
}
},
"value":{
"Rec":{
"channel":0,
"overwrite":1,
"packTime":"60Minutes", //NVR
"postRec":"1Minute",
"preRec":1,
"schedule":{
"enable":1,
"table":
"22222222222222222222222222222222222222222222222222222222222222222
222222222222222222222222222222222222222222222222222222222222222222
2222222222222222222222222222222222222"
}
}
}
}

]
Fielddescription
Field description
channel Channelnumber
overwrite Whetherthevideofilescanbeoverwritten
postRec Postrecordtime
preRec Enableprerecord
enable Enablescheduledrecording
table Astringwiththelengthof7days*24hours.Eachbyteinthis
hourindicateswhetherit’srecording.Withthevalueof0,
therecordingisoff,otherwisetherecordingison.
Note:Thiscommandsupportsmodel52Xonly
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“GetRecV20”
3.6.2 SetRec
 InterfaceDescription
Itisusedtosetconfigurationofrecord.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetRec&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"SetRec",
"param":
{

"Rec":
{
"channel":0,
"overwrite":1,
"postRec":"30Seconds",
"preRec":1,
"schedule":
{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
}
}
}
}
]
Fielddescription
Field Description M/O
channel SeealsoGetRec M
overwrite SeealsoGetRec O
postRec SeealsoGetRec O
preRec SeealsoGetRec O
enable SeealsoGetRec O
table SeealsoGetRec O
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“SetRecV20”
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetRec",
"code":0,
"value":{
"rspCode":200

}
}
]
Fielddescription
Field description
3.6.3 GetRecV20
 InterfaceDescription
Itisusedtogetconfigurationofrecord.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetRecV20&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetRecV20",
"action":1,
"param":{
"channel":0
}
}
Fielddescription
]
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{

"cmd":"GetRecV20",
"code":0,
"initial":{
"Rec":{
"enable":1,
"overwrite":1,
"packTime":"60Minutes",
"postRec":"2Minutes",
"preRec":1,
"saveDay":7,
"schedule":{
"channel":0,
"table":{
//NVR "AI_PEOPLE":
"00000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000",
//NVR "AI_VEHICLE":
"00000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000",
"MD":
"00000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000",
"TIMING":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
}
}
}
},
"range":{
"Rec":{
"enable":"boolean",
"overwrite":"boolean",
"packTime":["30Minutes","45Minutes","60
Minutes"],
"postRec":["1Minute","2Minutes","5Minutes",
"10Minutes"],
"preRec":"boolean",
"schedule":{
"channel":0,

"table":{
"AI_PEOPLE":"boolean", //NVR
"AI_VEHICLE":"boolean", //NVR
"MD":"boolean",
"TIMING":"boolean"
}
}
}
},
"value":{
"Rec":{
"enable":1,
"overwrite":1,
"packTime":"60Minutes",
"postRec":"1Minute",
"preRec":1,
"saveDay":30,
"schedule":{
"channel":0,
"table":{
//NVR "AI_PEOPLE":
"00000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000",
//NVR "AI_VEHICLE":
"00000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000",
"MD":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111",
"TIMING":
"00000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000"
}
}
}
}
}
]
Fielddescription

Field description
channel Channelnumber
overwrite Whetherthevideofilescanbeoverwritten
postRec Postrecordtime
preRec Enableprerecord
enable Enablescheduledrecording
table Astringwiththelengthof7days*24hours.Eachbyteinthis
hourindicateswhetherit’srecording.Withthevalueof0,
therecordingisoff,otherwisetherecordingison.
PackTime Packagingcycle
saveDay Customizetheretentiondaysofvideocoverage
3.6.4 SetRecV20
 InterfaceDescription
Itisusedtosetconfigurationofrecord.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetRecV20&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetRecV20",
"param":{
"Rec":{
"overwrite":1,
"postRec":"30Seconds",
"preRec":1,
"saveDay":30,

"schedule":{
"enable":1,
"channel":0,
"table":{
"MD":
"10011111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111100",
"TIMING":
"10111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
}
}
}
}
}]
Fielddescription
Field Description M/O
channel SeealsoGetRec M
overwrite SeealsoGetRec O
postRec SeealsoGetRec O
preRec SeealsoGetRec O
enable SeealsoGetRec O
table SeealsoGetRec O
saveDay SeealsoGetRec O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetRecV20",
"code":0,
"value":{
"rspCode":200
}
}

]
Fielddescription
Field description
3.6.5 Search
 InterfaceDescription
Itisusedtosearchvideofiles.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=Search&token=TOKEN
 PostData
Dataexample
[{
"cmd":"Search",
"action":0,
"param":{
"Search":{
"channel":0,
"onlyStatus":1,
"streamType":"main",
"StartTime":{
"year":2020,
"mon":12,
"day":21,
"hour":12,
"min":26,
"sec":1
},
"EndTime":{
"year":2020,

"mon":12,
"day":21,
"hour":12,
"min":34,
"sec":1
}
}
}
}]
Fielddescription
Field Description M/O
channel Channelnumber M
onlyStatus Thevalue1meansitwillonlygetthedataofdates M
insteadofrequiringthedetailsofthefiles.Thevalue0
meansitwillgetthedetailsinformationofacertain
day.
streamType Thestreamtypeoftherecordings,“main”isfor M
searchingmainstream,otherwiseisforsearchingsub
stream.
startTime Thestarttimeoftherecordings M
endTime Theendtimeoftherecordings M
Noted: Searching a big amount of files might lead to searching time
out
 Returndatadescription
Return datacorrectly
[
{
"cmd":"Search",
"code":0,
"value":{
"SearchResult":{
"Status":[
{
"mon":12,

"table":"1111000000000011110011110000000",
"year":2020
}
],
"channel":0
}
}
}
]
Fielddescription
Field description
mon Recorddate(month)
year Recorddate(year)
channel channelnumber
table Eachbyteinthestringrepresentthedaysofthemonth,
indicatingwhetherit’srecording.Withthevalueof0,the
recordingisoff,withthevalueof1,therecordingison.
Return datacorrectly (onlyStatus 为0)
[
{
"cmd":"Search",
"code":0,
"value":{
"SearchResult":{
"File":[
{
"EndTime":{
"day":21,
"hour":20,
"min":21,
"mon":12,
"sec":23,
"year":2020
},
"StartTime":{
"day":21,
"hour":12,

"min":20,
"mon":12,
"sec":57,
"year":2020
},
"frameRate":0,
"height":0,
"name":
"Mp4Record/2020-12-21/RecM01_20201221_122057_202123_6D28C08_E4B0AE.
mp4",
"size":14987438,
"type":"main",
"width":0
},
{
"EndTime":{
"day":21,
"hour":12,
"min":33,
"mon":12,
"sec":42,
"year":2020
},
"StartTime":{
"day":21,
"hour":12,
"min":33,
"mon":12,
"sec":39,
"year":2020
},
"frameRate":0,
"height":0,
"name":
"Mp4Record/2020-12-21/RecM01_20201221_123339_123342_6D28808_2D9AF5.
mp4",
"size":2988789,
"type":"main",
"width":0
},
{
"EndTime":{
"day":21,
"hour":12,

"min":38,
"mon":12,
"sec":49,
"year":2020
},
"StartTime":{
"day":21,
"hour":12,
"min":33,
"mon":12,
"sec":49,
"year":2020
},
"frameRate":0,
"height":0,
"name":
"Mp4Record/2020-12-21/RecM01_20201221_123349_123849_6D28C18_98ADFF
F.mp4",
"size":160096255,
"type":"main",
"width":0
}
],
"Status":[
{
"mon":12,
"table":"0000000000000000111110000000000",
"year":2020
}
],
"channel":0
}
}
}
]
Fielddescription
Field description
frameRate Framerate
height Theheightoftheimage
width Thewidthoftheimage

name Filename
size Filesize
type Streamtype
StartTime Thestarttimeoftherecordings
EndTime Theendtimeoftherecordings
mon Month
year Year
channel Channelnumber
table Eachbyteinthestringrepresentthedaysofthemonth,
indicatingwhetherit’srecording.Withthevalueof0,the
recordingisoff,withthevalueof1,therecordingison.
3.6.6 Download
 InterfaceDescription
Itisusedtodownloadvideofiles.
 Interfacecallinstructions
RequestURL https://192.168.1.238/cgi-bin/api.cgi?cmd=Download&sourc
e=Mp4Record/2020-12-21/RecM01_20201221_121551_1215
53_6D28808_2240A8.mp4&output=Mp4Record_2020-12-21
_RecM01_20201221_121551_121553_6D28808_2240A8.mp
4&token=TOKEN
 Requestparameterdescription


## Parameter M/O Description

source M Thenameofthesourcefile
output M Videofilesstoragename
 Returndatadescription

Return datacorrectly
Content-Type:apolication/octet-stream
Content-Length:2244776
Last-Modified:Mon,21Dec202003:15:56GMT
Connection:keep-alive
Content-Disposition:attachment;filename=Mp4Record_2020-12-21_RecM01_202
01221_121551_121553_6D28808_2240A8.mp4
ETag:"5fe0136c-2240a8"
X-Frame-Options:SAMEORIGIN
X-XSS-Protection:1;mode=block
X-Content-Type-Options:nosniff
Accept-Ranges:bytes
.............................(filecontent)
Fielddescription
Field description
filename Thenameofthevideofile
3.6.7 Snap
 InterfaceDescription
Itisusedtocaptureanimage.
 Interfacecallinstructions
RequestURL https://192.168.1.238/cgi-bin/api.cgi?cmd=Snap&channel=0
&rs=flsYJfZgM6RTB_os&token=TOKEN
 Requestparameterdescription


## Parameter M/O Description

channel M Channelnumber
rs M Randomcharacterwithfixedlength.It’susedto
preventbrowsercaching.
 Returndatadescription

Return datacorrectly
Content-Type:image/jpeg
Content-Length:171648
Connection:keep-alive
X-Frame-Options:SAMEORIGIN
X-XSS-Protection:1;mode=block
X-Content-Type-Options:nosniff
.............................(Filecontent)
Fielddescription
Field description
name Picturename
3.6.8 Playback
 InterfaceDescription
ItisusedtogetconfigurationofPlayback.
 Interfacecallinstructions
RequestURL https://192.168.1.238/cgi-bin/api.cgi?cmd=Playback&source=
Mp4Record/2020-12-22/RecM01_20201222_075939_080140
_6D28808_1A468F9.mp4&output=Mp4Record/2020-12-22/R
ecM01_20201222_075939_080140_6D28808_1A468F9.mp4
&token=TOKEN
 Requestparameterdescription


## Parameter M/O Description

source M Thenameofthesourcefile
output M Videofilesstoragename
 Returndatadescription
Return datacorrectly

Content-Type:apolication/octet-stream
Content-Length:2244776
Last-Modified:Mon,21Dec202003:15:56GMT
Connection:keep-alive
Content-Disposition:attachment;filename=Mp4Record/2020-12-22/RecM01_2020
1222_075939_080140_6D28808_1A468F9.mp4
ETag:"5fe0136c-2240a8"
X-Frame-Options:SAMEORIGIN
X-XSS-Protection:1;mode=block
X-Content-Type-Options:nosniff
Accept-Ranges:bytes
.............................(filecontent)
3.6.9 NvrDownload
 InterfaceDescription
ItisusedtoNvrDownload.
 Interfacecallinstructions
RequestURL https://NVR_IP/api.cgi?cmd=NvrDownload&token=TOKEN
 PostData
Dataexample
[{
"cmd":"NvrDownload",
"action":1,
"param":{
"NvrDownload":{
"channel":0,
"streamType":"sub",
"StartTime":{
"year":2022,
"mon":8,
"day":9,
"hour":0,
"min":1,

"sec":21
},
"EndTime":{
"year":2022,
"mon":8,
"day":9,
"hour":0,
"min":1,
"sec":41
}
}
}
}]
Fielddescription
Field Description M/O
StartTime Starttime O
EndTime Endtime O
streamType Thebitstreamtypeofthefiletodownload,mainor O
sub
 Returndatadescription
Return datacorrectly
[
{
"cmd":"NvrDownload",
"code":0,
"value":{
"fileCount":10,
"fileList":[
{
"fileName":"fragment_01_20201224101100.mp4",
"fileSize":"2122011"
},
{
"fileName":"fragment_01_20201224100925.mp4",
"fileSize":"39858411"
},
{
"fileName":"fragment_01_20201224101151.mp4",

"fileSize":"2728197"
},
{
"fileName":"fragment_01_20201224100848.mp4",
"fileSize":"14158847"
},
{
"fileName":"fragment_01_20201224100800.mp4",
"fileSize":"11221990"
},
{
"fileName":"fragment_01_20201224100834.mp4",
"fileSize":"2303298"
},
{
"fileName":"fragment_01_20201224101201.mp4",
"fileSize":"7295191"
},
{
"fileName":"fragment_01_20201224101135.mp4",
"fileSize":"2182079"
},
{
"fileName":"fragment_01_20201224101125.mp4",
"fileSize":"2222880"
},
{
"fileName":"fragment_01_20201224101222.mp4",
"fileSize":"18956748"
}
]
}
}
]
Fielddescription
Field description
Filename nameoffile
Filesize Szieoffile

3.7 PTZ
 Note:OnlyfordeviceswithPTZcapabilities
3.7.1 GetPtzPreset
 InterfaceDescription
ItisusedtogetconfigurationofPtzPreset.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPtzPreset&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetPtzPreset",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPtzPreset",
"code":0,
"initial":{

"PtzPreset":[
{
"channel":0,
"enable":1,
"id":1,
"name":"pos1"
},
{
"channel":0,
"enable":1,
"id":2,
"name":"pos1"
},
{
"channel":0,
"enable":0,
"id":3,
"name":""
},
{
"channel":0,
"enable":0,
"id":4,
"name":""
},
{
"channel":0,
"enable":0,
"id":5,
"name":""
},
{
"channel":0,
"enable":0,
"id":6,
"name":""
},
{
"channel":0,
"enable":0,
"id":7,
"name":""
},
{

"channel":0,
"enable":0,
"id":8,
"name":""
},
{
"channel":0,
"enable":0,
"id":9,
"name":""
},
{
"channel":0,
"enable":0,
"id":10,
"name":""
},
{
"channel":0,
"enable":0,
"id":11,
"name":""
},
{
"channel":0,
"enable":0,
"id":12,
"name":""
},
{
"channel":0,
"enable":0,
"id":13,
"name":""
},
{
"channel":0,
"enable":0,
"id":14,
"name":""
},
{
"channel":0,
"enable":0,

"id":15,
"name":""
},
{
"channel":0,
"enable":0,
"id":16,
"name":""
},
{
"channel":0,
"enable":0,
"id":17,
"name":""
},
{
"channel":0,
"enable":0,
"id":18,
"name":""
},
{
"channel":0,
"enable":0,
"id":19,
"name":""
},
{
"channel":0,
"enable":0,
"id":20,
"name":""
},
{
"channel":0,
"enable":0,
"id":21,
"name":""
},
{
"channel":0,
"enable":0,
"id":22,
"name":""

},
{
"channel":0,
"enable":0,
"id":23,
"name":""
},
{
"channel":0,
"enable":0,
"id":24,
"name":""
},
{
"channel":0,
"enable":0,
"id":25,
"name":""
},
{
"channel":0,
"enable":0,
"id":26,
"name":""
},
{
"channel":0,
"enable":0,
"id":27,
"name":""
},
{
"channel":0,
"enable":0,
"id":28,
"name":""
},
{
"channel":0,
"enable":0,
"id":29,
"name":""
},
{

"channel":0,
"enable":0,
"id":30,
"name":""
},
{
"channel":0,
"enable":0,
"id":31,
"name":""
},
{
"channel":0,
"enable":0,
"id":32,
"name":""
},
{
"channel":0,
"enable":0,
"id":33,
"name":""
},
{
"channel":0,
"enable":0,
"id":34,
"name":""
},
{
"channel":0,
"enable":0,
"id":35,
"name":""
},
{
"channel":0,
"enable":0,
"id":36,
"name":""
},
{
"channel":0,
"enable":0,

"id":37,
"name":""
},
{
"channel":0,
"enable":0,
"id":38,
"name":""
},
{
"channel":0,
"enable":0,
"id":39,
"name":""
},
{
"channel":0,
"enable":0,
"id":40,
"name":""
},
{
"channel":0,
"enable":0,
"id":41,
"name":""
},
{
"channel":0,
"enable":0,
"id":42,
"name":""
},
{
"channel":0,
"enable":0,
"id":43,
"name":""
},
{
"channel":0,
"enable":0,
"id":44,
"name":""

},
{
"channel":0,
"enable":0,
"id":45,
"name":""
},
{
"channel":0,
"enable":0,
"id":46,
"name":""
},
{
"channel":0,
"enable":0,
"id":47,
"name":""
},
{
"channel":0,
"enable":0,
"id":48,
"name":""
},
{
"channel":0,
"enable":0,
"id":49,
"name":""
},
{
"channel":0,
"enable":0,
"id":50,
"name":""
},
{
"channel":0,
"enable":0,
"id":51,
"name":""
},
{

"channel":0,
"enable":0,
"id":52,
"name":""
},
{
"channel":0,
"enable":0,
"id":53,
"name":""
},
{
"channel":0,
"enable":0,
"id":54,
"name":""
},
{
"channel":0,
"enable":0,
"id":55,
"name":""
},
{
"channel":0,
"enable":0,
"id":56,
"name":""
},
{
"channel":0,
"enable":0,
"id":57,
"name":""
},
{
"channel":0,
"enable":0,
"id":58,
"name":""
},
{
"channel":0,
"enable":0,

"id":59,
"name":""
},
{
"channel":0,
"enable":0,
"id":60,
"name":""
},
{
"channel":0,
"enable":0,
"id":61,
"name":""
},
{
"channel":0,
"enable":0,
"id":62,
"name":""
},
{
"channel":0,
"enable":0,
"id":63,
"name":""
},
{
"channel":0,
"enable":0,
"id":64,
"name":""
}
]
},
"range":{
"PtzPreset":{
"channel":0,
"enable":"boolean",
"id":{
"max":64,
"min":1
},
"name":{

"maxLen":31
}
}
},
"value":{
"PtzPreset":[
{
"channel":0,
"enable":1,
"id":1,
"name":"pos1"
},
{
"channel":0,
"enable":1,
"id":2,
"name":"pos1"
},
{
"channel":0,
"enable":0,
"id":3,
"name":""
},
{
"channel":0,
"enable":0,
"id":4,
"name":""
},
{
"channel":0,
"enable":0,
"id":5,
"name":""
},
{
"channel":0,
"enable":0,
"id":6,
"name":""
},
{
"channel":0,

"enable":0,
"id":7,
"name":""
},
{
"channel":0,
"enable":0,
"id":8,
"name":""
},
{
"channel":0,
"enable":0,
"id":9,
"name":""
},
{
"channel":0,
"enable":0,
"id":10,
"name":""
},
{
"channel":0,
"enable":0,
"id":11,
"name":""
},
{
"channel":0,
"enable":0,
"id":12,
"name":""
},
{
"channel":0,
"enable":0,
"id":13,
"name":""
},
{
"channel":0,
"enable":0,
"id":14,

"name":""
},
{
"channel":0,
"enable":0,
"id":15,
"name":""
},
{
"channel":0,
"enable":0,
"id":16,
"name":""
},
{
"channel":0,
"enable":0,
"id":17,
"name":""
},
{
"channel":0,
"enable":0,
"id":18,
"name":""
},
{
"channel":0,
"enable":0,
"id":19,
"name":""
},
{
"channel":0,
"enable":0,
"id":20,
"name":""
},
{
"channel":0,
"enable":0,
"id":21,
"name":""
},

{
"channel":0,
"enable":0,
"id":22,
"name":""
},
{
"channel":0,
"enable":0,
"id":23,
"name":""
},
{
"channel":0,
"enable":0,
"id":24,
"name":""
},
{
"channel":0,
"enable":0,
"id":25,
"name":""
},
{
"channel":0,
"enable":0,
"id":26,
"name":""
},
{
"channel":0,
"enable":0,
"id":27,
"name":""
},
{
"channel":0,
"enable":0,
"id":28,
"name":""
},
{
"channel":0,

"enable":0,
"id":29,
"name":""
},
{
"channel":0,
"enable":0,
"id":30,
"name":""
},
{
"channel":0,
"enable":0,
"id":31,
"name":""
},
{
"channel":0,
"enable":0,
"id":32,
"name":""
},
{
"channel":0,
"enable":0,
"id":33,
"name":""
},
{
"channel":0,
"enable":0,
"id":34,
"name":""
},
{
"channel":0,
"enable":0,
"id":35,
"name":""
},
{
"channel":0,
"enable":0,
"id":36,

"name":""
},
{
"channel":0,
"enable":0,
"id":37,
"name":""
},
{
"channel":0,
"enable":0,
"id":38,
"name":""
},
{
"channel":0,
"enable":0,
"id":39,
"name":""
},
{
"channel":0,
"enable":0,
"id":40,
"name":""
},
{
"channel":0,
"enable":0,
"id":41,
"name":""
},
{
"channel":0,
"enable":0,
"id":42,
"name":""
},
{
"channel":0,
"enable":0,
"id":43,
"name":""
},

{
"channel":0,
"enable":0,
"id":44,
"name":""
},
{
"channel":0,
"enable":0,
"id":45,
"name":""
},
{
"channel":0,
"enable":0,
"id":46,
"name":""
},
{
"channel":0,
"enable":0,
"id":47,
"name":""
},
{
"channel":0,
"enable":0,
"id":48,
"name":""
},
{
"channel":0,
"enable":0,
"id":49,
"name":""
},
{
"channel":0,
"enable":0,
"id":50,
"name":""
},
{
"channel":0,

"enable":0,
"id":51,
"name":""
},
{
"channel":0,
"enable":0,
"id":52,
"name":""
},
{
"channel":0,
"enable":0,
"id":53,
"name":""
},
{
"channel":0,
"enable":0,
"id":54,
"name":""
},
{
"channel":0,
"enable":0,
"id":55,
"name":""
},
{
"channel":0,
"enable":0,
"id":56,
"name":""
},
{
"channel":0,
"enable":0,
"id":57,
"name":""
},
{
"channel":0,
"enable":0,
"id":58,

"name":""
},
{
"channel":0,
"enable":0,
"id":59,
"name":""
},
{
"channel":0,
"enable":0,
"id":60,
"name":""
},
{
"channel":0,
"enable":0,
"id":61,
"name":""
},
{
"channel":0,
"enable":0,
"id":62,
"name":""
},
{
"channel":0,
"enable":0,
"id":63,
"name":""
},
{
"channel":0,
"enable":0,
"id":64,
"name":""
}
]
}
}
]
Fielddescription

Field description
enable Presetswitch,Thevalueof1representstheopen,andthe0
istheopposite.
id IDnumberofthePreset.
name NameofthePreset.
3.7.2 SetPtzPreset
 InterfaceDescription
ItisusedtosetconfigurationofPtzPreset.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPtzPreset&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPtzPreset",
"action":0,
"param":{
"PtzPreset":{
"channel":0,
"enable":1,
"id":1,
"name":"pos1"
}
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M

enable 1meansthatison,and0meansit’soff.Ifthatfield O
doesn’texistitmeansonlythenameofthepresetcan
berevised.
id IDnumberofpreset.Range[1~64]. M
name Nameofpreset,limit1~31characters. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPtzPreset",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.7.3 GetPtzPatrol
 InterfaceDescription
ItisusedtogetconfigurationofPtzPatrol.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPtzPatrol&token=TOKEN
 POSTData
Dataexample

[
{
"cmd":"GetPtzPatrol",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPtzPatrol",
"code":0,
"range":{
"PtzPatrol":{
"enable":"boolean",
"id":{
"max":1,
"min":1
},
"name":{
"maxLen":31
},
"preset":{
"dwellTime":{
"max":30,
"min":1
},
"id":{
"max":64,
"min":1
},
"speed":{
"max":64,
"min":1

}
},
"running":"boolean"
}
},
"value":{
"PtzPatrol":[
{
"channel":0,
"enable":1,
"id":1,
"name":"cruise1",
"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{
"dwellTime":4,
"id":2,
"speed":20
}
],
"running":0
},
{
"channel":0,
"enable":0,
"id":2,
"name":"",
"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{
"dwellTime":4,
"id":2,
"speed":20
}
],
"running":0

},
{
"channel":0,
"enable":0,
"id":3,
"name":"",
"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{
"dwellTime":4,
"id":2,
"speed":20
}
],
"running":0
},
{
"channel":0,
"enable":0,
"id":4,
"name":"",
"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{
"dwellTime":4,
"id":2,
"speed":20
}
],
"running":0
},
{
"channel":0,
"enable":0,
"id":5,
"name":"",

"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{
"dwellTime":4,
"id":2,
"speed":20
}
],
"running":0
},
{
"channel":0,
"enable":0,
"id":6,
"name":"",
"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{
"dwellTime":4,
"id":2,
"speed":20
}
],
"running":0
}
]
}
}
]
Fielddescription
Field description
enable Patrolswitch,Thevalue1meansthat’senabled,and0
meanstheopposite.

id IDnumberofthePatrol.
running Whetherrunningornot
preset->dwellTime Patroltime
Preset->id IDnumberofthepreset
preset->speed Patrolspeed
name Nameofthepatrol
3.7.4 SetPtzPatrol
 InterfaceDescription
ItisusedtosetconfigurationofPtzPatrol.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPtzPatrol&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPtzPatrol",
"action":0,
"param":{
"PtzPatrol":{
"channel":0,
"enable":1,
"id":1,
“running”:0,
“name”:”hello”
"preset":[
{
"dwellTime":3,
"id":1,
"speed":10
},
{

"dwellTime":4,
"id":2,
"speed":20
}
]
}
}
}
]
Fielddescription
Field Description M/O
channel IPCchannelnumber. M
enable Whetherenablethepresetornot M
id IDnumberofPatrol. M
Preset->dwellTime Patroltime M
Preset->id IDnumberofpreset.Range[1~64]. M
Preset->speed Patrolspeed M
Note:Supportupto16preset.
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPtzPatrol",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.7.5 PtzCtrl
 InterfaceDescription
ItisusedtocontroltheoperationofPTZ.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=PtzCtrl&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"PtzCtrl",
"param":{
"channel":0,
"op":"Auto",
"speed":32
}
},
{
"cmd":"PtzCtrl",
"param":{
"channel":0,
"op":"Stop"
}
},
{
"cmd":"PtzCtrl",
"param":{
"channel":0,
"op":"ToPos",
"id":1,
"speed":32
}
}
]
Fielddescription

Field Description M/O
channel IPCchannelnumber. M
op OperationtocontrolthePTZ. M
id PresetidnumberorPatrolidnumber. O
speed PTZrunningspeed. O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"PtzCtrl",
"code":0,
"value":{
"rspCode":200
}
},
{
"cmd":"PtzCtrl",
"code":0,
"value":{
"rspCode":200
}
},
{
"cmd":"PtzCtrl",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
Notes:
connecttotheptzcommand,someparametersareunneeded.youjustsetit"0".

thevalueofopis:
"Stop":PTZstopturning.
"Left":PTZturnleftinthespecifiedspeed.
"Right":PTZturnrightinthespecifiedspeed.
"Up":PTZturnupinthespecifiedspeed.
"Down":PTZturndowninthespecifiedspeed.
"LeftUp":PTZturnleft-upinthespecifiedspeed.
"LeftDown":PTZturnleft-downinthespecifiedspeed.
"RightUp":PTZturnright-upinthespecifiedspeed.
"RightDown":PTZturnright-downinthespecifiedspeed.
"IrisDec":Irisshrinkinthespecifiedspeed.
"IrisInc":Irisenlargeinthespecifiedspeed.
"ZoomDec":Zoomininthespecifiedspeed.
"ZoomInc":Zoomoutinthespecifiedspeed.
"FocusDec":Focusbackwardsinthespecifiedspeed.
"FocusInc":Focusforwardsinthespecifiedspeed.
"Auto":PTZturnautointhespecifiedspeed.
"StartPatrol":PTZpatrolinthespecifiedspeed.
"StopPatrol":PTZstoppatrol.
"ToPos":PTZturntoaspecifiedpresetinthespecifiedspeed.
3.7.6 GetPtzSerial
 InterfaceDescription
GetPtzSerial.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPtzSerial&token=TOKEN

 POSTData
Dataexample
[
{
"cmd":"GetPtzSerial",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPtzSerial",
"code":0,
"initial":{
"PtzSerial":{
"baudRate":1200,
"channel":0,
"ctrlAddr":0,
"ctrlProtocol":"PELCO_D",
"dataBit":"CS8",
"flowCtrl":"none",
"parity":"none",
"stopBit":1
}
},
"range":{
"PtzSerial":{
"baudRate":[1200,2400,4800,9600],
"channel":0,
"ctrlAddr":{
"max":64,

"min":1
},
"ctrlProtocol":["PELCO_D","PELCO_P"],
"dataBit":["CS8","CS7","CS6","CS5"],
"flowCtrl":["none","hard","xon","xoff"],
"parity":["none","odd","even"],
"stopBit":[1,2]
}
},
"value":{
"PtzSerial":{
"baudRate":1200,
"channel":0,
"ctrlAddr":0,
"ctrlProtocol":"PELCO_D",
"dataBit":"CS8",
"flowCtrl":"none",
"parity":"none",
"stopBit":1
}
}
}
]
Fielddescription
Field description
channel Thechannelnumber.
baudRate Thebaudrateoftheserialinptz
ctrlAddr Thecontroladdressoftheserialinptz
ctrlProtocol Thecontrolprotocoloftheserialinptz
dataBit Thedatabitoftheserialinptz
flowCtrl Theflowcontroloftheserialinptz
parity Theparityoftheserialinptz
stopBit Thestopbitoftheserialinptz

3.7.7 SetPtzSerial
 InterfaceDescription
SetPtzSerial.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPtzSerial&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPtzSerial",
"action":0,
"param":{
"PtzSerial":{
"channel":0,
"baudRate":9600,
"dataBit":"CS6",
"stopBit":2,
"parity":"odd",
"flowCtrl":"hard",
"crtlProtocol":"PELCO_P",
"ctrlAddr":2
}
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
baudRate Thebaudrateoftheserialinptz O
ctrlAddr Thecontroladdressoftheserialinptz,whichis O
defaultequaltochannelplus1
ctrlProtocol Thecontrolprotocoloftheserialinptz,whichis O

between“PELCO_D”and“PELCO_P”
dataBit Thedatabitoftheserialinptz,whichisbetween O
“CS8”,“CS7”,“CS6”and“CS5”
flowCtrl Theflowcontroloftheserialinptz,whichis O
between“none”,“hard”,“xon”and“xoff”
parity Theparityoftheserialinptz,whichisbetween O
“none”,“odd”and“even”
stopBit Thestopbitoftheserialinptz,whichcanbe1or O
2
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPtzSerial",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.7.8 GetPtzTattern
 InterfaceDescription
GetPtzTattern.
 Interfacecallinstructions

RequestURL https://IPC_IP/api.cgi?cmd=GetPtzTattern&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetPtzTattern",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPtzTattern",
"code":0,
"initial":{
"PtzTattern":{
"channel":0,
"track":[
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0

},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
}
]
}
},
"range":{
"PtzTattern":{
"track":{
"enable":"boolean",
"id":{
"max":6,
"min":1
},
"name":{
"maxLen":191
},
"running":"boolean"
}
}
},
"value":{

"PtzTattern":{
"channel":0,
"track":[
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
},
{
"enable":0,
"id":1,
"name":"",
"running":0
}
]
}
}
}
]

Fielddescription
Field description
channel Thechannelnumber.
id IDnumberofthetrack.
name Thenameofthetrack
enable Trackswitch,Thevalue1meansthat’senabled,and0means
theopposite
running Whetherrunningornot
3.7.9 SetPtzTattern
 InterfaceDescription
SetPtzTattern.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPtzTattern&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPtzTattern",
"action":0,
"param":{
"PtzTattern":{
"channel":0,
"track":[
{
"id":1,
"enable":0,
"running":0,
"name":"track1"
},

{
"id":2,
"enable":0,
"running":0,
"name":"track2"
}
]
}
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
id IDnumberofthetrack.Range[1~6] M
name Thenameofthetrack O
enable Trackswitch,Thevalue1meansthat’senabled, O
and0meanstheopposite
running Whetherrunningornot O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPtzTattern",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode

3.7.10 GetAutoFocus
 InterfaceDescription
GetAutoFocus.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAutoFocus&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetAutoFocus",
"action":1,
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetAutoFocus",
"code":0,
"initial":{
"AutoFocus":{
"channel":0,
"disable":0
}
},

"range":{
"AutoFocus":{
"disable":"boolean"
}
},
"value":{
"AutoFocus":{
"disable":0
}
}
}
]
Fielddescription
Field description
disable Forbidtheautofocusoftheptzornot
3.7.11 SetAutoFocus
 InterfaceDescription
SetAutoFocus.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAutoFocus&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetAutoFocus",
"action":0,
"param":{
"AutoFocus":{
"channel":0,
"disable":1
}

}
}
]
Fielddescription
Field Description M/O
disable Forbidtheautofocusoftheptz,1means M
forbidding,0meansenabling
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAutoFocus",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.7.12 GetZoomFocus
 InterfaceDescription
GetZoomFocus.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetZoomFocus&token=TOKEN
 POSTData
Dataexample

[{
"cmd":"GetZoomFocus",
"action":0,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetZoomFocus",
"code":0,
"value":{
"ZoomFocus":{
"channel":0,
"focus":{
"pos":23
},
"zoom":{
"pos":0
}
}
}
}
]
Fielddescription
Field description
disable Forbidtheautofocusoftheptzornot
3.7.13 StartZoomFocus
 InterfaceDescription

StartZoomFocus.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=StartZoomFocus&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"StartZoomFocus",
"action":0,
"param":{
"ZoomFocus":{
"channel":0,
"pos":6,
"op":"ZoomPos"
}
}
}]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
pos Movetotheposition
op Controlcommand O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"StartZoomFocus",
"code":0,
"value":{
"rspCode":200
}
}
]

Fielddescription
Field description
rspCode Responsecode
3.7.14 GetPtzGuard
 InterfaceDescription
GetPtzGuard.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPtzGuard&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"GetPtzGuard",
"action":0,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPtzGuard",
"code":0,
"value":{
"PtzGuard":{

"benable":1,
"bexistPos":1,
"channel":0,
"timeout":60
}
}
}
]
Fielddescription
Field description
benable whetherautomaticallyreturntoguardposition
bexistPos Whether there is a guard position
channel Devicechannelnumber
timeout Timeofautomaticallyreturntoguardposition
3.7.15 SetPtzGuard
 InterfaceDescription
SetPtzGuard.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPtzGuard&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPtzGuard",
"action":0,
"param":{
"PtzGuard":{
"channel":0,
"cmdStr":“”,
“benable”:1,
“bexistPos”:1,

“timeout”:60,
“bSaveCurrentPos”:1
}
}
}
]
Fielddescription
Field Description M/O
cmdStr setPos/toPos
setpos:setthisposasguard
M
topos:gototheguard
benable whetherautomaticallyreturntoguardposition O
timeout Timeofautomaticallyreturntoguardposition O
Canonlybe60secondnow
bsaveCurrentPos Whethersetthisposasguard O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPtzGuard",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.7.16 GetPtzCheckState
 InterfaceDescription

GetPtzCheckState.//NVR
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPtzCheckState&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"GetPtzCheckState",
"action":0,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Thechannelnumber. M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPtzCheckState",
"code":0,
"value":{
"PtzCheckState":2
}
}
]
Fielddescription
Field description
disable Forbidtheautofocusoftheptzornot
PtzCheckState 0:idle,1:doing,2:finish

3.7.17 PtzCheck
 InterfaceDescription
PtzCheck.//NVR
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=PtzCheck&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"PtzCheck",
"action":1,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"PtzCheck",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription

Field description
rspCode Responsecode
3.8 Alarm
3.8.1 GetAlarm
 InterfaceDescription
Itisusedtogetalarmsetting.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAlarm&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"GetAlarm",
"action":1,
"param":{
"Alarm":{
"type":"md",
"channel":0
}
}
}
]
Fielddescription
Field Description M/O
channel Indexofchannel M
type Alarmtype,onlysupport"md"now M
 Returndatadescription

Return datacorrectly
[
{
"cmd":"GetAlarm",
"code":0,
"initial":{
"Alarm":{
"channel":0,
"scope":{
"cols":80,
"rows":45,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
},
"sens":[
{
"beginHour":0,
"beginMin":0,
"endHour":6,
"endMin":0,
"sensitivity":9
},
{
"beginHour":6,
"beginMin":0,
"endHour":12,
"endMin":0,
"sensitivity":9
},
{
"beginHour":12,
"beginMin":0,

"endHour":18,
"endMin":0,
"sensitivity":9
},
{
"beginHour":18,
"beginMin":0,
"endHour":23,
"endMin":59,
"sensitivity":9
}
],
"type":"md"
}
},
"range":{
"Alarm":{
"channel":0,
"scope":{
"cols":{
"max":80,
"min":80
},
"rows":{
"max":45,
"min":45
},
"table":{
"maxLen":6399
}
},
"sens":[
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0

},
"endMin":{
"max":59,
"min":0
},
"id":0,
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":1,
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{

"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":2,
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":3,
"sensitivity":{
"max":50,
"min":1
}
}
],
"type":"md"
}
},
"value":{
"Alarm":{
"channel":0,
"scope":{

"cols":80,
"rows":45,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111110000000000000000111111111111111111111111111111111
111111111111111111111111111111100000000000000001111111111111111111
111111111111111111111111111111111111111111111000000000000000011111
111111111111111111111111111111111111111111111111111111111110000000
000000000111111111111111111111111111111111111111111111111111111111
111111100000000000000001111111111111111111111111111111111111111111
111111111111111111111000000000000000011111111111111111111111111111
111111111111111111111111111111111110000000000000000111111111111111
111111111111111111111111111111111111111111111111100000000000000001
111111111111111111111111111111111111111111111111111111111111111000
000000000000011111111111111111111111111111111111111111111111111111
111111111110000000000000000111111111111111111111111111111111111111
111111111111111111111111100000000000000001111111111111111111111111
111111111111111111111111111111111111111000000000000000011111111111
111111111111111111111111111111111111111111111111111110000000000000
000111111111111111111111111111111111111111111111111111111111111111
100000000000000001111111111111111111111111111111111111111111111111
111111111111111000000000000000011111111111111111111111111111111111
111111111111111111111111111110000000000000000111111111111111111111
111111111111111111111111111111111111111111100000000000000001111111
111111111111111111111111111111111111111111111111111111111000000000
000000011111111111111111111111111111111111111111111111111111111111
111110000000000000000111111111111111111111111111111111111111111111
111111111111111111100000000000000001111111111111111111111111111111
111111111111111111111111111111111000000000000000011111111111111111
111111111111111111111111111111111111111111111110000000000000000111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
},
"sens":[
{
"beginHour":2,
"beginMin":0,
"endHour":23,
"endMin":0,
"id":0,
"sensitivity":9
},
{
"beginHour":23,
"beginMin":0,
"endHour":23,
"endMin":0,
"id":1,
"sensitivity":9
},
{
"beginHour":23,
"beginMin":0,
"endHour":23,
"endMin":0,
"id":2,
"sensitivity":9
},
{
"beginHour":23,
"beginMin":0,
"endHour":23,

"endMin":59,
"id":3,
"sensitivity":9
}
],
"type":"md"
}
}
}
]
Fielddescription
Field description
channel Channelnumber
scope Motiondetectionscope,consistingof80columnsand45
rows.Appointedbycolsandrows.
cols Thenumberofcol
rows Thenumberofrow
table(scope) Astringwiththelengthof80*45,eachbyterepresentsan
area.Withthevalue1motiondetectionisactiveinthat
periodoftime.Withthevalueof0noresponsewillbemade
withanydetectedmotion.
sens Thesensitivitysettingsformotiondetection.Itisdevided
into4intervalsbytime.
beginHour Thestarthour.
beginMin Thestartminute.
endHour Theendinghour.
endMin Theendingminute.
sensitivity Sensitivity
id Sectionindex
type Alarmtype,only“md”issupported.
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“GetMdAlarm”

3.8.2 SetAlarm
 InterfaceDescription
Itisusedtosetalarmsetting.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAlarm&token=TOKEN
 PostData
Dataexample
[
{
"cmd":"SetAlarm",
"param":{
"Alarm":{
"channel":0,
"scope":{
"cols":80,
"rows":60,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111"
},
"sens":[
{
"beginHour":0,
"beginMin":0,
"endHour":6,
"endMin":0,
"sensitivity":10
},
{
"beginHour":6,
"beginMin":0,
"endHour":12,
"endMin":0,
"sensitivity":10
},
{
"beginHour":12,
"beginMin":0,
"endHour":18,
"endMin":0,
"sensitivity":10
},
{
"beginHour":18,
"beginMin":0,
"endHour":23,
"endMin":59,
"sensitivity":10
}
],
"type":"md"
}
}

}
]
Fielddescription
Field Description M/O
channel SeealsoGetAlarm M
scope SeealsoGetAlarm O
cols SeealsoGetAlarm O
rows SeealsoGetAlarm O
table SeealsoGetAlarm O
sens SeealsoGetAlarm O
beginHour SeealsoGetAlarm O
beginMin SeealsoGetAlarm O
endHour SeealsoGetAlarm O
endMin SeealsoGetAlarm O
sensitivity SeealsoGetAlarm O
id SeealsoGetAlarm O
type SeealsoGetAlarm M
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“SetMdAlarm”
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAlarm",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description

3.8.3 GetMdAlarm
 InterfaceDescription
Itisusedtogetmdalarmsetting.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetMdAlarm&token=TOKEN
 PostData
Dataexample
[{
"cmd":"GetMdAlarm",
"action":1,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetMdAlarm",
"code":0,
"initial":{
"MdAlarm":{
"channel":0,
"newSens":{
"sens":[
{

"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":0,
"priority":0,
"sensitivity":0
},
{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":1,
"priority":0,
"sensitivity":0
},
{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":2,
"priority":0,
"sensitivity":0
},
{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":3,
"priority":0,
"sensitivity":0
}
],
"sensDef":25
},
"scope":{
"cols":80,

"rows":60,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111"
},
"sens":[
{
"beginHour":0,
"beginMin":0,
"endHour":6,
"endMin":0,
"id":0,
"sensitivity":9
},
{
"beginHour":6,
"beginMin":0,

"endHour":12,
"endMin":0,
"id":1,
"sensitivity":9
},
{
"beginHour":12,
"beginMin":0,
"endHour":18,
"endMin":0,
"id":2,
"sensitivity":9
},
{
"beginHour":18,
"beginMin":0,
"endHour":23,
"endMin":59,
"id":3,
"sensitivity":9
}
],
"useNewSens":1
}
},
"range":{
"MdAlarm":{
"channel":0,
"newSens":{
"sens":[
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"enable":{
"max":1,
"min":0
},
"endHour":{

"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":0,
"priority":{
"max":0,
"min":0
},
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"enable":{
"max":1,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":1,
"priority":{
"max":0,
"min":0
},
"sensitivity":{

"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"enable":{
"max":1,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":2,
"priority":{
"max":0,
"min":0
},
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},

"enable":{
"max":1,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":3,
"priority":{
"max":0,
"min":0
},
"sensitivity":{
"max":50,
"min":1
}
}
],
"sensDef":{
"max":50,
"min":1
}
},
"scope":{
"cols":{
"max":80,
"min":80
},
"rows":{
"max":60,
"min":60
},
"table":{
"maxLen":8159
}
},
"sens":[
{
"beginHour":{

"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":0,
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":1,
"sensitivity":{
"max":50,
"min":1
}
},

{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":2,
"sensitivity":{
"max":50,
"min":1
}
},
{
"beginHour":{
"max":23,
"min":0
},
"beginMin":{
"max":59,
"min":0
},
"endHour":{
"max":23,
"min":0
},
"endMin":{
"max":59,
"min":0
},
"id":3,
"sensitivity":{
"max":50,
"min":1

}
}
],
"useNewSens":{
"max":1,
"min":0
}
}
},
"value":{
"MdAlarm":{
"channel":0,
"newSens":{
"sens":[
{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":0,
"priority":0,
"sensitivity":0
},
{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":1,
"priority":0,
"sensitivity":0
},
{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":2,
"priority":0,
"sensitivity":0
},

{
"beginHour":0,
"beginMin":0,
"enable":0,
"endHour":0,
"endMin":0,
"id":3,
"priority":0,
"sensitivity":0
}
],
"sensDef":25
},
"scope":{
"cols":80,
"rows":60,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111"
},
"sens":[
{
"beginHour":0,
"beginMin":0,
"endHour":6,
"endMin":0,
"id":0,
"sensitivity":9
},
{
"beginHour":6,
"beginMin":0,
"endHour":12,
"endMin":0,
"id":1,
"sensitivity":9
},
{
"beginHour":12,
"beginMin":0,
"endHour":18,
"endMin":0,
"id":2,
"sensitivity":9
},
{
"beginHour":18,
"beginMin":0,
"endHour":23,
"endMin":59,
"id":3,
"sensitivity":9
}
],
"useNewSens":1 //NVR
}
}
}
]
Fielddescription

Field description
channel Channelnumber
scope Motiondetectionscope,consistingof80columnsand45
rows.Appointedbycolsandrows.
cols Thenumberofcol
rows Thenumberofrow
table(scope) Astringwiththelengthof80*45,eachbyterepresentsan
area.Withthevalue1motiondetectionisactiveinthat
periodoftime.Withthevalueof0noresponsewillbemade
withanydetectedmotion.
sens Thesensitivitysettingsformotiondetection.Itisdevided
into4intervalsbytime.
beginHour Thestarthour.
beginMin Thestartminute.
endHour Theendinghour.
endMin Theendingminute.
sensitivity Sensitivity
id Sectionindex
type Alarmtype,only“md”issupported.
priority Priorityofalarmtype
sensDef Thesensitiveityvalue
useNewSens
3.8.4 SetMdAlarm
 InterfaceDescription
Itisusedtosetalarmsetting.

 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetMdAlarm&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetMdAlarm",
"param":{
"MdAlarm":{
"channel":0,
"scope":{
"cols":120,
"rows":67,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111"
},
"useNewSens":1,
"newSens":{
"sensDef":10,
"sens":{
"sensitivity":10,
"beginHour":0,
"beginMin":0,
"endHour":6,
"endMin":0,
"priority":0,
"enable":0
}
}
}
}
}]
Fielddescription
Field Description M/O
channel SeealsoGetAlarm M
scope SeealsoGetAlarm O
cols SeealsoGetAlarm O
rows SeealsoGetAlarm O
table SeealsoGetAlarm O
sens SeealsoGetAlarm O
beginHour SeealsoGetAlarm O
beginMin SeealsoGetAlarm O
endHour SeealsoGetAlarm O
endMin SeealsoGetAlarm O
sensitivity SeealsoGetAlarm O

id SeealsoGetAlarm O
type SeealsoGetAlarm M
priority SeealsoGetAlarm
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetMdAlarm",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.8.5 GetMdState
 InterfaceDescription
ItisusedtogetstateofMD.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetMdState&token=TOKEN
 POSTData
Dataexample
[
{

"cmd":"GetMdState",
"param":{
"channel":0
}
}
]
Fielddescription
Field Description M/O
chnnel Chnnelnum (ipcis0) O
Note: usethisurlnoneedtopostjsondate
“https://IPC_IP/api.cgi?cmd=GetMdState&channel=0&token=TOKEN”
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetMdState",
"code":0,
"value":{
"state":0
}
}
]
Fielddescription
Field description
state Thestateofmotiondetection.Thevalue1meansmotions
havebeendetectedand0meansnomotionhasbeen
detected.
3.8.6 GetAudioAlarm
 InterfaceDescription
GetAudioAlarm.

 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAudioAlarm&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetAudioAlarm",
"action":1,
"param":{}
}
]
Fielddescription
Field Description M/O
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“GetAudioAlarmV20”
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetAudioAlarm",
"code":0,
"initial":{
"Audio":{
"schedule":{
"enable":0,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
}
}

},
"range":{
"Audio":{
"schedule":{
"enable":"boolean",
"table":{
"maxLen":168,
"minLen":168
}
}
}
},
"value":{
"Audio":{
"schedule":{
"enable":0,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111"
}
}
}
}
]
Fielddescription
Field description
table SeealsoGetAlarm
3.8.7 SetAudioAlarm
 InterfaceDescription
SetAudioAlarm.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAudioAlarm&token=TOKEN

 PostData
Dataexample
[
{
"cmd":"SetAudioAlarm",
"param":{
"Audio":{
"schedule":{
"enable":1,
"table":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111"
}
}
}
}
]
Fielddescription
Field Description M/O
enable SeealsoGetAlarm O
table SeealsoGetAlarm O
Note:
WhenscheduleVersionver=1inthecapabilityset,usecmd“SetAudioAlarmV20”
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAlarm",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription

Field description
3.8.8 GetAudioAlarmV20
 InterfaceDescription
It isused to get configuration ofAudioAlarm
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=GetAudioAlarmV20&token=TOKE
N
 POSTData
Data example
[
{
"cmd":"GetAudioAlarmV20",
"action":1,
"param": {
"channel": 0
}
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return data correctly
[
{
"cmd" :"GetAudioAlarmV20",

"code" : 0,
"initial" :{
"Audio": {
"enable" : 0,
"schedule" : {
"channel" : 15,
"table" : {
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111"
}
}
}
},
"range" : {
"Audio": {
"enable" : "boolean",
"schedule" : {
"channel" : 15,
"table" : {
"AI_PEOPLE" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"AI_VEHICLE" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"MD" : {
"table" : {
"maxLen" : 168,

"minLen" : 168
}
}
}
}
}
},
"value" : {
"Audio": {
"enable" : 0,
"schedule" : {
"channel" : 15,
"table" : {
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111"
}
}
}
}
}
]
Fielddescription
Field description
table Audio alarm switch
channel Index ofchannel

3.8.9 SetAudioAlarmV20
 InterfaceDescription
It isused to set configuration of audio alarm
 Interfacecallinstructions
Request URL https://IPC_IP/api.cgi?cmd=
SetAudioAlarmV20&token=TOKEN
 POSTData
Data example
[{
"cmd": "SetAudioAlarmV20",
"param": {
"Audio": {
"enable": 1,
"schedule": {
"channel": 0,
"table": {
"MD":
"011111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111100"
}
}
}
}
}]
Fielddescription
Field Description M/O
Schedule->en Scheduleswitch O

able
Schedule->tab Scheduletable O
le
 Returndatadescription
Return data correctly
[
{
"cmd" :"SetAudioAlarmV20",
"code" : 0,
"value" : {
"rspCode" :200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.8.10 GetBuzzerAlarmV20
 InterfaceDescription
It isused to get configuration ofBuzzerAlarm
 Interfacecallinstructions
Request URL https://NVR_IP/api.cgi?cmd=GetBuzzerAlarmV20&token=TO
KEN
 POSTData
Data example
[

{
"cmd":"GetBuzzerAlarmV20",
"action":1,
"param": {
"channel": 0
}
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return data correctly
[
{
"cmd" :"GetBuzzerAlarmV20",
"code" : 0,
"initial" :{
"Buzzer" :{
"diskErrorAlert" :0,
"diskFullAlert" :0,
"enable" : 0,
"ipConflictAlert": 0,
"nvrDisconnectAlert" : 0,
"schedule" : {
"channel" : 0,
"table" : {
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111

11111111111111111111111111111111111",
"VL" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000"
}
}
}
},
"range" : {
"Buzzer" :{
"diskErrorAlert" :"boolean",
"diskFullAlert" :"boolean",
"enable" : "boolean",
"ipConflictAlert": "boolean",
"nvrDisconnectAlert" : "boolean",
"schedule" : {
"channel" : 0,
"table" : {
"AI_PEOPLE" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"AI_VEHICLE" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"MD" : {
"table" : {
"maxLen" : 168,
"minLen" : 168
}
},
"VL" :{
"table" : {
"maxLen" : 168,
"minLen" : 168
}
}
}

}
}
},
"value" : {
"Buzzer" :{
"diskErrorAlert" :0,
"diskFullAlert" :0,
"enable" : 0,
"ipConflictAlert": 0,
"nvrDisconnectAlert" : 0,
"schedule" : {
"channel" : 0,
"table" : {
"AI_PEOPLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"AI_VEHICLE" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000",
"MD" :
"011111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111100",
"VL" :
"000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000"
}
}
}
}
}
]
Fielddescription
Field description
diskErrorAlert Disk error Alert
diskFullAlert Disk full Alert
enable Buzzerswitch

ipconflictAlert Ipc conflict Alert
channel Index ofchannel
table Schedule table
nvrDisconnectAlert Nvr Disconnect Alert
3.8.11 SetBuzzerAlarmV20
 InterfaceDescription
It isused to set configuration of Buzzeralarm
 Interfacecallinstructions
Request URL https://NVR_IP/api.cgi?cmd=
SetBuzzerAlarmV20&token=TOKEN
 POSTData
Data example
[{
"cmd": "SetBuzzerAlarmV20",
"param": {
"Buzzer": {
"enable": 0,
"schedule": {
"channel": 0,
"table": {
"MD":
"011111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111100",
"TIMING":
"000111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111111"
}
}
}
}

}]
Fielddescription
Field Description M/O
Schedule->en Buzzerswitch O
able
Schedule->tab Scheduletable O
le
 Returndatadescription
Return data correctly
[
{
"cmd" :"SetBuzzerAlarmV20",
"code" : 0,
"value" : {
"rspCode" :200
}
}
]
Fielddescription
Field description
rspCode Responsecode
3.8.12 AudioAlarmPlay
 InterfaceDescription
Itisusedtoplayaudioalarm
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=AudioAlarmPlay&token=TOKEN
 PostData

Dataexample
[{
"cmd":"AudioAlarmPlay",
"action":0,
"param":{
"alarm_mode":"times",
"manual_switch":0,
"times":2,
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
manual_switch Switchofmanual O
times TimesofAudioalarm O
alarm_mode Alarmmode:“times”/”manu” O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"AudioAlarmPlay",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description

3.10 LED
3.10.1 GetIrLights
 InterfaceDescription
ItisusedtogetIrlightsinformationofdevice.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetIrLights&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetIrLights"
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetIrLights",
"code":0,
"value":{
"IrLights":{
"state":0
}
},
"initial":{

"IrLights":{
"state":0
}
},
"range":{
"IrLights":{
"state":{
"Auto"
"Off"
"On"
}
}
}
}
]
Fielddescription
Field description
state Thestateofirlight
3.10.2 SetIrLights
 InterfaceDescription
ItisusedtosetconfigurationofIrLights.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetIrLights&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetIrLights",
"action":0,
"param":{
"IrLights":{
"channel":0,
"state":"Auto"
}

}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetIrLights",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.10.3 GetPowerLed
 InterfaceDescription
Itisusedtogetpowerledinformationofdevice.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetPowerLed&token=TOKEN
 POSTData

Dataexample
[
{
"cmd":"GetPowerLed"
}
]
Fielddescription
Field Description M/O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetPowerLed",
"code":0,
"value":{
"PowerLed":{
"channel":0,
"state":0
}
},
"range":{
"PowerLed":{
"state":{
"On"
"Off"
}
}
}
}
]
Fielddescription
Field description
state Stateofpowerled

3.10.4 SetPowerLed
 InterfaceDescription
Itisusedtosetpowerledinformationofdevice.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetPowerLed&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"SetPowerLed",
"param":{
"PowerLed":{
"state":"Off",
"channel":0
}
}
}
]
Fielddescription
Field Description M/O
state Stateofpowerled
Note:Onlyfordeviceswithpowerled
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetPowerLed",
"code":0,
"value":{
"rspCode":200
}

}
]
Fielddescription
Field description
rspCode Responsecode
3.10.5 GetWhiteLed
 InterfaceDescription
Itisusedtogetconfigurationofwhiteled.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetWhiteLed&token=TOKEN
 PostData
Dataexample
[{
"cmd":"GetWhiteLed",
"action":0,
"param":{
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{

"cmd":"GetWhiteLed",
"code":0,
"initial":{
"WhiteLed":{
"wlAiDetectType":{
"dog_cat":0,
"face":0,
"people":0,
"vehicle":0
}
}
},
"range":{
"AiDetectType":{
"dog_cat":"boolean",
"face":"boolean",
"people":"boolean",
"vehicle":"boolean"
},
"WhiteLed":{
"bright":{
"max":100,
"min":0
}
}
},
"value":{
"WhiteLed":{
"LightingSchedule":{
"EndHour":6,
"EndMin":0,
"StartHour":18,
"StartMin":0
},
"bright":79,
"channel":0,
"mode":1,
"state":0,
"wlAiDetectType":{
"dog_cat":1,
"face":0,
"people":1,
"vehicle":0
}

}
}
}
]
Fielddescription
Field description
channel Channelnumber
state Whiteledstate
auto Whiteledautomode
bright Currentbrightness
mode Brightnessstate
3.10.6 SetWhiteLed
 InterfaceDescription
Itisusedtosetconfigurationofwhiteled.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetWhiteLed&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetWhiteLed",
"param":{
"WhiteLed":{
"state":0,
"channel":0,
"mode":1,
"bright":79,

"LightingSchedule":{
"EndHour":6,
"EndMin":0,
"StartHour":18,
"StartMin":0
},
"wlAiDetectType":{
"dog_cat":1,
"face":0,
"people":1,
"vehicle":0
}
}
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
state Whiteledstate0/1 O
0:Off
1:On
mode Brightnessstate0/1/2 O
0:it`salwayslightatnight
1:alarmtriggermode
2:lightonforspecificperiods
bright Currentbrightness1-100 O
wlAiDetectTyp Theaidetecttypeofwhiteled O
e
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetWhiteLed",
"code":0,
"value":{

"rspCode":200
}
}
]
Fielddescription
Field description
3.10.7 GetAiAlarm
 InterfaceDescription
Itisusedtogetconfigurationofaialarm
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAiAlarm&token=TOKEN
 PostData
Dataexample
[{
"cmd":"GetAiAlarm",
"action":0,
"param":{
"channel":0,
"ai_type":"people"
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
ai_type Aitype O
 Returndatadescription

Return datacorrectly
[
{
"cmd":"GetAiAlarm",
"code":0,
"value":{
"ai_detect_type":"people",
"height":60,
"max_target_height":0.0,
"max_target_width":0.0,
"min_target_height":0.0,
"min_target_width":0.0,
"scope":{
"area":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111"
},

"sensitivity":10,
"stay_time":0,
"width":80
}
}
]
Fielddescription
Field description
3.10.8 SetAiAlarm
 InterfaceDescription
Itisusedtosetconfigurationofaialarm
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAiAlarm&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetAiAlarm",
"param":{
"channel":0,
"AiAlarm":{
"ai_type":"people",
"sensitivity":10,
"stay_time":0,
"width":80,
"height":60,
"scope":{
"area":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111"
},
"min_target_height":0.0,
"max_target_height":1.0,
"min_target_width":0.0,
"max_target_width":1.0
}
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
ai_type Aitype O
sensitivity Sensitivityofaialarm O

stay_time Staytime O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAiAlarm",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.10.9 SetAlarmArea
 InterfaceDescription
Itisusedtosetalarmarea.
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAlarmArea&token=TOKEN
 PostData
Dataexample
[{
"cmd":"SetAlarmArea",
"param":{
"channel":0,
"ai_type":"people",

"width":80,
"height":60,
"area":
"11111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111

111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111111111111111
1111111111111111111111111111111111111111111111111"
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
ai_type Typeofaialarm O
width Widthofalarmarea O

height Heightofalarmarea O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAlarmArea",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.11 AI
3.11.1 GetAiCfg
 InterfaceDescription
Itisusedtogetconfigurationofai
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAiCfg&token=TOKEN
 PostData
Dataexample
[{
"cmd":"GetAiCfg",
"action":0,
"param":{

"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetAiCfg",
"code":0,
"value":{
"AiDetectType":{
"dog_cat":1,
"face":0,
"people":1,
"vehicle":1
},
"aiTrack":0,
"channel":0,
"trackType":{
"dog_cat":0,
"face":0,
"people":1,
"vehicle":0
}
}
}
]
Fielddescription
Field description

3.11.2 SetAiCfg
 InterfaceDescription
Itisusedtosetaidetecttypeandaitracktype
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=SetAiCfg&token=TOKEN
 POSTData
Dataexample
[{
"cmd":"SetAiCfg",
"action":0,
"param":{
"aiTrack":0,
"trackType":{},
"AiDetectType":{
"people":1,
"vehicle":1,
"dog_cat":1,
"face":0
},
"channel":0
}
}]
Fielddescription
Field Description M/O
channel Indexofchannel M
aiTrack SwitchtoaiTrack O
trackType Aitracktype O
AiDetectType Aidetecttype O
people Peopledetection O
vehicle Vehicledetection O
Dog_cat Dogandcatdetection O

face Facedetection O
 Returndatadescription
Return datacorrectly
[
{
"cmd":"SetAiCfg",
"code":0,
"value":{
"rspCode":200
}
}
]
Fielddescription
Field description
3.11.3 GetAiState
 InterfaceDescription
Itisusedtogetaialarmstate
 Interfacecallinstructions
RequestURL https://IPC_IP/api.cgi?cmd=GetAiState&token=TOKEN
 POSTData
Dataexample
[
{
"cmd":"GetAiState",
"param":{

"channel":0
}
}
]
Fielddescription
Field Description M/O
channel Indexofchannel M
 Returndatadescription
Return datacorrectly
[
{
"cmd":"GetAiState",
"code":0,
"value":{
"channel":0,
"dog_cat":{
"alarm_state":0,
"support":1
},
"face":{
"alarm_state":0,
"support":0
},
"people":{
"alarm_state":0,
"support":1
},
"vehicle":{
"alarm_state":0,
"support":1
}
}
}
]
Fielddescription
Field description

alarm_state Alarmstate
support Whethersupportornot
4. Response
4.1 Error


## Error Response

[
{
"cmd":string,
"code":0,
"error":{
"rspCode":int,
"detail":string
}
}
]
rspCode Details Description
-1 notexist Missingparameters
-2 outofmem Usedupmemory
-3 checkerr Checkerror
-4 paramerror Parameterserror
-5 maxsession Reached the max session
number.
-6 pleaseloginfirst Loginrequired
-7 loginfailed Loginerror
-8 timeout Operationtimeout
-9 notsupport Notsupported
-10 protocol Protocolerror
-11 fcgireadfailed Failedtoreadoperation
-12 getconfigfailed Failedtogetconfiguration.

-13 setconfigfailed Failedtosetconfiguration.
-14 mallocfailed Failedtoapplyformemory
-15 createsocketfailed Failedtocreatedsocket
-16 sendfailed Failedtosenddata
-17 rcvfailed Failedtoreceiverdata
-18 openfilefailed Failedtoopenfile
-19 readfilefailed Failedtoreadfile
-20 writefilefailed Failedtowritefile
-21 errortoken Tokenerror
-22 The length of the string exceeds the The length of the string
limit exceedsthelimitmation
-23 missingparam Missingparameters
-24 errorcommand Commanderror
-25 internalerror Internalerror
-26 abilityerror Abilityerror
-27 invaliduser Invaliduser
-28 useralreadyexist Useralreadyexist
-29 maximumnumberofusers Reached the maximum
numberofusers
-30 sameversion Theversionisidenticaltothe
currentone.
-31 busy Ensure only one user can
upgrade
-32 ipconflict Modify IP conflicted with
usedIP
-34 needbingemail Cloud login need bind email
first
-35 unbind Cloudloginunbindcamera
-36 networktimeout Cloud login get login
informationoutoftime

-37 passworderr Cloudloginpassworderror
-38 uiderr Cloudbindcamerauiderror
-39 usernotexist Cloudloginuserdoesn’texist
-40 unbindfailed Cloudunbindcamerafailed
-41 cloudnotsupport The device doesn’t support
cloud
-42 logincloudserverfailed Cloudloginserverfailed
-43 bindfailed Cloudbindcamerafailed
-44 cloudunknownerr Cloudunknownerror
-45 needverifycode Cloudbindcameraneed
verifycode
Anerroroccurredwhile
-46 Digestauthenticationfailed
usingthedigest


## authenticationprocess

DigestauthenticationNonceexpires AbstractAnexpirednonceis
-47
usedintheauthentication
process
-48 Fetchingapicturefailed Snapapicturefailed
-49 Channelinvalid Channelisinvalid
-99 Deviceoffline Deviceoffline
-100 testfailed TestEmail、Ftp、Wififailed
-101 checkfirmwarefailed Upgrade checking firmware
failed
-102 downloadonlinefailed Upgrade download online
failed
-103 getupgradestatusfailed Upgrade get upgrade status
failed
-105 Frequent logins, please try again Frequentlogins
later!
-220 Errordownloadingvideofile Errordownloadingvideofile
-221 Busyvideorecordingtask Busyvideorecordingtask
-222 Thevideofiledoesnotexist Thevideofiledoesnotexist

-301 DigestAuthenticationnonceerror Digest Authentication nonce


## error

-310 Aesdecryptionfailure Aesdecryptionfailure
-451 ftploginfailed ftptestloginfailed
-452 ftpcreatedirfailed Creatftpdirfailed
-453 ftpuploadfailed Uploadftpfilefailed
-454 ftpconnectfailed Cannotconnectftpserver
-480 emailundefinedfailed Someundifinederrors
-481 emailconnectfailed Cannotconnectemailserver
-482 emailauthfailed Authuserfailed
-483 emailnetworkerr Emailnetworkerr
-484 emailservererr Something wrong with email
server
-485 emailmemoryerr Somethingwrongwith
memory
-500 The number of IP addresses reaches ThenumberofIPaddresses
theupperlimit reachestheupperlimit
-501 Theuserdoesnotexist Theuserdoesnotexist
-502 Password err Passworderr
-503 Logindeny Logindeny
-505 Loginnotinit Loginnotinit
-506 Loginlocked Loginlocked
-507 Loginreachmax Thenumberoflogins
reachedtheupperlimit
Note:Field"details"meansmoredetailederrorinformation.



## Extracted Tables

### Table from Page 3

| RevisionHistory   | Description                             | Data       |
|:------------------|:----------------------------------------|:-----------|
| Version1.0        | Initialversion                          | 2016-06-01 |
| Revision1         |                                         |            |
| Version1.1        | 1. Addtheinterfaceofshortconnection     | 2016-11-07 |
| Revision2         | accessingCGI.                           |            |
|                   | 2. AddrtmpportparametertoGetNetPortand  |            |
|                   | SetNetPortinterfaces.                   |            |
|                   | 3. AddhourFmtparametertoGetTimeand      |            |
|                   | SetTimeinterfaces.                      |            |
|                   | 4. AddstreamTypeandintervalparametersto |            |
|                   | GetFtpandSetFtpinterfaces.              |            |
|                   | 5. AddscheduleparametertoGetEmailand    |            |
|                   | SetEmailinterfaces.                     |            |
|                   | 6. AddGetPushandSetPushinterfaces.      |            |
|                   | 7. Removeenable,actionandschedule       |            |
|                   | parameterstoGetAlarmandSetAlarm         |            |
|                   | interfaces.                             |            |
|                   | 8. AddemailSchedule,pushScheduleand     |            |
|                   | hourFmttoGetAbilityinterface.           |            |
| Version1.2        | 1. AddUpgradePrepare                    | 2019-4-26  |
| Revision3         | 2. AddShutdown                          |            |
|                   | 3. AddGetAuthandSetAuth                 |            |
|                   | 4. AddGetcloudandSetcloud               |            |
|                   | 5. Get3GandSet3G                        |            |
|                   | 6. GetP2pandSetP2p                      |            |
|                   | 7. AddPreview                           |            |
|                   | 8. Addrtmp=startandrtmp=stopand         |            |
|                   | rtmp=authforrtmp                        |            |
|                   | 9. PtzaddGetPtzSerialSetPtzSerial       |            |

### Table from Page 4

|            | GetPtzTatternSetPtzTatterncommand       |            |
|            | 10.CameraincreasesGetAutoFocus          |            |
|            | SetAutoFocuscommandoffocus              |            |
|            | 11.LEDincreasesGetIrLightsSetIrLights   |            |
|            | GetPowerLedSetPowerLedcommand           |            |
|            | 12.AddGetAudioAlarmSetAudioAlarm        |            |
|            | 13.AddHeartBeat                         |            |
|            | 14.AddGetCropSetCrop                    |            |
|            | 15.AddGetAutoUpgradeSetAutoUpgrade      |            |
|            | CheckFirmwareUpgradeOnline              |            |
|            | UpgradeStatusinsystemmode               |            |
|:-----------|:----------------------------------------|:-----------|
| Version1.3 | 1.PtzaddGetPtzSerialSetPtzSerial        | 2019-9-30  |
| Revision4  | GetPtzTatternSetPtzTatterncommand       |            |
|            | 2.SystemdeleteImportCfg                 |            |
|            | 3.SecuritydeleteGetAuthSetAuth          |            |
|            | 4.AlarmaddSetAudioAlarm                 |            |
|            | 5.Completetheresponsedcode              |            |
| Version1.4 | 1. MergeCGIcommandsforNVRandIPC         | 2021-01-05 |
| Revision5  |                                         |            |
| Version1.5 | 1. AIaddsGetAiCfgSetAiCfgGetAiState     | 2021-12-03 |
| Revison6   | 2. PtzaddsGetZoomFocusStartZoomFocus    |            |
|            | GetPtzGuardSetPtzGuardGetPtzCheckState  |            |
|            | PtzCheck                                |            |
|            | 3. AlarmaddsAudioAlarmPlay              |            |
|            | 4. LEDupdatesGetWhiteLedSetWilteLed     |            |
|            | 5. SystemupdatesGetAbility              |            |
|            | 6. NetworkupdatesGetFtpV20SetFtpV20     |            |
|            | TestFtpGetNetPortSetNetPort             |            |
|            | 7. NetworkaddsGetCertificateInfo        |            |
|            | CertificateClearGetRtspUrl              |            |

### Table from Page 5

|            | 8. videoinputupdatesSetIspGetIsp             |          |
|            | 9. EncupdatesGetEnc                          |          |
|            | 10. ResponseupdatesError                     |          |
|:-----------|:---------------------------------------------|:---------|
| Version1.6 | 1.Improvethedescriptionoftheexample          | 2022-9-6 |
| Revison7   | 2.Addthedescriptionofvideopreview            |          |
|            | 3.Deletetheabandonedcommand(rtmp             |          |
|            | start/rtmpstop/rtmpauth)                     |          |
|            | 4.Addtheversionfieldtothelogincommand        |          |
|            | 5.AddGetSysCfg/SetSysCfg/GetStitch/SetStitch |          |
|            | commands                                     |          |
|            | 6.ISPaddsmulti-levelframedropandsoftlight    |          |
|            | sensitivity                                  |          |
|            | 7.NVRcutanddownloadvideofileoptional         |          |
|            | streamtype                                   |          |
|            | 8.Increasetheptzguardparameter               |          |
|            | 9.Increasethewhitelightsettingparameters     |          |
|            | 10.Adddescriptionforftpcommand               |          |
|            | 11.Improvethecapabilityset                   |          |
|            | 12.Improvetheerrorcode                       |          |
| Version1.7 | AddPrivacyProtectionNoticeandDisclaimer      |          |
| Revison8   |                                              |          |

### Table from Page 33

| Dataexample         | None                                          | None   |
|:--------------------|:----------------------------------------------|:-------|
| [                   |                                               |        |
| {                   |                                               |        |
| "cmd":"GetAbility", |                                               |        |
| "param":{           |                                               |        |
| "User":{            |                                               |        |
| "userName":"admin"  |                                               |        |
| }                   |                                               |        |
| }                   |                                               |        |
| }                   |                                               |        |
| ]                   |                                               |        |
| Fielddescription    |                                               |        |
| Field               | Description                                   | M/O    |
| userName            | Username,itshouldbeconsistedoflessthan32      | M      |
|                     | characters,iftheusernameisNULL,thenitwouldget |        |
|                     | currentuserability.                           |        |

### Table from Page 34

| Eachdomainiscorrespondingtoafunctionalmodule.Thepermitfieldmarks             |
| accessright,validatinginleastsignificantthreebits:themostsignificantbit      |
| indicatesexecutionpermission,thefirstbitindicatesrevisionpermission,andthe   |
| secondbitindicatesread/writepermission.Theverfieldindicatestheversion        |
| number.0meansthefeatureisnotsupportedinthatversion,nonzeromeansthe           |
| featureissupported.Differentversionnumbersindicatethosecertainfunctional     |
| modulessupportdifferentfunctionaloptions.                                    |
|:-----------------------------------------------------------------------------|
| [{                                                                           |
| "cmd":"GetAbility",                                                          |
| "code":0,                                                                    |
| "value":{                                                                    |
| "Ability":{                                                                  |
| "3g":{                                                                       |
| "permit":0,                                                                  |
| "ver":0                                                                      |
| },                                                                           |
| "abilityChn":[{                                                              |
| "aiTrack":{                                                                  |
| "permit":0,                                                                  |
| "ver":0                                                                      |
| },                                                                           |
| "aiTrackDogCat":{                                                            |
| "permit":0,                                                                  |
| "ver":0                                                                      |
| },                                                                           |
| "alarmAudio":{                                                               |
| "permit":6,                                                                  |
| "ver":1                                                                      |
| },                                                                           |
| "alarmIoIn":{                                                                |
| "permit":0,                                                                  |
| "ver":0                                                                      |
| },                                                                           |
| "alarmIoOut":{                                                               |
| "permit":0,                                                                  |
| "ver":0                                                                      |
| },                                                                           |
| "alarmMd":{                                                                  |
| "permit":6,                                                                  |
| "ver":1                                                                      |
| },                                                                           |

### Table from Page 50

| }                         | None                        | None     |
| }                         |                             |          |
| }                         |                             |          |
| }]                        |                             |          |
|:--------------------------|:----------------------------|:---------|
| Fielddescription          |                             |          |
| Field                     | ver                         | permit   |
| abilityChn->mask          | 0:notsupport,1:support      | 1:option |
|                           | Whetherprivacyzone          | 2:write  |
|                           | configurationissupported    | 4:read   |
|                           |                             | 7:read&  |
|                           |                             | write&   |
|                           |                             | option   |
| abilityChn->image         | 0:notsupport,1:support      |          |
|                           | Whethervideoparameter       |          |
|                           | configurationissupported    |          |
| abilityChn->isp           | 0:notsupport,1:support      |          |
|                           | WhetherISPparameter         |          |
|                           | configurationissupported    |          |
| abilityChn->white_balance | 0:notsupport,1:support      |          |
|                           | Whetherwhitebalanceis       |          |
|                           | supported                   |          |
| abilityChn->cameraMode    | 0:notsupport,1:support      |          |
|                           | Whetheranalogcameramode     |          |
|                           | switchingissupported        |          |
| abilityChn->osd           | 0:notsupport,1:support,2:   |          |
|                           | supportosdanddistinctosd    |          |
| abilityChn->waterMark     | 0:notsupport,1:support      |          |
|                           | WhetherwatermarkSettingsare |          |
|                           | supported                   |          |
| abilityChn->enc           | 0:notsupportsetencodecfg,   |          |
|                           | 1:supportsetencodecfg       |          |
| abilityChn->live          | 0:notsupport1:support       |          |
|                           | main/extern/sub stream;     |          |
|                           | 2:supportmain/substream     |          |

### Table from Page 51

| abilityChn->snap        | 0:notsupportsnap,1:support    |    |
|                         | snap                          |    |
|:------------------------|:------------------------------|:---|
| abilityChn->ftp         | 0:notsupportftp;ver>0:support |    |
|                         | ftp                           |    |
|                         | (1:supportstream              |    |
|                         | 2:supportjpgpicture+stream    |    |
|                         | 3:supportStream+mode          |    |
|                         | selection                     |    |
|                         | 4:supportjpgpicture+stream+   |    |
|                         | modeselection                 |    |
|                         | 5:supportStream+mode          |    |
|                         | selection+streamtypeselection |    |
|                         | 6:supportjpgpicture+stream+   |    |
|                         | modeselection+streamtype      |    |
|                         | selection)                    |    |
| abilityChn->recCfg      | 0:notsupport,1:support        |    |
|                         | Supportsvideoconfiguration    |    |
|                         | (packagetime,preview,video    |    |
|                         | delay,videocoverage)          |    |
| abilityChn->recSchedule | 0:notsupport,                 |    |
|                         | 1:supportmdrecord,            |    |
|                         | 2:supportmdrecordandnormal    |    |
|                         | record                        |    |
| abilityChn->recDownload | 0:notsupportdownloadrecord    |    |
|                         | file,1:supportdownloadrecord  |    |
|                         | file                          |    |
| abilityChn->recReplay   | 0:notsupportplaybackrecord    |    |
|                         | fileonline,1:supportplayback  |    |
|                         | recordfileonlinefile          |    |
| abilityChn->ptzType     | 0:DoesnotsupportPTZordoes     |    |

### Table from Page 52

|                          | nothavepermissiontooperate     |    |
|                          | 1:supportAF                    |    |
|                          | 2:supportPTZ                   |    |
|                          | 3:supportPT                    |    |
|                          | 4:Simulatedballmachine         |    |
|                          | 5:PTZ(GM8136SPTZ)doesnot       |    |
|                          | supportspeedadjustment         |    |
|:-------------------------|:-------------------------------|:---|
| abilityChn->ptzCtrl      | 0:notsupport,                  |    |
|                          | 1:supportcontrolzoom           |    |
|                          | 2:supportcontrolzoomandfocus   |    |
|                          | withslider                     |    |
| abilityChn->ptzPreset    | 0:notsupport,                  |    |
|                          | 1:support                      |    |
|                          | WhetherPTZpresetpointsare      |    |
|                          | supported                      |    |
| abilityChn->ptzPatrol    | 0:notsupport,                  |    |
|                          | 1:support                      |    |
|                          | WhetherPTZcruisingis           |    |
|                          | supported                      |    |
| abilityChn->ptzTattern   | 0:notsupport,                  |    |
|                          | 1:support                      |    |
|                          | WhetherthePTZtrajectory        |    |
|                          | settingissupported             |    |
| abilityChn->ptzDirection | 0:support8directions+auto      |    |
|                          | scan,1:supportonly4directions, |    |
|                          | noautoscan                     |    |
| abilityChn->alarmIoIn    | 0:notsupport,                  |    |
|                          | 1:support                      |    |
|                          | WhetherIOalarminputis          |    |
|                          | supported                      |    |

### Table from Page 53

| abilityChn->alarmIoOut       | 0:notsupport,               |    |
|                              | 1:support                   |    |
|                              | WhetherIOalarmoutputis      |    |
|                              | supported                   |    |
|:-----------------------------|:----------------------------|:---|
| abilityChn->alarmRf          | 0:notsupport,               |    |
|                              | 1:supportRfalarmonDVR       |    |
|                              | 2:Batteryipc                |    |
|                              | 3:AddtheALARM/MDschedule    |    |
|                              | option                      |    |
| abilityChn->alarmMd          | 0:notsupport,               |    |
|                              | 1:support                   |    |
|                              | Whethermovementdetection    |    |
|                              | alarmsaresupported          |    |
| abilityChn->disableAutoFocus | 0:notsupportsetautofucus,   |    |
|                              | 1:supportsetautofucus       |    |
| abilityChn->floodLight       | 0:notsupportWhitelightLED,  |    |
|                              | 1:supportWhitelightLED      |    |
| abilityChn->battery          | 0:notsupport,               |    |
|                              | 1:support                   |    |
| abilityChn->indicatorLight   | 0:notsupportindicatorLight, |    |
|                              | 1:supportindicatorLight     |    |
| abilityChn->videoClip        | 0:notsupportvideoCutout     |    |
|                              | 1:supportcutoutwidthand     |    |
|                              | heightcannotbemodified;     |    |
|                              | 2:supportcutoutwidthand     |    |
|                              | heightcanbemodified         |    |
| abilityChn->powerLed         | 0:notsupport,               |    |
|                              | 1:support                   |    |
| abilityChn->mainEncType      | 0:mainstreamenctypeisH264   |    |
|                              | 1:mainstreamenctypeisH265   |    |

### Table from Page 54

| abilityChn->ispDayNight     | 0:notsupportday_nightmode     |    |
|                             | 1:supportday_nightmode        |    |
|                             | 2:Supportdayandnightmode      |    |
|                             | andsupportsettingswitching    |    |
|                             | threshold                     |    |
|:----------------------------|:------------------------------|:---|
| abilityChn->ispAntiFlick    | 0:notsupport                  |    |
|                             | 1:support                     |    |
|                             | Whetheranti-flickerfunctionis |    |
|                             | supporte                      |    |
| abilityChn->ispExposureMode | 0:notsupport                  |    |
|                             | 1:support                     |    |
|                             | Whetherexposureissupported    |    |
| abilityChn->ispWhiteBalance | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispBackLight    | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->isp3Dnr         | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispMirror       | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispFlip         | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispBright       | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispContrast     | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispSatruation   | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ispHue          | 0:notsupport                  |    |
|                             | 1:support                     |    |

### Table from Page 55

| abilityChn->ispSharpen      | 0:notsupport                  |    |
|                             | 1:support                     |    |
|:----------------------------|:------------------------------|:---|
| abilityChn->floodLight      | 0:notsupport                  |    |
|                             | 1:Supportwhitelight,2:Support |    |
|                             | whitelightautomaticmode       |    |
| abilityChn->mdWithPir       | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->mdTriggerAudio  | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->mdTriggerRecord | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->shelterCfg      | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->alarmAudio      | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->batAnalysis     | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->waterMark       | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->ledControl      | 0:notsupport                  |    |
|                             | 1:support                     |    |
| abilityChn->supportPtzCheck | 0:notsupport                  |    |
|                             | 1:support                     |    |
| hourFmt                     | 0:notsupport                  |    |
|                             | 1:supportchangehourformate    |    |
| time                        | 0:notsupport                  |    |
|                             | 1:Daylightsavingtimeonly      |    |
|                             | supportsSunday;               |    |
|                             | 2:Supportsanydayoftheweek     |    |

### Table from Page 56

| tvSystem    | 0:notsupport              |    |
|             | 1:support                 |    |
|:------------|:--------------------------|:---|
| display     | 0:notsupport              |    |
|             | 1:support                 |    |
| ipcManager  | 0:notsupport              |    |
|             | 1:support                 |    |
| devInfo     | 0:notsupport              |    |
|             | 1:support                 |    |
| autoMaint   | 0:notsupport              |    |
|             | 1:support                 |    |
| restore     | 0:notsupport              |    |
|             | 1:support                 |    |
| reboot      | 0:notsupport              |    |
|             | 1:support                 |    |
| log         | 0:notsupport              |    |
|             | 1:support                 |    |
| performance | 0:notsupport              |    |
|             | 1:support                 |    |
| upgrade     | 0:notsupport              |    |
|             | 1:supportmanualupgrade    |    |
|             | 2:supportmanualupgradeand |    |
|             | upgradeonline             |    |
| importCfg   | 0:notsupport              |    |
|             | 1:support                 |    |
| exportCfg   | 0:notsupport              |    |
|             | 1:support                 |    |
| disk        | 0:notsupport              |    |
|             | 1:support                 |    |
| sdCard      | 0:notsupport              |    |
|             | 1:support                 |    |

### Table from Page 57

| devName   | 0:notsupport                 |    |
|           | 1:support                    |    |
|:----------|:-----------------------------|:---|
| auth      | 0:notsupport                 |    |
|           | 1:support                    |    |
| user      | 0:notsupport                 |    |
|           | 1:support                    |    |
| online    | 0:notsupport                 |    |
|           | 1:support                    |    |
| rtsp      | 0:notsupport                 |    |
|           | 1:support                    |    |
| rtmp      | 0:notsupport                 |    |
|           | 1:support                    |    |
| ddns      | 0:notsupport                 |    |
|           | 1:swan                       |    |
|           | 2:3322                       |    |
|           | 3:dyndns                     |    |
|           | 4:swann+3322                 |    |
|           | 5:swann+dyndns               |    |
|           | 6:3322+dyndns                |    |
|           | 7:swann+3332+dyndns          |    |
|           | 8:noip                       |    |
|           | 9:dyndns+noip                |    |
| ddnsCfg   | 0:Doesnotsupportentering     |    |
|           | ddnsserveraddress            |    |
|           | 1:Supportinputddnsserver     |    |
|           | address                      |    |
| email     | 0:Mailfunctionisnotsupported |    |
|           | 1:Supportjpgattachment       |    |
|           | 2:Supportvideoandjpg         |    |
|           | attachments                  |    |

### Table from Page 58

|               | 3:Supportvideoandjpg        |    |
|               | attachments,supportsender   |    |
|               | nickname                    |    |
|:--------------|:----------------------------|:---|
| emailSchedule | 0:Scheduleisnotsupported    |    |
|               | 1:Supportschedule           |    |
| upnp          | 0:notsupport                |    |
|               | 1:support                   |    |
| onvif         | 0:notsupport                |    |
|               | 1:support                   |    |
| ntp           | 0:notsupport                |    |
|               | 1:support                   |    |
| mediaPort     | 0:notsupport                |    |
|               | 1:support                   |    |
| http          | 0:notsupport                |    |
|               | 1:support                   |    |
| https         | 0:notsupport                |    |
|               | 1:support                   |    |
| httpFlv       | 0:notsupport                |    |
|               | 1:support                   |    |
| p2p           | 0:notsupport                |    |
|               | 1:support                   |    |
| 3g            | 0:notsupport                |    |
|               | 1:support                   |    |
| localLink     | 0:notsupport                |    |
|               | 1:support                   |    |
| pppoe         | 0:notsupport                |    |
|               | 1:support                   |    |
| Wifi          | 0:notsupport                |    |
|               | 1:support                   |    |

### Table from Page 59

| Push             | 0:notsupport                |    |
|                  | 1:support                   |    |
|:-----------------|:----------------------------|:---|
| pushSchedule     | 0:notsupport                |    |
|                  | 1:support                   |    |
| Talk             | 0:notsupport                |    |
|                  | 1:support                   |    |
| alarmHddErr      | 0:notsupport                |    |
|                  | 1:support                   |    |
| alarmHddFull     | 0:notsupport                |    |
|                  | 1:support                   |    |
| alarmDisconnet   | 0:notsupport                |    |
|                  | 1:support                   |    |
| alarmIpConflict  | 0:notsupport                |    |
|                  | 1:support                   |    |
| ledControl       | 0:notsupport                |    |
|                  | 1:support                   |    |
| disableAutoFocus | 0:notsupport                |    |
|                  | 1:support                   |    |
| videoClip        | 1:Cutoutwidthandheight      |    |
|                  | cannotbemodified;           |    |
|                  | 2:Cutoutwidthandheightcanbe |    |
|                  | modified                    |    |
| alarmAudio       | 0:notsupport                |    |
|                  | 1:support                   |    |
| cloudStorage     | bit0:Whethertosupportcloud  |    |
|                  | upload                      |    |
|                  | bit1:Whethertosupportcloud  |    |
|                  | serviceconfiguration        |    |
|                  | bit3:Whethertosupportcloud  |    |
|                  | uploaddeployment            |    |

### Table from Page 60

| scheduleVersion   | 0:supportcmd:                     |    |
|                   | “GetRec”,“SetRec”,”GetEmail”,”    |    |
|                   | SetEmail”,”GetFtp”,“SetFtp”,      |    |
|                   | “GetPush”,“SetPush”,              |    |
|                   | “GetAudioAlarm”,                  |    |
|                   | “SetAudioAlarm”,                  |    |
|                   | “GetCloudSchedule”,“SetCloudSch   |    |
|                   | edule”,“GetAlarm”,“SetAlarm”      |    |
|                   | 1:supportcmd:                     |    |
|                   | “GetRecV20”,“SetRecV20”,”         |    |
|                   | GetEmailV20”,”SetEmailV20”,”      |    |
|                   | GetFtpV20”,“SetFtpV20”,           |    |
|                   | “GetPushV20”,“SetPushV20”,        |    |
|                   | “GetAudioAlarmV20”,               |    |
|                   | “SetAudioAlarmV20”,               |    |
|                   | “GetCloudScheduleV20”,            |    |
|                   | “SetCloudScheduleV20”;            |    |
|                   | “GetMdAlarm”                      |    |
|                   | “SetMdAlarm”                      |    |
|:------------------|:----------------------------------|:---|
| customAudio       | 0:notsupport                      |    |
|                   | 1:support                         |    |
| wifiTest          | 0:notsupport                      |    |
|                   | 1:support                         |    |
| simMoudule        | 0:notsupport                      |    |
|                   | 1:support                         |    |
| dateFormat        | 0:notsupport                      |    |
|                   | 1:support                         |    |
| emailInterval     | 0:notsupport                      |    |
|                   | 1:support                         |    |

### Table from Page 61

| showQrCode                  | 0:notsupport   |    |
|                             | 1:support      |    |
|:----------------------------|:---------------|:---|
| ftpTest                     | 0:notsupport   |    |
|                             | 1:support      |    |
| ftpSubStream                | 0:notsupport   |    |
|                             | 1:support      |    |
| ftpExtStream                | 0:notsupport   |    |
|                             | 1:support      |    |
| ftpPic                      | 0:notsupport   |    |
|                             | 1:support      |    |
| ftpAutoDir                  | 0:notsupport   |    |
|                             | 1:support      |    |
| recOverWrite                | 0:notsupport   |    |
|                             | 1:support      |    |
| recPackDuration             | 0:notsupport   |    |
|                             | 1:support      |    |
| recPreRecord                | 0:notsupport   |    |
|                             | 1:support      |    |
| recExtensionTimeList        | 0:notsupport   |    |
|                             | 1:support      |    |
| supportAudioAlarm           | 0:notsupport   |    |
|                             | 1:support      |    |
| supportAudioAlarmEnable     | 0:notsupport   |    |
|                             | 1:support      |    |
| supportAudioAlarmSchedule   | 0:notsupport   |    |
|                             | 1:support      |    |
| supportAudioAlarmTaskEnable | 0:notsupport   |    |
|                             | 1:support      |    |
| supportFtpTask              | 0:notsupport   |    |
|                             | 1:support      |    |

### Table from Page 62

| supportBuzzer            | 0:notsupport   |    |
|                          | 1:support      |    |
|:-------------------------|:---------------|:---|
| supportBuzzerEnable      | 0:notsupport   |    |
|                          | 1:support      |    |
| supportBuzzerTask        | 0:notsupport   |    |
|                          | 1:support      |    |
| supportBuzzerTaskEnable  | 0:notsupport   |    |
|                          | 1:support      |    |
| supportRecordEnable      | 0:notsupport   |    |
|                          | 1:support      |    |
| supportRecScheduleEnable | 0:notsupport   |    |
|                          | 1:support      |    |
| supportEmailEnable       | 0:notsupport   |    |
|                          | 1:support      |    |
| supportEmailTaskEnable   | 0:notsupport   |    |
|                          | 1:support      |    |
| supportFtpEnable         | 0:notsupport   |    |
|                          | 1:support      |    |
| supportFtpTaskEnable     | 0:notsupport   |    |
|                          | 1:support      |    |
| supportAi                | 0:notsupport   |    |
|                          | 1:support      |    |
| supportAiAnimal          | 0:notsupport   |    |
|                          | 1:support      |    |
| supportAiDetectConfig    | 0:notsupport   |    |
|                          | 1:support      |    |
| supportAiDogCat          | 0:notsupport   |    |
|                          | 1:support      |    |
| supportAiFace            | 0:notsupport   |    |
|                          | 1:support      |    |

### Table from Page 63

| supportAiPeople        | 0:notsupport   |    |
|                        | 1:support      |    |
|:-----------------------|:---------------|:---|
| supportAiSensitivity   | 0:notsupport   |    |
|                        | 1:support      |    |
| supportAiStayTime      | 0:notsupport   |    |
|                        | 1:support      |    |
| supportAiTargetSize    | 0:notsupport   |    |
|                        | 1:support      |    |
| supportAiVehicle       | 0:notsupport   |    |
|                        | 1:support      |    |
| supportAoAdjust        | 0:notsupport   |    |
|                        | 1:support      |    |
| supportFLBrightness    | 0:notsupport   |    |
|                        | 1:support      |    |
| supportFLIntelligent   | 0:notsupport   |    |
|                        | 1:support      |    |
| supportFLKeepOn        | 0:notsupport   |    |
|                        | 1:support      |    |
| supportFLSchedule      | 0:notsupport   |    |
|                        | 1:support      |    |
| supportFLswitch        | 0:notsupport   |    |
|                        | 1:support      |    |
| supportGop             | 0:notsupport   |    |
|                        | 1:support      |    |
| supportPtzCheck        | 0:notsupport   |    |
|                        | 1:support      |    |
| supportThresholdAdjust | 0:notsupport   |    |
|                        | 1:support      |    |
| supportWhiteDark       | 0:notsupport   |    |
|                        | 1:support      |    |

### Table from Page 64

| supportAudioAlarm           | 0:notsupport   |    |
|                             | 1:support      |    |
|:----------------------------|:---------------|:---|
| supportAudioAlarmEnable     | 0:notsupport   |    |
|                             | 1:support      |    |
| supportAudioAlarmSchedule   | 0:notsupport   |    |
|                             | 1:support      |    |
| supportAudioAlarmTaskEnable | 0:notsupport   |    |
|                             | 1:support      |    |
| supportBuzzer               | 0:notsupport   |    |
|                             | 1:support      |    |
| supportBuzzerEnable         | 0:notsupport   |    |
|                             | 1:support      |    |
| supportBuzzerTask           | 0:notsupport   |    |
|                             | 1:support      |    |
| supportBuzzerTaskEnable     | 0:notsupport   |    |
|                             | 1:support      |    |
| supportEmailEnable          | 0:notsupport   |    |
|                             | 1:support      |    |
| supportEmailTaskEnable      | 0:notsupport   |    |
|                             | 1:support      |    |
| supportFtpCoverPicture      | 0:notsupport   |    |
|                             | 1:support      |    |
| supportFtpCoverVideo        | 0:notsupport   |    |
|                             | 1:support      |    |
| supportFtpDirYM             | 0:notsupport   |    |
|                             | 1:support      |    |
| supportFtpPicCaptureMode    | 0:notsupport   |    |
|                             | 1:support      |    |
| supportFtpPicResoCustom     | 0:notsupport   |    |
|                             | 1:support      |    |

### Table from Page 65

| supportFtpPictureSwap    | 0:notsupport             |    |
|                          | 1:support                |    |
|:-------------------------|:-------------------------|:---|
| supportFtpTask           | 0:notsupport             |    |
|                          | 1:support                |    |
| supportFtpTaskEnable     | 0:notsupport             |    |
|                          | 1:support                |    |
| supportFtpVideoSwap      | 0:notsupport             |    |
|                          | 1:support                |    |
| supportFtpsEncrypt       | 0:notsupport             |    |
|                          | 1:support                |    |
| supportHttpEnable        | 0:notsupport             |    |
|                          | 1:support                |    |
| supportHttpsEnable       | 0:notsupport             |    |
|                          | 1:support                |    |
| supportOnvifEnable       | 0:notsupport             |    |
|                          | 1:support                |    |
| supportPushInterval      | 0:notsupport             |    |
|                          | 1:support                |    |
| supportRecScheduleEnable | 0:notsupport             |    |
|                          | 1:support                |    |
| supportRecordEnable      | 0:notsupport             |    |
|                          | 1:support                |    |
| supportRtmpEnable        | 0:notsupport             |    |
|                          | 1:support                |    |
| supportRtspEnable        | 0:notsupport             |    |
|                          | 1:support                |    |
| supportAutoTrackStream   | 0:notsupport             |    |
|                          | 1:support                |    |
|                          | Whetherthetrackingstream |    |
|                          | configurationissupported |    |

### Table from Page 66

| supportBinoStitch   | 0:notsupport                 |    |
|                     | 1:support                    |    |
|                     | Whethertheadjustmentof       |    |
|                     | binocularequipmentsplicing   |    |
|                     | pictureissupported           |    |
|:--------------------|:-----------------------------|:---|
| aiTrackDogCat       | Whethertrackingofcatsand     |    |
|                     | dogsissupported              |    |

### Table from Page 66

| Dataexample        | None        | None   |
|:-------------------|:------------|:-------|
| [                  |             |        |
| {                  |             |        |
| "cmd":"GetDevInfo" |             |        |
| }                  |             |        |
| ]                  |             |        |
| Fielddescription   |             |        |
| Field              | Description | M/O    |

### Table from Page 66

| Return datacorrectly   |
|:-----------------------|
| [                      |

### Table from Page 67

| {                                      | None                                        |
| "cmd":"GetDevInfo",                    |                                             |
| "code":0,                              |                                             |
| "value":{                              |                                             |
| "DevInfo":{                            |                                             |
| "B485":1,                              |                                             |
| "IOInputNum":0,                        |                                             |
| "IOOutputNum":0,                       |                                             |
| "audioNum":16,                         |                                             |
| "buildDay":"build20080734",            |                                             |
| "cfgVer":"v3.0.0.0",                   |                                             |
| "channelNum":16,                       |                                             |
| "detail":"NVR652410104001000200000",   |                                             |
| "diskNum":2,                           |                                             |
| "exactType":"NVR",                     |                                             |
| "firmVer":"v3.0.0.59_20080734",        |                                             |
| "frameworkVer":1,                      |                                             |
| "hardVer":"H3MB18",                    |                                             |
| "model":"RLN16-410",                   |                                             |
| "name":"NVR",                          |                                             |
| "pakSuffix":"pak,paks",                |                                             |
| "serial":"00000000000000",             |                                             |
| "type":"NVR",                          |                                             |
| "wifi":0                               |                                             |
| }                                      |                                             |
| }                                      |                                             |
| }                                      |                                             |
| ]                                      |                                             |
|:---------------------------------------|:--------------------------------------------|
| Fielddescription                       |                                             |
| Field                                  | Description                                 |
| IOInputNum                             | ThenumberofIOinputport.                     |
| IOOutputNum                            | ThenumberofIOoutputport.                    |
| buildDay                               | Theestablishdate.                           |
| cfgVer                                 | Theversionnumberofconfigurationinformation. |
| channelNum                             | Thechannelnumber.                           |
| detail                                 | Thedetailsofdeviceinformation.              |
| diskNum                                | ThenumberofUSBdiskorSDcard.                 |
| firmVer                                | Theversionnumberofthefirmware.              |

### Table from Page 68

| hardVer      | Theversionnumberofthehardware.   |
|:-------------|:---------------------------------|
| name         | Devicename.                      |
| type         | Devicetype.                      |
| wifi         | WhetherWi-Fiissupported.         |
| B485         | 0:no485,1:have485                |
| exactType    | Producttype                      |
| frameworkVer | Architectureversion              |

### Table from Page 68

| Dataexample         | None           | None   |
|:--------------------|:---------------|:-------|
| [{                  |                |        |
| "cmd":"GetDevName", |                |        |
| "param":{           |                |        |
| "channel":0         |                |        |
| }                   |                |        |
| }]                  |                |        |
| Fielddescription    |                |        |
| Field               | Description    | M/O    |
| channel             | Indexofchannel | M      |

### Table from Page 69

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"GetDevName",    |              |
| "code":0,              |              |
| "value":{              |              |
| "DevName":{            |              |
| "name":"NVR"           |              |
| }                      |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| name                   | nameofdevice |

### Table from Page 69

| Dataexample         |
|:--------------------|
| [{                  |
| "cmd":"SetDevName", |
| "param":{           |
| "DevName":{         |
| "name":"camera101"  |
| }                   |

### Table from Page 70

| }                | None           | None   |
| }]               |                |        |
|:-----------------|:---------------|:-------|
| Fielddescription |                |        |
| Field            | Description    | M/O    |
| channel          | Indexofchannel | M      |

### Table from Page 70

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetDevName",    |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 71

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetTime", |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 71

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetTime",       |
| "code":0,              |
| "initial":{            |
| "Dst":{                |
| "enable":0,            |
| "endHour":2,           |
| "endMin":0,            |
| "endMon":10,           |
| "endSec":0,            |
| "endWeek":5,           |
| "endWeekday":0,        |
| "offset":1,            |
| "startHour":2,         |
| "startMin":0,          |
| "startMon":3,          |
| "startSec":0,          |
| "startWeek":2,         |
| "startWeekday":0       |
| },                     |
| "Time":{               |
| "day":1,               |
| "hour":0,              |
| "hourFmt":0,           |
| "min":0,               |
| "mon":0,               |

### Table from Page 75

|                  | None                                           |
|:-----------------|:-----------------------------------------------|
| Fielddescription |                                                |
| Field            | description                                    |
| Dst              | DaylightSavingsTime                            |
| enable           | EnableDaylightSavingsTime                      |
| endHour          | TheendofDaylightSavingsTime(Hour)              |
| endMin           | TheendofDaylightSavingsTime(Minute)            |
| endMon           | TheendofDaylightSavingsTime(Month)             |
| endSec           | TheendofDaylightSavingsTime(Second)            |
| endWeek          | TheendofDaylightSavingsTime(Week)              |
| endWeekday       | TheendofDaylightSavingsTime(Day)               |
| offset           | Timeoffset                                     |
| startHour        | DaylightSavingsTimestartingtime(Hour)          |
| startMin         | DaylightSavingsTimestartingtime(Minute)        |
| startMon         | DaylightSavingsTimestartingtime(Month)         |
| startSec         | DaylightSavingsTimestartingtime(Second)        |
| startWeek        | DaylightSavingsTimestartingtime(Week)          |
| startWeekday     | DaylightSavingsTimestartingtime(Day)           |
| Time             | Systemtime                                     |
| year             | Year                                           |
| mon              | Month                                          |
| day              | Day                                            |
| hour             | Hour                                           |
| min              | Minute                                         |
| sec              | Second                                         |
| timeFmt          | Timeformat                                     |
| timeZone         | Timezone                                       |
| hourFmt          | Hourformat,0isfor24hourclock，1isfor12hourclock |

### Table from Page 76

| Dataexample             |
|:------------------------|
| [                       |
| {                       |
| "cmd":"SetTime",        |
| "param":{               |
| "Dst":{                 |
| "enable":0,             |
| "endHour":2,            |
| "endMin":0,             |
| "endMon":10,            |
| "endSec":0,             |
| "endWeek":5,            |
| "endWeekday":0,         |
| "offset":1,             |
| "startHour":2,          |
| "startMin":0,           |
| "startMon":3,           |
| "startSec":0,           |
| "startWeek":2,          |
| "startWeekday":0        |
| },                      |
| "Time":{                |
| "day":6,                |
| "hour":20,              |
| "min":9,                |
| "mon":6,                |
| "sec":32,               |
| "timeFmt":"DD/MM/YYYY", |
| "timeZone":-28800,      |
| "year":2016,            |

### Table from Page 77

| "hourFmt":0      | None           | None   |
| }                |                |        |
| }                |                |        |
| }                |                |        |
| ]                |                |        |
|:-----------------|:---------------|:-------|
| Fielddescription |                |        |
| Field            | Description    | M/O    |
| Dst              | SeealsoGetTime | O      |
| enable           | SeealsoGetTime | O      |
| endHour          | SeealsoGetTime | O      |
| endMin           | SeealsoGetTime | O      |
| endMon           | SeealsoGetTime | O      |
| endSec           | SeealsoGetTime | O      |
| endWeek          | SeealsoGetTime | O      |
| endWeekday       | SeealsoGetTime | O      |
| offset           | SeealsoGetTime | O      |
| startHour        | SeealsoGetTime | O      |
| startMin         | SeealsoGetTime | O      |
| startMon         | SeealsoGetTime | O      |
| startSec         | SeealsoGetTime | O      |
| startWeek        | SeealsoGetTime | O      |
| startWeekday     | SeealsoGetTime | O      |
| year             | SeealsoGetTime | O      |
| mon              | SeealsoGetTime | O      |
| day              | SeealsoGetTime | O      |
| hour             | SeealsoGetTime | O      |
| min              | SeealsoGetTime | O      |
| sec              | SeealsoGetTime | O      |
| timeFmt          | SeealsoGetTime | O      |
| timeZone         | SeealsoGetTime | O      |
| hourFmt          | SeealsoGetTime | O      |

### Table from Page 78

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetTime",       |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 78

| Dataexample           | None        | None   |
|:----------------------|:------------|:-------|
| [                     |             |        |
| {                     |             |        |
| "cmd":"GetAutoMaint", |             |        |
| "action":1            |             |        |
| }                     |             |        |
| ]                     |             |        |
| Fielddescription      |             |        |
| Field                 | Description | M/O    |

### Table from Page 79

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| [                      |
| {                      |
| "cmd":"GetAutoMaint",  |
| "code":0,              |
| "initial":{            |
| "AutoMaint":{          |
| "enable":0,            |
| "hour":0,              |
| "min":0,               |
| "sec":0,               |
| "weekDay":"Sunday"     |
| }                      |
| },                     |
| "range":{              |
| "AutoMaint":{          |
| "enable":"boolean",    |
| "hour":{               |
| "max":23,              |
| "min":0                |
| },                     |
| "min":{                |
| "max":59,              |
| "min":0                |
| },                     |
| "sec":{                |
| "max":59,              |
| "min":0                |
| },                     |
| "weekDay":[            |
| "Everyday",            |
| "Sunday",              |
| "Monday",              |
| "Tuesday",             |
| "Wednesday",           |
| "Thursday",            |
| "Friday",              |
| "Saturday"             |

### Table from Page 80

| ]                    | None                                   |
| }                    |                                        |
| },                   |                                        |
| "value":{            |                                        |
| "AutoMaint":{        |                                        |
| "enable":1,          |                                        |
| "hour":2,            |                                        |
| "min":0,             |                                        |
| "sec":0,             |                                        |
| "weekDay":"Sunday"   |                                        |
| }                    |                                        |
| }                    |                                        |
| }                    |                                        |
| ]                    |                                        |
|:---------------------|:---------------------------------------|
| Fielddescription     |                                        |
| Field                | description                            |
| enable               | Automaintainanceofenable/disableswitch |
| hour                 | Hour                                   |
| min                  | Minute                                 |
| sec                  | Second                                 |
| weekDay              | Thedayoftheweek                        |

### Table from Page 80

| Dataexample   |
|:--------------|
| [             |

### Table from Page 81

| {                       | None                | None   |
| "cmd":"SetAutoMaint",   |                     |        |
| "param":{               |                     |        |
| "AutoMaint":{           |                     |        |
| "enable":1,             |                     |        |
| "weekDay":"Everyday",   |                     |        |
| "hour":3,               |                     |        |
| "min":52,               |                     |        |
| "sec":4                 |                     |        |
| }                       |                     |        |
| }                       |                     |        |
| }                       |                     |        |
| ]                       |                     |        |
|:------------------------|:--------------------|:-------|
| Fielddescription        |                     |        |
| Field                   | Description         | M/O    |
| enable                  | SeealsoGetAutoMaint | O      |
| hour                    | SeealsoGetAutoMaint | O      |
| min                     | SeealsoGetAutoMaint | O      |
| sec                     | SeealsoGetAutoMaint | O      |
| weekDay                 | SeealsoGetAutoMaint | O      |

### Table from Page 81

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetAutoMaint",  |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 82

| Dataexample        | None        | None   |
|:-------------------|:------------|:-------|
| [                  |             |        |
| {                  |             |        |
| "cmd":"GetHddInfo" |             |        |
| }                  |             |        |
| ]                  |             |        |
| Fielddescription   |             |        |
| Field              | Description | M/O    |

### Table from Page 82

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetHddInfo",    |
| "code":0,              |
| "value":{              |
| "HddInfo":[            |
| {                      |
| "capacity":938610,     |
| "format":1,            |
| "mount":1,             |
| "number":1,            |
| "size":549219,         |
| "storageType":1        |
| }                      |
| ]                      |

### Table from Page 83

| }                | None                         |
| }                |                              |
| ]                |                              |
|:-----------------|:-----------------------------|
| Fielddescription |                              |
| Field            | description                  |
| capacity         | ThecapacityofHDDorSDcard(Mb) |
| format           | Whetheritisformattedornot    |
| id               | IndexforHDDorSDcard          |
| mount            | Whetheritismountedornot      |
| size             | Theremainingcapacity(Mb)     |
| storageType      | Typeofstorage                |
| number           | ExternalSATAinterface        |

### Table from Page 83

| Dataexample     |
|:----------------|
| [{              |
| "cmd":"Format", |
| "param":{       |
| "HddInfo":{     |
| "id":[0]        |
| }               |
| }               |
| }]              |

### Table from Page 84

| Fielddescription   | None                                     | None   |
|:-------------------|:-----------------------------------------|:-------|
| Field              | Description                              | M/O    |
| id                 | Indexoftheharddiskorsd-Cardthatyouwantto | M      |
|                    | format.                                  |        |

### Table from Page 84

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"Format",        |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 84

| Parameter   | M/O   | Description                        |
|:------------|:------|:-----------------------------------|
| clearConfig | M     | Whethertocleartheconfigurationmark |

### Table from Page 85

| Dataexample                                                             | None                       | None   |
|:------------------------------------------------------------------------|:---------------------------|:-------|
| Content-Type:multipart/form-data;                                       |                            |        |
| boundary=----WebKitFormBoundaryYkwJBwvTHAd3Nukl                         |                            |        |
| Referer:https://192.168.2.232/?1466148584152                            |                            |        |
| Accept-Encoding:gzip,deflate                                            |                            |        |
| Accept-Language:zh-CN,zh;q=0.8                                          |                            |        |
| ------WebKitFormBoundaryYkwJBwvTHAd3Nukl                                |                            |        |
| Content-Disposition:form-data;name="upgrade-package";filename="xxx.pak" |                            |        |
| Content-Type:application/octet-stream                                   |                            |        |
| xxxxxxxxxxx......(Filecontent)                                          |                            |        |
| ------WebKitFormBoundaryYkwJBwvTHAd3Nukl--                              |                            |        |
| Note:Thiscommandcanonlycarryupto40Kpacketsatatime,anditneedstobe        |                            |        |
| calledseveraltimestocompletethedeviceupdate                             |                            |        |
| Fielddescription                                                        |                            |        |
| Field                                                                   | Description                | M/O    |
| boundary                                                                | Delimiter                  | M      |
| filename                                                                | Thenameoftheupdatefile     | M      |
| name                                                                    | Boundtobe"upgrade-package" | M      |

### Table from Page 85

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"Upgrade",       |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |

### Table from Page 86

| Fielddescription   | None        |
|:-------------------|:------------|
| Field              | description |

### Table from Page 86

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"Restore"  |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 86

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"Restore",       |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |

### Table from Page 87

| Fielddescription   | None        |
|:-------------------|:------------|
| Field              | description |

### Table from Page 87

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"Reboot"   |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 87

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"Reboot",        |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |
| Fielddescription       |

### Table from Page 88

| Dataexample             | None                               | None   |
|:------------------------|:-----------------------------------|:-------|
| [                       |                                    |        |
| {                       |                                    |        |
| "cmd":"UpgradePrepare", |                                    |        |
| "action":1,             |                                    |        |
| "param":                |                                    |        |
| {                       |                                    |        |
| "restoreCfg":0,         |                                    |        |
| "fileName":"XXX.pak"    |                                    |        |
| }                       |                                    |        |
| }                       |                                    |        |
| ]                       |                                    |        |
| Fielddescription        |                                    |        |
| Field                   | Description                        | M/O    |
| restoreCfg              | Whethertocleartheconfigurationmark | M      |
| fileName                | Thefilenameoftheupgradefile        | M      |

### Table from Page 88

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |

### Table from Page 89

| "cmd":"UpgratePrepare",   | None         |
| "code":0,                 |              |
| "value":{                 |              |
| "rspCode":200             |              |
| }                         |              |
| }                         |              |
| ]                         |              |
|:--------------------------|:-------------|
| Fielddescription          |              |
| Field                     | description  |
| rspCode                   | Responsecode |

### Table from Page 89

| Dataexample            | None        | None   |
|:-----------------------|:------------|:-------|
| [                      |             |        |
| {                      |             |        |
| "cmd":"GetAutoUpgrade" |             |        |
| }                      |             |        |
| ]                      |             |        |
| Fielddescription       |             |        |
| Field                  | Description | M/O    |
|                        |             | M      |

### Table from Page 90

| [                         | None         |
| {                         |              |
| "cmd":"GetAutoUpgrade",   |              |
| "code":0,                 |              |
| "initial":{               |              |
| "AutoUpgrade":{           |              |
| "enable":1                |              |
| }                         |              |
| },                        |              |
| "range":{                 |              |
| "AutoUpgrade":{           |              |
| "enable":"boolean"        |              |
| }                         |              |
| },                        |              |
| "value":{                 |              |
| "AutoUpgrade":{           |              |
| "enable":1                |              |
| }                         |              |
| }                         |              |
| }                         |              |
| ]                         |              |
|:--------------------------|:-------------|
| Fielddescription          |              |
| Field                     | description  |
| rspCode                   | Responsecode |

### Table from Page 91

| [                         | None        | None   |
| {                         |             |        |
| "cmd":"SetAutoUpgrade",   |             |        |
| "param":{                 |             |        |
| "AutoUpgrade":{           |             |        |
| "enable":0                |             |        |
| }                         |             |        |
| }                         |             |        |
| }                         |             |        |
| ]                         |             |        |
|:--------------------------|:------------|:-------|
| Fielddescription          |             |        |
| Field                     | Description | M/O    |
|                           |             | M      |

### Table from Page 91

| Return datacorrectly    | None         |
|:------------------------|:-------------|
| [                       |              |
| {                       |              |
| "cmd":"SetAutoUpgrade", |              |
| "code":0,               |              |
| "value":{               |              |
| "rspCode":200           |              |
| }                       |              |
| }                       |              |
| ]                       |              |
| Fielddescription        |              |
| Field                   | description  |
| rspCode                 | Responsecode |

### Table from Page 92

| Dataexample           | None        | None   |
|:----------------------|:------------|:-------|
| [                     |             |        |
| {                     |             |        |
| "cmd":"CheckFirmware" |             |        |
| }                     |             |        |
| ]                     |             |        |
| Fielddescription      |             |        |
| Field                 | Description | M/O    |
|                       |             | M      |

### Table from Page 92

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"CheckFirmware", |              |
| "code":0,              |              |
| "value":{              |              |
| "newFirmware":00       |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |
| newFirmware            | Newfirmware  |

### Table from Page 93

| Dataexample            | None        | None   |
|:-----------------------|:------------|:-------|
| [                      |             |        |
| {                      |             |        |
| "cmd":"UpgradeOnline", |             |        |
| }                      |             |        |
| ]                      |             |        |
| Fielddescription       |             |        |
| Field                  | Description | M/O    |
|                        |             | M      |

### Table from Page 93

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"UpgradeOnline", |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 94

| Dataexample           | None        | None   |
|:----------------------|:------------|:-------|
| [                     |             |        |
| {                     |             |        |
| "cmd":"UpgradeStatus" |             |        |
| }                     |             |        |
| ]                     |             |        |
| Fielddescription      |             |        |
| Field                 | Description | M/O    |
|                       |             | M      |

### Table from Page 94

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"UpgradeStatus", |              |
| "code":0,              |              |
| "value":{              |              |
| "Status":{             |              |
| "Persent":0,           |              |
| "code":0               |              |
| }                      |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 95

| Dataexample              | None        | None   |
|:-------------------------|:------------|:-------|
| [{                       |             |        |
| "cmd":"Getchannelstatus" |             |        |
| }]                       |             |        |
| Fielddescription         |             |        |
| Field                    | Description | M/O    |

### Table from Page 95

| Return datacorrectly      |
|:--------------------------|
| [                         |
| {                         |
| "cmd":"GetChannelstatus", |
| "code":0,                 |
| "value":{                 |
| "count":16,               |
| "status":[                |
| {                         |
| "channel":0,              |
| "name":"E1X",             |
| "online":1,               |
| "typeInfo":"E1X"          |
| },                        |
| {                         |
| "channel":1,              |
| "name":"",                |

### Table from Page 98

| }                | None               |
| }                |                    |
| ]                |                    |
|:-----------------|:-------------------|
| Fielddescription |                    |
| Field            | description        |
| channel          | Channelnumber      |
| name             | Devicename         |
| online           | Whetheronlineornot |
| typeinfo         | Infomationoftype   |

### Table from Page 98

| Dataexample         |
|:--------------------|
| [{                  |
| "cmd":"Login",      |
| "param":{           |
| "User":{            |
| "Version":"0",      |
| "userName":"admin", |
| "password":"111111" |
| }                   |
| }                   |
| }]]                 |

### Table from Page 99

| Fielddescription   | None                                                   | None   |
|:-------------------|:-------------------------------------------------------|:-------|
| Field              | Description                                            | M/O    |
| userName           | Accountname,limit1~31characters.                       | M      |
| password           | Accountpassword,limit1~31characters.                   | O      |
| Version            | Loginversion                                           | O      |
|                    | 0:Donotapplyprivateencryptionprotocol                  |        |
|                    | 1:Applyaprivateencryptionprotocol                      |        |
|                    | Theprivateencryptionprotocolisnotprovidedexternally,so |        |
|                    | pleaseselect0                                          |        |

### Table from Page 99

| Return datacorrectly   | None                                            |
|:-----------------------|:------------------------------------------------|
| [                      |                                                 |
| {                      |                                                 |
| "cmd":"Login",         |                                                 |
| "code":0,              |                                                 |
| "value":{              |                                                 |
| "Token":{              |                                                 |
| "leaseTime":3600,      |                                                 |
| "name":"031465962723"  |                                                 |
| }                      |                                                 |
| }                      |                                                 |
| }                      |                                                 |
| ]                      |                                                 |
| Fielddescription       |                                                 |
| Field                  | description                                     |
| leaseTime              | Leasetimebysecond.                              |
| name                   | Tokenstring,lengthshouldbelessthan32characters. |

### Table from Page 100

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"Logout",  |             |        |
| "param":{        |             |        |
| }                |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 100

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"Logout",        |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 101

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetUser", |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 101

| Return datacorrectly       |
|:---------------------------|
| [                          |
| {                          |
| "cmd":"GetUser",           |
| "code":0,                  |
| "initial":{                |
| "User":{                   |
| "level":"guest"            |
| }                          |
| },                         |
| "range":{                  |
| "User":{                   |
| "level":["guest","admin"], |
| "password":{               |
| "maxLen":31,               |

### Table from Page 102

| "minLen":6           | None           |
| },                   |                |
| "userName":{         |                |
| "maxLen":31,         |                |
| "minLen":1           |                |
| }                    |                |
| }                    |                |
| },                   |                |
| "value":{            |                |
| "User":[             |                |
| {                    |                |
| "level":"admin",     |                |
| "userName":"admin"   |                |
| }                    |                |
| ]                    |                |
| }                    |                |
| }                    |                |
| ]                    |                |
|:---------------------|:---------------|
| Fielddescription     |                |
| Field                | description    |
| level                | Usercompetence |
| userName             | Username       |
| maxlen               | Maxlength      |
| minlen               | Minlength      |

### Table from Page 103

| Dataexample             | None             | None   |
|:------------------------|:-----------------|:-------|
| [                       |                  |        |
| {                       |                  |        |
| "cmd":"AddUser",        |                  |        |
| "param":{               |                  |        |
| "User":{                |                  |        |
| "userName":"GuestUser", |                  |        |
| "password":"123456",    |                  |        |
| "level":"guest"         |                  |        |
| }                       |                  |        |
| }                       |                  |        |
| }                       |                  |        |
| ]                       |                  |        |
| Fielddescription        |                  |        |
| Field                   | Description      | M/O    |
| userName                | Accountname.     | M      |
| password                | Accountpassword. | M      |
| level                   | Usercompetence   | M      |
| Note:Canaddupto20users  |                  |        |

### Table from Page 103

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"AddUser",       |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 104

| Dataexample           | None                             | None   |
|:----------------------|:---------------------------------|:-------|
| [                     |                                  |        |
| {                     |                                  |        |
| "cmd":"DelUser",      |                                  |        |
| "param":{             |                                  |        |
| "User":{              |                                  |        |
| "userName":"TestUser" |                                  |        |
| }                     |                                  |        |
| }                     |                                  |        |
| }                     |                                  |        |
| ]                     |                                  |        |
| Fielddescription      |                                  |        |
| Field                 | Description                      | M/O    |
| userName              | Accountname,limit1~31characters. | M      |

### Table from Page 104

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"DelUser",       |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |

### Table from Page 105

| Fielddescription   | None         |
|:-------------------|:-------------|
| Field              | description  |
| rspCode            | Responsecode |

### Table from Page 105

| Dataexample             | None                | None   |
|:------------------------|:--------------------|:-------|
| [{                      |                     |        |
| "cmd":"ModifyUser",     |                     |        |
| "action":0,             |                     |        |
| "param":{               |                     |        |
| "User":{                |                     |        |
| "userName":"admin",     |                     |        |
| "newPassword":"111111", |                     |        |
| "oldPassword":"000000"  |                     |        |
| }                       |                     |        |
| }                       |                     |        |
| }]                      |                     |        |
| Fielddescription        |                     |        |
| Field                   | Description         | M/O    |
| userName                | Accountname.        | M      |
| newPassword             | Accountnewpassword. | M      |
| oldPassword             | Accountoldpassword. |        |

### Table from Page 106

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"ModifyUser",    |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 106

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetOnline",     |
| "code":0,              |
| "value":{              |
| "User":[               |
| {                      |
| "canbeDisconn":0,      |
| "ip":"192.168.2.166",  |
| "level":"admin",       |
| "sessionId":1000,      |

### Table from Page 107

| "userName":"admin"                    | None                                              |
| },                                    |                                                   |
| ...//Theremaybemultipleonlineusers.   |                                                   |
| ]                                     |                                                   |
| }                                     |                                                   |
| }                                     |                                                   |
| ]                                     |                                                   |
|:--------------------------------------|:--------------------------------------------------|
| Fielddescription                      |                                                   |
| Field                                 | description                                       |
| canbeDisconn                          | Whenthefieldvalueis1,theonlineusercanbeforcedto   |
|                                       | disconnect.Whenthevalueis0,thereverseisthecase.   |
| ip                                    | TheIPaddressoftheonlineuser.                      |
| level                                 | Usercompetenceforonlineusers                      |
| sessionId                             | Sessioniddistributedtoonlineusersbythesystem,itis |
|                                       | usedtoforcetheusertogooffline.                    |
| userName                              | Theonlineuser’sloginaccount.                      |

### Table from Page 107

| Dataexample            |
|:-----------------------|
| [{                     |
| "cmd":"Disconnect",    |
| "param":{              |
| "User":{               |
| "userName":"userName", |
| "sessionId":1001       |

### Table from Page 108

| }                | None                                            | None   |
| }                |                                                 |        |
| }]               |                                                 |        |
|:-----------------|:------------------------------------------------|:-------|
| Fielddescription |                                                 |        |
| Field            | Description                                     | M/O    |
| userName         | Theonlineuser’sloginaccount.                    | M      |
| sessionId        | ThesessionIDwhichSystemassignedtotheonlineuser. | M      |

### Table from Page 108

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"Disconnect",    |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 109

| Dataexample        | None                | None   |
|:-------------------|:--------------------|:-------|
| [{                 |                     |        |
| "cmd":"GetSysCfg", |                     |        |
| "action":1,        |                     |        |
| "param":{          |                     |        |
| "channel":0        |                     |        |
| }                  |                     |        |
| }]                 |                     |        |
| Fielddescription   |                     |        |
| Field              | Description         | M/O    |
| channel            | Devicechannelnumber |        |

### Table from Page 109

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetSysCfg",     |
| "code":0,              |
| "initial":{            |
| "SysCfg":{             |
| "LockTime":300,        |
| "allowedTimes":5,      |
| "loginLock":0          |
| }                      |
| },                     |
| "range":{              |
| "SysCfg":{             |
| "LockTime":{           |
| "max":300,             |
| "min":0                |
| },                     |
| "allowedTimes":{       |
| "max":5,               |
| "min":0                |
| },                     |
| "loginLock":"boolean"  |
| }                      |
| },                     |

### Table from Page 110

| "value":{           | None                           |
| "SysCfg":{          |                                |
| "LockTime":300,     |                                |
| "allowedTimes":5,   |                                |
| "loginLock":0       |                                |
| }                   |                                |
| }                   |                                |
| }                   |                                |
| ]                   |                                |
|:--------------------|:-------------------------------|
| Fielddescription    |                                |
| Field               | description                    |
| LockTime            | Loginlocktime                  |
| allowedTimes        | Maximumnumberofallowedattempts |
| loginLock           | Loginlockswitch                |

### Table from Page 110

| Dataexample        |
|:-------------------|
| [{                 |
| "cmd":"SetSysCfg", |
| "action":0,        |
| "param":{          |
| "SysCfg":{         |
| "loginLock":1      |

### Table from Page 111

| }                                                                 | None            | None   |
| }                                                                 |                 |        |
| }]                                                                |                 |        |
|:------------------------------------------------------------------|:----------------|:-------|
| Fielddescription                                                  |                 |        |
| Field                                                             | Description     | M/O    |
| loginLock                                                         | Loginlockswitch |        |
| Note:Youcanonlysetwhethertoenabletheloginlockfunction,thenumberof |                 |        |
| attemptsandlocktimecannotbechanged                                |                 |        |

### Table from Page 111

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetSysCfg",     |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 112

| Dataexample           | None        | None   |
|:----------------------|:------------|:-------|
| [                     |             |        |
| {                     |             |        |
| "cmd":"GetLocalLink", |             |        |
| "action":1            |             |        |
| }                     |             |        |
| ]                     |             |        |
| Fielddescription      |             |        |
| Field                 | Description | M/O    |

### Table from Page 112

| Return datacorrectly       |
|:---------------------------|
| [                          |
| {                          |
| "cmd":"GetLocalLink",      |
| "code":0,                  |
| "initial":{                |
| "LocalLink":{              |
| "activeLink":"LAN",        |
| "dns":{                    |
| "auto":1,                  |
| "dns1":"192.168.0.1",      |
| "dns2":"192.168.0.1"       |
| },                         |
| "mac":"EC:71:DB:36:8E:C7", |
| "static":{                 |
| "gateway":"192.168.0.1",   |
| "ip":"192.168.0.100",      |
| "mask":"255.255.255.0"     |
| },                         |
| "type":"DHCP"              |
| }                          |
| },                         |
| "range":{                  |
| "LocalLink":{              |
| "dns":{                    |

### Table from Page 113

| "auto":"boolean",            |
| "dns1":{                     |
| "maxLen":15                  |
| },                           |
| "dns2":{                     |
| "maxLen":15                  |
| }                            |
| },                           |
| "static":{                   |
| "gateway":{                  |
| "maxLen":15                  |
| },                           |
| "ip":{                       |
| "maxLen":15                  |
| },                           |
| "mask":{                     |
| "maxLen":15                  |
| }                            |
| },                           |
| "type":["DHCP","Static"]     |
| }                            |
| },                           |
| "value":{                    |
| "LocalLink":{                |
| "activeLink":"LAN",          |
| "dns":{                      |
| "auto":1,                    |
| "dns1":"192.168.2.1",        |
| "dns2":"114.114.114.114"     |
| },                           |
| "mac":"ec:71:db:0f:93:91",   |
| "static":{                   |
| "gateway":"192.168.2.1",     |
| "ip":"192.168.3.38",         |
| "mask":"255.255.252.0"       |
| },                           |
| "type":"DHCP"                |
| }                            |
| }                            |
| }                            |
| ]                            |
|:-----------------------------|
| Fielddescription             |

### Table from Page 114

| Field           | description                              |
|:----------------|:-----------------------------------------|
| activeLink      | Networkconnectiontype[LAN,Wi-Fi]         |
| mac             | Networkcard’shardwareaddress             |
| type            | NetworkIP’sdistrbuitingway,[DHCP,Static] |
| Static->ip      | Ipaddress                                |
| Static->gateway | Gatewayaddress                           |
| Static->mask    | Subnetmask                               |
| Dns->auto       | Whetherautogetddnsornot                  |
| Dns->dns1       | PreferredDNSServer.                      |
| Dns->dns2       | AlternateDNSserver.                      |

### Table from Page 114

| Dataexample             |
|:------------------------|
| [                       |
| {                       |
| "cmd":"SetLocalLink",   |
| "action":0,             |
| "param":{               |
| "LocalLink":{           |
| "type":"Static",        |
| "static":{              |
| "ip":"192.168.2.122",   |
| "mask":"255.255.255.0", |
| "gateway":"192.168.2.1" |
| },                      |

### Table from Page 115

| "dns":{                    | None                                     | None   |
| "auto":0,                  |                                          |        |
| "dns1":"202.96.128.166",   |                                          |        |
| "dns2":"202.96.134.133"    |                                          |        |
| }                          |                                          |        |
| }                          |                                          |        |
| }                          |                                          |        |
| }                          |                                          |        |
| ]                          |                                          |        |
|:---------------------------|:-----------------------------------------|:-------|
| Fielddescription           |                                          |        |
| Field                      | Description                              | M/O    |
| type                       | NetworkIP’sdistrbuitingway,[DHCP,Static] | O      |
| Static->ip                 | Ipaddress                                | O      |
| Static->gateway            | Gatewayaddress                           | O      |
| Static->mask               | Subnetmask                               | O      |
| Dns->auto                  | Whetherautogetddnsornot[0,1]             | O      |
| Dns->dns1                  | PreferredDNSServer.                      | O      |
| Dns->dns2                  | AlternateDNSserver.                      | O      |

### Table from Page 115

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetLocalLink",  |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 116

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetDdns", |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 116

| Return datacorrectly                    |
|:----------------------------------------|
| [                                       |
| {                                       |
| "cmd":"GetDdns",                        |
| "code":0,                               |
| "initial":{                             |
| "Ddns":{                                |
| "domain":"",                            |
| "enable":1,                             |
| "password":"",                          |
| "servAddr":"dynupdate.no-ip.com", //NVR |
| "type":"no-ip",                         |
| "userName":""                           |
| }                                       |
| },                                      |

### Table from Page 117

| "range":{                                 | None                                            |
| "Ddns":{                                  |                                                 |
| "domain":{                                |                                                 |
| "maxLen":127                              |                                                 |
| },                                        |                                                 |
| "enable":"boolean",                       |                                                 |
| "password":{                              |                                                 |
| "maxLen":127                              |                                                 |
| },                                        |                                                 |
| "servAddr":{ //NVR                        |                                                 |
| "maxLen":127,                             |                                                 |
| "servAddrList":{                          |                                                 |
| "Dyndns":"members.dyndns.org",            |                                                 |
| "no-ip":"dynupdate.no-ip.com"             |                                                 |
| }                                         |                                                 |
| },                                        |                                                 |
| "type":["no-ip","Dyndns"],                |                                                 |
| "userName":{                              |                                                 |
| "maxLen":127                              |                                                 |
| }                                         |                                                 |
| }                                         |                                                 |
| },                                        |                                                 |
| "value":{                                 |                                                 |
| "Ddns":{                                  |                                                 |
| "domain":"",                              |                                                 |
| "enable":1,                               |                                                 |
| "password":"",                            |                                                 |
| "servAddr":"dynupdate.no-ip.com", //NVR   |                                                 |
| "type":"no-ip",                           |                                                 |
| "userName":""                             |                                                 |
| }                                         |                                                 |
| }                                         |                                                 |
| }                                         |                                                 |
| ]                                         |                                                 |
|:------------------------------------------|:------------------------------------------------|
| Fielddescription                          |                                                 |
| Field                                     | description                                     |
| domain                                    | Thedomainwhichyouset.                           |
| enable                                    | Ddnsenableswitch.                               |
| type                                      | DdnsServertype.Rangeofvalueis["3322","Dyndns"]. |
| userName                                  | DdnsuserName.                                   |

### Table from Page 118

| password   | Ddnspassword.   |
|:-----------|:----------------|
| servAddr   | Serveraddress   |

### Table from Page 118

| Dataexample            | None                                  | None   |
|:-----------------------|:--------------------------------------|:-------|
| [                      |                                       |        |
| {                      |                                       |        |
| "cmd":"SetDdns",       |                                       |        |
| "param":{              |                                       |        |
| "Ddns":{               |                                       |        |
| "enable":1,            |                                       |        |
| "type":"dyndns",       |                                       |        |
| "userName":"username", |                                       |        |
| "password":"password", |                                       |        |
| "domain":"domain"      |                                       |        |
| }                      |                                       |        |
| }                      |                                       |        |
| }                      |                                       |        |
| ]                      |                                       |        |
| Fielddescription       |                                       |        |
| Field                  | Description                           | M/O    |
| domain                 | Thedomainwhichyouset.                 | O      |
| enable                 | Ddnsenableswitch.                     | O      |
| type                   | DdnsServertype.Rangeofvalueis["3322", | O      |
|                        | "Dyndns"].                            |        |
| userName               | DdnsuserName.                         | O      |

### Table from Page 119

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetDdns",       |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 119

| Dataexample       |
|:------------------|
| [                 |
| {                 |
| "cmd":"GetEmail", |
| "action":1        |
| }                 |
| ]                 |

### Table from Page 120

| Fielddescription   | None        | None   |
|:-------------------|:------------|:-------|
| Field              | Description | M/O    |

### Table from Page 120

| Return datacorrectly                                               |
|:-------------------------------------------------------------------|
| [                                                                  |
| {                                                                  |
| "cmd":"GetEmail",                                                  |
| "code":0,                                                          |
| "initial":{                                                        |
| "Email":{                                                          |
| "addr1":"",                                                        |
| "addr2":"",                                                        |
| "addr3":"",                                                        |
| "attachment":"picture",                                            |
| "interval":"5Minutes",                                             |
| "nickName":"NVR", //NVR                                            |
| "password":"",                                                     |
| "schedule":{                                                       |
| "enable":0,                                                        |
| "table":                                                           |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 1111111111111111111111111111111111111"                             |
| },                                                                 |
| "smtpPort":465,                                                    |
| "smtpServer":"smtp.gmail.com",                                     |
| "ssl":1,                                                           |
| "userName":""                                                      |
| }                                                                  |
| },                                                                 |
| "range":{                                                          |
| "Email":{                                                          |
| "addr1":{                                                          |
| "maxLen":127                                                       |
| },                                                                 |
| "addr2":{                                                          |
| "maxLen":127                                                       |
| },                                                                 |
| "addr3":{                                                          |
| "maxLen":127                                                       |

### Table from Page 122

| 1111111111111111111111111111111111111"                         | None                                          |
| },                                                             |                                               |
| "smtpPort":465,                                                |                                               |
| "smtpServer":"smtp.gmail.com",                                 |                                               |
| "ssl":1,                                                       |                                               |
| "userName":"***@sz-bcs.com.cn"                                 |                                               |
| }                                                              |                                               |
| }                                                              |                                               |
| }                                                              |                                               |
| ]                                                              |                                               |
|:---------------------------------------------------------------|:----------------------------------------------|
| Fielddescription                                               |                                               |
| Field                                                          | description                                   |
| smtpServer                                                     | Emailserverofsender,atmost127characters.      |
| smtpPort                                                       | PortofEmailserver,limit1~65535.               |
| userName                                                       | Senderaddress,atmost127characters.            |
| password                                                       | Senderpassword,atmost31characters.            |
| attachment                                                     | Thetypeofemailattachment.                     |
| ssl                                                            | Whethertoopentheencryptionmode,thetypeofsslis |
|                                                                | Boolean.                                      |
| interval                                                       | Sendmailinterval.                             |
| addr1                                                          | Recveraddress1,atmost127characters.           |
| addr2                                                          | Recveraddress2,atmost127characters.           |
| addr3                                                          | Recveraddress3,atmost127characters.           |
| Schedule->enable                                               | Whetheremailreceivethealarminformation        |
| Schedule->table                                                | Thescheduleaboutwhenemailreceivesthealarm     |
|                                                                | information                                   |
| Note:                                                          |                                               |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“GetEmailV20” |                                               |

### Table from Page 123

| Dataexample                                                        | None                                     | None   |
|:-------------------------------------------------------------------|:-----------------------------------------|:-------|
| [                                                                  |                                          |        |
| {                                                                  |                                          |        |
| "cmd":"SetEmail",                                                  |                                          |        |
| "param":{                                                          |                                          |        |
| "Email":{                                                          |                                          |        |
| "smtpServer":"smtp.exmail.qq.com",                                 |                                          |        |
| "smtpPort":25,                                                     |                                          |        |
| "userName":"xxx@sz-bcs.com.cn",                                    |                                          |        |
| "password":"xxxxxx",                                               |                                          |        |
| "attachment":"video",                                              |                                          |        |
| "ssl":0,                                                           |                                          |        |
| "interval":"5Minutes",                                             |                                          |        |
| "addr1":"xxx@sz-bcs.com.cn",                                       |                                          |        |
| "addr2":"xxx@sz-bcs.com.cn",                                       |                                          |        |
| "addr3":"xxx@sz-bcs.com.cn",                                       |                                          |        |
| "schedule":{                                                       |                                          |        |
| "enable":1,                                                        |                                          |        |
| "table":                                                           |                                          |        |
| "11111111111111111111111111111111111111111111111111111111111111111 |                                          |        |
| 111111111111111111111111111111111111111111111111111111111111111111 |                                          |        |
| 1111111111111111111111111111111"                                   |                                          |        |
| }                                                                  |                                          |        |
| }                                                                  |                                          |        |
| }                                                                  |                                          |        |
| }                                                                  |                                          |        |
| ]                                                                  |                                          |        |
| Fielddescription                                                   |                                          |        |
| Field                                                              | Description                              | M/O    |
| smtpServer                                                         | Emailserverofsender,atmost127characters. | O      |
| smtpPort                                                           | PortofEmailserver,limit1~65535.          | O      |
| userName                                                           | Senderaddress,atmost127characters.       | O      |

### Table from Page 124

| password      | Senderpassword,atmost31characters.             | O   |
|:--------------|:-----------------------------------------------|:----|
| attachment    | Thetypeofemailattachment.Rangeofvalueis["O",   | O   |
|               | "picture","video","onlyPicture"].              |     |
| Ssl           | Whethertoopentheencryptionmode,thetypeofssl    | O   |
|               | isBoolean.                                     |     |
| interval      | Sendmailinterval.Rangeofvalueis["30Seconds","1 | O   |
|               | Minute","5Minutes","10Minutes"].               |     |
| addr1         | Recveraddress1,atmost127characters.            | O   |
| addr2         | Recveraddress2,atmost127characters.            | O   |
| addr3         | Recveraddress3,atmost127characters.            | O   |
| Schedule->en  | Whetheremailreceivethealarminformation[0,1]    | O   |
| able          |                                                |     |
| Schedule->tab | Thescheduleaboutwhenemailreceivesthealarm      | O   |
| le            | information                                    |     |

### Table from Page 124

| Return datacorrectly                                           | None         |
|:---------------------------------------------------------------|:-------------|
| [                                                              |              |
| {                                                              |              |
| "cmd":"SetEmail",                                              |              |
| "code":0,                                                      |              |
| "value":{                                                      |              |
| "rspCode":200                                                  |              |
| }                                                              |              |
| }                                                              |              |
| ]                                                              |              |
| Fielddescription                                               |              |
| Field                                                          | description  |
| rspCode                                                        | Responsecode |
| Note:                                                          |              |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“SetEmailV20” |              |

### Table from Page 125

| Data example          | None        | None   |
|:----------------------|:------------|:-------|
| [{                    |             |        |
| "cmd": "GetEmailV20", |             |        |
| "param": {            |             |        |
| "channel": 0          |             |        |
| }                     |             |        |
| }]                    |             |        |
| Fielddescription      |             |        |
| Field                 | Description | M/O    |

### Table from Page 125

| Return data correctly          |
|:-------------------------------|
| [                              |
| {                              |
| "cmd" :"GetEmailV20",          |
| "code" : 0,                    |
| "value" : {                    |
| "Email": {                     |
| "addr1" : "xxx@sz-bcs.com.cn", |
| "addr2" : "xxx@sz-bcs.com.cn", |
| "addr3" : "xxx@sz-bcs.com.cn", |
| "attachmentType" : 2,          |
| "diskErrorAlert" :0,           |

### Table from Page 126

| "diskFullAlert" :0,                                                   | None                                         |
| "enable" : 0,                                                         |                                              |
| "interval" : "5Minutes",                                              |                                              |
| "nickName" : "NVR",                                                   |                                              |
| "password" : "xxxxxx",                                                |                                              |
| "schedule" : {                                                        |                                              |
| "channel" : 0,                                                        |                                              |
| "table" : {                                                           |                                              |
| "AI_PEOPLE" :                                                         |                                              |
| "000000000000000000000000000000000000000000000000000000000000000000   |                                              |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                                              |
| 00000000000000000000000000000000000",                                 |                                              |
| "AI_VEHICLE" :                                                        |                                              |
| "000000000000000000000000000000000000000000000000000000000000000000   |                                              |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                                              |
| 00000000000000000000000000000000000",                                 |                                              |
| "MD" :                                                                |                                              |
| "111111111111111111111111111111111111111111111111111111111111111111   |                                              |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                                              |
| 11111111111111111111111111111111111",                                 |                                              |
| "VL" :                                                                |                                              |
| "000000000000000000000000000000000000000000000000000000000000000000   |                                              |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                                              |
| 00000000000000000000000000000000000"                                  |                                              |
| }                                                                     |                                              |
| },                                                                    |                                              |
| "smtpPort": 25,                                                       |                                              |
| "smtpServer" : "smtp.exmail.qq.com",                                  |                                              |
| "ssl" : 0,                                                            |                                              |
| "supportTextType" : 1,                                                |                                              |
| "supportVideo" : 1,                                                   |                                              |
| "textType" : 1,                                                       |                                              |
| "userName" : "xxx@sz-bcs.com.cn"                                      |                                              |
| }                                                                     |                                              |
| }                                                                     |                                              |
| }                                                                     |                                              |
| ]                                                                     |                                              |
|:----------------------------------------------------------------------|:---------------------------------------------|
| Fielddescription                                                      |                                              |
| Field                                                                 | description                                  |
| smtpServer                                                            | Email server of sender,at most127characters. |
| smtpPort                                                              | Port ofEmail server,limit1~65535.            |

### Table from Page 127

| userName         | Sender address,at most 127characters.               |
|:-----------------|:----------------------------------------------------|
| password         | Sender password,at most31characters.                |
| attachmentType   | The type ofemail attachment.                        |
| Ssl              | Whether toopen theencryption mode,the type ofssl is |
|                  | Boolean.                                            |
| interval         | Send mail interval.                                 |
| addr1            | Recver address1, at most 127characters.             |
| addr2            | Recver address2, at most 127characters.             |
| addr3            | Recver address3, at most 127characters.             |
| Schedule->enable | Start usingschedule                                 |
| Schedule->table  | Table ofAlarmtype                                   |
| nickname         | Corresponds tothe username                          |
| supportTextType  | Support thetype of Test                             |
| supportVideo     | Support thetype of video                            |
| textType         | Textof type                                         |

### Table from Page 127

| Data example          |
|:----------------------|
| [{                    |
| "cmd": "SetEmailV20", |
| "param": {            |

### Table from Page 128

| "Email": {                            | None                                               | None   |
| "ssl": 0,                             |                                                    |        |
| "smtpPort": 25,                       |                                                    |        |
| "smtpServer": "smtp.exmail.qq.com",   |                                                    |        |
| "userName": "xxx@sz-bcs.com.cn",      |                                                    |        |
| "nickName": "",                       |                                                    |        |
| "addr1": "xxx@sz-bcs.com.cn",         |                                                    |        |
| "addr2": "xxx@sz-bcs.com.cn",         |                                                    |        |
| "addr3": "xxx@sz-bcs.com.cn",         |                                                    |        |
| "interval": "5Minutes"                |                                                    |        |
| }                                     |                                                    |        |
| }                                     |                                                    |        |
| }]                                    |                                                    |        |
|:--------------------------------------|:---------------------------------------------------|:-------|
| Fielddescription                      |                                                    |        |
| Field                                 | Description                                        | M/O    |
| smtpServer                            | Emailserver ofsender, at most127characters.        | O      |
| smtpPort                              | Portof Emailserver, limit1~65535.                  | O      |
| userName                              | Senderaddress, at most 127characters.              | O      |
| password                              | Senderpassword, at most31characters.               | O      |
| nickName                              |                                                    | O      |
| Ssl                                   | Whethertoopen theencryptionmode, thetype ofssl is  | O      |
|                                       | Boolean.                                           |        |
| interval                              | Send mailinterval. Range ofvalue is ["30 Seconds", | O      |
|                                       | "1Minute", "5 Minutes", "10 Minutes"].             |        |
| addr1                                 | Recver address1,at most127characters.              | O      |
| addr2                                 | Recver address2,at most127characters.              | O      |
| addr3                                 | Recver address3,at most127characters.              | O      |
| Schedule->en                          | Startusing schedule                                | O      |
| able                                  |                                                    |        |
| Schedule->tab                         | TableofAlarmtype                                   | O      |
| le                                    |                                                    |        |

### Table from Page 129

| Return data correctly   | None         |
|:------------------------|:-------------|
| [                       |              |
| {                       |              |
| "cmd" :"SetEmailV20",   |              |
| "code" : 0,             |              |
| "value" : {             |              |
| "rspCode" :200          |              |
| }                       |              |
| }                       |              |
| ]                       |              |
| Fielddescription        |              |
| Field                   | description  |
| rspCode                 | Responsecode |

### Table from Page 129

| Dataexample                    |
|:-------------------------------|
| [{                             |
| "cmd":"TestEmail",             |
| "param":{                      |
| "Email":{                      |
| "addr1":"****@sz-bcs.com.cn",  |
| "addr2":"",                    |
| "addr3":"",                    |
| "interval":"5Minutes",         |
| "nickName":"000",              |
| "password":"lwmypvelvexadfab", |

### Table from Page 130

| "smtpPort":465,                                                   | None                                        | None   |
| "smtpServer":"smtp.qq.com",                                       |                                             |        |
| "ssl":1,                                                          |                                             |        |
| "userName":"**********@qq.com"                                    |                                             |        |
| }                                                                 |                                             |        |
| }                                                                 |                                             |        |
| }]                                                                |                                             |        |
|:------------------------------------------------------------------|:--------------------------------------------|:-------|
| Fielddescription                                                  |                                             |        |
| Field                                                             | Description                                 | M/O    |
| smtpServer                                                        | Emailserverofsender,atmost127characters.    | M      |
| smtpPort                                                          | PortofEmailserver,limit1~65535.             | M      |
| userName                                                          | Senderaddress,atmost127characters.          | M      |
| password                                                          | Senderpassword,atmost31characters.          | O      |
| ssl                                                               | Whethertoopentheencryptionmode,thetypeofssl | M      |
|                                                                   | isBoolean.                                  |        |
| addr1                                                             | Recveraddress1,atmost127characters.         | O      |
| addr2                                                             | Recveraddress2,atmost127characters.         | O      |
| addr3                                                             | Recveraddress3,atmost127characters.         | O      |
| nickName                                                          | Correspondstotheusername                    | O      |
| Note:Atleastoneofthethreeaddresses(addr1,addr2,addr3)iscompleted. |                                             |        |

### Table from Page 130

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"TestEmail",     |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 131

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetFtp",  |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 131

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetFtp",        |
| "code":0,              |
| "initial":{            |
| "Ftp":{                |
| "anonymous":0,         |
| "autoDir":1, //NVR     |
| "interval":30,         |
| "maxSize":100,         |
| "mode":0, //NVR        |

### Table from Page 133

| "maxLen":168,                                                        | None        |
| "minLen":168                                                         |             |
| }                                                                    |             |
| },                                                                   |             |
| "server":{                                                           |             |
| "maxLen":127                                                         |             |
| },                                                                   |             |
| "streamType":{                                                       |             |
| "max":2,                                                             |             |
| "min":0                                                              |             |
| },                                                                   |             |
| "userName":{                                                         |             |
| "maxLen":127                                                         |             |
| }                                                                    |             |
| }                                                                    |             |
| },                                                                   |             |
| "value":{                                                            |             |
| "Ftp":{                                                              |             |
| "anonymous":0,                                                       |             |
| "autoDir":1, //NVR                                                   |             |
| "interval":30,                                                       |             |
| "maxSize":100,                                                       |             |
| "mode":0,                                                            |             |
| "password":"",                                                       |             |
| "port":21,                                                           |             |
| "remoteDir":"",                                                      |             |
| "schedule":{                                                         |             |
| "enable":1,                                                          |             |
| "table":                                                             |             |
| "22222222222222222222222222222222222222222222222222222222222222222   |             |
| 222222222222222222222222222222222222222222222222222222222222222222   |             |
| 2222222222222222222222222222222222222"                               |             |
| },                                                                   |             |
| "server":"",                                                         |             |
| "streamType":0,                                                      |             |
| "userName":""                                                        |             |
| }                                                                    |             |
| }                                                                    |             |
| }                                                                    |             |
| ]                                                                    |             |
|:---------------------------------------------------------------------|:------------|
| Fielddescription                                                     |             |
| Field                                                                | Description |

### Table from Page 134

| initial                                                      | TheinitialvalueoftheFtpfield.                      |
|:-------------------------------------------------------------|:---------------------------------------------------|
| range                                                        | TherangeoftheFtpfield.                             |
| value                                                        | TherealvalueoftheFtpfield.                         |
| server                                                       | FTPserver,canfillintheIPaddressordomainname.       |
|                                                              | Atmost127characters.                               |
| port                                                         | PortofFTPServer,Limit1~65535.                      |
| anonymous                                                    | Whetheranonymousornot                              |
| userName                                                     | FTPaccountname.                                    |
| password                                                     | FTPaccountpassword.                                |
| remoteDir                                                    | FTProotdirectory.                                  |
| maxSize                                                      | MaximumsizeofFTPfile.                              |
| streamType                                                   | Thetypesoftheuploadingfiles.0isforuploadingboth    |
|                                                              | picturesandvideos,and1isforuploadingpicturesonly.  |
| interval                                                     | WhenstreamType=0,intervalstandsforthetimeofpost    |
|                                                              | record,therangeisbetween30to1800seconds.           |
|                                                              | WhenstreamType=1,intervalstandsforthetimeinterval, |
|                                                              | therangeisbetween1to1800seconds.                   |
| Schedule->enable                                             | Whetherftpreceivesthealarminformationornot.        |
| Schedule->table                                              | Thescheduleaboutwhenftpreceivesthealarminformation |
| autoDir                                                      |                                                    |
| Note:                                                        |                                                    |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“GetFtpV20” |                                                    |

### Table from Page 135

| Dataexample                                                        | None                                         | None   |
|:-------------------------------------------------------------------|:---------------------------------------------|:-------|
| [{                                                                 |                                              |        |
| "cmd":"SetFtp",                                                    |                                              |        |
| "param":{                                                          |                                              |        |
| "Ftp":{                                                            |                                              |        |
| "anonymous":0,                                                     |                                              |        |
| "autoDir":1,                                                       |                                              |        |
| "bpicSingle":0,                                                    |                                              |        |
| "bvideoSingle":0,                                                  |                                              |        |
| "interval":30,                                                     |                                              |        |
| "maxSize":100,                                                     |                                              |        |
| "mode":0,                                                          |                                              |        |
| "onlyFtps":0,                                                      |                                              |        |
| "password":"",                                                     |                                              |        |
| "picInterval":60,                                                  |                                              |        |
| "picName":"",                                                      |                                              |        |
| "port":21,                                                         |                                              |        |
| "remoteDir":"",                                                    |                                              |        |
| "schedule":{                                                       |                                              |        |
| "enable":1,                                                        |                                              |        |
| "table":                                                           |                                              |        |
| "11111111111111111111111111111111111111111111111111111111111111111 |                                              |        |
| 111111111111111111111111111111111111111111111111111111111111111111 |                                              |        |
| 1111111111111111111111111111111111111"                             |                                              |        |
| },                                                                 |                                              |        |
| "server":"",                                                       |                                              |        |
| "size":"",                                                         |                                              |        |
| "streamType":0,                                                    |                                              |        |
| "userName":"",                                                     |                                              |        |
| "videoName":""                                                     |                                              |        |
| }                                                                  |                                              |        |
| }                                                                  |                                              |        |
| }]                                                                 |                                              |        |
| Fielddescription                                                   |                                              |        |
| Field                                                              | Description                                  | M/O    |
| server                                                             | FTPserver,canfillintheIPaddressordomainname. | O      |
| port                                                               | PortofFTPServer.                             | O      |

### Table from Page 136

| aonymous                                                     | Whetheranonymousornot                          | O   |
|:-------------------------------------------------------------|:-----------------------------------------------|:----|
| userName                                                     | FTPaccountname.Whenthevalueofanonymousis       | O   |
| (Dependon                                                    | 0,theuserNamefieldisnecessary.                 |     |
| anonymous)                                                   |                                                |     |
| Password                                                     | FTPaccountpassword.FTPaccountname.Whenthe      | O   |
| (Dependon                                                    | valueofaOnymousis0,thepasswordfieldis          |     |
| anonymous)                                                   | necessary.                                     |     |
| remoteDir                                                    | FTProotdirectory.                              | O   |
| maxSize                                                      | MaximumsizeofFTPfile.                          | O   |
| streamType                                                   | Thetypeoftheuploadingfiles.0isforuploadingboth | O   |
|                                                              | picturesandvideos,and1isforuploadingpictures   |     |
|                                                              | only.                                          |     |
| interval                                                     | WhenstreamType=0,intervalstandsforthetimeof    | O   |
|                                                              | postrecord,therangeisbetween30to1800seconds.   |     |
|                                                              | WhenstreamType=1,intervalstandsforthetime      |     |
|                                                              | interval,therangeisbetween1to1800seconds.      |     |
| Schedule->en                                                 | Whetherftpreceivethealarminformation[0,1]      | O   |
| able                                                         |                                                |     |
| Schedule->tab                                                | Thescheduleaboutwhenftpreceivesthealarm        | O   |
| le                                                           | information                                    |     |
| Note:                                                        |                                                |     |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“SetFtpV20” |                                                |     |

### Table from Page 136

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetFtp",        |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |

### Table from Page 137

| }                                    | None         |
| ]                                    |              |
|:-------------------------------------|:-------------|
| Fielddescription                     |              |
| Field                                | Description  |
| rspCode                              | Responsecode |
| Note:Thiscommandsupportsmodel52Xonly |              |

### Table from Page 137

| Data example       | None        | None   |
|:-------------------|:------------|:-------|
| [                  |             |        |
| {                  |             |        |
| "cmd":"GetFtpV20", |             |        |
| "action":1         |             |        |
| }                  |             |        |
| ]                  |             |        |
| Fielddescription   |             |        |
| Field              | Description | M/O    |

### Table from Page 137

| Return data correctly   |
|:------------------------|
| [                       |
| {                       |
| "cmd" :"GetFtpV20",     |
| "code" : 0,             |

### Table from Page 142

| 11111111111111111111111111111111111",                                 | None                                                       |
| "TIMING" :                                                            |                                                            |
| "000000000000000000000000000000000000000000000000000000000000000000   |                                                            |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                                                            |
| 00000000000000000000000000000000000"                                  |                                                            |
| }                                                                     |                                                            |
| },                                                                    |                                                            |
| "server" :"192.168.0.132",                                            |                                                            |
| "streamType" : 3,                                                     |                                                            |
| "userName" : "ft***er",                                               |                                                            |
| "videoName" : ""                                                      |                                                            |
| }                                                                     |                                                            |
| }                                                                     |                                                            |
| }                                                                     |                                                            |
| ]                                                                     |                                                            |
|:----------------------------------------------------------------------|:-----------------------------------------------------------|
| Fielddescription                                                      |                                                            |
| Field                                                                 | Description                                                |
| initial                                                               | The initialvalueof theFtp field.                           |
| range                                                                 | The range oftheFtp field.                                  |
| value                                                                 | The real value ofthe Ftpfield.                             |
| server                                                                | FTP server, can fill in theIP address ordomain name.       |
|                                                                       | At most 127characters.                                     |
| port                                                                  | Port ofFTP Server, Limit 1~65535.                          |
| Anonymous                                                             | Whether tobe anonymous                                     |
| userName                                                              | FTP account name.                                          |
| password                                                              | FTP account password.                                      |
| remoteDir                                                             | FTP root directory.                                        |
| maxSize                                                               | Maximum size ofFTP file.                                   |
| streamType                                                            | The types oftheuploading files. 0is for uploading both     |
|                                                                       | pictures andvideos, and 1isfor uploading pictures only.    |
| interval                                                              | When streamType=0, interval stands for thetimeof post      |
|                                                                       | record, the range is between 30to 1800seconds.             |
|                                                                       | When streamType=1, interval stands for thetimeinterval,the |
|                                                                       | range is between 1to 1800seconds.                          |

### Table from Page 143

| Schedule->enable   | Whether Startusing schedule ornot                            |
|:-------------------|:-------------------------------------------------------------|
| Schedule->table    | Table ofAlarm type                                           |
| autoDir            | Whether tocreate directories automatically                   |
|                    | 0:Create directories byyear, month and day, like:            |
|                    | YYYY-MM-DD                                                   |
|                    | 1:0:Create directories byyear, month,like:                   |
|                    | YYYY-MM                                                      |
| mode               | Transport mode                                               |
|                    | 0:Chooseactive modeorpassive modeautonomously                |
|                    | 1:Active mode                                                |
|                    | 2:Passivemode                                                |
| onlyFtps           | Ftps switch,Whethertoselect theencryption mode               |
| picCaptureMode     | Image resolution mode                                        |
|                    | 0:Aclear picture                                             |
|                    | 1:Standard image                                             |
|                    | 2:Smooth image                                               |
|                    | Note: Clearpictures have thehighest resolution, smooth       |
|                    | pictures havethe lowest resolution                           |
| picHeight          | Pictureheight                                                |
|                    | Note: Thewidth and height oftheimage are not arbitrary and   |
|                    | need to match theresolution supported bytheimage             |
| picWidth           | Pitcurewidth                                                 |
| bpicSingle         | Image upload mode                                            |
|                    | 0:All images are retained and willnot bedeleted              |
|                    | 1:Only thelatest image will bekept, and theothers willbe     |
|                    | replaced                                                     |
|                    | 2:Theother replacement strategy, which is different, instead |
|                    | ofreplacing directly, is tofirst storethesecond image and    |
|                    | then deletethefirst one                                      |
| bvideoSingle       | Video upload mode                                            |

### Table from Page 144

|             | 0:All videos are retained and will not bedeleted               |
|             | 1:Only thelatest video will bekept, and theothers will be      |
|             | replaced                                                       |
|             | 2:Theother replacement strategy, which is different, instead   |
|             | ofreplacing directly, is tofirst storethesecond video and      |
|             | then deletethefirst one                                        |
|:------------|:---------------------------------------------------------------|
| picInterval | Image upload interval                                          |

### Table from Page 144

| Data example               |
|:---------------------------|
| [{                         |
| "cmd": "SetFtpV20",        |
| "param": {                 |
| "Ftp":{                    |
| "anonymous": 0,            |
| "autoDir": 1,              |
| "bpicSingle": 0,           |
| "bvideoSingle": 0,         |
| "enable": 1,               |
| "interval": 30,            |
| "maxSize": 100,            |
| "mode": 0,                 |
| "onlyFtps": 1,             |
| "password": "***********", |
| "picCaptureMode": 3,       |

### Table from Page 145

| "picHeight": 1920,                                                    | None                                                | None   |
| "picInterval": 60,                                                    |                                                     |        |
| "picName": "",                                                        |                                                     |        |
| "picWidth": 2304,                                                     |                                                     |        |
| "port": 21,                                                           |                                                     |        |
| "remoteDir": "hello",                                                 |                                                     |        |
| "schedule": {                                                         |                                                     |        |
| "channel": 0,                                                         |                                                     |        |
| "table": {                                                            |                                                     |        |
| "AI_DOG_CAT":                                                         |                                                     |        |
| "111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 11111111111111111111111111111111111",                                 |                                                     |        |
| "AI_PEOPLE":                                                          |                                                     |        |
| "111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 11111111111111111111111111111111111",                                 |                                                     |        |
| "AI_VEHICLE":                                                         |                                                     |        |
| "111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 11111111111111111111111111111111111",                                 |                                                     |        |
| "MD":                                                                 |                                                     |        |
| "111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                                                     |        |
| 11111111111111111111111111111111111",                                 |                                                     |        |
| "TIMING":                                                             |                                                     |        |
| "000000000000000000000000000000000000000000000000000000000000000000   |                                                     |        |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                                                     |        |
| 00000000000000000000000000000000000"                                  |                                                     |        |
| }                                                                     |                                                     |        |
| },                                                                    |                                                     |        |
| "server": "192.168.1.236",                                            |                                                     |        |
| "streamType": 6,                                                      |                                                     |        |
| "userName": "ft***er",                                                |                                                     |        |
| "videoName": "sdfs"                                                   |                                                     |        |
| }                                                                     |                                                     |        |
| }                                                                     |                                                     |        |
| }]                                                                    |                                                     |        |
|:----------------------------------------------------------------------|:----------------------------------------------------|:-------|
| Fielddescription                                                      |                                                     |        |
| Field                                                                 | Description                                         | M/O    |
| server                                                                | FTP server, can fillin theIP address ordomain name. | O      |
| port                                                                  | Portof FTP Server.                                  | O      |

### Table from Page 146

| anonymous     | Whethertobe anoymous ornot                           | O   |
|:--------------|:-----------------------------------------------------|:----|
| userName      | FTP account name. When thevalue ofanonymous is 0,    | O   |
| (Depend on    | theuserName field is necessary.                      |     |
| anonymous)    |                                                      |     |
| Password      | FTP account password. FTP account name. When the     | O   |
| (Depend on    | valueofanonymous is 0,thepassword field is           |     |
| anonymous)    | necessary.                                           |     |
| remoteDir     | FTP root directory.                                  | O   |
| maxSize       | MaximumsizeofFTP file.                               | O   |
| streamType    | Thetype ofthe uploading files. 0isfor uploading both | O   |
|               | pictures and videos, and 1is foruploading pictures   |     |
|               | only.                                                |     |
| interval      | WhenstreamType=0, interval stands for thetimeof      | O   |
|               | postrecord, the range is between 30to 1800seconds.   |     |
|               | WhenstreamType=1, interval stands for thetime        |     |
|               | interval,therange is between 1to 1800seconds.        |     |
| Schedule->en  | WhetherStart usingschedule or not                    | O   |
| able          |                                                      |     |
| Schedule->tab | TableofAlarm type                                    | O   |
| le            |                                                      |     |
| mode          | Transport mode                                       |     |

### Table from Page 146

| Return data correctly   |
|:------------------------|
| [                       |
| {                       |
| "cmd" :"SetFtp",        |
| "code" : 0,             |
| "value" : {             |
| "rspCode" :200          |
| }                       |
| }                       |

### Table from Page 147

| ]                | None         |
|:-----------------|:-------------|
| Fielddescription |              |
| Field            | description  |
| rspCode          | Responsecode |

### Table from Page 147

| Dataexample               |
|:--------------------------|
| [{                        |
| "cmd":"TestFtp",          |
| "action":0,               |
| "param":{                 |
| "Ftp":{                   |
| "server":"192.168.0.132", |
| "port":21,                |
| "anonymous":0,            |
| "mode":2,                 |
| "userName":"ftpuser",     |
| "password":"000000",      |
| "remoteDir":"fadad",      |
| "onlyFtps":1,             |
| "bpicSingle":2,           |
| "bvideoSingle":2          |
| }                         |
| }                         |
| }]                        |

### Table from Page 148

| Fielddescription   | None                                         | None   |
|:-------------------|:---------------------------------------------|:-------|
| Field              | Description                                  | M/O    |
| server             | FTPserver,canfillintheIPaddressordomainname. | M      |
|                    | Atmost127characters.                         |        |
| port               | PortofFTPServer,Limit1~65535.                | M      |
| anonymous          | Whetheranonymousornot                        | M      |
| userName           | FTPaccountname.FTPaccountpassword.FTP        | O      |
| (Dependon          | accountname.Whenthevalueofanonymousis0,the   |        |
| anonymous)         | userNamefieldisnecessary.                    |        |
| Password           | FTPaccountpassword.FTPaccountpassword.FTP    | O      |
| (Dependon          | accountname.Whenthevalueofanonymousis0,the   |        |
| anonymous)         | passwordfieldisnecessary.                    |        |
| remoteDir          | FTProotdirectory.                            | M      |
| mode               | Transporttype                                | M      |
| onlyFtps           | Ftpsswitch                                   | M      |
| bpicSingle         | Imageuploadmode                              | M      |
| bvideoSingle       | Videouploadmode                              | M      |

### Table from Page 148

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"TestFtp",       |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | Description  |
| rspCode                | Responsecode |

### Table from Page 149

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetNtp",  |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 149

| Return datacorrectly    |
|:------------------------|
| [                       |
| {                       |
| "cmd":"GetNtp",         |
| "code":0,               |
| "initial":{             |
| "Ntp":{                 |
| "enable":0,             |
| "interval":1440,        |
| "port":123,             |
| "server":"pool.ntp.org" |
| }                       |

### Table from Page 150

| },                        | None                                             |
| "range":{                 |                                                  |
| "Ntp":{                   |                                                  |
| "enable":"boolean",       |                                                  |
| "interval":{              |                                                  |
| "max":65535,              |                                                  |
| "min":60                  |                                                  |
| },                        |                                                  |
| "port":{                  |                                                  |
| "max":65535,              |                                                  |
| "min":1                   |                                                  |
| },                        |                                                  |
| "server":{                |                                                  |
| "maxLen":127              |                                                  |
| }                         |                                                  |
| }                         |                                                  |
| },                        |                                                  |
| "value":{                 |                                                  |
| "Ntp":{                   |                                                  |
| "enable":0,               |                                                  |
| "interval":1440,          |                                                  |
| "port":123,               |                                                  |
| "server":"pool.ntp.org"   |                                                  |
| }                         |                                                  |
| }                         |                                                  |
| }                         |                                                  |
| ]                         |                                                  |
|:--------------------------|:-------------------------------------------------|
| Fielddescription          |                                                  |
| Field                     | Description                                      |
| enable                    | NTPswitch,Thevalueof1representstheopen,andthe0is |
|                           | theopposite.                                     |
| server                    | NTPserver,canfillintheIPaddressordomainname.     |
| port                      | PortofNTPServer.                                 |
| interval                  | Timesynchronizationinterval.Limit10~65535,and0on |
|                           | behalfoftheimmediatesynchronization.             |

### Table from Page 151

| Dataexample              | None                                           | None   |
|:-------------------------|:-----------------------------------------------|:-------|
| [                        |                                                |        |
| {                        |                                                |        |
| "cmd":"SetNtp",          |                                                |        |
| "param":{                |                                                |        |
| "Ntp":{                  |                                                |        |
| "enable":1,              |                                                |        |
| "server":"pool.ntp.org", |                                                |        |
| "port":123,              |                                                |        |
| "interval":1440          |                                                |        |
| }                        |                                                |        |
| }                        |                                                |        |
| }                        |                                                |        |
| ]                        |                                                |        |
| Fielddescription         |                                                |        |
| Field                    | Description                                    | M/O    |
| enable                   | NTPswitch,thevalueof1representstheopen,and     | O      |
|                          | the0istheopposite.                             |        |
| server                   | NTPserver,canfillintheIPaddressordomainname.   | O      |
| port                     | PortofNTPServer.                               | O      |
| interval                 | Timesynchronizationinterval.Limit10~65535,and0 | O      |
|                          | onbehalfoftheimmediatesynchronization.         |        |

### Table from Page 152

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetNtp",        |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | Description  |
| rspCode                | Responsecode |

### Table from Page 152

| Dataexample         | None        | None   |
|:--------------------|:------------|:-------|
| [                   |             |        |
| {                   |             |        |
| "cmd":"GetNetPort", |             |        |
| "action":1          |             |        |
| }                   |             |        |
| ]                   |             |        |
| Fielddescription    |             |        |
| Field               | Description | M/O    |

### Table from Page 153

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"GetNetPort",    |              |
| "code":0,              |              |
| "value":{              |              |
| "NetPort":{            |              |
| "httpEnable":0,        |              |
| "httpPort":80,         |              |
| "httpsEnable":1,       |              |
| "httpsPort":443,       |              |
| "mediaPort":9000,      |              |
| "onvifEnable":1,       |              |
| "onvifPort":8000,      |              |
| "rtmpEnable":0,        |              |
| "rtmpPort":1935,       |              |
| "rtspEnable":1,        |              |
| "rtspPort":554         |              |
| }                      |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | Description  |
| httpPort               | Portofhttp.  |
| httpsPort              | Portofhttps. |
| mediaPort              | Portofmedia. |
| onvifPort              | Portofonvif. |
| rtspPort               | Portofrtsp.  |
| rtmpPort               | Portofrtmp.  |
| httpEnable             | httpswitch   |
| httpsEnable            | httpsswitch  |
| rtmpEnable             | Rtmpswitch   |
| rtspEnable             | Rtspswitch   |
| onvifEnable            | Onvifswitch  |

### Table from Page 154

| Dataexample         | None         | None   |
|:--------------------|:-------------|:-------|
| [{                  |              |        |
| "cmd":"SetNetPort", |              |        |
| "param":{           |              |        |
| "NetPort":{         |              |        |
| "httpEnable":0,     |              |        |
| "httpPort":80,      |              |        |
| "httpsEnable":1,    |              |        |
| "httpsPort":443,    |              |        |
| "mediaPort":9000,   |              |        |
| "onvifEnable":1,    |              |        |
| "onvifPort":8000,   |              |        |
| "rtmpEnable":0,     |              |        |
| "rtmpPort":1935,    |              |        |
| "rtspEnable":1,     |              |        |
| "rtspPort":554      |              |        |
| }                   |              |        |
| }                   |              |        |
| }]                  |              |        |
| Fielddescription    |              |        |
| Field               | Description  | M/O    |
| httpPort            | Portofhttp.  | O      |
| httpsPort           | Portofhttps. | O      |
| mediaPort           | Portofmedia. | O      |
| onvifPort           | Portofonvif. | O      |

### Table from Page 155

| rtspPort   | Portofrtsp.   | O   |
|:-----------|:--------------|:----|
| rtmpPort   | Portofrtmp.   | O   |

### Table from Page 155

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetNetPort",    |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| FieldDescription       |              |
| Field                  | Description  |
| rspCode                | Responsecode |

### Table from Page 155

| Dataexample      |
|:-----------------|
| [                |
| {                |
| "cmd":"GetUpnp", |
| "action":1       |
| }                |

### Table from Page 156

| ]                | None        | None   |
|:-----------------|:------------|:-------|
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 156

| Return datacorrectly   | None                                              |
|:-----------------------|:--------------------------------------------------|
| [                      |                                                   |
| {                      |                                                   |
| "cmd":"GetUpnp",       |                                                   |
| "code":0,              |                                                   |
| "initial":{            |                                                   |
| "Upnp":{               |                                                   |
| "enable":0             |                                                   |
| }                      |                                                   |
| },                     |                                                   |
| "range":{              |                                                   |
| "Upnp":{               |                                                   |
| "enable":"boolean"     |                                                   |
| }                      |                                                   |
| },                     |                                                   |
| "value":{              |                                                   |
| "Upnp":{               |                                                   |
| "enable":0             |                                                   |
| }                      |                                                   |
| }                      |                                                   |
| }                      |                                                   |
| ]                      |                                                   |
| Fielddescription       |                                                   |
| Field                  | Description                                       |
| enable                 | Upnpswitch,Thevalueof1representstheopen,andthe0is |
|                        | theopposite.                                      |

### Table from Page 157

| Dataexample      | None                                        | None   |
|:-----------------|:--------------------------------------------|:-------|
| [                |                                             |        |
| {                |                                             |        |
| "cmd":"SetUpnp", |                                             |        |
| "param":{        |                                             |        |
| "Upnp":{         |                                             |        |
| "enable":1       |                                             |        |
| }                |                                             |        |
| }                |                                             |        |
| }                |                                             |        |
| ]                |                                             |        |
| Fielddescription |                                             |        |
| Field            | Description                                 | M/O    |
| enable           | Upnpswitch,Thevalueof1representstheopen,and | O      |
|                  | the0istheopposite.                          |        |

### Table from Page 157

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetUpnp",       |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 158

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetWifi", |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 158

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetWifi",       |
| "code":0,              |
| "initial":{            |
| "Wifi":{               |
| "password":"",         |
| "ssid":""              |
| }                      |
| },                     |
| "range":{              |

### Table from Page 159

| "Wifi":{                    | None                            |
| "password":{                |                                 |
| "maxLen":127                |                                 |
| },                          |                                 |
| "ssid":{                    |                                 |
| "maxLen":127                |                                 |
| }                           |                                 |
| }                           |                                 |
| },                          |                                 |
| "value":{                   |                                 |
| "Wifi":{                    |                                 |
| "password":"***********",   |                                 |
| "ssid":"reolink_pyc"        |                                 |
| }                           |                                 |
| }                           |                                 |
| }                           |                                 |
| ]                           |                                 |
|:----------------------------|:--------------------------------|
| Fielddescription            |                                 |
| Field                       | description                     |
| ssid                        | Thenameofthewirelessnetwork     |
| password                    | Thepasswordofthewirelessnetwork |

### Table from Page 159

| Dataexample      |
|:-----------------|
| [                |
| {                |
| "cmd":"SetWifi", |

### Table from Page 160

| "param":{             | None                            | None   |
| "Wifi":{              |                                 |        |
| "ssid":"ssid",        |                                 |        |
| "password":"000000"   |                                 |        |
| }                     |                                 |        |
| }                     |                                 |        |
| }                     |                                 |        |
| ]                     |                                 |        |
|:----------------------|:--------------------------------|:-------|
| Fielddescription      |                                 |        |
| Field                 | Description                     | M/O    |
| ssid                  | Thenameofthewirelessnetwork     | O      |
| password              | Thepasswordofthewirelessnetwork | O      |

### Table from Page 160

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetWifi",       |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 161

| Dataexample           | None                            | None   |
|:----------------------|:--------------------------------|:-------|
| [                     |                                 |        |
| {                     |                                 |        |
| "cmd":"TestWifi",     |                                 |        |
| "param":{             |                                 |        |
| "Wifi":{              |                                 |        |
| "ssid":"ssid",        |                                 |        |
| "password":"password" |                                 |        |
| }                     |                                 |        |
| }                     |                                 |        |
| }                     |                                 |        |
| ]                     |                                 |        |
| Fielddescription      |                                 |        |
| Field                 | Description                     | M/O    |
| ssid                  | Thenameofthewirelessnetwork     | M      |
| password              | Thepasswordofthewirelessnetwork | O      |

### Table from Page 161

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"TestWifi",      |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 162

| Dataexample       | None        | None   |
|:------------------|:------------|:-------|
| [                 |             |        |
| {                 |             |        |
| "cmd":"ScanWifi", |             |        |
| "param":{}        |             |        |
| }                 |             |        |
| ]                 |             |        |
| Fielddescription  |             |        |
| Field             | Description | M/O    |

### Table from Page 162

| Return datacorrectly                     |
|:-----------------------------------------|
| [                                        |
| {                                        |
| "cmd":"ScanWifi",                        |
| "code":0,                                |
| "value":{                                |
| "Wifi":[                                 |
| {                                        |
| "bencrypt":1,                            |
| "signal":4,                              |
| "ssid":"HUAWEI-D1FC"                     |
| },                                       |
| ...//Theremaybemultiplewirelessnetworks. |
| ]                                        |
| }                                        |

### Table from Page 163

| }                | None                     |
| ]                |                          |
|:-----------------|:-------------------------|
| Fielddescription |                          |
| Field            | description              |
| signal           | Wirelesssignalstrength   |
|                  | (1:signal<=-60)          |
|                  | (2:signal<=-50)          |
|                  | (3:signal<=-40)          |
|                  | (4:signal>-40)           |
| ssid             | Thenameofwirelessnetwork |
| bencrypt         |                          |

### Table from Page 163

| Data example           | None        | None   |
|:-----------------------|:------------|:-------|
| [                      |             |        |
| {                      |             |        |
| "cmd":"GetWifiSignal", |             |        |
| "action":1             |             |        |
| }                      |             |        |
| ]                      |             |        |
| Fielddescription       |             |        |
| Field                  | Description | M/O    |

### Table from Page 164

| Return data correctly   | None        |
|:------------------------|:------------|
| [                       |             |
| {                       |             |
| "cmd" :"GetWifiSignal", |             |
| "code" : 0,             |             |
| "initial" :{            |             |
| "wifiSignal" : 100      |             |
| },                      |             |
| "range" : {             |             |
| "wifiSignal" : {        |             |
| "max" :255,             |             |
| "min" : 0               |             |
| }                       |             |
| },                      |             |
| "value" : {             |             |
| "wifiSignal" : 100      |             |
| }                       |             |
| }                       |             |
| ]                       |             |
| Fielddescription        |             |
| Field                   | description |
| wifiSignal              |             |

### Table from Page 165

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetPush", |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |

### Table from Page 165

| Return datacorrectly                                               |
|:-------------------------------------------------------------------|
| [                                                                  |
| {                                                                  |
| "cmd":"GetPush",                                                   |
| "code":0,                                                          |
| "initial":{                                                        |
| "Push":{                                                           |
| "schedule":{                                                       |
| "enable":1,                                                        |
| "table":                                                           |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 1111111111111111111111111111111"                                   |
| }                                                                  |
| }                                                                  |
| },                                                                 |
| "range":{                                                          |
| "Push":{                                                           |
| "schedule":{                                                       |
| "enable":"boolean",                                                |
| "table":{                                                          |
| "maxLen":168,                                                      |
| "minLen":168                                                       |
| }                                                                  |
| }                                                                  |
| }                                                                  |
| },                                                                 |
| "value":{                                                          |

### Table from Page 166

| "Push":{                                                             | None                                        |
| "schedule":{                                                         |                                             |
| "enable":1,                                                          |                                             |
| "table":                                                             |                                             |
| "11111111111111111111111111111111111111111111111111111111111111111   |                                             |
| 111111111111111111111111111111111111111111111111111111111111111111   |                                             |
| 1111111111111111111111111111111"                                     |                                             |
| }                                                                    |                                             |
| }                                                                    |                                             |
| }                                                                    |                                             |
| }                                                                    |                                             |
| ]                                                                    |                                             |
|:---------------------------------------------------------------------|:--------------------------------------------|
| Fielddescription                                                     |                                             |
| Field                                                                | description                                 |
| Schedule->enable                                                     | Whetherpushthealarminformation              |
| Schedule->table                                                      | Thescheduleaboutwhenpushthealarminformation |
| Note:                                                                |                                             |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“GetPushV20”        |                                             |

### Table from Page 166

| Dataexample      |
|:-----------------|
| [                |
| {                |
| "cmd":"SetPush", |
| "param":{        |
| "Push":{         |

### Table from Page 167

| "schedule":{                                                         | None                                        | None   |
| "enable":1,                                                          |                                             |        |
| "table":                                                             |                                             |        |
| "11111111111111111111111111111111111111111111111111111111111111111   |                                             |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                                             |        |
| 1111111111111111111111111111111"                                     |                                             |        |
| }                                                                    |                                             |        |
| }                                                                    |                                             |        |
| }                                                                    |                                             |        |
| }                                                                    |                                             |        |
| ]                                                                    |                                             |        |
|:---------------------------------------------------------------------|:--------------------------------------------|:-------|
| Fielddescription                                                     |                                             |        |
| Field                                                                | Description                                 | M/O    |
| Schedule->enab                                                       | Whetherpushthealarminformation[0,1]         | O      |
| le                                                                   |                                             |        |
| Schedule->table                                                      | Thescheduleaboutwhenpushthealarminformation | O      |
| Note:Thiscommandsupportsmodel52Xonly                                 |                                             |        |

### Table from Page 167

| Return datacorrectly                                          | None         |
|:--------------------------------------------------------------|:-------------|
| [                                                             |              |
| {                                                             |              |
| "cmd":"SetPush",                                              |              |
| "code":0,                                                     |              |
| "value":{                                                     |              |
| "rspCode":200                                                 |              |
| }                                                             |              |
| }                                                             |              |
| ]                                                             |              |
| Fielddescription                                              |              |
| Field                                                         | description  |
| rspCode                                                       | Responsecode |
| Note:                                                         |              |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“SetPushV20” |              |

### Table from Page 168

| Data example        | None        | None   |
|:--------------------|:------------|:-------|
| [                   |             |        |
| {                   |             |        |
| "cmd":"GetPushV20", |             |        |
| "action":1,         |             |        |
| "param": {          |             |        |
| "channel": 0        |             |        |
| }                   |             |        |
| }                   |             |        |
| ]                   |             |        |
| Fielddescription    |             |        |
| Field               | Description | M/O    |

### Table from Page 168

| Return data correctly   |
|:------------------------|
| [                       |
| {                       |
| "cmd" :"GetPushV20",    |
| "code" : 0,             |
| "initial" :{            |
| "Push" : {              |
| "enable" : 0,           |
| "schedule" : {          |
| "channel" : 0,          |
| "table" : {             |
| //NVR "AI_PEOPLE" :     |

### Table from Page 170

| "Push" : {                                                            | None            |
| "enable" : 1,                                                         |                 |
| "schedule" : {                                                        |                 |
| "channel" : 0,                                                        |                 |
| "table" : {                                                           |                 |
| //NVR "AI_PEOPLE" :                                                   |                 |
| "000000000000000000000000000000000000000000000000000000000000000000   |                 |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                 |
| 00000000000000000000000000000000000",                                 |                 |
| //NVR "AI_VEHICLE" :                                                  |                 |
| "000000000000000000000000000000000000000000000000000000000000000000   |                 |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                 |
| 00000000000000000000000000000000000",                                 |                 |
| "MD" :                                                                |                 |
| "011111111111111111111111111111111111111111111111111111111111111111   |                 |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                 |
| 11111111111111111111111111111111100"                                  |                 |
| }                                                                     |                 |
| }                                                                     |                 |
| }                                                                     |                 |
| }                                                                     |                 |
| }                                                                     |                 |
| ]                                                                     |                 |
|:----------------------------------------------------------------------|:----------------|
| Fielddescription                                                      |                 |
| Field                                                                 | description     |
| Schedule->enable                                                      | Schedule switch |
| Schedule->table                                                       | Schdeule table  |

### Table from Page 171

| Data example                                                        | None           | None   |
|:--------------------------------------------------------------------|:---------------|:-------|
| [{                                                                  |                |        |
| "cmd": "SetPushV20",                                                |                |        |
| "param": {                                                          |                |        |
| "Push": {                                                           |                |        |
| "enable": 1,                                                        |                |        |
| "schedule": {                                                       |                |        |
| "channel": 0,                                                       |                |        |
| "table": {                                                          |                |        |
| "MD":                                                               |                |        |
| "011111111111111111111111111111111111111111111111111111111111111111 |                |        |
| 1111111111111111111111111111111111111111111111111111111111111111111 |                |        |
| 11111111111111111111111111111111100"                                |                |        |
| }                                                                   |                |        |
| }                                                                   |                |        |
| }                                                                   |                |        |
| }                                                                   |                |        |
| }]                                                                  |                |        |
| Fielddescription                                                    |                |        |
| Field                                                               | Description    | M/O    |
| Schedule->en                                                        | Scheduleswitch | O      |
| able                                                                |                |        |
| Schedule->tab                                                       | Scheduletable  | O      |
| le                                                                  |                |        |

### Table from Page 171

| Return data correctly   |
|:------------------------|
| [                       |
| {                       |
| "cmd" :"SetEmail",      |
| "code" : 0,             |
| "value" : {             |
| "rspCode" :200          |
| }                       |
| }                       |
| ]                       |

### Table from Page 172

| Fielddescription   | None         |
|:-------------------|:-------------|
| Field              | description  |
| rspCode            | Responsecode |

### Table from Page 172

| Dataexample         | None        | None   |
|:--------------------|:------------|:-------|
| [                   |             |        |
| {                   |             |        |
| "cmd":"GetPushCfg", |             |        |
| "action":1          |             |        |
| }                   |             |        |
| ]                   |             |        |
| Fielddescription    |             |        |
| Field               | Description | M/O    |

### Table from Page 172

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetPushCfg",    |
| "code":0,              |
| "initial":{            |
| "PushCfg":{            |
| "pushInterval":0       |

### Table from Page 173

| }                               | None                          |
| },                              |                               |
| "range":{                       |                               |
| "PushCfg":{                     |                               |
| "pushInterval":[20,30,60,120]   |                               |
| }                               |                               |
| },                              |                               |
| "value":{                       |                               |
| "PushCfg":{                     |                               |
| "pushInterval":30               |                               |
| }                               |                               |
| }                               |                               |
| }                               |                               |
| ]                               |                               |
|:--------------------------------|:------------------------------|
| Fielddescription                |                               |
| Field                           | description                   |
| initial                         | TheinitialvalueoftheFtpfield. |
| range                           | TherangeoftheFtpfield.        |
| value                           | TherealvalueoftheFtpfield.    |
| pushInterval                    | Theintervalofpush             |

### Table from Page 173

| Dataexample   |
|:--------------|
| [{            |

### Table from Page 174

| "cmd":"SetPushCfg",   | None          | None   |
| "param":{             |               |        |
| "PushCfg":{           |               |        |
| "pushInterval":30     |               |        |
| }                     |               |        |
| }                     |               |        |
| }]                    |               |        |
|:----------------------|:--------------|:-------|
| Fielddescription      |               |        |
| Field                 | Description   | M/O    |
| pushInterval          | Pushinterval. | O      |

### Table from Page 174

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetPushCfg",    |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 175

| Dataexample      | None        | None   |
|:-----------------|:------------|:-------|
| [                |             |        |
| {                |             |        |
| "cmd":"GetP2p",  |             |        |
| "action":1       |             |        |
| }                |             |        |
| ]                |             |        |
| Fielddescription |             |        |
| Field            | Description | M/O    |
|                  |             | M      |

### Table from Page 175

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetP2p",        |
| "code":0,              |
| "initial":{            |
| "P2p":{                |
| "enable":1             |
| }                      |
| },                     |

### Table from Page 176

| "range":{                  | None                  |
| "P2p":{                    |                       |
| "enable":"boolean"         |                       |
| }                          |                       |
| },                         |                       |
| "value":{                  |                       |
| "P2p":{                    |                       |
| "enable":1,                |                       |
| "uid":"95270000SXIPOGIJ"   |                       |
| }                          |                       |
| }                          |                       |
| }                          |                       |
| ]                          |                       |
|:---------------------------|:----------------------|
| Fielddescription           |                       |
| Field                      | description           |
| enable                     | Whetherenablep2pornot |
| uid                        | IPCuid                |

### Table from Page 176

| Dataexample     |
|:----------------|
| [               |
| {               |
| "cmd":"SetP2p", |
| "param":{       |
| "P2p":{         |
| "enable":0      |
| }               |
| }               |

### Table from Page 177

| }                | None                  | None   |
| ]                |                       |        |
|:-----------------|:----------------------|:-------|
| Fielddescription |                       |        |
| Field            | Description           | M/O    |
| enable           | Whetherenablep2pornot | O      |

### Table from Page 177

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetP2P",        |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 177

| Dataexample                 |
|:----------------------------|
| [{                          |
| "cmd":"GetCertificateInfo", |
| "action":0,                 |

### Table from Page 178

| "param":{}       | None        | None   |
| }]               |             |        |
|:-----------------|:------------|:-------|
| Fielddescription |             |        |
| Field            | Description | M/O    |
|                  |             | M      |

### Table from Page 178

| Return datacorrectly        | None                  |
|:----------------------------|:----------------------|
| [                           |                       |
| {                           |                       |
| "cmd":"GetCertificateInfo", |                       |
| "code":0,                   |                       |
| "value":{                   |                       |
| "CertificateInfo":{         |                       |
| "crtName":"",               |                       |
| "enable":0,                 |                       |
| "keyName":""                |                       |
| }                           |                       |
| }                           |                       |
| }                           |                       |
| ]                           |                       |
| Fielddescription            |                       |
| Field                       | description           |
| enable                      | Whetherenablep2pornot |
| uid                         | IPCuid                |

### Table from Page 179

| Dataexample               | None        | None   |
|:--------------------------|:------------|:-------|
| [{                        |             |        |
| "cmd":"CertificateClear", |             |        |
| "action":0,               |             |        |
| "param":{}                |             |        |
| }]                        |             |        |
| Fielddescription          |             |        |
| Field                     | Description | M/O    |
|                           |             | M      |

### Table from Page 179

| Return datacorrectly      | None                  |
|:--------------------------|:----------------------|
| [                         |                       |
| {                         |                       |
| "cmd":"CertificateClear", |                       |
| "code":0,                 |                       |
| "value":{                 |                       |
| "rspCode":200             |                       |
| }                         |                       |
| }                         |                       |
| ]                         |                       |
| Fielddescription          |                       |
| Field                     | description           |
| enable                    | Whetherenablep2pornot |
| uid                       | IPCuid                |

### Table from Page 180

| Dataexample         | None        | None   |
|:--------------------|:------------|:-------|
| [{                  |             |        |
| "cmd":"GetRtspUrl", |             |        |
| "action":0,         |             |        |
| "param":{           |             |        |
| "channel":1         |             |        |
| }                   |             |        |
| }]                  |             |        |
| Fielddescription    |             |        |
| Field               | Description | M/O    |
|                     |             | M      |

### Table from Page 180

| Return datacorrectly                                    | None                |
|:--------------------------------------------------------|:--------------------|
| [                                                       |                     |
| {                                                       |                     |
| "cmd":"GetRtspUrl",                                     |                     |
| "code":0,                                               |                     |
| "value":{                                               |                     |
| "rtspUrl":{                                             |                     |
| "channel":1,                                            |                     |
| "mainStream":"rtsp://192.168.1.58:554/Preview_02_main", |                     |
| "subStream":"rtsp://192.168.1.58:554/Preview_02_sub"    |                     |
| }                                                       |                     |
| }                                                       |                     |
| }                                                       |                     |
| ]                                                       |                     |
| Fielddescription                                        |                     |
| Field                                                   | description         |
| mainStream                                              | Rtspurlofmainstream |
| subStream                                               | Rtspurlofsubstream  |

### Table from Page 181

| Dataexample       | None        | None   |
|:------------------|:------------|:-------|
| [                 |             |        |
| {                 |             |        |
| "cmd":"GetImage", |             |        |
| "action":1,       |             |        |
| "param":{         |             |        |
| "channel":0       |             |        |
| }                 |             |        |
| }                 |             |        |
| ]                 |             |        |
| Fielddescription  |             |        |
| Field             | Description | M/O    |

### Table from Page 181

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetImage",      |
| "code":0,              |
| "initial":{            |

### Table from Page 183

| }                | None               |
| ]                |                    |
|:-----------------|:-------------------|
| Fielddescription |                    |
| Field            | description        |
| bright           | Brightofvideo.     |
| contrast         | Contrastofvideo.   |
| saturation       | Saturationofvideo. |
| hue              | Hueofvideo.        |
| sharpen          | Sharpenofvideo.    |

### Table from Page 183

| Dataexample       |
|:------------------|
| [                 |
| {                 |
| "cmd":"SetImage", |
| "param":{         |
| "Image":{         |
| "channel":0,      |
| "bright":150,     |
| "contrast":150,   |
| "saturation":150, |
| "hue":150,        |
| "sharpen":150     |
| }                 |
| }                 |

### Table from Page 184

| }                | None               | None   |
| ]                |                    |        |
|:-----------------|:-------------------|:-------|
| Fielddescription |                    |        |
| Field            | Description        | M/O    |
| channel          | IPCchannelnumber.  | M      |
| bright           | Brightofvideo.     | M      |
| contrast         | Contrastofvideo.   | M      |
| saturation       | Saturationofvideo. | M      |
| hue              | Hueofvideo.        | M      |
| sharpen          | Sharpenofvideo.    | M      |

### Table from Page 184

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetImage",      |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 185

| Dataexample      | None             | None   |
|:-----------------|:-----------------|:-------|
| [                |                  |        |
| {                |                  |        |
| "cmd":"GetOsd",  |                  |        |
| "action":1,      |                  |        |
| "param":{        |                  |        |
| "channel":0      |                  |        |
| }                |                  |        |
| }                |                  |        |
| ]                |                  |        |
| Fielddescription |                  |        |
| Field            | Description      | M/O    |
| channel          | IPCchannelnumber | M      |

### Table from Page 185

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetOsd",        |
| "code":0,              |
| "initial":{            |
| "Osd":{                |
| "bgcolor":0,           |
| "channel":0,           |
| "osdChannel":{         |
| "enable":1,            |
| "name":"Camera1",      |
| "pos":"LowerRight"     |
| },                     |
| "osdTime":{            |
| "enable":1,            |
| "pos":"TopCenter"      |
| },                     |
| "watermark":1          |
| }                      |

### Table from Page 187

| "osdTime":{         | None                       |
| "enable":1,         |                            |
| "pos":"TopCenter"   |                            |
| },                  |                            |
| "watermark":1       |                            |
| }                   |                            |
| }                   |                            |
| }                   |                            |
| ]                   |                            |
|:--------------------|:---------------------------|
| Fielddescription    |                            |
| Field               | description                |
| osdChannel->enable  | Cameranamedisplayswitch.   |
| osdChannel->name    | Cameraname                 |
| osdChannel->pos     | Cameranamedisplayposition. |
| osdTime->enable     | Cameratimedisplayswitch.   |
| osdTime->pos        | Cameratimedisplayposition. |
| bgcolor             | Backgroundcolor            |
| watermark           | Watermark                  |

### Table from Page 187

| Dataexample     |
|:----------------|
| [               |
| {               |
| "cmd":"SetOsd", |

### Table from Page 188

| "param":{             | None                       | None   |
| "Osd":{               |                            |        |
| "channel":0,          |                            |        |
| "osdChannel":{        |                            |        |
| "enable":1,           |                            |        |
| "name":"Camera101",   |                            |        |
| "pos":"LowerRight"    |                            |        |
| },                    |                            |        |
| "osdTime":{           |                            |        |
| "enable":1,           |                            |        |
| "pos":"UpperRight"    |                            |        |
| }                     |                            |        |
| }                     |                            |        |
| }                     |                            |        |
| }                     |                            |        |
| ]                     |                            |        |
|:----------------------|:---------------------------|:-------|
| Fielddescription      |                            |        |
| Field                 | Description                | M/O    |
| channel               | IPCchannelnumber.          | M      |
| osdChannel->enable    | Cameranamedisplayswitch.   | M      |
| osdChannel->name      | Cameraname                 | M      |
| osdChannel->pos       | Cameranamedisplayposition. | M      |
| osdTime->enable       | Cameratimedisplayswitch.   | M      |
| osdTime->pos          | Cameratimedisplayposition. | M      |

### Table from Page 188

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetOsd",        |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |
| Fielddescription       |

### Table from Page 189

| Field   | description   |
|:--------|:--------------|
| rspCode | Responsecode  |

### Table from Page 189

| Dataexample      | None             | None   |
|:-----------------|:-----------------|:-------|
| [                |                  |        |
| {                |                  |        |
| "cmd":"GetIsp",  |                  |        |
| "action":1,      |                  |        |
| "param":{        |                  |        |
| "channel":0      |                  |        |
| }                |                  |        |
| }                |                  |        |
| ]                |                  |        |
| Fielddescription |                  |        |
| Field            | Description      | M/O    |
| channel          | IPCchannelnumber | M      |

### Table from Page 189

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetIsp",        |
| "code":0,              |
| "initial":{            |
| "Isp":{                |

### Table from Page 193

| "bright":128,             | None                                              |
| "dark":128,               |                                                   |
| "mode":"Auto"             |                                                   |
| },                        |                                                   |
| "blc":128,                |                                                   |
| "blueGain":128,           |                                                   |
| "cdsType":0,              |                                                   |
| "channel":0,              |                                                   |
| "constantFrameRate":1,    |                                                   |
| "dayNight":"Auto",        |                                                   |
| "dayNightThreshold":73,   |                                                   |
| "drc":128,                |                                                   |
| "exposure":"Auto",        |                                                   |
| "gain":{                  |                                                   |
| "max":62,                 |                                                   |
| "min":1                   |                                                   |
| },                        |                                                   |
| "mirroring":0,            |                                                   |
| "nr3d":1,                 |                                                   |
| "redGain":128,            |                                                   |
| "rotation":0,             |                                                   |
| "shutter":{               |                                                   |
| "max":125,                |                                                   |
| "min":0                   |                                                   |
| },                        |                                                   |
| "whiteBalance":"Auto"     |                                                   |
| }                         |                                                   |
| }                         |                                                   |
| }                         |                                                   |
| ]                         |                                                   |
|:--------------------------|:--------------------------------------------------|
| Fielddescription          |                                                   |
| Field                     | description                                       |
| antiFlicker               | Flickerprevention,["Outdoor","50HZ","60HZ","Off"] |
| exposure                  | Exposuremode,                                     |
|                           | ["Auto","LowOise","Anti-Smearing","Manual"]       |
| gain                      | WhenthevalueofexposureisLowOiseorManual,the       |
| (Dependon                 | gainfieldiseffective.                             |
| exposure)                 |                                                   |
| shutter                   | WhenthevalueofexposureisAnti-SmearingorManual,    |

### Table from Page 194

| (Dependon         | theshutterfieldiseffective.                           |
| exposure)         |                                                       |
|:------------------|:------------------------------------------------------|
| whiteBalance      | WhiteBalance,["Auto","Manual"]                        |
| blueGain          | WhenthevalueofwhiteBalanceisAnti-Smearingor           |
| (Dependon         | Manual,theblueGainfieldiseffective.                   |
| whiteBalance)     |                                                       |
| redGain           | WhenthevalueofwhiteBalanceisAnti-Smearingor           |
| (Dependon         | Manual,theredGainfieldiseffective.                    |
| whiteBalance)     |                                                       |
| dayNight          | Day&Night,["Auto","Color","Black&White"]              |
| backLight         | Backlightcompensation,                                |
|                   | ["Off","BackLightControl","DynamicRangeControl"]      |
| Blc               | WhenthevalueofbackLightisBackLightControl,theblc      |
| (Dependon         | fieldiseffective.                                     |
| backLight)        |                                                       |
| drc               | WhenthevalueofbackLightisDynamicRangeControl,the      |
| (Dependon         | drcfieldiseffective.                                  |
| backLight)        |                                                       |
| nr3d              |                                                       |
| mirroring         | Videomirroring.                                       |
| rotation          | Videorotation.                                        |
| cdsType           | Softlightsensitiveswitch,offwhenthehardlightsensitive |
|                   | effect,canusethedayandnightswitchingthreshold         |
|                   | adjustment,openwhenthesoftlightsensitiveeffect,can    |
|                   | usethedayandnightswitchingsensitivityadjustment       |
| constantFrameRate | Fixedframerateswitch,whenon,tothevideofluency         |
|                   | priority,whenofftothequalityofthepicturepriority      |

### Table from Page 195

| Dataexample            |
|:-----------------------|
| [{                     |
| "cmd":"SetIsp",        |
| "action":0,            |
| "param":{              |
| "Isp":{                |
| "antiFlicker":"Off",   |
| "backLight":"Off",     |
| "constantFrameRate":1, |
| "blc":128,             |
| "blueGain":128,        |
| "channel":0,           |
| "dayNight":"Auto",     |
| "drc":128,             |
| "exposure":"Auto",     |
| "cdsType":0,           |
| "gain":{               |
| "max":62,              |
| "min":1                |
| },                     |
| "mirroring":0,         |
| "nr3d":1,              |
| "redGain":128,         |
| "rotation":0,          |
| "shutter":{            |
| "max":125,             |
| "min":0                |
| },                     |
| "whiteBalance":"Auto", |
| "bd_day":{             |

### Table from Page 196

| "iAvailable":1,          | None                                        | None   |
| "bright":128,            |                                             |        |
| "dark":128,              |                                             |        |
| "mode":"Auto"            |                                             |        |
| },                       |                                             |        |
| "bd_led_color":{         |                                             |        |
| "iAvailable":0,          |                                             |        |
| "bright":0,              |                                             |        |
| "dark":0,                |                                             |        |
| "mode":"Auto"            |                                             |        |
| },                       |                                             |        |
| "bd_night":{             |                                             |        |
| "iAvailable":1,          |                                             |        |
| "bright":128,            |                                             |        |
| "dark":128,              |                                             |        |
| "mode":"Auto"            |                                             |        |
| },                       |                                             |        |
| "dayNightThreshold":73   |                                             |        |
| }                        |                                             |        |
| }                        |                                             |        |
| }]                       |                                             |        |
|:-------------------------|:--------------------------------------------|:-------|
| Fielddescription         |                                             |        |
| Field                    | Description                                 | M/O    |
| channel                  | IPCchannelnumber.                           | M      |
| antiFlicker              | Flickerprevention,["Outdoor","50HZ","60HZ", | M      |
|                          | "Off"]                                      |        |
| exposure                 | Exposuremode,                               | M      |
|                          | ["Auto","LowOise","Anti-Smearing","Manual"] |        |
| gain                     | WhenthevalueofexposureisLowOiseorManual,    | M      |
| (Dependon                | thegainfieldiseffective.                    |        |
| exposure)                |                                             |        |
| shutter                  | WhenthevalueofexposureisAnti-Smearingor     | M      |
| (Dependon                | Manual,theshutterfieldiseffective.          |        |
| exposure)                |                                             |        |
| whiteBalance             | WhiteBalance,["Auto","Manual"]              | M      |
| blueGain                 | WhenthevalueofwhiteBalanceisAnti-Smearingor | M      |
| (Dependon                | Manual,theblueGainfieldiseffective.         |        |

### Table from Page 197

| whiteBalance)   |                                                  |    |
|:----------------|:-------------------------------------------------|:---|
| redGain         | WhenthevalueofwhiteBalanceisAnti-Smearingor      | M  |
| (Dependon       | Manual,theredGainfieldiseffective.               |    |
| whiteBalance)   |                                                  |    |
| dayNight        | Day&Night,["Auto","Color","Black&White"]         | M  |
| backLight       | Backlightcompensation,                           | M  |
|                 | ["Off","BackLightControl","DynamicRangeControl"] |    |
| Blc             | WhenthevalueofbackLightisBackLightControl,the    | M  |
| (Dependon       | blcfieldiseffective.                             |    |
| backLight)      |                                                  |    |
| Drc             | WhenthevalueofbackLightis                        | M  |
| (Dependon       | DynamicRangeControl,thedrcfieldiseffective.      |    |
| backLight)      |                                                  |    |
| nr3d            |                                                  | M  |
| mirroring       | Videomirroring.                                  | M  |
| rotation        | Videorotation.                                   | M  |
| cdsType         | Softlightsensitiveswitch,offwhenthehardlight     | M  |
|                 | sensitiveeffect,canusethedayandnightswitching    |    |
|                 | thresholdadjustment,openwhenthesoftlight         |    |
|                 | sensitiveeffect,canusethedayandnightswitching    |    |
|                 | sensitivityadjustment                            |    |
| constantFrame   | Fixedframerateswitch,whenon,tothevideo           | M  |
| Rate            | fluencypriority,whenofftothequalityofthepicture  |    |
|                 | priority                                         |    |

### Table from Page 197

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |

### Table from Page 198

| "cmd":"SetOsd",   | None         |
| "code":0,         |              |
| "value":{         |              |
| "rspCode":200     |              |
| }                 |              |
| }                 |              |
| ]                 |              |
|:------------------|:-------------|
| Fielddescription  |              |
| Field             | description  |
| rspCode           | Responsecode |

### Table from Page 198

| Dataexample      | None             | None   |
|:-----------------|:-----------------|:-------|
| [                |                  |        |
| {                |                  |        |
| "cmd":"GetMask", |                  |        |
| "action":1,      |                  |        |
| "param":{        |                  |        |
| "channel":0      |                  |        |
| }                |                  |        |
| }                |                  |        |
| ]                |                  |        |
| Fielddescription |                  |        |
| Field            | Description      | M/O    |
| channel          | IPCchannelnumber | M      |

### Table from Page 199

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetMask",       |
| "code":0,              |
| "initial":{            |
| "Mask":{               |
| "area":[               |
| {                      |
| "block":{              |
| "height":0,            |
| "width":0,             |
| "x":0,                 |
| "y":0                  |
| },                     |
| "screen":{             |
| "height":0,            |
| "width":0              |
| }                      |
| }                      |
| ],                     |
| "channel":0,           |
| "enable":0             |
| }                      |
| },                     |
| "range":{              |
| "Mask":{               |
| "channel":0,           |
| "enable":"boolean",    |
| "maxAreas":4           |
| }                      |
| },                     |
| "value":{              |
| "Mask":{               |
| "area":[               |
| {                      |
| "block":{              |
| "height":163,          |
| "width":121,           |
| "x":192,               |
| "y":143                |

### Table from Page 200

| },               | None                      |
| "screen":{       |                           |
| "height":480,    |                           |
| "width":640      |                           |
| }                |                           |
| }                |                           |
| ],               |                           |
| "channel":0,     |                           |
| "enable":1       |                           |
| }                |                           |
| }                |                           |
| }                |                           |
| ]                |                           |
|:-----------------|:--------------------------|
| Fielddescription |                           |
| Field            | description               |
| enable           | Videomaskswitch.          |
| Block->height    | Blockheight.              |
| Block->width     | Blockwidth.               |
| Block->x         | LeftupperXaxiscoordinates |
| Block->y         | LeftupperYaxiscoordinates |
| Screen->height   | Screenheight.             |
| Screen->width    | Screenwidth.              |

### Table from Page 200

| Dataexample   |
|:--------------|
| [             |

### Table from Page 202

| {                | None                      | None   |
| "screen":{       |                           |        |
| "height":720,    |                           |        |
| "width":1280     |                           |        |
| },               |                           |        |
| "block":{        |                           |        |
| "x":632,         |                           |        |
| "y":88,          |                           |        |
| "width":51,      |                           |        |
| "height":245     |                           |        |
| }                |                           |        |
| }                |                           |        |
| ]                |                           |        |
| }                |                           |        |
| }                |                           |        |
| }                |                           |        |
| ]                |                           |        |
|:-----------------|:--------------------------|:-------|
| Fielddescription |                           |        |
| Field            | Description               | M/O    |
| channel          | IPCchannelnumber.         | M      |
| enable           | Videomaskswitch.          | M      |
| block->height    | Blockheight.              | M      |
| block->width     | Blockwidth.               | M      |
| block->x         | LeftupperXaxiscoordinates | M      |
| block->y         | LeftupperYaxiscoordinates | M      |
| screen->height   | Screenheight.             | M      |
| screen->width    | Screenwidth.              | M      |

### Table from Page 202

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetMask",       |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |

### Table from Page 203

| }                | None         |
| ]                |              |
|:-----------------|:-------------|
| Fielddescription |              |
| Field            | description  |
| rspCode          | Responsecode |

### Table from Page 203

| Dataexample       | None        | None   |
|:------------------|:------------|:-------|
| [{                |             |        |
| "cmd":"GetCrop",  |             |        |
| "action":0, //NVR |             |        |
| "param":{ //NVR   |             |        |
| "channel":0 //NVR |             |        |
| }                 |             |        |
| }]                |             |        |
| Fielddescription  |             |        |
| Field             | Description | M/O    |

### Table from Page 203

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |

### Table from Page 204

| "cmd":"GetCrop",     |
| "code":0,            |
| "initial":{          |
| "Crop":{             |
| "cropHeight":480,    |
| "cropWidth":640,     |
| "mainHeight":1920,   |
| "mainWidth":2560,    |
| "minHeight":480,     |
| "minWidth":640,      |
| "topLeftX":960,      |
| "topLeftY":720       |
| }                    |
| },                   |
| "range":{            |
| "Crop":{             |
| "topLeftX":{         |
| "max":1920,          |
| "min":0              |
| },                   |
| "topLeftY":{         |
| "max":1440,          |
| "min":0              |
| }                    |
| }                    |
| },                   |
| "value":{            |
| "Crop":{             |
| "channel":0, //NVR   |
| "cropHeight":480,    |
| "cropWidth":640,     |
| "mainHeight":1920,   |
| "mainWidth":2560,    |
| "minHeight":480,     |
| "minWidth":640,      |
| "topLeftX":960,      |
| "topLeftY":720       |
| }                    |
| }                    |
| }                    |
| ]                    |
|:---------------------|
| Fielddescription     |

### Table from Page 205

| Field      | description                                       |
|:-----------|:--------------------------------------------------|
| rspCode    | Responsecode                                      |
| minHeight  | Minimumheightofcroparea                           |
| minWidth   | Minimumwidthofcroparea                            |
| mainHeight | heightofMainstream                                |
| mainWidth  | widthofMainstream                                 |
| cropHeight | heightofcroparea                                  |
| cropWidth  | widthofcroparea                                   |
| topLeftY   | Distancebetweentheupperleftcornerofthecropareaand |
|            | theupperboundary                                  |
| topLeftX   | Distancebetweentheupperleftcornerofthecropareaand |
|            | theleftboundary                                   |

### Table from Page 205

| Dataexample          |
|:---------------------|
| [{                   |
| "cmd":"SetCrop",     |
| "action":0,          |
| "param":{            |
| "Crop":{             |
| "channel":0, //NVR   |
| "screenWidth":2560,  |
| "screenHeight":1920, |
| "cropWidth":640,     |
| "cropHeight":480,    |

### Table from Page 206

| "topLeftX":960,   | None        | None   |
| "topLeftY":720    |             |        |
| }                 |             |        |
| }                 |             |        |
| }]                |             |        |
|:------------------|:------------|:-------|
| Fielddescription  |             |        |
| Field             | Description | M/O    |

### Table from Page 206

| Return datacorrectly   | None                                              |
|:-----------------------|:--------------------------------------------------|
| [                      |                                                   |
| {                      |                                                   |
| "cmd":"SetCrop",       |                                                   |
| "code":0,              |                                                   |
| "value":{              |                                                   |
| "rspCode":200          |                                                   |
| }                      |                                                   |
| }                      |                                                   |
| ]                      |                                                   |
| Fielddescription       |                                                   |
| Field                  | description                                       |
| rspCode                | Responsecode                                      |
| minHeight              | Minimumheightofcroparea                           |
| minWidth               | Minimumwidthofcroparea                            |
| mainHeight             | heightofMainstream                                |
| mainWidth              | widthofMainstream                                 |
| cropHeight             | heightofcroparea                                  |
| cropWidth              | widthofcroparea                                   |
| topLeftY               | Distancebetweentheupperleftcornerofthecropareaand |
|                        | theupperboundary                                  |
| topLeftX               | Distancebetweentheupperleftcornerofthecropareaand |

### Table from Page 207

| This      |    | command   | None   | None    |    | is   | used   |    | for   |    | "stitching   |    | binocular"   |    | IPC   |    | to   |    | adjust   |    | the   |    |
|:----------|:---|:----------|:-------|:--------|:---|:-----|:-------|:---|:------|:---|:-------------|:---|:-------------|:---|:------|:---|:-----|:---|:---------|:---|:------|:---|
| stitching |    |           |        | picture |    |      |        |    |       |    |              |    |              |    |       |    |      |    |          |    |       |    |

### Table from Page 207

| Dataexample        | None        | None   |
|:-------------------|:------------|:-------|
| [{                 |             |        |
| "cmd":"GetStitch", |             |        |
| "action":1         |             |        |
| }]                 |             |        |
| Fielddescription   |             |        |
| Field              | Description | M/O    |

### Table from Page 207

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetStitch",     |
| "code":0,              |
| "initial":{            |
| "stitch":{             |
| "distance":2.0,        |
| "stitchXMove":0,       |

### Table from Page 208

| "stitchYMove":0                 | None                     |
| }                               |                          |
| },                              |                          |
| "range":{                       |                          |
| "stitch":{                      |                          |
| "distance":{                    |                          |
| "max":20.0,                     |                          |
| "min":2.0                       |                          |
| },                              |                          |
| "stitchXMove":{                 |                          |
| "max":100,                      |                          |
| "min":-100                      |                          |
| },                              |                          |
| "stitchYMove":{                 |                          |
| "max":-100,                     |                          |
| "min":100                       |                          |
| }                               |                          |
| }                               |                          |
| },                              |                          |
| "value":{                       |                          |
| "stitch":{                      |                          |
| "distance":8.100000381469727,   |                          |
| "stitchXMove":5,                |                          |
| "stitchYMove":3                 |                          |
| }                               |                          |
| }                               |                          |
| }                               |                          |
| ]                               |                          |
|:--------------------------------|:-------------------------|
| Fielddescription                |                          |
| Field                           | description              |
| distance                        | Distancebetweenimages    |
| stitchXMove                     | Adjustpixelshorizontally |
| stitchYMove                     | Adjustpixelsvertically   |

### Table from Page 209

| Dataexample        | None                     | None   |
|:-------------------|:-------------------------|:-------|
| [{                 |                          |        |
| "cmd":"setStitch", |                          |        |
| "param":{          |                          |        |
| "stitch":{         |                          |        |
| "distance":8.1,    |                          |        |
| "stitchXMove":5,   |                          |        |
| "stitchYMove":3    |                          |        |
| }                  |                          |        |
| }                  |                          |        |
| }]                 |                          |        |
| Fielddescription   |                          |        |
| Field              | Description              | M/O    |
| distance           | Distancebetweenimages    | M      |
| stitchXMove        | Adjustpixelshorizontally | M      |
| stitchYMove        | Adjustpixelsvertically   | M      |

### Table from Page 209

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetStitch",     |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |
| Fielddescription       |

### Table from Page 210

| Dataexample      | None             | None   |
|:-----------------|:-----------------|:-------|
| [                |                  |        |
| {                |                  |        |
| "cmd":"GetEnc",  |                  |        |
| "action":1,      |                  |        |
| "param":{        |                  |        |
| "channel":0      |                  |        |
| }                |                  |        |
| }                |                  |        |
| ]                |                  |        |
| Fielddescription |                  |        |
| Field            | Description      | M/O    |
| channel          | IPCchannelnumber | M      |

### Table from Page 210

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetEnc",        |

### Table from Page 215

| }                      | None                                         |
| }                      |                                              |
| }                      |                                              |
| }                      |                                              |
| ]                      |                                              |
|:-----------------------|:---------------------------------------------|
| Fielddescription       |                                              |
| Field                  | description                                  |
| audio                  | Audioswitch.                                 |
| mainStream->bitRate    | Bitrateofmainstream.                         |
| mainStream->frameRate  | FrameRateofmainstream.                       |
| mainStream->profile    | H.264Profile.                                |
| mainStream->size       | Resolution.                                  |
| subStream->bitRate     | Bitrateofsubstream.                          |
| subStream->frameRate   | FrameRateofsubstream.                        |
| subStream->profile     | H.264Profile.                                |
| subStream->size        | Resolution.                                  |
| mainstream->height     | Heightofmainstream                           |
|                        | (Thisitemisinternaluseonly,andnoneededforcmd |
|                        | “SetEnc”)                                    |
| mainstream->resolution | Resolutionenumerateofmainstream              |
|                        | (Thisitemisinternaluseonly,andnoneededforcmd |
|                        | “SetEnc”)                                    |
| mainstream->width      | Widthofmainstream                            |
|                        | (Thisitemisinternaluseonly,andnoneededforcmd |
|                        | “SetEnc”)                                    |
| substeram->height      | Heightofsubstream                            |
|                        | (Thisitemisinternaluseonly,andnoneededforcmd |
|                        | “SetEnc”)                                    |
| substeram->resolution  | Resolutionenumerateofsubstream               |
|                        | (Thisitemisinternaluseonly,andnoneededfor    |
|                        | cmd“SetEnc”)                                 |

### Table from Page 216

| Dataexample         |
|:--------------------|
| [{                  |
| "cmd":"SetEnc",     |
| "action":0,         |
| "param":{           |
| "Enc":{             |
| "channel":0,        |
| "audio":1,          |
| "mainStream":{      |
| "size":"2560*1920", |
| "frameRate":20,     |
| "bitRate":4096,     |
| "profile":"High"    |
| },                  |
| "subStream":{       |
| "size":"640*480",   |
| "frameRate":10,     |
| "bitRate":256,      |
| "profile":"High"    |
| }                   |
| }                   |
| }                   |

### Table from Page 217

| }]                    | None                   | None   |
|:----------------------|:-----------------------|:-------|
| Fielddescription      |                        |        |
| Field                 | Description            | M/O    |
| channel               | IPCchannelnumber.      | M      |
| audio                 | Audioswitch.           | M      |
| mainStream->bitRate   | Bitrateofmainstream.   | M      |
| mainStream->frameRate | FrameRateofmainstream. | M      |
| mainStream->profile   | H.264Profile.          | M      |
| mainStream->size      | Resolution.            | M      |
| subStream->bitRate    | Bitrateofsubstream.    | M      |
| subStream->frameRate  | FrameRateofsubstream.  | M      |
| subStream->profile    | H.264Profile.          | M      |
| subStream->size       | Resolution.            | M      |

### Table from Page 217

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetEnc",        |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 218

| Dataexample      | None           | None   |
|:-----------------|:---------------|:-------|
| [                |                |        |
| {                |                |        |
| "cmd":"GetRec",  |                |        |
| "action":1,      |                |        |
| "param":{        |                |        |
| "channel":0      |                |        |
| }                |                |        |
| }                |                |        |
| ]                |                |        |
| Fielddescription |                |        |
| Field            | Description    | M/O    |
| channel          | Indexofchannel | M      |

### Table from Page 218

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetRec",        |
| "code":0,              |
| "initial":{            |
| "Rec":{                |
| "channel":0,           |

### Table from Page 220

| ]                                                            | None                                               |
|:-------------------------------------------------------------|:---------------------------------------------------|
| Fielddescription                                             |                                                    |
| Field                                                        | description                                        |
| channel                                                      | Channelnumber                                      |
| overwrite                                                    | Whetherthevideofilescanbeoverwritten               |
| postRec                                                      | Postrecordtime                                     |
| preRec                                                       | Enableprerecord                                    |
| enable                                                       | Enablescheduledrecording                           |
| table                                                        | Astringwiththelengthof7days*24hours.Eachbyteinthis |
|                                                              | hourindicateswhetherit’srecording.Withthevalueof0, |
|                                                              | therecordingisoff,otherwisetherecordingison.       |
| Note:Thiscommandsupportsmodel52Xonly                         |                                                    |
| Note:                                                        |                                                    |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“GetRecV20” |                                                    |

### Table from Page 220

| Dataexample     |
|:----------------|
| [               |
| {               |
| "cmd":"SetRec", |
| "param":        |
| {               |

### Table from Page 221

| "Rec":                                                               | None          | None   |
| {                                                                    |               |        |
| "channel":0,                                                         |               |        |
| "overwrite":1,                                                       |               |        |
| "postRec":"30Seconds",                                               |               |        |
| "preRec":1,                                                          |               |        |
| "schedule":                                                          |               |        |
| {                                                                    |               |        |
| "enable":1,                                                          |               |        |
| "table":                                                             |               |        |
| "11111111111111111111111111111111111111111111111111111111111111111   |               |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |               |        |
| 1111111111111111111111111111111111111"                               |               |        |
| }                                                                    |               |        |
| }                                                                    |               |        |
| }                                                                    |               |        |
| }                                                                    |               |        |
| ]                                                                    |               |        |
|:---------------------------------------------------------------------|:--------------|:-------|
| Fielddescription                                                     |               |        |
| Field                                                                | Description   | M/O    |
| channel                                                              | SeealsoGetRec | M      |
| overwrite                                                            | SeealsoGetRec | O      |
| postRec                                                              | SeealsoGetRec | O      |
| preRec                                                               | SeealsoGetRec | O      |
| enable                                                               | SeealsoGetRec | O      |
| table                                                                | SeealsoGetRec | O      |
| Note:                                                                |               |        |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“SetRecV20”         |               |        |

### Table from Page 221

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetRec",        |
| "code":0,              |
| "value":{              |
| "rspCode":200          |

### Table from Page 222

| }                | None        |
| }                |             |
| ]                |             |
|:-----------------|:------------|
| Fielddescription |             |
| Field            | description |

### Table from Page 222

| Dataexample        | None           | None   |
|:-------------------|:---------------|:-------|
| [                  |                |        |
| {                  |                |        |
| "cmd":"GetRecV20", |                |        |
| "action":1,        |                |        |
| "param":{          |                |        |
| "channel":0        |                |        |
| }                  |                |        |
| }                  |                |        |
| Fielddescription   |                |        |
| ]                  |                |        |
| Field              | Description    | M/O    |
| channel            | Indexofchannel | M      |

### Table from Page 222

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |

### Table from Page 224

| "table":{                                                            |
| "AI_PEOPLE":"boolean", //NVR                                         |
| "AI_VEHICLE":"boolean", //NVR                                        |
| "MD":"boolean",                                                      |
| "TIMING":"boolean"                                                   |
| }                                                                    |
| }                                                                    |
| }                                                                    |
| },                                                                   |
| "value":{                                                            |
| "Rec":{                                                              |
| "enable":1,                                                          |
| "overwrite":1,                                                       |
| "packTime":"60Minutes",                                              |
| "postRec":"1Minute",                                                 |
| "preRec":1,                                                          |
| "saveDay":30,                                                        |
| "schedule":{                                                         |
| "channel":0,                                                         |
| "table":{                                                            |
| //NVR "AI_PEOPLE":                                                   |
| "00000000000000000000000000000000000000000000000000000000000000000   |
| 000000000000000000000000000000000000000000000000000000000000000000   |
| 0000000000000000000000000000000000000",                              |
| //NVR "AI_VEHICLE":                                                  |
| "00000000000000000000000000000000000000000000000000000000000000000   |
| 000000000000000000000000000000000000000000000000000000000000000000   |
| 0000000000000000000000000000000000000",                              |
| "MD":                                                                |
| "11111111111111111111111111111111111111111111111111111111111111111   |
| 111111111111111111111111111111111111111111111111111111111111111111   |
| 1111111111111111111111111111111111111",                              |
| "TIMING":                                                            |
| "00000000000000000000000000000000000000000000000000000000000000000   |
| 000000000000000000000000000000000000000000000000000000000000000000   |
| 0000000000000000000000000000000000000"                               |
| }                                                                    |
| }                                                                    |
| }                                                                    |
| }                                                                    |
| }                                                                    |
| ]                                                                    |
|:---------------------------------------------------------------------|
| Fielddescription                                                     |

### Table from Page 225

| Field     | description                                        |
|:----------|:---------------------------------------------------|
| channel   | Channelnumber                                      |
| overwrite | Whetherthevideofilescanbeoverwritten               |
| postRec   | Postrecordtime                                     |
| preRec    | Enableprerecord                                    |
| enable    | Enablescheduledrecording                           |
| table     | Astringwiththelengthof7days*24hours.Eachbyteinthis |
|           | hourindicateswhetherit’srecording.Withthevalueof0, |
|           | therecordingisoff,otherwisetherecordingison.       |
| PackTime  | Packagingcycle                                     |
| saveDay   | Customizetheretentiondaysofvideocoverage           |

### Table from Page 225

| Dataexample            |
|:-----------------------|
| [{                     |
| "cmd":"SetRecV20",     |
| "param":{              |
| "Rec":{                |
| "overwrite":1,         |
| "postRec":"30Seconds", |
| "preRec":1,            |
| "saveDay":30,          |

### Table from Page 226

| "schedule":{                                                         | None          | None   |
| "enable":1,                                                          |               |        |
| "channel":0,                                                         |               |        |
| "table":{                                                            |               |        |
| "MD":                                                                |               |        |
| "10011111111111111111111111111111111111111111111111111111111111111   |               |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |               |        |
| 1111111111111111111111111111111111100",                              |               |        |
| "TIMING":                                                            |               |        |
| "10111111111111111111111111111111111111111111111111111111111111111   |               |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |               |        |
| 1111111111111111111111111111111111111"                               |               |        |
| }                                                                    |               |        |
| }                                                                    |               |        |
| }                                                                    |               |        |
| }                                                                    |               |        |
| }]                                                                   |               |        |
|:---------------------------------------------------------------------|:--------------|:-------|
| Fielddescription                                                     |               |        |
| Field                                                                | Description   | M/O    |
| channel                                                              | SeealsoGetRec | M      |
| overwrite                                                            | SeealsoGetRec | O      |
| postRec                                                              | SeealsoGetRec | O      |
| preRec                                                               | SeealsoGetRec | O      |
| enable                                                               | SeealsoGetRec | O      |
| table                                                                | SeealsoGetRec | O      |
| saveDay                                                              | SeealsoGetRec | O      |

### Table from Page 226

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetRecV20",     |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |

### Table from Page 227

| ]                | None        |
|:-----------------|:------------|
| Fielddescription |             |
| Field            | description |

### Table from Page 227

| Dataexample          |
|:---------------------|
| [{                   |
| "cmd":"Search",      |
| "action":0,          |
| "param":{            |
| "Search":{           |
| "channel":0,         |
| "onlyStatus":1,      |
| "streamType":"main", |
| "StartTime":{        |
| "year":2020,         |
| "mon":12,            |
| "day":21,            |
| "hour":12,           |
| "min":26,            |
| "sec":1              |
| },                   |
| "EndTime":{          |
| "year":2020,         |

### Table from Page 228

| "mon":12,                                                           | None                                             | None   |
| "day":21,                                                           |                                                  |        |
| "hour":12,                                                          |                                                  |        |
| "min":34,                                                           |                                                  |        |
| "sec":1                                                             |                                                  |        |
| }                                                                   |                                                  |        |
| }                                                                   |                                                  |        |
| }                                                                   |                                                  |        |
| }]                                                                  |                                                  |        |
|:--------------------------------------------------------------------|:-------------------------------------------------|:-------|
| Fielddescription                                                    |                                                  |        |
| Field                                                               | Description                                      | M/O    |
| channel                                                             | Channelnumber                                    | M      |
| onlyStatus                                                          | Thevalue1meansitwillonlygetthedataofdates        | M      |
|                                                                     | insteadofrequiringthedetailsofthefiles.Thevalue0 |        |
|                                                                     | meansitwillgetthedetailsinformationofacertain    |        |
|                                                                     | day.                                             |        |
| streamType                                                          | Thestreamtypeoftherecordings,“main”isfor         | M      |
|                                                                     | searchingmainstream,otherwiseisforsearchingsub   |        |
|                                                                     | stream.                                          |        |
| startTime                                                           | Thestarttimeoftherecordings                      | M      |
| endTime                                                             | Theendtimeoftherecordings                        | M      |
| Noted: Searching a big amount of files might lead to searching time |                                                  |        |
| out                                                                 |                                                  |        |

### Table from Page 228

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"Search",        |
| "code":0,              |
| "value":{              |
| "SearchResult":{       |
| "Status":[             |
| {                      |
| "mon":12,              |

### Table from Page 229

| "table":"1111000000000011110011110000000",   | None                                               |
| "year":2020                                  |                                                    |
| }                                            |                                                    |
| ],                                           |                                                    |
| "channel":0                                  |                                                    |
| }                                            |                                                    |
| }                                            |                                                    |
| }                                            |                                                    |
| ]                                            |                                                    |
|:---------------------------------------------|:---------------------------------------------------|
| Fielddescription                             |                                                    |
| Field                                        | description                                        |
| mon                                          | Recorddate(month)                                  |
| year                                         | Recorddate(year)                                   |
| channel                                      | channelnumber                                      |
| table                                        | Eachbyteinthestringrepresentthedaysofthemonth,     |
|                                              | indicatingwhetherit’srecording.Withthevalueof0,the |
|                                              | recordingisoff,withthevalueof1,therecordingison.   |

### Table from Page 229

| Return datacorrectly (onlyStatus 为0)   |
|:---------------------------------------|
| [                                      |
| {                                      |
| "cmd":"Search",                        |
| "code":0,                              |
| "value":{                              |
| "SearchResult":{                       |
| "File":[                               |
| {                                      |
| "EndTime":{                            |
| "day":21,                              |
| "hour":20,                             |
| "min":21,                              |
| "mon":12,                              |
| "sec":23,                              |
| "year":2020                            |
| },                                     |
| "StartTime":{                          |
| "day":21,                              |
| "hour":12,                             |

### Table from Page 231

| "min":38,                                                            | None                |
| "mon":12,                                                            |                     |
| "sec":49,                                                            |                     |
| "year":2020                                                          |                     |
| },                                                                   |                     |
| "StartTime":{                                                        |                     |
| "day":21,                                                            |                     |
| "hour":12,                                                           |                     |
| "min":33,                                                            |                     |
| "mon":12,                                                            |                     |
| "sec":49,                                                            |                     |
| "year":2020                                                          |                     |
| },                                                                   |                     |
| "frameRate":0,                                                       |                     |
| "height":0,                                                          |                     |
| "name":                                                              |                     |
| "Mp4Record/2020-12-21/RecM01_20201221_123349_123849_6D28C18_98ADFF   |                     |
| F.mp4",                                                              |                     |
| "size":160096255,                                                    |                     |
| "type":"main",                                                       |                     |
| "width":0                                                            |                     |
| }                                                                    |                     |
| ],                                                                   |                     |
| "Status":[                                                           |                     |
| {                                                                    |                     |
| "mon":12,                                                            |                     |
| "table":"0000000000000000111110000000000",                           |                     |
| "year":2020                                                          |                     |
| }                                                                    |                     |
| ],                                                                   |                     |
| "channel":0                                                          |                     |
| }                                                                    |                     |
| }                                                                    |                     |
| }                                                                    |                     |
| ]                                                                    |                     |
|:---------------------------------------------------------------------|:--------------------|
| Fielddescription                                                     |                     |
| Field                                                                | description         |
| frameRate                                                            | Framerate           |
| height                                                               | Theheightoftheimage |
| width                                                                | Thewidthoftheimage  |

### Table from Page 232

| name      | Filename                                           |
|:----------|:---------------------------------------------------|
| size      | Filesize                                           |
| type      | Streamtype                                         |
| StartTime | Thestarttimeoftherecordings                        |
| EndTime   | Theendtimeoftherecordings                          |
| mon       | Month                                              |
| year      | Year                                               |
| channel   | Channelnumber                                      |
| table     | Eachbyteinthestringrepresentthedaysofthemonth,     |
|           | indicatingwhetherit’srecording.Withthevalueof0,the |
|           | recordingisoff,withthevalueof1,therecordingison.   |

### Table from Page 232

| Parameter   | M/O   | Description            |
|:------------|:------|:-----------------------|
| source      | M     | Thenameofthesourcefile |
| output      | M     | Videofilesstoragename  |

### Table from Page 233

| Return datacorrectly                                                    | None                  |
|:------------------------------------------------------------------------|:----------------------|
| Content-Type:apolication/octet-stream                                   |                       |
| Content-Length:2244776                                                  |                       |
| Last-Modified:Mon,21Dec202003:15:56GMT                                  |                       |
| Connection:keep-alive                                                   |                       |
| Content-Disposition:attachment;filename=Mp4Record_2020-12-21_RecM01_202 |                       |
| 01221_121551_121553_6D28808_2240A8.mp4                                  |                       |
| ETag:"5fe0136c-2240a8"                                                  |                       |
| X-Frame-Options:SAMEORIGIN                                              |                       |
| X-XSS-Protection:1;mode=block                                           |                       |
| X-Content-Type-Options:nosniff                                          |                       |
| Accept-Ranges:bytes                                                     |                       |
| .............................(filecontent)                              |                       |
| Fielddescription                                                        |                       |
| Field                                                                   | description           |
| filename                                                                | Thenameofthevideofile |

### Table from Page 233

| Parameter   | M/O   | Description                               |
|:------------|:------|:------------------------------------------|
| channel     | M     | Channelnumber                             |
| rs          | M     | Randomcharacterwithfixedlength.It’susedto |
|             |       | preventbrowsercaching.                    |

### Table from Page 234

| Return datacorrectly                       | None        |
|:-------------------------------------------|:------------|
| Content-Type:image/jpeg                    |             |
| Content-Length:171648                      |             |
| Connection:keep-alive                      |             |
| X-Frame-Options:SAMEORIGIN                 |             |
| X-XSS-Protection:1;mode=block              |             |
| X-Content-Type-Options:nosniff             |             |
| .............................(Filecontent) |             |
| Fielddescription                           |             |
| Field                                      | description |
| name                                       | Picturename |

### Table from Page 234

| Parameter   | M/O   | Description            |
|:------------|:------|:-----------------------|
| source      | M     | Thenameofthesourcefile |
| output      | M     | Videofilesstoragename  |

### Table from Page 235

| Dataexample          |
|:---------------------|
| [{                   |
| "cmd":"NvrDownload", |
| "action":1,          |
| "param":{            |
| "NvrDownload":{      |
| "channel":0,         |
| "streamType":"sub",  |
| "StartTime":{        |
| "year":2022,         |
| "mon":8,             |
| "day":9,             |
| "hour":0,            |
| "min":1,             |

### Table from Page 236

| "sec":21         | None                                       | None   |
| },               |                                            |        |
| "EndTime":{      |                                            |        |
| "year":2022,     |                                            |        |
| "mon":8,         |                                            |        |
| "day":9,         |                                            |        |
| "hour":0,        |                                            |        |
| "min":1,         |                                            |        |
| "sec":41         |                                            |        |
| }                |                                            |        |
| }                |                                            |        |
| }                |                                            |        |
| }]               |                                            |        |
|:-----------------|:-------------------------------------------|:-------|
| Fielddescription |                                            |        |
| Field            | Description                                | M/O    |
| StartTime        | Starttime                                  | O      |
| EndTime          | Endtime                                    | O      |
| streamType       | Thebitstreamtypeofthefiletodownload,mainor | O      |
|                  | sub                                        |        |

### Table from Page 236

| Return datacorrectly                         |
|:---------------------------------------------|
| [                                            |
| {                                            |
| "cmd":"NvrDownload",                         |
| "code":0,                                    |
| "value":{                                    |
| "fileCount":10,                              |
| "fileList":[                                 |
| {                                            |
| "fileName":"fragment_01_20201224101100.mp4", |
| "fileSize":"2122011"                         |
| },                                           |
| {                                            |
| "fileName":"fragment_01_20201224100925.mp4", |
| "fileSize":"39858411"                        |
| },                                           |
| {                                            |
| "fileName":"fragment_01_20201224101151.mp4", |

### Table from Page 237

| "fileSize":"2728197"                           | None        |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224100848.mp4",   |             |
| "fileSize":"14158847"                          |             |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224100800.mp4",   |             |
| "fileSize":"11221990"                          |             |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224100834.mp4",   |             |
| "fileSize":"2303298"                           |             |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224101201.mp4",   |             |
| "fileSize":"7295191"                           |             |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224101135.mp4",   |             |
| "fileSize":"2182079"                           |             |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224101125.mp4",   |             |
| "fileSize":"2222880"                           |             |
| },                                             |             |
| {                                              |             |
| "fileName":"fragment_01_20201224101222.mp4",   |             |
| "fileSize":"18956748"                          |             |
| }                                              |             |
| ]                                              |             |
| }                                              |             |
| }                                              |             |
| ]                                              |             |
|:-----------------------------------------------|:------------|
| Fielddescription                               |             |
| Field                                          | description |
| Filename                                       | nameoffile  |
| Filesize                                       | Szieoffile  |

### Table from Page 238

| Dataexample           | None              | None   |
|:----------------------|:------------------|:-------|
| [                     |                   |        |
| {                     |                   |        |
| "cmd":"GetPtzPreset", |                   |        |
| "action":1,           |                   |        |
| "param":{             |                   |        |
| "channel":0           |                   |        |
| }                     |                   |        |
| }                     |                   |        |
| ]                     |                   |        |
| Fielddescription      |                   |        |
| Field                 | Description       | M/O    |
| channel               | Thechannelnumber. | M      |

### Table from Page 238

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetPtzPreset",  |
| "code":0,              |
| "initial":{            |

### Table from Page 256

| "name":""        |
| },               |
| {                |
| "channel":0,     |
| "enable":0,      |
| "id":59,         |
| "name":""        |
| },               |
| {                |
| "channel":0,     |
| "enable":0,      |
| "id":60,         |
| "name":""        |
| },               |
| {                |
| "channel":0,     |
| "enable":0,      |
| "id":61,         |
| "name":""        |
| },               |
| {                |
| "channel":0,     |
| "enable":0,      |
| "id":62,         |
| "name":""        |
| },               |
| {                |
| "channel":0,     |
| "enable":0,      |
| "id":63,         |
| "name":""        |
| },               |
| {                |
| "channel":0,     |
| "enable":0,      |
| "id":64,         |
| "name":""        |
| }                |
| ]                |
| }                |
| }                |
| ]                |
|:-----------------|
| Fielddescription |

### Table from Page 257

| Field   | description                                       |
|:--------|:--------------------------------------------------|
| enable  | Presetswitch,Thevalueof1representstheopen,andthe0 |
|         | istheopposite.                                    |
| id      | IDnumberofthePreset.                              |
| name    | NameofthePreset.                                  |

### Table from Page 257

| Dataexample           | None              | None   |
|:----------------------|:------------------|:-------|
| [                     |                   |        |
| {                     |                   |        |
| "cmd":"SetPtzPreset", |                   |        |
| "action":0,           |                   |        |
| "param":{             |                   |        |
| "PtzPreset":{         |                   |        |
| "channel":0,          |                   |        |
| "enable":1,           |                   |        |
| "id":1,               |                   |        |
| "name":"pos1"         |                   |        |
| }                     |                   |        |
| }                     |                   |        |
| }                     |                   |        |
| ]                     |                   |        |
| Fielddescription      |                   |        |
| Field                 | Description       | M/O    |
| channel               | IPCchannelnumber. | M      |

### Table from Page 258

| enable   | 1meansthatison,and0meansit’soff.Ifthatfield    | O   |
|          | doesn’texistitmeansonlythenameofthepresetcan   |     |
|          | berevised.                                     |     |
|:---------|:-----------------------------------------------|:----|
| id       | IDnumberofpreset.Range[1~64].                  | M   |
| name     | Nameofpreset,limit1~31characters.              | M   |

### Table from Page 258

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetPtzPreset",  |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 259

| [                       | None              | None   |
| {                       |                   |        |
| "cmd":"GetPtzPatrol",   |                   |        |
| "action":1,             |                   |        |
| "param":{               |                   |        |
| "channel":0             |                   |        |
| }                       |                   |        |
| }                       |                   |        |
| ]                       |                   |        |
|:------------------------|:------------------|:-------|
| Fielddescription        |                   |        |
| Field                   | Description       | M/O    |
| channel                 | Thechannelnumber. | M      |

### Table from Page 259

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetPtzPatrol",  |
| "code":0,              |
| "range":{              |
| "PtzPatrol":{          |
| "enable":"boolean",    |
| "id":{                 |
| "max":1,               |
| "min":1                |
| },                     |
| "name":{               |
| "maxLen":31            |
| },                     |
| "preset":{             |
| "dwellTime":{          |
| "max":30,              |
| "min":1                |
| },                     |
| "id":{                 |
| "max":64,              |
| "min":1                |
| },                     |
| "speed":{              |
| "max":64,              |
| "min":1                |

### Table from Page 262

| "preset":[       | None                                          |
| {                |                                               |
| "dwellTime":3,   |                                               |
| "id":1,          |                                               |
| "speed":10       |                                               |
| },               |                                               |
| {                |                                               |
| "dwellTime":4,   |                                               |
| "id":2,          |                                               |
| "speed":20       |                                               |
| }                |                                               |
| ],               |                                               |
| "running":0      |                                               |
| },               |                                               |
| {                |                                               |
| "channel":0,     |                                               |
| "enable":0,      |                                               |
| "id":6,          |                                               |
| "name":"",       |                                               |
| "preset":[       |                                               |
| {                |                                               |
| "dwellTime":3,   |                                               |
| "id":1,          |                                               |
| "speed":10       |                                               |
| },               |                                               |
| {                |                                               |
| "dwellTime":4,   |                                               |
| "id":2,          |                                               |
| "speed":20       |                                               |
| }                |                                               |
| ],               |                                               |
| "running":0      |                                               |
| }                |                                               |
| ]                |                                               |
| }                |                                               |
| }                |                                               |
| ]                |                                               |
|:-----------------|:----------------------------------------------|
| Fielddescription |                                               |
| Field            | description                                   |
| enable           | Patrolswitch,Thevalue1meansthat’senabled,and0 |
|                  | meanstheopposite.                             |

### Table from Page 263

| id                | IDnumberofthePatrol.   |
|:------------------|:-----------------------|
| running           | Whetherrunningornot    |
| preset->dwellTime | Patroltime             |
| Preset->id        | IDnumberofthepreset    |
| preset->speed     | Patrolspeed            |
| name              | Nameofthepatrol        |

### Table from Page 263

| Dataexample           |
|:----------------------|
| [                     |
| {                     |
| "cmd":"SetPtzPatrol", |
| "action":0,           |
| "param":{             |
| "PtzPatrol":{         |
| "channel":0,          |
| "enable":1,           |
| "id":1,               |
| “running”:0,          |
| “name”:”hello”        |
| "preset":[            |
| {                     |
| "dwellTime":3,        |
| "id":1,               |
| "speed":10            |
| },                    |
| {                     |

### Table from Page 264

| "dwellTime":4,            | None                          | None   |
| "id":2,                   |                               |        |
| "speed":20                |                               |        |
| }                         |                               |        |
| ]                         |                               |        |
| }                         |                               |        |
| }                         |                               |        |
| }                         |                               |        |
| ]                         |                               |        |
|:--------------------------|:------------------------------|:-------|
| Fielddescription          |                               |        |
| Field                     | Description                   | M/O    |
| channel                   | IPCchannelnumber.             | M      |
| enable                    | Whetherenablethepresetornot   | M      |
| id                        | IDnumberofPatrol.             | M      |
| Preset->dwellTime         | Patroltime                    | M      |
| Preset->id                | IDnumberofpreset.Range[1~64]. | M      |
| Preset->speed             | Patrolspeed                   | M      |
| Note:Supportupto16preset. |                               |        |

### Table from Page 264

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetPtzPatrol",  |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 265

| Dataexample      |
|:-----------------|
| [                |
| {                |
| "cmd":"PtzCtrl", |
| "param":{        |
| "channel":0,     |
| "op":"Auto",     |
| "speed":32       |
| }                |
| },               |
| {                |
| "cmd":"PtzCtrl", |
| "param":{        |
| "channel":0,     |
| "op":"Stop"      |
| }                |
| },               |
| {                |
| "cmd":"PtzCtrl", |
| "param":{        |
| "channel":0,     |
| "op":"ToPos",    |
| "id":1,          |
| "speed":32       |
| }                |
| }                |
| ]                |
| Fielddescription |

### Table from Page 266

| Field   | Description                     | M/O   |
|:--------|:--------------------------------|:------|
| channel | IPCchannelnumber.               | M     |
| op      | OperationtocontrolthePTZ.       | M     |
| id      | PresetidnumberorPatrolidnumber. | O     |
| speed   | PTZrunningspeed.                | O     |

### Table from Page 266

| Return datacorrectly                                              | None         |
|:------------------------------------------------------------------|:-------------|
| [                                                                 |              |
| {                                                                 |              |
| "cmd":"PtzCtrl",                                                  |              |
| "code":0,                                                         |              |
| "value":{                                                         |              |
| "rspCode":200                                                     |              |
| }                                                                 |              |
| },                                                                |              |
| {                                                                 |              |
| "cmd":"PtzCtrl",                                                  |              |
| "code":0,                                                         |              |
| "value":{                                                         |              |
| "rspCode":200                                                     |              |
| }                                                                 |              |
| },                                                                |              |
| {                                                                 |              |
| "cmd":"PtzCtrl",                                                  |              |
| "code":0,                                                         |              |
| "value":{                                                         |              |
| "rspCode":200                                                     |              |
| }                                                                 |              |
| }                                                                 |              |
| ]                                                                 |              |
| Fielddescription                                                  |              |
| Field                                                             | description  |
| rspCode                                                           | Responsecode |
| Notes:                                                            |              |
| connecttotheptzcommand,someparametersareunneeded.youjustsetit"0". |              |

### Table from Page 268

| Dataexample           | None              | None   |
|:----------------------|:------------------|:-------|
| [                     |                   |        |
| {                     |                   |        |
| "cmd":"GetPtzSerial", |                   |        |
| "action":1,           |                   |        |
| "param":{             |                   |        |
| "channel":0           |                   |        |
| }                     |                   |        |
| }                     |                   |        |
| ]                     |                   |        |
| Fielddescription      |                   |        |
| Field                 | Description       | M/O    |
| channel               | Thechannelnumber. | M      |

### Table from Page 268

| Return datacorrectly              |
|:----------------------------------|
| [                                 |
| {                                 |
| "cmd":"GetPtzSerial",             |
| "code":0,                         |
| "initial":{                       |
| "PtzSerial":{                     |
| "baudRate":1200,                  |
| "channel":0,                      |
| "ctrlAddr":0,                     |
| "ctrlProtocol":"PELCO_D",         |
| "dataBit":"CS8",                  |
| "flowCtrl":"none",                |
| "parity":"none",                  |
| "stopBit":1                       |
| }                                 |
| },                                |
| "range":{                         |
| "PtzSerial":{                     |
| "baudRate":[1200,2400,4800,9600], |
| "channel":0,                      |
| "ctrlAddr":{                      |
| "max":64,                         |

### Table from Page 269

| "min":1                                    | None                               |
| },                                         |                                    |
| "ctrlProtocol":["PELCO_D","PELCO_P"],      |                                    |
| "dataBit":["CS8","CS7","CS6","CS5"],       |                                    |
| "flowCtrl":["none","hard","xon","xoff"],   |                                    |
| "parity":["none","odd","even"],            |                                    |
| "stopBit":[1,2]                            |                                    |
| }                                          |                                    |
| },                                         |                                    |
| "value":{                                  |                                    |
| "PtzSerial":{                              |                                    |
| "baudRate":1200,                           |                                    |
| "channel":0,                               |                                    |
| "ctrlAddr":0,                              |                                    |
| "ctrlProtocol":"PELCO_D",                  |                                    |
| "dataBit":"CS8",                           |                                    |
| "flowCtrl":"none",                         |                                    |
| "parity":"none",                           |                                    |
| "stopBit":1                                |                                    |
| }                                          |                                    |
| }                                          |                                    |
| }                                          |                                    |
| ]                                          |                                    |
|:-------------------------------------------|:-----------------------------------|
| Fielddescription                           |                                    |
| Field                                      | description                        |
| channel                                    | Thechannelnumber.                  |
| baudRate                                   | Thebaudrateoftheserialinptz        |
| ctrlAddr                                   | Thecontroladdressoftheserialinptz  |
| ctrlProtocol                               | Thecontrolprotocoloftheserialinptz |
| dataBit                                    | Thedatabitoftheserialinptz         |
| flowCtrl                                   | Theflowcontroloftheserialinptz     |
| parity                                     | Theparityoftheserialinptz          |
| stopBit                                    | Thestopbitoftheserialinptz         |

### Table from Page 270

| Dataexample               | None                                       | None   |
|:--------------------------|:-------------------------------------------|:-------|
| [                         |                                            |        |
| {                         |                                            |        |
| "cmd":"SetPtzSerial",     |                                            |        |
| "action":0,               |                                            |        |
| "param":{                 |                                            |        |
| "PtzSerial":{             |                                            |        |
| "channel":0,              |                                            |        |
| "baudRate":9600,          |                                            |        |
| "dataBit":"CS6",          |                                            |        |
| "stopBit":2,              |                                            |        |
| "parity":"odd",           |                                            |        |
| "flowCtrl":"hard",        |                                            |        |
| "crtlProtocol":"PELCO_P", |                                            |        |
| "ctrlAddr":2              |                                            |        |
| }                         |                                            |        |
| }                         |                                            |        |
| }                         |                                            |        |
| ]                         |                                            |        |
| Fielddescription          |                                            |        |
| Field                     | Description                                | M/O    |
| channel                   | Thechannelnumber.                          | M      |
| baudRate                  | Thebaudrateoftheserialinptz                | O      |
| ctrlAddr                  | Thecontroladdressoftheserialinptz,whichis  | O      |
|                           | defaultequaltochannelplus1                 |        |
| ctrlProtocol              | Thecontrolprotocoloftheserialinptz,whichis | O      |

### Table from Page 271

|          | between“PELCO_D”and“PELCO_P”              |    |
|:---------|:------------------------------------------|:---|
| dataBit  | Thedatabitoftheserialinptz,whichisbetween | O  |
|          | “CS8”,“CS7”,“CS6”and“CS5”                 |    |
| flowCtrl | Theflowcontroloftheserialinptz,whichis    | O  |
|          | between“none”,“hard”,“xon”and“xoff”       |    |
| parity   | Theparityoftheserialinptz,whichisbetween  | O  |
|          | “none”,“odd”and“even”                     |    |
| stopBit  | Thestopbitoftheserialinptz,whichcanbe1or  | O  |
|          | 2                                         |    |

### Table from Page 271

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetPtzSerial",  |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 272

| Dataexample            | None              | None   |
|:-----------------------|:------------------|:-------|
| [                      |                   |        |
| {                      |                   |        |
| "cmd":"GetPtzTattern", |                   |        |
| "action":1,            |                   |        |
| "param":{              |                   |        |
| "channel":0            |                   |        |
| }                      |                   |        |
| }                      |                   |        |
| ]                      |                   |        |
| Fielddescription       |                   |        |
| Field                  | Description       | M/O    |
| channel                | Thechannelnumber. | M      |

### Table from Page 272

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetPtzTattern", |
| "code":0,              |
| "initial":{            |
| "PtzTattern":{         |
| "channel":0,           |
| "track":[              |
| {                      |
| "enable":0,            |
| "id":1,                |
| "name":"",             |
| "running":0            |
| },                     |
| {                      |
| "enable":0,            |
| "id":1,                |
| "name":"",             |
| "running":0            |

### Table from Page 275

|                  | None                                              |
|:-----------------|:--------------------------------------------------|
| Fielddescription |                                                   |
| Field            | description                                       |
| channel          | Thechannelnumber.                                 |
| id               | IDnumberofthetrack.                               |
| name             | Thenameofthetrack                                 |
| enable           | Trackswitch,Thevalue1meansthat’senabled,and0means |
|                  | theopposite                                       |
| running          | Whetherrunningornot                               |

### Table from Page 275

| Dataexample            |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetPtzTattern", |
| "action":0,            |
| "param":{              |
| "PtzTattern":{         |
| "channel":0,           |
| "track":[              |
| {                      |
| "id":1,                |
| "enable":0,            |
| "running":0,           |
| "name":"track1"        |
| },                     |

### Table from Page 276

| {                 | None                                     | None   |
| "id":2,           |                                          |        |
| "enable":0,       |                                          |        |
| "running":0,      |                                          |        |
| "name":"track2"   |                                          |        |
| }                 |                                          |        |
| ]                 |                                          |        |
| }                 |                                          |        |
| }                 |                                          |        |
| }                 |                                          |        |
| ]                 |                                          |        |
|:------------------|:-----------------------------------------|:-------|
| Fielddescription  |                                          |        |
| Field             | Description                              | M/O    |
| channel           | Thechannelnumber.                        | M      |
| id                | IDnumberofthetrack.Range[1~6]            | M      |
| name              | Thenameofthetrack                        | O      |
| enable            | Trackswitch,Thevalue1meansthat’senabled, | O      |
|                   | and0meanstheopposite                     |        |
| running           | Whetherrunningornot                      | O      |

### Table from Page 276

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetPtzTattern", |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 277

| Dataexample           | None              | None   |
|:----------------------|:------------------|:-------|
| [                     |                   |        |
| {                     |                   |        |
| "cmd":"GetAutoFocus", |                   |        |
| "action":1,           |                   |        |
| "param":{             |                   |        |
| "channel":0           |                   |        |
| }                     |                   |        |
| }                     |                   |        |
| ]                     |                   |        |
| Fielddescription      |                   |        |
| Field                 | Description       | M/O    |
| channel               | Thechannelnumber. | M      |

### Table from Page 277

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetAutoFocus",  |
| "code":0,              |
| "initial":{            |
| "AutoFocus":{          |
| "channel":0,           |
| "disable":0            |
| }                      |
| },                     |

### Table from Page 278

| "range":{             | None                            |
| "AutoFocus":{         |                                 |
| "disable":"boolean"   |                                 |
| }                     |                                 |
| },                    |                                 |
| "value":{             |                                 |
| "AutoFocus":{         |                                 |
| "disable":0           |                                 |
| }                     |                                 |
| }                     |                                 |
| }                     |                                 |
| ]                     |                                 |
|:----------------------|:--------------------------------|
| Fielddescription      |                                 |
| Field                 | description                     |
| disable               | Forbidtheautofocusoftheptzornot |

### Table from Page 278

| Dataexample           |
|:----------------------|
| [                     |
| {                     |
| "cmd":"SetAutoFocus", |
| "action":0,           |
| "param":{             |
| "AutoFocus":{         |
| "channel":0,          |
| "disable":1           |
| }                     |

### Table from Page 279

| }                | None                              | None   |
| }                |                                   |        |
| ]                |                                   |        |
|:-----------------|:----------------------------------|:-------|
| Fielddescription |                                   |        |
| Field            | Description                       | M/O    |
| disable          | Forbidtheautofocusoftheptz,1means | M      |
|                  | forbidding,0meansenabling         |        |

### Table from Page 279

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetAutoFocus",  |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 280

| [{                      | None              | None   |
| "cmd":"GetZoomFocus",   |                   |        |
| "action":0,             |                   |        |
| "param":{               |                   |        |
| "channel":0             |                   |        |
| }                       |                   |        |
| }]                      |                   |        |
|:------------------------|:------------------|:-------|
| Fielddescription        |                   |        |
| Field                   | Description       | M/O    |
| channel                 | Thechannelnumber. | M      |

### Table from Page 280

| Return datacorrectly   | None                            |
|:-----------------------|:--------------------------------|
| [                      |                                 |
| {                      |                                 |
| "cmd":"GetZoomFocus",  |                                 |
| "code":0,              |                                 |
| "value":{              |                                 |
| "ZoomFocus":{          |                                 |
| "channel":0,           |                                 |
| "focus":{              |                                 |
| "pos":23               |                                 |
| },                     |                                 |
| "zoom":{               |                                 |
| "pos":0                |                                 |
| }                      |                                 |
| }                      |                                 |
| }                      |                                 |
| }                      |                                 |
| ]                      |                                 |
| Fielddescription       |                                 |
| Field                  | description                     |
| disable                | Forbidtheautofocusoftheptzornot |

### Table from Page 281

| Dataexample             | None              | None   |
|:------------------------|:------------------|:-------|
| [{                      |                   |        |
| "cmd":"StartZoomFocus", |                   |        |
| "action":0,             |                   |        |
| "param":{               |                   |        |
| "ZoomFocus":{           |                   |        |
| "channel":0,            |                   |        |
| "pos":6,                |                   |        |
| "op":"ZoomPos"          |                   |        |
| }                       |                   |        |
| }                       |                   |        |
| }]                      |                   |        |
| Fielddescription        |                   |        |
| Field                   | Description       | M/O    |
| channel                 | Thechannelnumber. | M      |
| pos                     | Movetotheposition |        |
| op                      | Controlcommand    | O      |

### Table from Page 281

| Return datacorrectly    |
|:------------------------|
| [                       |
| {                       |
| "cmd":"StartZoomFocus", |
| "code":0,               |
| "value":{               |
| "rspCode":200           |
| }                       |
| }                       |
| ]                       |

### Table from Page 282

|                  | None         |
|:-----------------|:-------------|
| Fielddescription |              |
| Field            | description  |
| rspCode          | Responsecode |

### Table from Page 282

| Dataexample          | None              | None   |
|:---------------------|:------------------|:-------|
| [{                   |                   |        |
| "cmd":"GetPtzGuard", |                   |        |
| "action":0,          |                   |        |
| "param":{            |                   |        |
| "channel":0          |                   |        |
| }                    |                   |        |
| }]                   |                   |        |
| Fielddescription     |                   |        |
| Field                | Description       | M/O    |
| channel              | Thechannelnumber. | M      |

### Table from Page 282

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetPtzGuard",   |
| "code":0,              |
| "value":{              |
| "PtzGuard":{           |

### Table from Page 283

| "benable":1,     | None                                      |
| "bexistPos":1,   |                                           |
| "channel":0,     |                                           |
| "timeout":60     |                                           |
| }                |                                           |
| }                |                                           |
| }                |                                           |
| ]                |                                           |
|:-----------------|:------------------------------------------|
| Fielddescription |                                           |
| Field            | description                               |
| benable          | whetherautomaticallyreturntoguardposition |
| bexistPos        | Whether there is a guard position         |
| channel          | Devicechannelnumber                       |
| timeout          | Timeofautomaticallyreturntoguardposition  |

### Table from Page 283

| Dataexample          |
|:---------------------|
| [                    |
| {                    |
| "cmd":"SetPtzGuard", |
| "action":0,          |
| "param":{            |
| "PtzGuard":{         |
| "channel":0,         |
| "cmdStr":“”,         |
| “benable”:1,         |
| “bexistPos”:1,       |

### Table from Page 284

| “timeout”:60,         | None                                      | None   |
| “bSaveCurrentPos”:1   |                                           |        |
| }                     |                                           |        |
| }                     |                                           |        |
| }                     |                                           |        |
| ]                     |                                           |        |
|:----------------------|:------------------------------------------|:-------|
| Fielddescription      |                                           |        |
| Field                 | Description                               | M/O    |
| cmdStr                | setPos/toPos                              | M      |
|                       | setpos:setthisposasguard                  |        |
|                       | topos:gototheguard                        |        |
| benable               | whetherautomaticallyreturntoguardposition | O      |
| timeout               | Timeofautomaticallyreturntoguardposition  | O      |
|                       | Canonlybe60secondnow                      |        |
| bsaveCurrentPos       | Whethersetthisposasguard                  | O      |

### Table from Page 284

| Return datacorrectly   | None         |
|:-----------------------|:-------------|
| [                      |              |
| {                      |              |
| "cmd":"SetPtzGuard",   |              |
| "code":0,              |              |
| "value":{              |              |
| "rspCode":200          |              |
| }                      |              |
| }                      |              |
| ]                      |              |
| Fielddescription       |              |
| Field                  | description  |
| rspCode                | Responsecode |

### Table from Page 285

| Dataexample               | None              | None   |
|:--------------------------|:------------------|:-------|
| [{                        |                   |        |
| "cmd":"GetPtzCheckState", |                   |        |
| "action":0,               |                   |        |
| "param":{                 |                   |        |
| "channel":0               |                   |        |
| }                         |                   |        |
| }]                        |                   |        |
| Fielddescription          |                   |        |
| Field                     | Description       | M/O    |
| channel                   | Thechannelnumber. | M      |

### Table from Page 285

| Return datacorrectly      | None                            |
|:--------------------------|:--------------------------------|
| [                         |                                 |
| {                         |                                 |
| "cmd":"GetPtzCheckState", |                                 |
| "code":0,                 |                                 |
| "value":{                 |                                 |
| "PtzCheckState":2         |                                 |
| }                         |                                 |
| }                         |                                 |
| ]                         |                                 |
| Fielddescription          |                                 |
| Field                     | description                     |
| disable                   | Forbidtheautofocusoftheptzornot |
| PtzCheckState             | 0:idle,1:doing,2:finish         |

### Table from Page 286

| Dataexample       | None           | None   |
|:------------------|:---------------|:-------|
| [{                |                |        |
| "cmd":"PtzCheck", |                |        |
| "action":1,       |                |        |
| "param":{         |                |        |
| "channel":0       |                |        |
| }                 |                |        |
| }]                |                |        |
| Fielddescription  |                |        |
| Field             | Description    | M/O    |
| channel           | Indexofchannel | M      |

### Table from Page 286

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"PtzCheck",      |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |
| Fielddescription       |

### Table from Page 287

| Field   | description   |
|:--------|:--------------|
| rspCode | Responsecode  |

### Table from Page 287

| Dataexample       | None                         | None   |
|:------------------|:-----------------------------|:-------|
| [                 |                              |        |
| {                 |                              |        |
| "cmd":"GetAlarm", |                              |        |
| "action":1,       |                              |        |
| "param":{         |                              |        |
| "Alarm":{         |                              |        |
| "type":"md",      |                              |        |
| "channel":0       |                              |        |
| }                 |                              |        |
| }                 |                              |        |
| }                 |                              |        |
| ]                 |                              |        |
| Fielddescription  |                              |        |
| Field             | Description                  | M/O    |
| channel           | Indexofchannel               | M      |
| type              | Alarmtype,onlysupport"md"now | M      |

### Table from Page 288

| Return datacorrectly                                               |
|:-------------------------------------------------------------------|
| [                                                                  |
| {                                                                  |
| "cmd":"GetAlarm",                                                  |
| "code":0,                                                          |
| "initial":{                                                        |
| "Alarm":{                                                          |
| "channel":0,                                                       |
| "scope":{                                                          |
| "cols":80,                                                         |
| "rows":45,                                                         |
| "table":                                                           |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |

### Table from Page 295

| "endMin":59,                                                  | None                                                 |
| "id":3,                                                       |                                                      |
| "sensitivity":9                                               |                                                      |
| }                                                             |                                                      |
| ],                                                            |                                                      |
| "type":"md"                                                   |                                                      |
| }                                                             |                                                      |
| }                                                             |                                                      |
| }                                                             |                                                      |
| ]                                                             |                                                      |
|:--------------------------------------------------------------|:-----------------------------------------------------|
| Fielddescription                                              |                                                      |
| Field                                                         | description                                          |
| channel                                                       | Channelnumber                                        |
| scope                                                         | Motiondetectionscope,consistingof80columnsand45      |
|                                                               | rows.Appointedbycolsandrows.                         |
| cols                                                          | Thenumberofcol                                       |
| rows                                                          | Thenumberofrow                                       |
| table(scope)                                                  | Astringwiththelengthof80*45,eachbyterepresentsan     |
|                                                               | area.Withthevalue1motiondetectionisactiveinthat      |
|                                                               | periodoftime.Withthevalueof0noresponsewillbemade     |
|                                                               | withanydetectedmotion.                               |
| sens                                                          | Thesensitivitysettingsformotiondetection.Itisdevided |
|                                                               | into4intervalsbytime.                                |
| beginHour                                                     | Thestarthour.                                        |
| beginMin                                                      | Thestartminute.                                      |
| endHour                                                       | Theendinghour.                                       |
| endMin                                                        | Theendingminute.                                     |
| sensitivity                                                   | Sensitivity                                          |
| id                                                            | Sectionindex                                         |
| type                                                          | Alarmtype,only“md”issupported.                       |
| Note:                                                         |                                                      |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“GetMdAlarm” |                                                      |

### Table from Page 296

| Dataexample                                                        |
|:-------------------------------------------------------------------|
| [                                                                  |
| {                                                                  |
| "cmd":"SetAlarm",                                                  |
| "param":{                                                          |
| "Alarm":{                                                          |
| "channel":0,                                                       |
| "scope":{                                                          |
| "cols":80,                                                         |
| "rows":60,                                                         |
| "table":                                                           |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |

### Table from Page 299

| }                                                             | None            | None   |
| ]                                                             |                 |        |
|:--------------------------------------------------------------|:----------------|:-------|
| Fielddescription                                              |                 |        |
| Field                                                         | Description     | M/O    |
| channel                                                       | SeealsoGetAlarm | M      |
| scope                                                         | SeealsoGetAlarm | O      |
| cols                                                          | SeealsoGetAlarm | O      |
| rows                                                          | SeealsoGetAlarm | O      |
| table                                                         | SeealsoGetAlarm | O      |
| sens                                                          | SeealsoGetAlarm | O      |
| beginHour                                                     | SeealsoGetAlarm | O      |
| beginMin                                                      | SeealsoGetAlarm | O      |
| endHour                                                       | SeealsoGetAlarm | O      |
| endMin                                                        | SeealsoGetAlarm | O      |
| sensitivity                                                   | SeealsoGetAlarm | O      |
| id                                                            | SeealsoGetAlarm | O      |
| type                                                          | SeealsoGetAlarm | M      |
| Note:                                                         |                 |        |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“SetMdAlarm” |                 |        |

### Table from Page 299

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetAlarm",      |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 300

| Dataexample         | None           | None   |
|:--------------------|:---------------|:-------|
| [{                  |                |        |
| "cmd":"GetMdAlarm", |                |        |
| "action":1,         |                |        |
| "param":{           |                |        |
| "channel":0         |                |        |
| }                   |                |        |
| }]                  |                |        |
| Fielddescription    |                |        |
| Field               | Description    | M/O    |
| channel             | Indexofchannel | M      |

### Table from Page 300

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetMdAlarm",    |
| "code":0,              |
| "initial":{            |
| "MdAlarm":{            |
| "channel":0,           |
| "newSens":{            |
| "sens":[               |
| {                      |

### Table from Page 313

| 111111111111111111111111111111111111111111111111111111111111111111   |
| 1111111111111111111111111111111111111111111111111"                   |
| },                                                                   |
| "sens":[                                                             |
| {                                                                    |
| "beginHour":0,                                                       |
| "beginMin":0,                                                        |
| "endHour":6,                                                         |
| "endMin":0,                                                          |
| "id":0,                                                              |
| "sensitivity":9                                                      |
| },                                                                   |
| {                                                                    |
| "beginHour":6,                                                       |
| "beginMin":0,                                                        |
| "endHour":12,                                                        |
| "endMin":0,                                                          |
| "id":1,                                                              |
| "sensitivity":9                                                      |
| },                                                                   |
| {                                                                    |
| "beginHour":12,                                                      |
| "beginMin":0,                                                        |
| "endHour":18,                                                        |
| "endMin":0,                                                          |
| "id":2,                                                              |
| "sensitivity":9                                                      |
| },                                                                   |
| {                                                                    |
| "beginHour":18,                                                      |
| "beginMin":0,                                                        |
| "endHour":23,                                                        |
| "endMin":59,                                                         |
| "id":3,                                                              |
| "sensitivity":9                                                      |
| }                                                                    |
| ],                                                                   |
| "useNewSens":1 //NVR                                                 |
| }                                                                    |
| }                                                                    |
| }                                                                    |
| ]                                                                    |
|:---------------------------------------------------------------------|
| Fielddescription                                                     |

### Table from Page 314

| Field        | description                                          |
|:-------------|:-----------------------------------------------------|
| channel      | Channelnumber                                        |
| scope        | Motiondetectionscope,consistingof80columnsand45      |
|              | rows.Appointedbycolsandrows.                         |
| cols         | Thenumberofcol                                       |
| rows         | Thenumberofrow                                       |
| table(scope) | Astringwiththelengthof80*45,eachbyterepresentsan     |
|              | area.Withthevalue1motiondetectionisactiveinthat      |
|              | periodoftime.Withthevalueof0noresponsewillbemade     |
|              | withanydetectedmotion.                               |
| sens         | Thesensitivitysettingsformotiondetection.Itisdevided |
|              | into4intervalsbytime.                                |
| beginHour    | Thestarthour.                                        |
| beginMin     | Thestartminute.                                      |
| endHour      | Theendinghour.                                       |
| endMin       | Theendingminute.                                     |
| sensitivity  | Sensitivity                                          |
| id           | Sectionindex                                         |
| type         | Alarmtype,only“md”issupported.                       |
| priority     | Priorityofalarmtype                                  |
| sensDef      | Thesensitiveityvalue                                 |
| useNewSens   |                                                      |

### Table from Page 315

| Dataexample                                                        |
|:-------------------------------------------------------------------|
| [{                                                                 |
| "cmd":"SetMdAlarm",                                                |
| "param":{                                                          |
| "MdAlarm":{                                                        |
| "channel":0,                                                       |
| "scope":{                                                          |
| "cols":120,                                                        |
| "rows":67,                                                         |
| "table":                                                           |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |

### Table from Page 318

| 111111111111111111111111111111111111111111111111111111111111111111   | None            | None   |
| 111111111111111111111111111111111111111111111111111111111111111111   |                 |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                 |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                 |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                 |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                 |        |
| 1111111111111111111111111111111111111111111111111111111"             |                 |        |
| },                                                                   |                 |        |
| "useNewSens":1,                                                      |                 |        |
| "newSens":{                                                          |                 |        |
| "sensDef":10,                                                        |                 |        |
| "sens":{                                                             |                 |        |
| "sensitivity":10,                                                    |                 |        |
| "beginHour":0,                                                       |                 |        |
| "beginMin":0,                                                        |                 |        |
| "endHour":6,                                                         |                 |        |
| "endMin":0,                                                          |                 |        |
| "priority":0,                                                        |                 |        |
| "enable":0                                                           |                 |        |
| }                                                                    |                 |        |
| }                                                                    |                 |        |
| }                                                                    |                 |        |
| }                                                                    |                 |        |
| }]                                                                   |                 |        |
|:---------------------------------------------------------------------|:----------------|:-------|
| Fielddescription                                                     |                 |        |
| Field                                                                | Description     | M/O    |
| channel                                                              | SeealsoGetAlarm | M      |
| scope                                                                | SeealsoGetAlarm | O      |
| cols                                                                 | SeealsoGetAlarm | O      |
| rows                                                                 | SeealsoGetAlarm | O      |
| table                                                                | SeealsoGetAlarm | O      |
| sens                                                                 | SeealsoGetAlarm | O      |
| beginHour                                                            | SeealsoGetAlarm | O      |
| beginMin                                                             | SeealsoGetAlarm | O      |
| endHour                                                              | SeealsoGetAlarm | O      |
| endMin                                                               | SeealsoGetAlarm | O      |
| sensitivity                                                          | SeealsoGetAlarm | O      |

### Table from Page 319

| id       | SeealsoGetAlarm   | O   |
|:---------|:------------------|:----|
| type     | SeealsoGetAlarm   | M   |
| priority | SeealsoGetAlarm   |     |

### Table from Page 319

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetMdAlarm",    |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 319

| Dataexample   |
|:--------------|
| [             |
| {             |

### Table from Page 320

| "cmd":"GetMdState",                                           | None               | None   |
| "param":{                                                     |                    |        |
| "channel":0                                                   |                    |        |
| }                                                             |                    |        |
| }                                                             |                    |        |
| ]                                                             |                    |        |
|:--------------------------------------------------------------|:-------------------|:-------|
| Fielddescription                                              |                    |        |
| Field                                                         | Description        | M/O    |
| chnnel                                                        | Chnnelnum (ipcis0) | O      |
| Note: usethisurlnoneedtopostjsondate                          |                    |        |
| “https://IPC_IP/api.cgi?cmd=GetMdState&channel=0&token=TOKEN” |                    |        |

### Table from Page 320

| Return datacorrectly   | None                                            |
|:-----------------------|:------------------------------------------------|
| [                      |                                                 |
| {                      |                                                 |
| "cmd":"GetMdState",    |                                                 |
| "code":0,              |                                                 |
| "value":{              |                                                 |
| "state":0              |                                                 |
| }                      |                                                 |
| }                      |                                                 |
| ]                      |                                                 |
| Fielddescription       |                                                 |
| Field                  | description                                     |
| state                  | Thestateofmotiondetection.Thevalue1meansmotions |
|                        | havebeendetectedand0meansnomotionhasbeen        |
|                        | detected.                                       |

### Table from Page 321

| Dataexample                                                         | None        | None   |
|:--------------------------------------------------------------------|:------------|:-------|
| [                                                                   |             |        |
| {                                                                   |             |        |
| "cmd":"GetAudioAlarm",                                              |             |        |
| "action":1,                                                         |             |        |
| "param":{}                                                          |             |        |
| }                                                                   |             |        |
| ]                                                                   |             |        |
| Fielddescription                                                    |             |        |
| Field                                                               | Description | M/O    |
| Note:                                                               |             |        |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“GetAudioAlarmV20” |             |        |

### Table from Page 321

| Return datacorrectly                                               |
|:-------------------------------------------------------------------|
| [                                                                  |
| {                                                                  |
| "cmd":"GetAudioAlarm",                                             |
| "code":0,                                                          |
| "initial":{                                                        |
| "Audio":{                                                          |
| "schedule":{                                                       |
| "enable":0,                                                        |
| "table":                                                           |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 1111111111111111111111111111111111111"                             |
| }                                                                  |
| }                                                                  |

### Table from Page 322

| },                                                                   | None            |
| "range":{                                                            |                 |
| "Audio":{                                                            |                 |
| "schedule":{                                                         |                 |
| "enable":"boolean",                                                  |                 |
| "table":{                                                            |                 |
| "maxLen":168,                                                        |                 |
| "minLen":168                                                         |                 |
| }                                                                    |                 |
| }                                                                    |                 |
| }                                                                    |                 |
| },                                                                   |                 |
| "value":{                                                            |                 |
| "Audio":{                                                            |                 |
| "schedule":{                                                         |                 |
| "enable":0,                                                          |                 |
| "table":                                                             |                 |
| "11111111111111111111111111111111111111111111111111111111111111111   |                 |
| 111111111111111111111111111111111111111111111111111111111111111111   |                 |
| 1111111111111111111111111111111111111"                               |                 |
| }                                                                    |                 |
| }                                                                    |                 |
| }                                                                    |                 |
| }                                                                    |                 |
| ]                                                                    |                 |
|:---------------------------------------------------------------------|:----------------|
| Fielddescription                                                     |                 |
| Field                                                                | description     |
| table                                                                | SeealsoGetAlarm |

### Table from Page 323

| Dataexample                                                         | None            | None   |
|:--------------------------------------------------------------------|:----------------|:-------|
| [                                                                   |                 |        |
| {                                                                   |                 |        |
| "cmd":"SetAudioAlarm",                                              |                 |        |
| "param":{                                                           |                 |        |
| "Audio":{                                                           |                 |        |
| "schedule":{                                                        |                 |        |
| "enable":1,                                                         |                 |        |
| "table":                                                            |                 |        |
| "11111111111111111111111111111111111111111111111111111111111111111  |                 |        |
| 111111111111111111111111111111111111111111111111111111111111111111  |                 |        |
| 1111111111111111111111111111111"                                    |                 |        |
| }                                                                   |                 |        |
| }                                                                   |                 |        |
| }                                                                   |                 |        |
| }                                                                   |                 |        |
| ]                                                                   |                 |        |
| Fielddescription                                                    |                 |        |
| Field                                                               | Description     | M/O    |
| enable                                                              | SeealsoGetAlarm | O      |
| table                                                               | SeealsoGetAlarm | O      |
| Note:                                                               |                 |        |
| WhenscheduleVersionver=1inthecapabilityset,usecmd“SetAudioAlarmV20” |                 |        |

### Table from Page 323

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetAlarm",      |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |
| }                      |
| ]                      |
| Fielddescription       |

### Table from Page 324

| Data example              | None        | None   |
|:--------------------------|:------------|:-------|
| [                         |             |        |
| {                         |             |        |
| "cmd":"GetAudioAlarmV20", |             |        |
| "action":1,               |             |        |
| "param": {                |             |        |
| "channel": 0              |             |        |
| }                         |             |        |
| }                         |             |        |
| ]                         |             |        |
| Fielddescription          |             |        |
| Field                     | Description | M/O    |

### Table from Page 324

| Return data correctly      |
|:---------------------------|
| [                          |
| {                          |
| "cmd" :"GetAudioAlarmV20", |

### Table from Page 326

| "minLen" : 168                                                        | None               |
| }                                                                     |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| },                                                                    |                    |
| "value" : {                                                           |                    |
| "Audio": {                                                            |                    |
| "enable" : 0,                                                         |                    |
| "schedule" : {                                                        |                    |
| "channel" : 15,                                                       |                    |
| "table" : {                                                           |                    |
| "AI_PEOPLE" :                                                         |                    |
| "000000000000000000000000000000000000000000000000000000000000000000   |                    |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                    |
| 00000000000000000000000000000000000",                                 |                    |
| "AI_VEHICLE" :                                                        |                    |
| "000000000000000000000000000000000000000000000000000000000000000000   |                    |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                    |
| 00000000000000000000000000000000000",                                 |                    |
| "MD" :                                                                |                    |
| "111111111111111111111111111111111111111111111111111111111111111111   |                    |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                    |
| 11111111111111111111111111111111111"                                  |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| }                                                                     |                    |
| ]                                                                     |                    |
|:----------------------------------------------------------------------|:-------------------|
| Fielddescription                                                      |                    |
| Field                                                                 | description        |
| table                                                                 | Audio alarm switch |
| channel                                                               | Index ofchannel    |

### Table from Page 327

| Data example                                                        | None           | None   |
|:--------------------------------------------------------------------|:---------------|:-------|
| [{                                                                  |                |        |
| "cmd": "SetAudioAlarmV20",                                          |                |        |
| "param": {                                                          |                |        |
| "Audio": {                                                          |                |        |
| "enable": 1,                                                        |                |        |
| "schedule": {                                                       |                |        |
| "channel": 0,                                                       |                |        |
| "table": {                                                          |                |        |
| "MD":                                                               |                |        |
| "011111111111111111111111111111111111111111111111111111111111111111 |                |        |
| 1111111111111111111111111111111111111111111111111111111111111111111 |                |        |
| 11111111111111111111111111111111100"                                |                |        |
| }                                                                   |                |        |
| }                                                                   |                |        |
| }                                                                   |                |        |
| }                                                                   |                |        |
| }]                                                                  |                |        |
| Fielddescription                                                    |                |        |
| Field                                                               | Description    | M/O    |
| Schedule->en                                                        | Scheduleswitch | O      |

### Table from Page 328

| able          |               |    |
|:--------------|:--------------|:---|
| Schedule->tab | Scheduletable | O  |
| le            |               |    |

### Table from Page 328

| Return data correctly      | None         |
|:---------------------------|:-------------|
| [                          |              |
| {                          |              |
| "cmd" :"SetAudioAlarmV20", |              |
| "code" : 0,                |              |
| "value" : {                |              |
| "rspCode" :200             |              |
| }                          |              |
| }                          |              |
| ]                          |              |
| Fielddescription           |              |
| Field                      | description  |
| rspCode                    | Responsecode |

### Table from Page 328

| Data example   |
|:---------------|
| [              |

### Table from Page 329

| {                            | None        | None   |
| "cmd":"GetBuzzerAlarmV20",   |             |        |
| "action":1,                  |             |        |
| "param": {                   |             |        |
| "channel": 0                 |             |        |
| }                            |             |        |
| }                            |             |        |
| ]                            |             |        |
|:-----------------------------|:------------|:-------|
| Fielddescription             |             |        |
| Field                        | Description | M/O    |

### Table from Page 329

| Return data correctly                                               |
|:--------------------------------------------------------------------|
| [                                                                   |
| {                                                                   |
| "cmd" :"GetBuzzerAlarmV20",                                         |
| "code" : 0,                                                         |
| "initial" :{                                                        |
| "Buzzer" :{                                                         |
| "diskErrorAlert" :0,                                                |
| "diskFullAlert" :0,                                                 |
| "enable" : 0,                                                       |
| "ipConflictAlert": 0,                                               |
| "nvrDisconnectAlert" : 0,                                           |
| "schedule" : {                                                      |
| "channel" : 0,                                                      |
| "table" : {                                                         |
| "AI_PEOPLE" :                                                       |
| "000000000000000000000000000000000000000000000000000000000000000000 |
| 0000000000000000000000000000000000000000000000000000000000000000000 |
| 00000000000000000000000000000000000",                               |
| "AI_VEHICLE" :                                                      |
| "000000000000000000000000000000000000000000000000000000000000000000 |
| 0000000000000000000000000000000000000000000000000000000000000000000 |
| 00000000000000000000000000000000000",                               |
| "MD" :                                                              |
| "111111111111111111111111111111111111111111111111111111111111111111 |
| 1111111111111111111111111111111111111111111111111111111111111111111 |

### Table from Page 331

| }                                                                     | None             |
| }                                                                     |                  |
| },                                                                    |                  |
| "value" : {                                                           |                  |
| "Buzzer" :{                                                           |                  |
| "diskErrorAlert" :0,                                                  |                  |
| "diskFullAlert" :0,                                                   |                  |
| "enable" : 0,                                                         |                  |
| "ipConflictAlert": 0,                                                 |                  |
| "nvrDisconnectAlert" : 0,                                             |                  |
| "schedule" : {                                                        |                  |
| "channel" : 0,                                                        |                  |
| "table" : {                                                           |                  |
| "AI_PEOPLE" :                                                         |                  |
| "000000000000000000000000000000000000000000000000000000000000000000   |                  |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                  |
| 00000000000000000000000000000000000",                                 |                  |
| "AI_VEHICLE" :                                                        |                  |
| "000000000000000000000000000000000000000000000000000000000000000000   |                  |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                  |
| 00000000000000000000000000000000000",                                 |                  |
| "MD" :                                                                |                  |
| "011111111111111111111111111111111111111111111111111111111111111111   |                  |
| 1111111111111111111111111111111111111111111111111111111111111111111   |                  |
| 11111111111111111111111111111111100",                                 |                  |
| "VL" :                                                                |                  |
| "000000000000000000000000000000000000000000000000000000000000000000   |                  |
| 0000000000000000000000000000000000000000000000000000000000000000000   |                  |
| 00000000000000000000000000000000000"                                  |                  |
| }                                                                     |                  |
| }                                                                     |                  |
| }                                                                     |                  |
| }                                                                     |                  |
| }                                                                     |                  |
| ]                                                                     |                  |
|:----------------------------------------------------------------------|:-----------------|
| Fielddescription                                                      |                  |
| Field                                                                 | description      |
| diskErrorAlert                                                        | Disk error Alert |
| diskFullAlert                                                         | Disk full Alert  |
| enable                                                                | Buzzerswitch     |

### Table from Page 332

| ipconflictAlert    | Ipc conflict Alert   |
|:-------------------|:---------------------|
| channel            | Index ofchannel      |
| table              | Schedule table       |
| nvrDisconnectAlert | Nvr Disconnect Alert |

### Table from Page 332

| Data example                                                        |
|:--------------------------------------------------------------------|
| [{                                                                  |
| "cmd": "SetBuzzerAlarmV20",                                         |
| "param": {                                                          |
| "Buzzer": {                                                         |
| "enable": 0,                                                        |
| "schedule": {                                                       |
| "channel": 0,                                                       |
| "table": {                                                          |
| "MD":                                                               |
| "011111111111111111111111111111111111111111111111111111111111111111 |
| 1111111111111111111111111111111111111111111111111111111111111111111 |
| 11111111111111111111111111111111100",                               |
| "TIMING":                                                           |
| "000111111111111111111111111111111111111111111111111111111111111111 |
| 1111111111111111111111111111111111111111111111111111111111111111111 |
| 11111111111111111111111111111111111"                                |
| }                                                                   |
| }                                                                   |
| }                                                                   |
| }                                                                   |

### Table from Page 333

| }]               | None          | None   |
|:-----------------|:--------------|:-------|
| Fielddescription |               |        |
| Field            | Description   | M/O    |
| Schedule->en     | Buzzerswitch  | O      |
| able             |               |        |
| Schedule->tab    | Scheduletable | O      |
| le               |               |        |

### Table from Page 333

| Return data correctly       | None         |
|:----------------------------|:-------------|
| [                           |              |
| {                           |              |
| "cmd" :"SetBuzzerAlarmV20", |              |
| "code" : 0,                 |              |
| "value" : {                 |              |
| "rspCode" :200              |              |
| }                           |              |
| }                           |              |
| ]                           |              |
| Fielddescription            |              |
| Field                       | description  |
| rspCode                     | Responsecode |

### Table from Page 334

| Dataexample             | None                     | None   |
|:------------------------|:-------------------------|:-------|
| [{                      |                          |        |
| "cmd":"AudioAlarmPlay", |                          |        |
| "action":0,             |                          |        |
| "param":{               |                          |        |
| "alarm_mode":"times",   |                          |        |
| "manual_switch":0,      |                          |        |
| "times":2,              |                          |        |
| "channel":0             |                          |        |
| }                       |                          |        |
| }]                      |                          |        |
| Fielddescription        |                          |        |
| Field                   | Description              | M/O    |
| channel                 | Indexofchannel           | M      |
| manual_switch           | Switchofmanual           | O      |
| times                   | TimesofAudioalarm        | O      |
| alarm_mode              | Alarmmode:“times”/”manu” | O      |

### Table from Page 334

| Return datacorrectly    | None        |
|:------------------------|:------------|
| [                       |             |
| {                       |             |
| "cmd":"AudioAlarmPlay", |             |
| "code":0,               |             |
| "value":{               |             |
| "rspCode":200           |             |
| }                       |             |
| }                       |             |
| ]                       |             |
| Fielddescription        |             |
| Field                   | description |

### Table from Page 335

| Dataexample         | None        | None   |
|:--------------------|:------------|:-------|
| [                   |             |        |
| {                   |             |        |
| "cmd":"GetIrLights" |             |        |
| }                   |             |        |
| ]                   |             |        |
| Fielddescription    |             |        |
| Field               | Description | M/O    |

### Table from Page 335

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"GetIrLights",   |
| "code":0,              |
| "value":{              |
| "IrLights":{           |
| "state":0              |
| }                      |
| },                     |
| "initial":{            |

### Table from Page 336

| "IrLights":{     | None              |
| "state":0        |                   |
| }                |                   |
| },               |                   |
| "range":{        |                   |
| "IrLights":{     |                   |
| "state":{        |                   |
| "Auto"           |                   |
| "Off"            |                   |
| "On"             |                   |
| }                |                   |
| }                |                   |
| }                |                   |
| }                |                   |
| ]                |                   |
|:-----------------|:------------------|
| Fielddescription |                   |
| Field            | description       |
| state            | Thestateofirlight |

### Table from Page 336

| Dataexample          |
|:---------------------|
| [{                   |
| "cmd":"SetIrLights", |
| "action":0,          |
| "param":{            |
| "IrLights":{         |
| "channel":0,         |
| "state":"Auto"       |
| }                    |

### Table from Page 337

| }                | None           | None   |
| }]               |                |        |
|:-----------------|:---------------|:-------|
| Fielddescription |                |        |
| Field            | Description    | M/O    |
| channel          | Indexofchannel | M      |

### Table from Page 337

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetIrLights",   |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 338

| Dataexample         | None        | None   |
|:--------------------|:------------|:-------|
| [                   |             |        |
| {                   |             |        |
| "cmd":"GetPowerLed" |             |        |
| }                   |             |        |
| ]                   |             |        |
| Fielddescription    |             |        |
| Field               | Description | M/O    |

### Table from Page 338

| Return datacorrectly   | None            |
|:-----------------------|:----------------|
| [                      |                 |
| {                      |                 |
| "cmd":"GetPowerLed",   |                 |
| "code":0,              |                 |
| "value":{              |                 |
| "PowerLed":{           |                 |
| "channel":0,           |                 |
| "state":0              |                 |
| }                      |                 |
| },                     |                 |
| "range":{              |                 |
| "PowerLed":{           |                 |
| "state":{              |                 |
| "On"                   |                 |
| "Off"                  |                 |
| }                      |                 |
| }                      |                 |
| }                      |                 |
| }                      |                 |
| ]                      |                 |
| Fielddescription       |                 |
| Field                  | description     |
| state                  | Stateofpowerled |

### Table from Page 339

| Dataexample                     | None            | None   |
|:--------------------------------|:----------------|:-------|
| [                               |                 |        |
| {                               |                 |        |
| "cmd":"SetPowerLed",            |                 |        |
| "param":{                       |                 |        |
| "PowerLed":{                    |                 |        |
| "state":"Off",                  |                 |        |
| "channel":0                     |                 |        |
| }                               |                 |        |
| }                               |                 |        |
| }                               |                 |        |
| ]                               |                 |        |
| Fielddescription                |                 |        |
| Field                           | Description     | M/O    |
| state                           | Stateofpowerled |        |
| Note:Onlyfordeviceswithpowerled |                 |        |

### Table from Page 339

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetPowerLed",   |
| "code":0,              |
| "value":{              |
| "rspCode":200          |
| }                      |

### Table from Page 340

| }                | None         |
| ]                |              |
|:-----------------|:-------------|
| Fielddescription |              |
| Field            | description  |
| rspCode          | Responsecode |

### Table from Page 340

| Dataexample          | None           | None   |
|:---------------------|:---------------|:-------|
| [{                   |                |        |
| "cmd":"GetWhiteLed", |                |        |
| "action":0,          |                |        |
| "param":{            |                |        |
| "channel":0          |                |        |
| }                    |                |        |
| }]                   |                |        |
| Fielddescription     |                |        |
| Field                | Description    | M/O    |
| channel              | Indexofchannel | M      |

### Table from Page 340

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |

### Table from Page 342

| }                | None              |
| }                |                   |
| }                |                   |
| ]                |                   |
|:-----------------|:------------------|
| Fielddescription |                   |
| Field            | description       |
| channel          | Channelnumber     |
| state            | Whiteledstate     |
| auto             | Whiteledautomode  |
| bright           | Currentbrightness |
| mode             | Brightnessstate   |

### Table from Page 342

| Dataexample          |
|:---------------------|
| [{                   |
| "cmd":"SetWhiteLed", |
| "param":{            |
| "WhiteLed":{         |
| "state":0,           |
| "channel":0,         |
| "mode":1,            |
| "bright":79,         |

### Table from Page 343

| "LightingSchedule":{   | None                        | None   |
| "EndHour":6,           |                             |        |
| "EndMin":0,            |                             |        |
| "StartHour":18,        |                             |        |
| "StartMin":0           |                             |        |
| },                     |                             |        |
| "wlAiDetectType":{     |                             |        |
| "dog_cat":1,           |                             |        |
| "face":0,              |                             |        |
| "people":1,            |                             |        |
| "vehicle":0            |                             |        |
| }                      |                             |        |
| }                      |                             |        |
| }                      |                             |        |
| }]                     |                             |        |
|:-----------------------|:----------------------------|:-------|
| Fielddescription       |                             |        |
| Field                  | Description                 | M/O    |
| channel                | Indexofchannel              | M      |
| state                  | Whiteledstate0/1            | O      |
|                        | 0:Off                       |        |
|                        | 1:On                        |        |
| mode                   | Brightnessstate0/1/2        | O      |
|                        | 0:it`salwayslightatnight    |        |
|                        | 1:alarmtriggermode          |        |
|                        | 2:lightonforspecificperiods |        |
| bright                 | Currentbrightness1-100      | O      |
| wlAiDetectTyp          | Theaidetecttypeofwhiteled   | O      |
| e                      |                             |        |

### Table from Page 343

| Return datacorrectly   |
|:-----------------------|
| [                      |
| {                      |
| "cmd":"SetWhiteLed",   |
| "code":0,              |
| "value":{              |

### Table from Page 344

| "rspCode":200    | None        |
| }                |             |
| }                |             |
| ]                |             |
|:-----------------|:------------|
| Fielddescription |             |
| Field            | description |

### Table from Page 344

| Dataexample         | None           | None   |
|:--------------------|:---------------|:-------|
| [{                  |                |        |
| "cmd":"GetAiAlarm", |                |        |
| "action":0,         |                |        |
| "param":{           |                |        |
| "channel":0,        |                |        |
| "ai_type":"people"  |                |        |
| }                   |                |        |
| }]                  |                |        |
| Fielddescription    |                |        |
| Field               | Description    | M/O    |
| channel             | Indexofchannel | M      |
| ai_type             | Aitype         | O      |

### Table from Page 345

| Return datacorrectly                                               |
|:-------------------------------------------------------------------|
| [                                                                  |
| {                                                                  |
| "cmd":"GetAiAlarm",                                                |
| "code":0,                                                          |
| "value":{                                                          |
| "ai_detect_type":"people",                                         |
| "height":60,                                                       |
| "max_target_height":0.0,                                           |
| "max_target_width":0.0,                                            |
| "min_target_height":0.0,                                           |
| "min_target_width":0.0,                                            |
| "scope":{                                                          |
| "area":                                                            |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |

### Table from Page 347

| "sensitivity":10,   | None        |
| "stay_time":0,      |             |
| "width":80          |             |
| }                   |             |
| }                   |             |
| ]                   |             |
|:--------------------|:------------|
| Fielddescription    |             |
| Field               | description |

### Table from Page 347

| Dataexample                                                        |
|:-------------------------------------------------------------------|
| [{                                                                 |
| "cmd":"SetAiAlarm",                                                |
| "param":{                                                          |
| "channel":0,                                                       |
| "AiAlarm":{                                                        |
| "ai_type":"people",                                                |
| "sensitivity":10,                                                  |
| "stay_time":0,                                                     |
| "width":80,                                                        |
| "height":60,                                                       |
| "scope":{                                                          |
| "area":                                                            |
| "11111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |
| 111111111111111111111111111111111111111111111111111111111111111111 |

### Table from Page 349

| 111111111111111111111111111111111111111111111111111111111111111111   | None                 | None   |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                      |        |
| 1111111111111111111111111111111111111111111111111"                   |                      |        |
| },                                                                   |                      |        |
| "min_target_height":0.0,                                             |                      |        |
| "max_target_height":1.0,                                             |                      |        |
| "min_target_width":0.0,                                              |                      |        |
| "max_target_width":1.0                                               |                      |        |
| }                                                                    |                      |        |
| }                                                                    |                      |        |
| }]                                                                   |                      |        |
|:---------------------------------------------------------------------|:---------------------|:-------|
| Fielddescription                                                     |                      |        |
| Field                                                                | Description          | M/O    |
| channel                                                              | Indexofchannel       | M      |
| ai_type                                                              | Aitype               | O      |
| sensitivity                                                          | Sensitivityofaialarm | O      |

### Table from Page 350

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetAiAlarm",    |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 350

| Dataexample           |
|:----------------------|
| [{                    |
| "cmd":"SetAlarmArea", |
| "param":{             |
| "channel":0,          |
| "ai_type":"people",   |

### Table from Page 352

| 111111111111111111111111111111111111111111111111111111111111111111   | None             | None   |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 111111111111111111111111111111111111111111111111111111111111111111   |                  |        |
| 1111111111111111111111111111111111111111111111111"                   |                  |        |
| }                                                                    |                  |        |
| }]                                                                   |                  |        |
|:---------------------------------------------------------------------|:-----------------|:-------|
| Fielddescription                                                     |                  |        |
| Field                                                                | Description      | M/O    |
| channel                                                              | Indexofchannel   | M      |
| ai_type                                                              | Typeofaialarm    | O      |
| width                                                                | Widthofalarmarea | O      |

### Table from Page 353

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetAlarmArea",  |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 353

| Dataexample       |
|:------------------|
| [{                |
| "cmd":"GetAiCfg", |
| "action":0,       |
| "param":{         |

### Table from Page 354

| "channel":0      | None           | None   |
| }                |                |        |
| }]               |                |        |
|:-----------------|:---------------|:-------|
| Fielddescription |                |        |
| Field            | Description    | M/O    |
| channel          | Indexofchannel | M      |

### Table from Page 354

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"GetAiCfg",      |             |
| "code":0,              |             |
| "value":{              |             |
| "AiDetectType":{       |             |
| "dog_cat":1,           |             |
| "face":0,              |             |
| "people":1,            |             |
| "vehicle":1            |             |
| },                     |             |
| "aiTrack":0,           |             |
| "channel":0,           |             |
| "trackType":{          |             |
| "dog_cat":0,           |             |
| "face":0,              |             |
| "people":1,            |             |
| "vehicle":0            |             |
| }                      |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 355

| Dataexample       | None               | None   |
|:------------------|:-------------------|:-------|
| [{                |                    |        |
| "cmd":"SetAiCfg", |                    |        |
| "action":0,       |                    |        |
| "param":{         |                    |        |
| "aiTrack":0,      |                    |        |
| "trackType":{},   |                    |        |
| "AiDetectType":{  |                    |        |
| "people":1,       |                    |        |
| "vehicle":1,      |                    |        |
| "dog_cat":1,      |                    |        |
| "face":0          |                    |        |
| },                |                    |        |
| "channel":0       |                    |        |
| }                 |                    |        |
| }]                |                    |        |
| Fielddescription  |                    |        |
| Field             | Description        | M/O    |
| channel           | Indexofchannel     | M      |
| aiTrack           | SwitchtoaiTrack    | O      |
| trackType         | Aitracktype        | O      |
| AiDetectType      | Aidetecttype       | O      |
| people            | Peopledetection    | O      |
| vehicle           | Vehicledetection   | O      |
| Dog_cat           | Dogandcatdetection | O      |

### Table from Page 356

| face   | Facedetection   | O   |
|:-------|:----------------|:----|
|        |                 |     |

### Table from Page 356

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"SetAiCfg",      |             |
| "code":0,              |             |
| "value":{              |             |
| "rspCode":200          |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 356

| Dataexample         |
|:--------------------|
| [                   |
| {                   |
| "cmd":"GetAiState", |
| "param":{           |

### Table from Page 357

| "channel":0      | None           | None   |
| }                |                |        |
| }                |                |        |
| ]                |                |        |
|:-----------------|:---------------|:-------|
| Fielddescription |                |        |
| Field            | Description    | M/O    |
| channel          | Indexofchannel | M      |

### Table from Page 357

| Return datacorrectly   | None        |
|:-----------------------|:------------|
| [                      |             |
| {                      |             |
| "cmd":"GetAiState",    |             |
| "code":0,              |             |
| "value":{              |             |
| "channel":0,           |             |
| "dog_cat":{            |             |
| "alarm_state":0,       |             |
| "support":1            |             |
| },                     |             |
| "face":{               |             |
| "alarm_state":0,       |             |
| "support":0            |             |
| },                     |             |
| "people":{             |             |
| "alarm_state":0,       |             |
| "support":1            |             |
| },                     |             |
| "vehicle":{            |             |
| "alarm_state":0,       |             |
| "support":1            |             |
| }                      |             |
| }                      |             |
| }                      |             |
| ]                      |             |
| Fielddescription       |             |
| Field                  | description |

### Table from Page 358

| alarm_state   | Alarmstate          |
|:--------------|:--------------------|
| support       | Whethersupportornot |

### Table from Page 358

| Error Response   | None             | None                      |
|:-----------------|:-----------------|:--------------------------|
| [                |                  |                           |
| {                |                  |                           |
| "cmd":string,    |                  |                           |
| "code":0,        |                  |                           |
| "error":{        |                  |                           |
| "rspCode":int,   |                  |                           |
| "detail":string  |                  |                           |
| }                |                  |                           |
| }                |                  |                           |
| ]                |                  |                           |
| rspCode          | Details          | Description               |
| -1               | notexist         | Missingparameters         |
| -2               | outofmem         | Usedupmemory              |
| -3               | checkerr         | Checkerror                |
| -4               | paramerror       | Parameterserror           |
| -5               | maxsession       | Reached the max session   |
|                  |                  | number.                   |
| -6               | pleaseloginfirst | Loginrequired             |
| -7               | loginfailed      | Loginerror                |
| -8               | timeout          | Operationtimeout          |
| -9               | notsupport       | Notsupported              |
| -10              | protocol         | Protocolerror             |
| -11              | fcgireadfailed   | Failedtoreadoperation     |
| -12              | getconfigfailed  | Failedtogetconfiguration. |

### Table from Page 359

|   -13 | setconfigfailed                      | Failedtosetconfiguration.   |
|------:|:-------------------------------------|:----------------------------|
|   -14 | mallocfailed                         | Failedtoapplyformemory      |
|   -15 | createsocketfailed                   | Failedtocreatedsocket       |
|   -16 | sendfailed                           | Failedtosenddata            |
|   -17 | rcvfailed                            | Failedtoreceiverdata        |
|   -18 | openfilefailed                       | Failedtoopenfile            |
|   -19 | readfilefailed                       | Failedtoreadfile            |
|   -20 | writefilefailed                      | Failedtowritefile           |
|   -21 | errortoken                           | Tokenerror                  |
|   -22 | The length of the string exceeds the | The length of the string    |
|       | limit                                | exceedsthelimitmation       |
|   -23 | missingparam                         | Missingparameters           |
|   -24 | errorcommand                         | Commanderror                |
|   -25 | internalerror                        | Internalerror               |
|   -26 | abilityerror                         | Abilityerror                |
|   -27 | invaliduser                          | Invaliduser                 |
|   -28 | useralreadyexist                     | Useralreadyexist            |
|   -29 | maximumnumberofusers                 | Reached the maximum         |
|       |                                      | numberofusers               |
|   -30 | sameversion                          | Theversionisidenticaltothe  |
|       |                                      | currentone.                 |
|   -31 | busy                                 | Ensure only one user can    |
|       |                                      | upgrade                     |
|   -32 | ipconflict                           | Modify IP conflicted with   |
|       |                                      | usedIP                      |
|   -34 | needbingemail                        | Cloud login need bind email |
|       |                                      | first                       |
|   -35 | unbind                               | Cloudloginunbindcamera      |
|   -36 | networktimeout                       | Cloud login get login       |
|       |                                      | informationoutoftime        |

### Table from Page 360

|   -37 | passworderr                       | Cloudloginpassworderror    |
|------:|:----------------------------------|:---------------------------|
|   -38 | uiderr                            | Cloudbindcamerauiderror    |
|   -39 | usernotexist                      | Cloudloginuserdoesn’texist |
|   -40 | unbindfailed                      | Cloudunbindcamerafailed    |
|   -41 | cloudnotsupport                   | The device doesn’t support |
|       |                                   | cloud                      |
|   -42 | logincloudserverfailed            | Cloudloginserverfailed     |
|   -43 | bindfailed                        | Cloudbindcamerafailed      |
|   -44 | cloudunknownerr                   | Cloudunknownerror          |
|   -45 | needverifycode                    | Cloudbindcameraneed        |
|       |                                   | verifycode                 |
|   -46 | Digestauthenticationfailed        | Anerroroccurredwhile       |
|       |                                   | usingthedigest             |
|       |                                   | authenticationprocess      |
|   -47 | DigestauthenticationNonceexpires  | AbstractAnexpirednonceis   |
|       |                                   | usedintheauthentication    |
|       |                                   | process                    |
|   -48 | Fetchingapicturefailed            | Snapapicturefailed         |
|   -49 | Channelinvalid                    | Channelisinvalid           |
|   -99 | Deviceoffline                     | Deviceoffline              |
|  -100 | testfailed                        | TestEmail、Ftp、Wififailed   |
|  -101 | checkfirmwarefailed               | Upgrade checking firmware  |
|       |                                   | failed                     |
|  -102 | downloadonlinefailed              | Upgrade download online    |
|       |                                   | failed                     |
|  -103 | getupgradestatusfailed            | Upgrade get upgrade status |
|       |                                   | failed                     |
|  -105 | Frequent logins, please try again | Frequentlogins             |
|       | later!                            |                            |
|  -220 | Errordownloadingvideofile         | Errordownloadingvideofile  |
|  -221 | Busyvideorecordingtask            | Busyvideorecordingtask     |
|  -222 | Thevideofiledoesnotexist          | Thevideofiledoesnotexist   |

### Table from Page 361

| -301                                                  | DigestAuthenticationnonceerror     | None         | None   | Digest Authentication nonce   |
|                                                       |                                    |              |        | error                         |
|:------------------------------------------------------|:-----------------------------------|:-------------|:-------|:------------------------------|
| -310                                                  | Aesdecryptionfailure               |              |        | Aesdecryptionfailure          |
| -451                                                  | ftploginfailed                     |              |        | ftptestloginfailed            |
| -452                                                  | ftpcreatedirfailed                 |              |        | Creatftpdirfailed             |
| -453                                                  | ftpuploadfailed                    |              |        | Uploadftpfilefailed           |
| -454                                                  | ftpconnectfailed                   |              |        | Cannotconnectftpserver        |
| -480                                                  | emailundefinedfailed               |              |        | Someundifinederrors           |
| -481                                                  | emailconnectfailed                 |              |        | Cannotconnectemailserver      |
| -482                                                  | emailauthfailed                    |              |        | Authuserfailed                |
| -483                                                  | emailnetworkerr                    |              |        | Emailnetworkerr               |
| -484                                                  | emailservererr                     |              |        | Something wrong with email    |
|                                                       |                                    |              |        | server                        |
| -485                                                  | emailmemoryerr                     |              |        | Somethingwrongwith            |
|                                                       |                                    |              |        | memory                        |
| -500                                                  | The number of IP addresses reaches |              |        | ThenumberofIPaddresses        |
|                                                       | theupperlimit                      |              |        | reachestheupperlimit          |
| -501                                                  | Theuserdoesnotexist                |              |        | Theuserdoesnotexist           |
| -502                                                  |                                    | Password err |        | Passworderr                   |
| -503                                                  | Logindeny                          |              |        | Logindeny                     |
| -505                                                  | Loginnotinit                       |              |        | Loginnotinit                  |
| -506                                                  | Loginlocked                        |              |        | Loginlocked                   |
| -507                                                  | Loginreachmax                      |              |        | Thenumberoflogins             |
|                                                       |                                    |              |        | reachedtheupperlimit          |
| Note:Field"details"meansmoredetailederrorinformation. |                                    |              |        |                               |

