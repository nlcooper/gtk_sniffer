mkdir /opt/gtk_sniffer/
cp sniffer.py /opt/gtk_sniffer/
cp sniff.sh /opt/gtk_sniffer/
ln -s /opt/gtk_sniffer/sniffer.py /usr/sbin/sniff
apt install gksu
