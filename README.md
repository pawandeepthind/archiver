# archiver
A simple configurable python script that archives files in folder that are older then configurable number of days.

Script can be configured, using the archiver_config.json file. Some of the important flags in the confiigurable files,

# configuration

* __debug__ - _boolean_ - enable more verbose flags
* __remove_files__ - _boolean_ - removes the original files once they are achived
* __archival_days__ - _int_ - files older then these days will be archived when the script runs
* __archival_folder_name__ - _string - folder name in the current directory where the archives will be created
* __log_file_name__ - _string - file name for the log file
* __enable_disk_space_check__ - _boolean_ - flag enables archiving only if used disk is above a limit set in configuration  __disk_space_check_percentage_limit__
* __disk_space_check_percentage_limit__ -  int - limit of used space when crossed, files older then __archival_days__ will be archived
* __disk_path__ - string - path to find out the disk usage
* __folders__ - List of following properties that enables archiving in multiple folders
  * __path__ - string - folder path to check files for archiving
  * __description__ - string - just the description of the folder used for displaying information
  * __archive_name_prefix__ - _string_ - Archive file name prefix
  

# process
1. Checks if we have enabled disk check (if used disk is above a limit set in configuration, then it will compress and archive the files in a folder in current directory
2. Reads the folders from configuration, and collects files that are older then configurable number of days and compress them.
3. Remove the files once archived (controlled by a configuration)
