import os
import json
import time
import tarfile
import logging


def disk_stat(path):
    """
      This function returns disk usage percentage
    """
    disk = os.statvfs(path)
    percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail) + 1
    return percent


def init_logging(log_file_name="archive.log"):
    """
      This function setup the logging
    """
    logging.basicConfig(format='%(asctime)s [%(filename)-12s:%(lineno)-3s] - %(levelname)-5s - %(message)s',
                        level=logging.INFO,
                        filename=log_file_name)


def main(config):
    """
      This is the main part of the logic.
      1. Checks if we have enabled disk check (if used disk is above a limit set in configuration, then it will
      compress and archive the files in a folder in current directory
      2. Reads the folders from configuration, and collects files that are older then configurable number of days
      and compress them.
      3. Remove the files once archived (controlled by a configuration)
    """
    now = int(time.time())
    now_formatted = time.strftime('%Y%m%d%H%M%S', time.localtime(now))

    print "Archive script started."
    logging.info("=====================")
    logging.info("Start Archive Process")
    logging.info("Will archive files older then %s days", str(config['archival_days']))

    if config['enable_disk_space_check']:
        usage_percentage = disk_stat(config['disk_path'])
        if usage_percentage < config['disk_space_check_percentage_limit']:
            logging.info("No need to archive the files as disk usage %d%% is below configured limit %d%%"
                         , usage_percentage
                         , config['disk_space_check_percentage_limit'])
            print "Archive script completed successfully."
            exit()
        else:
            logging.info("Archive the files as disk usage %d%% is above configured limit %d%%"
                         , usage_percentage
                         , config['disk_space_check_percentage_limit'])
    try:
        archival_folder_path = os.path.join(os.getcwd(), config['archival_folder_name'])
        logging.info("Archival Folder Path: %s", archival_folder_path)
        if not os.path.isdir(archival_folder_path):
            logging.info("Archival Folder Path: %s does not exists. Create it", archival_folder_path)
            os.mkdir(archival_folder_path)

        for folder in config['folders']:
            logging.info("Working on %s with description: %s", folder['path'], folder['description'])
            files_to_archive = []
            for filename in os.listdir(folder['path']):
                fullname = os.path.join(folder['path'], filename)
                file_modified_time = os.path.getmtime(fullname)
                days_old = int((now - file_modified_time)/(60*60*24))
                if days_old > config['archival_days']:
                    if config['debug']:
                        logging.info("%s is %s old", fullname, str(days_old))
                    files_to_archive.append(fullname)

            if len(files_to_archive) > 0:
                tar_file_name = folder['archive_name_prefix'] + now_formatted + ".tar.gz"
                tar_file_name_with_path = os.path.join(archival_folder_path, tar_file_name)
                tar = tarfile.open(tar_file_name_with_path, "w:gz")
                # raise RuntimeError("IGNORE the alert i am generating the error")

                for fl in files_to_archive:
                    if config['debug']:
                        logging.info("Adding %s to archive.", fl)
                    tar.add(fl, arcname=os.path.basename(fl))
                tar.close()
                logging.info("%s created with %s files archived.", tar_file_name_with_path, str(len(files_to_archive)))

                if config['remove_files']:
                    for fl in files_to_archive:
                        if config['debug']:
                            logging.info("Removing %s from archive.", fl)
                        os.remove(fl)
            else:
                logging.info("Nothing to archive in %s", folder['path'])
    except Exception as err:
        logging.error("End Archive Process with error %s", err.__str__())
        print "Archive script completed with error, check logs for details"
        #Raise alert
        exit()

    finally:
        logging.info("End Archive Process")

    print "Archive script completed successfully."

if __name__== "__main__":
    config_file_path = './archiver_config.json'
    config = None

    with open(config_file_path) as config_file:
        config = json.load(config_file)

    init_logging(config['log_file_name'])
    main(config)
