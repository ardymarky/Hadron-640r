pool us.pool.ntp.org iburst

driftfile /var/lib/ntp/ntp.drift
logfile /var/log/ntp.log

restrict default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery
restrict 127.0.0.1 mask 255.255.255.0
restrict -6 ::1

# GPS Serial data reference (NTP0)
server 127.127.28.0
fudge 127.127.28.0 refid GPS

# GPS PPS reference (NTP1)
server 127.127.28.1 prefer
fudge 127.127.28.1 refid PPS

