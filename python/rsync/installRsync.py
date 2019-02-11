#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys,stat,shutil

pass_file = "/etc/rsync.pass"
rsync_config_file = "/etc/rsyncd.conf"
rc_local_file = "/etc/rc.local"

def installServer():
    """
    ��װ����Ŀ�����(���ļ�ͬ�����Ļ���)
    ���Ŷ˿�(Ĭ��873),����rsync,��������,���뿪������
    """
    print("���Ŷ˿�873")
    os.system("firewall-cmd --zone=internal --add-port=873/tcp --permanent")
    os.system("firewall-cmd --reload")
    print("��װrsync")
    if os.access("/usr/bin/rsync",os.F_OK):
        print("�Ѵ���rsync")
    else:
        os.system("yum install rsync")
    config_text = "\nlog file =/var/log/rsyncd.log\n" \
                  "pid file =/var/run/rsyncd.pid\n" \
                  "lock file =/var/run/rsync.lock\n" \
                  "ignore errors\n" \
                  "uid=root\n" \
                  "gid=root\n" \
                  "read only=no\n" \
                  "list=no\n" \
                  "timeout=600\n" \
                  "[�Զ�������]\n" \
                  "path=/ͬ��Ŀ���ļ���·��\n"
    print("д�������ļ�/etc/rsyncd.conf")
    with open(rsync_config_file, "a") as file:
        file.write(config_text)
    print("д�������ļ�/etc/rsync.pass")
    with open(pass_file, "w+") as passfile:
        passfile.write("user:passwd")
    os.chmod(pass_file,stat.S_IRWXU)
    run_daemon_cmd = "rsync --daemon --config=/etc/rsyncd.conf"
    print("���뿪������")
    with open(rc_local_file, "a") as rcfile:
        rcfile.write(run_daemon_cmd)
    print("��װ�ɹ�,��̨ģʽ����")
    os.system(run_daemon_cmd)
    return


def installClient():
    print("��װrsync client")
    os.system("yum install rsync")
    print("д�������ļ�/etc/rsync.pass")
    with open(pass_file, "w+") as passfile:
        passfile.write("passwd")
    os.system("rsync --daemon")
    print("��װsersync")
    sersync_path="/usr/local/sersync"
    shutil.copytree("sersync",sersync_path)
    os.chmod(sersync_path+"/sersync2",stat.S_IEXEC)
    print("��װ���")
    print("���뿪������")
    run_daemon_cmd=sersync_path+"/sersync2 -r -d -o /usr/local/sersync/confxml.xml"
    with open(rc_local_file, "a") as rcfile:
        rcfile.write(run_daemon_cmd)
    print("��ʼ����")
    os.system(run_daemon_cmd)
    return


if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("��������� 0= install server ,1=install client")
        sys.exit()
    else:
        if "0" in sys.argv:
            installServer()
        elif "1" in sys.argv:
            installClient()
        else:
            print("��Ч�Ĳ���")