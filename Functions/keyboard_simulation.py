#bad_usb.py
import config
import os
import subprocess
import time
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, ROOT)



def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def setup_gadget():
    gadget = "/sys/kernel/config/usb_gadget/keyboard"   

    if os.path.exists(gadget+'/UDC') and open(gadget+'/UDC').read().strip():
        print('gadgetmode already running (skip setup)')
        return
    run('modprobe libcomposite')

    os.makedirs(f'{gadget}/strings/0x409', exist_ok=True)
    os.makedirs(f'{gadget}/functions/hid.usb0', exist_ok=True)
    os.makedirs(f'{gadget}/configs/c.1/strings/0x409', exist_ok=True)

    def w(path, value):
        with open(path, 'w') as f:
            f.write(str(value))
    #metadata
    w(f'{gadget}/idVendor', '0x1d6b')
    w(f'{gadget}/idProduct', '0x0104')
    w(f"{gadget}/bcdDevice", "0x0043")
    w(f'{gadget}/bcdUSB', '0x0200')

    w(f'{gadget}/strings/0x409/serialnumber', '6767meowIusearchbtw')
    w(f'{gadget}/strings/0x409/manufacturer', 'MeowPi')
    w(f'{gadget}/strings/0x409/product', 'MeowPi coolThingy :3')

    w(f'{gadget}/functions/hid.usb0/protocol', '1')
    w(f'{gadget}/functions/hid.usb0/subclass', '1')
    w(f'{gadget}/functions/hid.usb0/report_length', '8')
    
    descriptor = bytes([       #compicated stuff i dont want to learn
        0x05,0x01, 0x09,0x06, 0xa1,0x01,   
        0x05,0x07, 0x19,0xe0, 0x29,0xe7,   
        0x15,0x00, 0x25,0x01, 0x75,0x01,   
        0x95,0x08, 0x81,0x02, 0x95,0x01,   
        0x75,0x08, 0x81,0x03, 0x95,0x05,   
        0x75,0x01, 0x05,0x08, 0x19,0x01,   
        0x29,0x05, 0x91,0x02, 0x95,0x01,   
        0x75,0x03, 0x91,0x03, 0x95,0x06,   
        0x75,0x08, 0x15,0x00, 0x25,0x65,   
        0x05,0x07, 0x19,0x00, 0x29,0x65,   
        0x81,0x00, 0xc0                   
    ])

    with open(f'{gadget}/functions/hid.usb0/report_desc', 'wb') as f:
        f.write(descriptor) #writes the complicated stuff into kernel

    w(f'{gadget}/configs/c.1/strings/0x409/configuration', 'Config 1: HID Keyboard')
    w(f'{gadget}/configs/c.1/MaxPower', '250')

    link = f'{gadget}/configs/c.1/hid.usb0'
    if not os.path.exists(link):
        os.symlink(f'{gadget}/functions/hid.usb0', link)
    
    udc = os.listdir('/sys/class/udc')[0]
    w(f'{gadget}/UDC', udc)

    print('gadgetmode setup complete')
    time.sleep(1) #gives host time to recognize

keycodes_us = { #codes for keys in us layout obv
    'a':0x04,'b':0x05,'c':0x06,'d':0x07,'e':0x08,'f':0x09,'g':0x0a,
    'h':0x0b,'i':0x0c,'j':0x0d,'k':0x0e,'l':0x0f,'m':0x10,'n':0x11,
    'o':0x12,'p':0x13,'q':0x14,'r':0x15,'s':0x16,'t':0x17,'u':0x18,
    'v':0x19,'w':0x1a,'x':0x1b,'y':0x1c,'z':0x1d,
    '1':0x1e,'2':0x1f,'3':0x20,'4':0x21,'5':0x22,
    '6':0x23,'7':0x24,'8':0x25,'9':0x26,'0':0x27,
    ' ':0x2c,'\n':0x28,'\t':0x2b,
    '-':0x2d,'=':0x2e,'[':0x2f,']':0x30,
    ';':0x33,"'":0x34,'`':0x35,',':0x36,'.':0x37,'/':0x38,
}
keycodes_cz = {
    'a':0x04,'b':0x05,'c':0x06,'d':0x07,'e':0x08,'f':0x09,'g':0x0a,
    'h':0x0b,'i':0x0c,'j':0x0d,'k':0x0e,'l':0x0f,'m':0x10,'n':0x11,
    'o':0x12,'p':0x13,'q':0x14,'r':0x15,'s':0x16,'t':0x17,'u':0x18,
    'v':0x19,'w':0x1a,'x':0x1b,'z':0x1c,'y':0x1d,
    '+':0x1e,'ě':0x1f,'š':0x20,'č':0x21,'ř':0x22,
    'ž':0x23,'ý':0x24,'á':0x25,'í':0x26,'é':0x27,
    'ú':0x2f,')':0x30,'ů':0x33,'§':0x34,';':0x35,',':0x36,'.':0x37,'-':0x38,
    ' ':0x2c,'\n':0x28,'\t':0x2b,
}



shift_codes_us = {  #same thing but with shift, for capital letters and symbols
    **{c.upper(): c for c in 'abcdefghijklmnopqrstuvwxyz'},  
    '!':'1','@':'2','#':'3','$':'4','%':'5',  #symbols on number keys
    '^':'6','&':'7','*':'8','(':'9',')':'0',
    '_':'-','+':'=','{':'[','}':']',
    ':':';','"':"'",'~':'`','<':',','>':'.','?':'/',
}

shift_codes_cz = {
    **{c.upper(): c for c in 'abcdefghijklmnopqrstuvwxyz'},
    
    '1':'+','2':'ě','3':'š','4':'č','5':'ř',
    '6':'ž','7':'ý','8':'á','9':'í','0':'é',
    
    '?':',',':':'.','_':'-',
    '(':'ú','/':')','"':'ů','!':'§',
}

if config.used_layout == 'us':
    keycodes = keycodes_us
    shift_codes = shift_codes_us
elif config.used_layout == 'cz':
    keycodes = keycodes_cz
    shift_codes = shift_codes_cz


def type_string(text,delay=0.05, device='/dev/hidg0'):
    with open(device, 'wb') as hid:
        for char in text:
            modifier = 0
            if char in shift_codes:
                modifier = 0x02  # Shift key
                keycode = keycodes.get(shift_codes[char], 0)
            else:
                keycode = keycodes.get(char, 0)

            if keycode == 0:
                print(f'{char} not found skipping.')
                continue

            hid.write(bytes([modifier, 0,keycode, 0, 0, 0, 0, 0])) #key press
            hid.flush()
            time.sleep(delay)
            hid.write(bytes([0, 0, 0, 0, 0, 0, 0, 0]))  # key release
            hid.flush()
            time.sleep(delay)

def press_key(modifier, keycode, device='/dev/hidg0'):
    with open(device, 'wb') as hid:
        hid.write(bytes([modifier, 0, keycode, 0, 0, 0, 0, 0]))
        hid.flush()
        time.sleep(0.05)
        hid.write(bytes([0, 0, 0, 0, 0, 0, 0, 0]))
        hid.flush()

if __name__ == "__main__":
    setup_gadget()
    #scripts
    import importlib
    
    scripts_dir=os.path.join(os.path.dirname(__file__), 'bad_usb_scripts')
    scriptname = 'buttons+keyboardsim'
    module = importlib.import_module(f'modes.bad_usb.bad_usb_scripts.{scriptname}')
    
    module.run()