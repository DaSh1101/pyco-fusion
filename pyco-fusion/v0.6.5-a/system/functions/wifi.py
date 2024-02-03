import network
import machine
import time
import rp2
import ujson
from system.functions import oled_i2c
wlan = network.WLAN(network.STA_IF)
led = machine.Pin("LED", machine.Pin.OUT)
# Function to load saved networks from file
def load_saved_networks():
    try:
        with open('/system/misc/saved_networks', 'r') as f:
            saved_networks = ujson.load(f)
        return saved_networks
    except (OSError, ValueError):
        return []

# Function to save networks to file
def save_network(network_name, password):
    saved_networks = load_saved_networks()

    # Check if the SSID already exists
    for entry in saved_networks:
        if entry['SSID'] == network_name:
            entry['PASSWORD'] = password
            break
    else:
        # If the SSID doesn't exist, append a new entry
        saved_networks.append({'SSID': network_name, 'PASSWORD': password})

    with open('/system/misc/saved_networks', 'w') as f:
        ujson.dump(saved_networks, f)

# Function to find the saved network with the strongest signal
def find_strongest_saved_network(nearby_networks, saved_networks):
    strongest_saved_network = None
    strongest_signal_strength = -100  # Initialize with a very weak signal strength

    for saved_network in saved_networks:
        for nearby_network in nearby_networks:
            if saved_network['SSID'] == nearby_network[0].decode():
                signal_strength = nearby_network[3]
                if signal_strength > strongest_signal_strength:
                    strongest_saved_network = saved_network
                    strongest_signal_strength = signal_strength

    return strongest_saved_network

def wlanConnectToSavedNetworks():
    try:
        wlan.active(True)
        nearby_networks = wlan.scan()
        nearby_networks.sort(key=lambda x: x[3], reverse=True)

        saved_networks = load_saved_networks()

        strongest_saved_network = find_strongest_saved_network(nearby_networks, saved_networks)

        if strongest_saved_network:
            wlan.connect(strongest_saved_network['SSID'], strongest_saved_network['PASSWORD'])
            timeoutbase = 0
            timeout = 75
            while not wlan.isconnected():
                timeoutbase += 1
                led.toggle()
                time.sleep(.2)
                if timeout < timeoutbase:
                    print('Timed Out, to change this variable, modify the "timeout" int')
                    break

            wlan_status = wlan.status()
            if wlan_status != 3:
                raise RuntimeError('Wi-Fi connection failed')
                led.off()
            else:
                print(f"Connected to {strongest_saved_network['SSID']}")
                oled_i2c.println("Connected:")
                oled_i2c.println(f"{strongest_saved_network['SSID']}")
                status = wlan.ifconfig()
                print('Local ip:', status[0])
                led.on()
    except Exception as e:
        print('Unable to connect to network...')
        oled_i2c.println('Error connecting')        
def wlanDisconnect():
    led = machine.Pin("LED", machine.Pin.OUT)
    if wlan.isconnected():
        wlan.disconnect()
        print('All connections terminated')
        oled_i2c.println('disconnected')
        led.off()
    else:
        print('no connections to be terminated')
        oled_i2c.println('disconnected')
        
def wlanConnect():
    print('Beginning WiFi Connection Setup...')
    oled_i2c.println('WiFi Setup began')
    led = machine.Pin("LED", machine.Pin.OUT)
    rp2.country('US')
    wlan.active(True)
    print('')
    oled_i2c.println("SSID:")
    ssid = input("SSID: \n")
    oled_i2c.println("PASSWORD:")
    pw = input("PASSWORD: \n")

    # Save the entered network to the saved networks list
    save_network(ssid, pw)

    wlan.connect(ssid, pw)
    timeoutbase = 0
    timeout = 75
    print('Attempting to connect...')
    oled_i2c.println("Connecting...")
    while not wlan.isconnected():
        led.toggle()
        timeoutbase = timeoutbase + 1
        time.sleep(.2)
        if timeout < timeoutbase:
            print('Timed Out, to change this variable, modify the "timeout" int')
            oled_i2c.println("Timed Out...")
            break

    def blink_onboard_led(num_blinks):
        led = machine.Pin('LED', machine.Pin.OUT)
        for i in range(num_blinks):
            led.on()
            time.sleep(.2)
            led.off()
            time.sleep(.2)

    wlan_status = wlan.status()
    blink_onboard_led(wlan_status)

    if wlan_status != 3:
        raise RuntimeError('Wi-Fi connection failed')
    else:
        print('Connected')
        oled_i2c.println("Connected:")
        status = wlan.ifconfig()
        led.on()
        print('Local ip: ' + status[0])
        oled_i2c.println(status[0])

def wlanScan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    networks.sort(key=lambda x: x[3], reverse=True)
    print("{} networks found:\n".format(len(networks)))
    oled_i2c.println("{} Found networks!\n".format(len(networks)))
    
    print("{:<32} {:<6}".format("SSID", "RSSI"))
    oled_i2c.println("{:<32}".format("SSID"))
    for net in networks:
        print("{:<32} {:<6}".format(net[0].decode(), net[3]))
        oled_i2c.println("{:<32} {:<6}".format(net[0].decode(), net[3]))

def check_wifi_connection():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()

def wlanActive():
    if wlan.active() and wlan.isconnected():
        ssid = wlan.config("essid")
        print("The currently connected network is:", ssid)
        oled_i2c.println(ssid)
    else:
        print("The WLAN interface is not active or connected.")
        oled_i2c.println("Not connected")