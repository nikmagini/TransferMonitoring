import json

import csv

def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value

    return dict(items())
#TODO: cllean unnecesary comments
#employee_data = '{"tr_id":"2016-06-22-2201__tbn18.nikhef.nl__grid002.ft.uam.es__856147523__4d964812-2576-58e0-92d0-a2ef2e24afac","endpnt":"fts3.cern.ch","src_srm_v":"2.2.0","dest_srm_v":"2.2.0","vo":"atlas","src_url":"srm://tbn18.nikhef.nl:8446/srm/managerv2?SFN=/dpm/nikhef.nl/home/atlas/atlasdatadisk/rucio/mc15_13TeV/5d/cb/EVNT.08775130._013235.pool.root.1","dst_url":"srm://grid002.ft.uam.es:8443/srm/managerv2?SFN=/pnfs/ft.uam.es/data/atlas/atlasdatadisk/rucio/mc15_13TeV/5d/cb/EVNT.08775130._013235.pool.root.1","src_hostname":"tbn18.nikhef.nl","dst_hostname":"grid002.ft.uam.es","src_site_name":"","dst_site_name":"","t_channel":"srm://tbn18.nikhef.nl__srm://grid002.ft.uam.es","timestamp_tr_st":"1466632862284","timestamp_tr_comp":"1466632865616","timestamp_chk_src_st":"1466632860931","timestamp_chk_src_ended":"1466632861355","timestamp_checksum_dest_st":"1466632865692","timestamp_checksum_dest_ended":"1466632865737","t_timeout":"1121","chk_timeout":"1800","t_error_code":"","tr_error_scope":"","t_failure_phase":"","tr_error_category":"","t_final_transfer_state":"Ok","tr_bt_transfered":"10565043","nstreams":"3","buf_size":"0","tcp_buf_size":"0","block_size":"0","f_size":"10565043","time_srm_prep_st":"1466632860931","time_srm_prep_end":"1466632862284","time_srm_fin_st":"1466632865616","time_srm_fin_end":"1466632865692","srm_space_token_src":"","srm_space_token_dst":"ATLASDATADISK","t__error_message":"","tr_timestamp_start":"1466632860151.000000","tr_timestamp_complete":"1466632866232.000000","channel_type":"urlcopy","user_dn":"/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ddmadmin/CN=531497/CN=Robot: ATLAS Data Management","file_metadata":{"adler32": "68e800b9", "src_type": "DISK", "src_rse": "NIKHEF-ELPROD_DATADISK", "request_id": "c0c7d290714848f8a1592873a2aafe3f", "src_rse_id": "4ed5590e5d6e4008b1b9e92253962784", "name": "EVNT.08775130._013235.pool.root.1", "request_type": "transfer", "filesize": 10565043, "dest_rse_id": "a07afdb2953442f78bd87136e32c2674", "activity": "Data Consolidation", "dst_rse": "UAM-LCG2_DATADISK", "dst_type": "DISK", "scope": "mc15_13TeV", "md5": null},"job_metadata":{"multi_sources": true, "issuer": "rucio"},"retry":"0","retry_max":"0","job_m_replica":"true","job_state":"FINISHED","is_recoverable":"1"}'
#employee_data = '{"employee_name": "James", "email": "james@gmail.com", "job_profile": [{"title1":"Team Lead", "title2":"Sr. Developer"}]}'

import sys, os
print(sys.path)
# os.chdir("~/mnt/private/TransferMonitoring/Zygimantas/src/data")
path_colors_record = '/home/zygis/mnt/private/TransferMonitoring/Zygimantas/src/data/recordsColorsExample.json'
with open(path_colors_record) as json_file:
    employee_parsed= json.load(json_file)



# employee_parsed = json.loads(employee_data)

flat_dict = flatten_dict(employee_parsed)
# print (employee_parsed)

# a = employee_parsed.keys

# for key, value in employee_parsed.items() :
#     print (key, value)

# emp_data = employee_parsed['file_metadata']

"""
how to get list of keys from dict (dif between 2.7 and 3.x)
"""
# print(list(flat_dict.values()))

# for key in flat_dict:
#     print(key)

# open a file for writing

employ_data = open('/tmp/EmployData.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(employ_data)

count = 0

for emp in employee_parsed:
    print(emp)
    print(type(emp))
    if count == 0:

        header = list(emp)

        csvwriter.writerow(header)

        count += 1

    csvwriter.writerow(list(emp.values()))

employ_data.close()
