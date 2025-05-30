import re
import csv

def extract_stats(stats_file):
    """
    Extracts CPU, traffic generator, and DRAM latency and bandwidth
    statistics from a gem5 stats.txt file.

    Args:
        stats_file (str): Path to the stats.txt file.

    Returns:
        dict: A dictionary containing the extracted statistics, with units.
    """

    stats = {}

    with open(stats_file, 'r') as f:
        content = f.read()

    # CPU Statistics
    stats['cpu_ipc'] = (extract_stat(content, r"system\.cpu\.ipc\s+([\d\.]+)"), "Instructions per cycle")
    stats['cpu_cpi'] = (extract_stat(content, r"system\.cpu\.cpi\s+([\d\.]+)"), "Cycles per instruction")

    # ICache Statistics
    stats['icache_miss_rate'] = (extract_stat(content, r"system\.cpu\.icache\.overallMissRate::total\s+([\d\.]+)"), "Misses per access")
    stats['icache_avg_miss_latency'] = (extract_stat(content, r"system\.cpu\.icache\.demandAvgMissLatency::total\s+([\d\.]+)"), "Ticks")

    # DCache Statistics
    stats['dcache_miss_rate'] = (extract_stat(content, r"system\.cpu\.dcache\.overallMissRate::total\s+([\d\.]+)"), "Misses per access")
    stats['dcache_avg_miss_latency'] = (extract_stat(content, r"system\.cpu\.dcache\.demandAvgMissLatency::total\s+([\d\.]+)"), "Ticks")

    # Traffic Generator Statistics
    stats['trafficgen_avg_read_latency'] = (extract_stat(content, r"system\.trafficgen\.avgReadLatency\s+([\d\.]+)"), "Ticks")
    stats['trafficgen_avg_write_latency'] = (extract_stat(content, r"system\.trafficgen\.avgWriteLatency\s+([\d\.]+)"), "Ticks")
    stats['trafficgen_read_bw'] = (extract_stat(content, r"system\.trafficgen\.readBW\s+([\d\.]+)"), "Bytes per second")
    stats['trafficgen_write_bw'] = (extract_stat(content, r"system\.trafficgen\.writeBW\s+([\d\.]+)"), "Bytes per second")

    # DRAM Statistics (Mem_ctrl1)
    stats['dram1_avg_mem_acc_lat'] = (extract_stat(content, r"system\.mem_ctrl1\.dram\.avgMemAccLat\s+([\d\.]+)"), "Ticks")
    stats['dram1_avg_rd_bw'] = (extract_stat(content, r"system\.mem_ctrl1\.dram\.bwRead::total\s+([\d\.]+)"), "Bytes per second")
    stats['dram1_avg_wr_bw'] = (extract_stat(content, r"system\.mem_ctrl1\.dram\.bwWrite::total\s+([\d\.]+)"), "Bytes per second")

    # DRAM Statistics (Mem_ctrl2)
    stats['dram2_avg_mem_acc_lat'] = (extract_stat(content, r"system\.mem_ctrl2\.dram\.avgMemAccLat\s+([\d\.]+)"), "Ticks")
    stats['dram2_avg_rd_bw'] = (extract_stat(content, r"system\.mem_ctrl2\.dram\.bwRead::total\s+([\d\.]+)"), "Bytes per second")
    stats['dram2_avg_wr_bw'] = (extract_stat(content, r"system\.mem_ctrl2\.dram\.bwWrite::total\s+([\d\.]+)"), "Bytes per second")

    return stats


def extract_stat(content, regex):
    """
    Extracts a single statistic from the stats.txt content using a regular expression.

    Args:
        content (str): The content of the stats.txt file.
        regex (str): The regular expression to use for extraction.

    Returns:
        tuple: (float or None, str): The extracted statistic as a float,
               or None if not found, and the unit of the statistic.
    """
    match = re.search(regex, content)
    if match:
        return float(match.group(1))
    else:
        return None


def save_to_csv(stats, csv_file):
    """
    Saves the extracted statistics to a CSV file.

    Args:
        stats (dict): A dictionary containing the extracted statistics.
        csv_file (str): The path to the CSV file to create.
    """

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        header = list(stats.keys())
        header_with_units = [f"{key} ({stats[key][1]})" for key in header]  # Add units to header
        writer.writerow(header_with_units)

        # Write data row
        data = [stats[key][0] if stats[key][0] is not None else "N/A" for key in header]  # Handle None values
        writer.writerow(data)


if __name__ == "__main__":
    stats_file = "./l2Cache_128KB/stats.txt"  # Replace with your stats file path
    csv_file = "extracted_stats.csv"  # Replace with your desired CSV file path

    extracted_stats = extract_stats(stats_file)

    if extracted_stats:
        print("Extracted Statistics:")
        for key, value in extracted_stats.items():
            if value[0] is not None:
                print(f"{key}: {value[0]} {value[1]}")
            else:
                print(f"{key}: None")

        save_to_csv(extracted_stats, csv_file)
        print(f"Statistics saved to {csv_file}")

    else:
        print("Could not extract statistics.  Check the stats file path and format.")
