import os
import multiprocessing as mp
import tqdm

log_dir = "path/that/contains/your/log/files"  # this is the directory where your log files are located
io_log_prefix = "cyberdrop-dl.io"  # this is the prefix of the log files you want to parse (i.e. if your log file is named cyberdrop-dl.vm.1670871055460181.txt, then the prefix is cyberdrop-dl.vm)

link_filter = "Starting scrape of "
link_blacklist = ["https://forum.thotsbay.to/threads/", "https://simpcity.st"]
links = []


def get_links(log_file):
    links = []
    with open(log_file, "r") as f:
        lines = [line.strip() for line in f]
    for line in lines:
        if link_filter in line:
            if not any(blacklisted_link in line for blacklisted_link in link_blacklist):
                links.append(line.split(link_filter)[1])
    return links


def get_log_files(prefix):
    log_files = []
    for file in os.listdir(log_dir):
        if prefix in file:
            log_files.append(os.path.normpath(os.path.join(log_dir, file)))
    log_files = [(os.path.getsize(f), f) for f in log_files]
    log_files.sort(key=lambda x: x[0], reverse=True)
    log_files = [f[1] for f in log_files]
    return log_files


def main():
    os.system("cls")
    threads = 6

    io_logs = get_log_files(io_log_prefix)
    total_logs_io = len(io_logs)
    io_links = []

    print(f"[+] Found {total_logs_io} IO logs")

    print("\n[+] Gathering IO links")
    with mp.Pool(threads) as pool_io:
        for links in tqdm.tqdm(
            pool_io.imap_unordered(get_links, io_logs), total=total_logs_io
        ):
            io_links.extend(links)

    before_links_io = len(io_links)
    io_links = sorted(list(set(io_links)))
    after_links_io = len(io_links)
    print(
        f"\n[+] IO links: {str(after_links_io)}. (removed {before_links_io - after_links_io} duplicates)"
    )

    for link in io_links:
        print(link)

    print("\nDone!")

    input("\nPress enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] User Aborted")
        exit()
