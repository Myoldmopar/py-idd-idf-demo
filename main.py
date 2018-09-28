import glob
import os

from pyiddidf.idf.processor import IDFProcessor


class FileInfo:
    """A simple data class holding info about a single IDF"""
    def __init__(self, file_name, climate_zone, vintage, object_list):
        self.file_name = file_name
        self.climate_zone = climate_zone
        self.vintage = vintage
        self.object_list = object_list


# Get all the IDFs in a directory, if there are subdirectories,
# the glob will need to be updated to do a recursive search
idf_directory = '/Applications/EnergyPlus-8-9-0/ExampleFiles'
idf_wildcard = os.path.join(idf_directory, '*.idf')
all_idfs = glob.glob(idf_wildcard)

# Loop over each IDF to get information
idf_info = []
num_idfs = len(all_idfs)
for counter, idf_path in enumerate(all_idfs):
    if counter % 50 == 0:
        print("Processing idf %s/%s" % (counter, num_idfs))

    # Here you can process out information from the filename/directory/etc.
    this_file_name = os.path.basename(idf_path)
    this_climate_zone = 'Nothing'  # Maybe you need to parse this from the filename?
    this_vintage = 'Nothing'  # Maybe you need to parse this from the filename?

    # Process the IDF, then loop over the contents and get whatever info you need
    idf_processor = IDFProcessor().process_file_given_file_path(idf_path)
    unique_objs = set()
    for obj in idf_processor.objects:
        if obj.comment:
            continue
        unique_objs.add(obj.object_name)

    # Add the resulting information to the list; add data members to the class above as desired
    idf_info.append(
        FileInfo(
            this_file_name,
            this_climate_zone,
            this_vintage,
            list(unique_objs)
        )
    )

# At this point, you have a pretty rich list of IDF information
# You should be able to do all sorts of processing to come up with statistics

# Like printing out how many different object types there are in each file
print("\n***Number of Unique Objects in Each IDF:")
for idf in idf_info:
    print("%s: %s" % (idf.file_name, len(idf.object_list)))

# Or printing out objects that are common in all idfs that start with Z  (-:
print("\n***Objects common to IDFs that start with \"Z\":")
z_files = [idf for idf in idf_info if idf.file_name[0].startswith("Z")]
common_object_set = set()  # this initialization is really only necessary to shut up a warning
for counter, idf in enumerate(idf_info):
    if counter == 0:  # start with a base set
        common_object_set = set(idf.object_list)
    else:  # then only keep the things common between the two
        this_file_object_set = set(idf.object_list)
        common_object_set = common_object_set & this_file_object_set
print("%s common objects:" % len(common_object_set))
for common_object in common_object_set:
    print(" - %s" % common_object)
