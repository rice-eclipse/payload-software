# Scraping values from the journalctl logs and plotting them
import matplotlib.pyplot as plt


def extract_value(string, substring):
    # Given a string, extract the numerical value between the end of substring and "\n"
    # This assumes that the substring is already present
    return float(string[string.find(substring)+len(substring):string.find("\n")])


with open("data\\activestate_journallogs.txt", 'r') as journalfile:
    lines = journalfile.readlines()
    active_cycle_alt = []
    active_cycle_avg_alt = []
    active_cycle_timestamps = []
    image_capture_alt = []
    image_capture_timestamps = []

    for i in range(len(lines)):
        if ": Altitude Reading: " in lines[i]:
            active_cycle_alt.append(extract_value(lines[i], ": Altitude Reading: "))
        if ": Average Altitude Window Reading: " in lines[i]:
            active_cycle_avg_alt.append(extract_value(lines[i], ": Average Altitude Window Reading: "))
        if i < len(lines)-1 and ":     Active Timer Time:" in lines[i] and ": Image Timestamp:" not in lines[i+1]:
            active_cycle_timestamps.append(extract_value(lines[i], ":     Active Timer Time:") / 1000)
        if ": Image Altitude:" in lines[i]:
            image_capture_alt.append(extract_value(lines[i], ": Image Altitude:"))
        if i < len(lines)-1 and ":     Active Timer Time:" in lines[i] and ": Image Timestamp:" in lines[i+1]:
            image_capture_timestamps.append(extract_value(lines[i], ":     Active Timer Time:") / 1000)

    print(active_cycle_alt)
    print(active_cycle_avg_alt)
    print(active_cycle_timestamps)
    print(image_capture_alt)
    print(image_capture_timestamps)

    # plt.xkcd()  # apparently this is something that you can do
    plt.plot(active_cycle_timestamps, active_cycle_alt, label="Active Cycle Altitude")
    plt.plot(active_cycle_timestamps, active_cycle_avg_alt, label="Active Cycle Average Altitude")

    plt.plot(image_capture_timestamps, image_capture_alt, 'bx', label="Image Capture Altitude")

    plt.legend()
    plt.title("Active Cycle & Imaging Altitudes vs Time")
    plt.xlabel("Time since active state condition trigger (seconds)")
    plt.ylabel("Altitude (ft)")
    plt.show()
