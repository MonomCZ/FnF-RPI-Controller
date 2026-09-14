echo "dtoverlay=dwc2,dr_mode=peripheral" | sudo tee -a /boot/firmware/config.txt
sudo sed -i 's/rootwait/rootwait modules-load=dwc2,g_hid/' /boot/firmware/cmdline.txt