import threading
import time
from bluezero import adapter
from bluezero import peripheral

# HID Service UUIDs (16-bit)
HID_SERVICE = '1812'
PROTOCOL_MODE = '2A4E'
REPORT = '2A4D'
REPORT_MAP = '2A4B'
HID_INFO = '2A4A'
REPORT_REF_DSCP = '2908'

# Consumer Control Report Map
# Defines a 1-byte report where bit 0 is Volume Up (Usage 0xE9 in Consumer Page 0x0C)
CONSUMER_REPORT_MAP = [
    0x05, 0x0C,        # Usage Page (Consumer)
    0x09, 0x01,        # Usage (Consumer Control)
    0xA1, 0x01,        # Collection (Application)
    0x09, 0xE9,        #   Usage (Volume Increment)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x75, 0x01,        #   Report Size (1)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    0x75, 0x07,        #   Report Size (7)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x03,        #   Input (Const,Var,Abs)
    0xC0               # End Collection
]

HID_INFORMATION = [
    0x11, 0x01,  # bcdHID (1.11)
    0x00,        # bCountryCode (0x00)
    0x03         # Flags (0x01: RemoteWake, 0x02: NormallyConnectable)
]


class BLEKeyboard:
    def __init__(self):
        self.p = None
        self.report_chr = None
        self.thread = None

    def start(self):
        try:
            adapters = list(adapter.Adapter.available())
            if not adapters:
                print("No Bluetooth adapters found")
                return
            ad_addr = adapters[0].address

            # Appearance 961 = Keyboard
            self.p = peripheral.Peripheral(ad_addr, local_name='Lenochka Shutter', appearance=961)

            # Add HID Service
            self.p.add_service(srv_id=1, uuid=HID_SERVICE, primary=True)

            # Report Map
            self.p.add_characteristic(srv_id=1, chr_id=1, uuid=REPORT_MAP,
                                     value=CONSUMER_REPORT_MAP, notifying=False,
                                     flags=['read'])

            # HID Information
            self.p.add_characteristic(srv_id=1, chr_id=2, uuid=HID_INFO,
                                     value=HID_INFORMATION, notifying=False,
                                     flags=['read'])

            # Protocol Mode
            self.p.add_characteristic(srv_id=1, chr_id=3, uuid=PROTOCOL_MODE,
                                     value=[0x01], notifying=False,
                                     flags=['read', 'write-without-response'])

            # Report
            self.p.add_characteristic(srv_id=1, chr_id=4, uuid=REPORT,
                                     value=[0x00], notifying=True,
                                     flags=['read', 'notify'])

            # Report Reference Descriptor for the Report characteristic
            # Report ID = 0, Report Type = 1 (Input)
            self.p.add_descriptor(srv_id=1, chr_id=4, dsc_id=1, uuid=REPORT_REF_DSCP,
                                 value=[0x00, 0x01], flags=['read'])

            # Find the report characteristic object to update its value later
            # We use the internal list of characteristics in the Peripheral object
            for c in self.p.characteristics:
                # UUIDs in bluezero are stored in the props dictionary
                if 'org.bluez.GattCharacteristic1' in c.props:
                    c_uuid = c.props['org.bluez.GattCharacteristic1'].get('UUID', '')
                    if REPORT.lower() in c_uuid.lower():
                        self.report_chr = c
                        break

            print("Starting BLE Peripheral in background thread...")
            self.thread = threading.Thread(target=self.p.publish, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f"Failed to start BLE Peripheral: {e}")

    def send_volume_up(self):
        if not self.report_chr:
            print("BLE Keyboard not initialized or Report characteristic not found")
            return

        print("Sending Volume Up report")
        # Press (bit 0 = 1)
        self.report_chr.set_value([0x01])
        time.sleep(0.1)
        # Release (bit 0 = 0)
        self.report_chr.set_value([0x00])


ble_kb = BLEKeyboard()


def start_ble():
    ble_kb.start()


def send_shutter():
    ble_kb.send_volume_up()
