import re

def extract_stats(stats_file):
    """
    Extracts CPU, traffic generator, and DRAM latency and bandwidth
    statistics from a gem5 stats.txt file.

    Args:
        stats_file (str): Path to the stats.txt file.

    Returns:
        dict: A dictionary containing the extracted statistics.
    """

    stats = {}

    with open(stats_file, 'r') as f:
        content = f.read()

    # CPU Statistics
    stats['cpu_ipc'] = extract_stat(content, r"system\.cpu\.ipc\s+([\d\.]+)")
    stats['cpu_cpi'] = extract_stat(content, r"system\.cpu\.cpi\s+([\d\.]+)")

    # ICache Statistics
    stats['icache_miss_rate'] = extract_stat(content, r"system\.cpu\.icache\.overallMissRate::total\s+([\d\.]+)")
    stats['icache_avg_miss_latency'] = extract_stat(content, r"system\.cpu\.icache\.demandAvgMissLatency::total\s+([\d\.]+)")

    # DCache Statistics
    stats['dcache_miss_rate'] = extract_stat(content, r"system\.cpu\.dcache\.overallMissRate::total\s+([\d\.]+)")
    stats['dcache_avg_miss_latency'] = extract_stat(content, r"system\.cpu\.dcache\.demandAvgMissLatency::total\s+([\d\.]+)")

    # Traffic Generator Statistics
    stats['trafficgen_avg_read_latency'] = extract_stat(content, r"system\.trafficgen\.avgReadLatency\s+([\d\.]+)")
    stats['trafficgen_avg_write_latency'] = extract_stat(content, r"system\.trafficgen\.avgWriteLatency\s+([\d\.]+)")
    stats['trafficgen_read_bw'] = extract_stat(content, r"system\.trafficgen\.readBW\s+([\d\.]+)")
    stats['trafficgen_write_bw'] = extract_stat(content, r"system\.trafficgen\.writeBW\s+([\d\.]+)")

    # DRAM Statistics (Mem_ctrl1)
    stats['dram1_avg_mem_acc_lat'] = extract_stat(content, r"system\.mem_ctrl1\.dram\.avgMemAccLat\s+([\d\.]+)")
    stats['dram1_avg_rd_bw'] = extract_stat(content, r"system\.mem_ctrl1\.dram\.bwRead::total\s+([\d\.]+)")
    stats['dram1_avg_wr_bw'] = extract_stat(content, r"system\.mem_ctrl1\.dram\.bwWrite::total\s+([\d\.]+)")

    # DRAM Statistics (Mem_ctrl2)
    stats['dram2_avg_mem_acc_lat'] = extract_stat(content, r"system\.mem_ctrl2\.dram\.avgMemAccLat\s+([\d\.]+)")
    stats['dram2_avg_rd_bw'] = extract_stat(content, r"system\.mem_ctrl2\.dram\.bwRead::total\s+([\d\.]+)")
    stats['dram2_avg_wr_bw'] = extract_stat(content, r"system\.mem_ctrl2\.dram\.bwWrite::total\s+([\d\.]+)")

    return stats


def extract_stat(content, regex):
    """
    Extracts a single statistic from the stats.txt content using a regular expression.

    Args:
        content (str): The content of the stats.txt file.
        regex (str): The regular expression to use for extraction.

    Returns:
        float or None: The extracted statistic as a float, or None if not found.
    """
    match = re.search(regex, content)
    if match:
        return float(match.group(1))
    else:
        return None


if __name__ == "__main__":
    stats_file = "stats.txt"  # Replace with your stats file path
    extracted_stats = extract_stats(stats_file)

    if extracted_stats:
        print("Extracted Statistics:")
        for key, value in extracted_stats.items():
            if value is not None:
                print(f"{key}: {value}")
            else:
                print(f"{key}: Not found")
    else:
        print("Could not extract statistics.  Check the stats file path and format.")
