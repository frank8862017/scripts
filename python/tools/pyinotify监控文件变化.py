官方参考：

https://github.com/seb-m/pyinotify/wiki/Events-types

https://github.com/seb-m/pyinotify/wiki/Install

 

最近在网上看到python有个pyinotify模块，其中他们可以监控文件夹内的文件的创建，修改，读取，删除等系列操作，我修改了下，添加了可以吧操作记录写到日志里的一点方法，下面就贴出代码了给大家分享下：#!/usr/bin/env python

01
02
03
04
05
06
07
08
09
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
import os
import datetime
import pyinotify
import logging
class MyEventHandler(pyinotify.ProcessEvent):
    logging.basicConfig(level=logging.INFO,filename='/var/log/monitor.log')
    #自定义写入那个文件，可以自己修改
    logging.info("Starting monitor...")
     
    def process_IN_ACCESS(self, event):
        print "ACCESS event:", event.pathname
    logging.info("ACCESS event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
    def process_IN_ATTRIB(self, event):
        print "ATTRIB event:", event.pathname
    logging.info("IN_ATTRIB event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
   def process_IN_CLOSE_NOWRITE(self, event):
        print "CLOSE_NOWRITE event:", event.pathname
        logging.info("CLOSE_NOWRITE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
   def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname
    logging.info("CLOSE_WRITE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
   def process_IN_CREATE(self, event):
        print "CREATE event:", event.pathname
    logging.info("CREATE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
   def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname
    logging.info("DELETE event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
   def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname
    logging.info("MODIFY event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
   def process_IN_OPEN(self, event):
        print "OPEN event:", event.pathname
    logging.info("OPEN event : %s  %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
     
     
def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('/tmp', pyinotify.ALL_EVENTS, rec=True)
    #/tmp是可以自己修改的监控的目录
    # event handler
    eh = MyEventHandler()
 
    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()
 
if __name__ == '__main__':
    main()
    
下面来看看效果如何呢：我在代码定义的是监控tmp目录下的变化：

01
02
03
04
05
06
07
08
09
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
[root@centos6 monitor-folder]# python total-monitor.py
OPEN event: /tmp/.ICE-unix
CLOSE_NOWRITE event: /tmp/.ICE-unix
OPEN event: /tmp
CLOSE_NOWRITE event: /tmp
OPEN event: /tmp
CLOSE_NOWRITE event: /tmp
DELETE event: /tmp/aa
DELETE event: /tmp/adduser.conf
DELETE event: /tmp/adjtime
DELETE event: /tmp/aliases
DELETE event: /tmp/bash.bashrc
DELETE event: /tmp/bindresvport.blacklist
DELETE event: /tmp/environment
DELETE event: /tmp/fstab
DELETE event: /tmp/ipt.err
DELETE event: /tmp/ipt.out
DELETE event: /tmp/krb5.conf
DELETE event: /tmp/odbc.ini
DELETE event: /tmp/odbcinst.ini
DELETE event: /tmp/timezone
DELETE event: /tmp/ucf.conf
DELETE event: /tmp/warnquota.conf
DELETE event: /tmp/wgetrc
DELETE event: /tmp/xinetd.conf
CREATE event: /tmp/aa
OPEN event: /tmp/aa
ATTRIB event: /tmp/aa
CLOSE_WRITE event: /tmp/aa
CREATE event: /tmp/bb
OPEN event: /tmp/bb
ATTRIB event: /tmp/bb
CLOSE_WRITE event: /tmp/bb
CREATE event: /tmp/cc
OPEN event: /tmp/cc
ATTRIB event: /tmp/cc
CLOSE_WRITE event: /tmp/cc
 
上面是打印出来的监控状态，下面是我的操作代码：
 
[root@centos6 tmp]# ls
aa            bash.bashrc             ipt.err    odbcinst.ini    wgetrc
adduser.conf  bindresvport.blacklist  ipt.out    timezone        xinetd.conf
adjtime       environment             krb5.conf  ucf.conf
aliases       fstab                   odbc.ini   warnquota.conf
[root@centos6 tmp]# rm -rf *
[root@centos6 tmp]# touch aa
[root@centos6 tmp]# touch bb
[root@centos6 tmp]# touch cc
[root@centos6 tmp]#
 上面是直接打印出来的，下面在看看我吧操作记录在日志文件里面，也可以看下日志文件的记录：

01
02
03
04
05
06
07
08
09
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
INFO:root:Starting monitor...
INFO:root:OPEN event : /tmp/.ICE-unix  2011-10-27 13:31:57.219168
INFO:root:CLOSE_NOWRITE event : /tmp/.ICE-unix  2011-10-27 13:31:57.219609
INFO:root:OPEN event : /tmp/  2011-10-27 13:32:21.395228
INFO:root:CLOSE_NOWRITE event : /tmp/  2011-10-27 13:32:21.398105
INFO:root:OPEN event : /tmp/  2011-10-27 13:32:25.108997
INFO:root:CLOSE_NOWRITE event : /tmp/  2011-10-27 13:32:25.110239
INFO:root:CREATE event : /tmp/aa  2011-10-27 13:32:28.004863
INFO:root:OPEN event : /tmp/aa  2011-10-27 13:32:28.005860
INFO:root:IN_ATTRIB event : /tmp/aa  2011-10-27 13:32:28.006723
INFO:root:CLOSE_WRITE event : /tmp/aa  2011-10-27 13:32:28.014617
INFO:root:CREATE event : /tmp/bb  2011-10-27 13:32:30.149758
INFO:root:OPEN event : /tmp/bb  2011-10-27 13:32:30.164415
INFO:root:IN_ATTRIB event : /tmp/bb  2011-10-27 13:32:30.164877
INFO:root:CLOSE_WRITE event : /tmp/bb  2011-10-27 13:32:30.165303
INFO:root:CREATE event : /tmp/cc  2011-10-27 13:32:32.725418
INFO:root:OPEN event : /tmp/cc  2011-10-27 13:32:32.726367
INFO:root:IN_ATTRIB event : /tmp/cc  2011-10-27 13:32:32.727229
INFO:root:CLOSE_WRITE event : /tmp/cc  2011-10-27 13:32:32.735052
INFO:root:CREATE event : /tmp/dd  2011-10-27 13:32:39.771041
INFO:root:OPEN event : /tmp/dd  2011-10-27 13:32:39.780881
INFO:root:IN_ATTRIB event : /tmp/dd  2011-10-27 13:32:39.781455
INFO:root:CLOSE_WRITE event : /tmp/dd  2011-10-27 13:32:39.781893
INFO:root:Starting monitor...
INFO:root:OPEN event : /tmp/.ICE-unix  2011-10-27 14:01:43.742477
INFO:root:CLOSE_NOWRITE event : /tmp/.ICE-unix  2011-10-27 14:01:43.742915
INFO:root:OPEN event : /tmp/  2011-10-27 14:01:50.579778
INFO:root:CLOSE_NOWRITE event : /tmp/  2011-10-27 14:01:50.581317
INFO:root:DELETE event : /tmp/aa  2011-10-27 14:01:54.999528
INFO:root:DELETE event : /tmp/bb  2011-10-27 14:01:58.995966
INFO:root:DELETE event : /tmp/cc  2011-10-27 14:02:02.795950
INFO:root:DELETE event : /tmp/dd  2011-10-27 14:02:06.284208
INFO:root:OPEN event : /tmp/  2011-10-27 14:02:07.738560
INFO:root:CLOSE_NOWRITE event : /tmp/  2011-10-27 14:02:07.741922
INFO:root:CREATE event : /tmp/aa  2011-10-27 14:02:11.110322
INFO:root:OPEN event : /tmp/aa  2011-10-27 14:02:11.113150
INFO:root:IN_ATTRIB event : /tmp/aa  2011-10-27 14:02:11.116381
INFO:root:CLOSE_WRITE event : /tmp/aa  2011-10-27 14:02:11.118382
INFO:root:Starting monitor...
INFO:root:OPEN event : /tmp/.ICE-unix  2011-10-27 21:39:12.520432
INFO:root:CLOSE_NOWRITE event : /tmp/.ICE-unix  2011-10-27 21:39:12.520879
INFO:root:OPEN event : /tmp/  2011-10-27 21:39:23.784759
INFO:root:CLOSE_NOWRITE event : /tmp/  2011-10-27 21:39:23.793211
INFO:root:OPEN event : /tmp/  2011-10-27 21:39:33.916232
INFO:root:CLOSE_NOWRITE event : /tmp/  2011-10-27 21:39:33.916823
INFO:root:DELETE event : /tmp/aa  2011-10-27 21:39:33.939008
INFO:root:DELETE event : /tmp/adduser.conf  2011-10-27 21:39:33.958143
INFO:root:DELETE event : /tmp/adjtime  2011-10-27 21:39:33.962497
INFO:root:DELETE event : /tmp/aliases  2011-10-27 21:39:33.978506
INFO:root:DELETE event : /tmp/bash.bashrc  2011-10-27 21:39:33.980834
INFO:root:DELETE event : /tmp/bindresvport.blacklist  2011-10-27 21:39:33.997176
INFO:root:DELETE event : /tmp/environment  2011-10-27 21:39:33.997683
INFO:root:DELETE event : /tmp/fstab  2011-10-27 21:39:33.998110
INFO:root:DELETE event : /tmp/ipt.err  2011-10-27 21:39:33.998532
INFO:root:DELETE event : /tmp/ipt.out  2011-10-27 21:39:34.000360
INFO:root:DELETE event : /tmp/krb5.conf  2011-10-27 21:39:34.000816
INFO:root:DELETE event : /tmp/odbc.ini  2011-10-27 21:39:34.002217
INFO:root:DELETE event : /tmp/odbcinst.ini  2011-10-27 21:39:34.002675
INFO:root:DELETE event : /tmp/timezone  2011-10-27 21:39:34.003110
INFO:root:DELETE event : /tmp/ucf.conf  2011-10-27 21:39:34.003538
INFO:root:DELETE event : /tmp/warnquota.conf  2011-10-27 21:39:34.018152
INFO:root:DELETE event : /tmp/wgetrc  2011-10-27 21:39:34.018641
INFO:root:DELETE event : /tmp/xinetd.conf  2011-10-27 21:39:34.041880
INFO:root:CREATE event : /tmp/aa  2011-10-27 21:39:40.639965
INFO:root:OPEN event : /tmp/aa  2011-10-27 21:39:40.640914
INFO:root:IN_ATTRIB event : /tmp/aa  2011-10-27 21:39:40.647835
INFO:root:CLOSE_WRITE event : /tmp/aa  2011-10-27 21:39:40.652158
INFO:root:CREATE event : /tmp/bb  2011-10-27 21:39:43.064526
INFO:root:OPEN event : /tmp/bb  2011-10-27 21:39:43.070849
INFO:root:IN_ATTRIB event : /tmp/bb  2011-10-27 21:39:43.071329
INFO:root:CLOSE_WRITE event : /tmp/bb  2011-10-27 21:39:43.071762
INFO:root:CREATE event : /tmp/cc  2011-10-27 21:39:47.046752
INFO:root:OPEN event : /tmp/cc  2011-10-27 21:39:47.051537
INFO:root:IN_ATTRIB event : /tmp/cc  2011-10-27 21:39:47.056211
INFO:root:CLOSE_WRITE event : /tmp/cc  2011-10-27 21:39:47.057490
[root@centos6 tmp]#<br><br><br><a href="http://www.pyshell.com/index.php/archives/477">http://www.pyshell.com/index.php/archives/477</a>