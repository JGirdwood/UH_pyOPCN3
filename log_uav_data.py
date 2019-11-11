import pyOPCN3logger
import pyOPCN3spi
from time import sleep
from time import time


if __name__ == '__main__':
    print "------------------------------------------------"
    resolution_sec = 1
    run_forever = True
    run_time = 10
    OPC_chip_select = 25

    FMI_OPC = pyOPCN3spi.OPCN3(OPC_chip_select)
    print("OPCN3 Connected")

    sd_log = pyOPCN3logger.LogFile("FMI_OPC", "/home/pi")
    usb_log = pyOPCN3logger.LogFile("FMI_OPC", "/media/usb/")

    FMI_OPC.read_info_string()
    FMI_OPC.read_serial_string()
    FMI_OPC.read_config_vars()

    print("Creating SD Log File")
    sd_log.make_headers(FMI_OPC)
    print("Creating USB Log File")
    usb_log.make_headers(FMI_OPC)

    print("Starting Main Loop")
    loop_num = 0
    while True:
        t1 = time()
        FMI_OPC.read_histogram_data()
        sd_log.write_data_log(FMI_OPC)
        print "Written to SD log"
        usb_log.write_data_log(FMI_OPC)
        print "written to USB log"
        t2 = time()
        delay_sec = resolution_sec-(t2-t1)
        loop_num += 1
        if delay_sec > 0:
            sleep(delay_sec)
        else:
            print("Loop Time Exceeds Resolution")
        if (run_forever is False) & (loop_num > run_time):
            print("Loop Finished")
            break
