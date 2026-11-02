import subprocess
import time

# Mapping of WiFi channels to their frequencies
channel_freq = {
    36: '5180',
    40: '5200',
    44: '5220',
    48: '5240',
    116: '5580',
    149: '5745',
    157: '5785',
    161: '5805'
}

def enable_monitor_mode(interface):
    try:
        subprocess.check_output(['sudo', 'rfkill', 'unblock', 'wifi'])  # Unblock RF-kill
        subprocess.check_output(['sudo', 'ifconfig', interface, 'down'])
        subprocess.check_output(['sudo', 'iwconfig', interface, 'mode', 'monitor'])
        subprocess.check_output(['sudo', 'ifconfig', interface, 'up'])
        print("{} is now in monitor mode".format(interface))
    except subprocess.CalledProcessError as e:
        print("Error enabling monitor mode: {}".format(e))
    except Exception as e:
        print("Unexpected error: {}".format(e))

def reset_interface(interface):
    try:
        print("Resetting interface {}".format(interface))
        subprocess.check_output(['sudo', 'rfkill', 'block', 'wifi'])
        time.sleep(1)  # Delay to ensure the interface is blocked
        subprocess.check_output(['sudo', 'rfkill', 'unblock', 'wifi'])
        time.sleep(1)  # Delay to ensure the interface is unblocked
        subprocess.check_output(['sudo', 'ifconfig', interface, 'down'])
        time.sleep(1)  # Delay to ensure the interface is down
        subprocess.check_output(['sudo', 'ifconfig', interface, 'up'])
        time.sleep(1)  # Delay to ensure the interface is up
        print("Interface {} reset successfully".format(interface))
    except subprocess.CalledProcessError as e:
        print("Error resetting interface {}: {}".format(interface, e))

def set_channel(interface, channel):
    retry_count = 3
    while retry_count > 0:
        try:
            reset_interface(interface)
            freq = channel_freq.get(channel, None)
            if freq:
                subprocess.check_output(['sudo', 'iwconfig', interface, 'channel', str(channel)])
                print("Set {} to channel {} with frequency {} MHz".format(interface, channel, freq))
            else:
                subprocess.check_output(['sudo', 'iwconfig', interface, 'channel', str(channel)])
                print("Set {} to channel {}".format(interface, channel))
            subprocess.check_output(['sudo', 'ifconfig', interface, 'up'])
            subprocess.check_output(['sudo', 'iwconfig', interface, 'mode', 'monitor'])  # Ensure monitor mode
            print("Channel set successfully: {}".format(channel))
            return  # Exit the function if successful
        except subprocess.CalledProcessError as e:
            print("Error setting channel: {}. Retrying...".format(e))
            retry_count -= 1
            if retry_count == 0:
                # Perform a more aggressive reset on the last retry
                subprocess.check_output(['sudo', 'rfkill', 'block', 'all'])
                time.sleep(3)
                subprocess.check_output(['sudo', 'rfkill', 'unblock', 'all'])
                time.sleep(3)
            else:
                time.sleep(3)  # Increase the wait time between retries
        except Exception as e:
            print("Unexpected error: {}. Retrying...".format(e))
            retry_count -= 1
            time.sleep(3)
    print("Failed to set channel {} after retries".format(channel))

def capture_traffic(interface, channel, duration):
    file_name = "capture_channel_{}.pcap".format(channel)
    end_time = None
    try:
        reset_interface(interface)
        subprocess.check_output(['sudo', 'iwconfig', interface, 'mode', 'monitor'])  # Ensure monitor mode before capture
        print("Capturing traffic on channel {} for {} seconds...".format(channel, duration))
        start_time = time.time()  # Record start time before starting tcpdump
        p = subprocess.Popen(['sudo', 'tcpdump', '-i', interface, '-w', file_name])
        time.sleep(duration)
        p.terminate()
        try:
            p.wait(timeout=5)  # Wait for tcpdump to terminate
        except:
            p.kill()
            p.wait()
        end_time = time.time()  # Record end time after stopping tcpdump
        print("Finished capturing traffic on channel {}, saved to {}".format(channel, file_name))
        print("Capture duration: {} seconds".format(end_time - start_time))
    except subprocess.CalledProcessError as e:
        print("Error capturing traffic: {}".format(e))
    except Exception as e:
        print("Unexpected error: {}".format(e))
    finally:
        reset_interface(interface)  # Ensure interface is reset after capture
        if end_time is None:
            end_time = time.time()
    return end_time - start_time  # Return capture duration

def main():
    interface = 'wlan1'
    channels = [36, 40, 44, 48, 116]  # Adjusted channels based on active networks
    duration = 5  # Capture duration per channel in seconds

    # Enable monitor mode on the interface
    enable_monitor_mode(interface)

    while True:
        for channel in channels:
            switch_start_time = time.time()
            print("Switching to channel {}".format(channel))
            set_channel(interface, channel)
            switch_end_time = time.time()
            print("Channel set to {}".format(channel))
            switch_duration = switch_end_time - switch_start_time
            print("Time taken to switch to channel {}: {:.2f} seconds".format(channel, switch_duration))

            capture_start_time = time.time()
            capture_duration = capture_traffic(interface, channel, duration)
            capture_end_time = time.time()
            time_between_captures = capture_start_time - switch_end_time
            print("Time taken from finishing capturing on previous channel to start capturing on channel {}: {:.2f} seconds".format(channel, time_between_captures))
            print("Total capture time on channel {}: {:.2f} seconds".format(channel, capture_duration))

            time.sleep(2)  # Small delay to ensure proper switching

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting...")
